"""This is the Mitype main app script."""

import curses
import os
import sys
import time
import webbrowser

import mitype.signals
from mitype.calculations import (
    accuracy,
    first_index_at_which_strings_differ,
    get_space_count_after_ith_word,
    number_of_lines_to_fit_text_in_window,
    speed_in_wpm,
    word_wrap,
)
from mitype.commandline import load_from_database, resolve_commandline_arguments
from mitype.history import save_history
from mitype.keycheck import (
    is_backspace,
    is_ctrl_backspace,
    is_ctrl_c,
    is_ctrl_t,
    is_enter,
    is_escape,
    is_left_arrow_key,
    is_resize,
    is_right_arrow_key,
    is_tab,
    is_valid_initial_key,
)
from mitype.timer import get_elapsed_seconds_since_first_keypress


class App:
    """Class for enclosing all methods required to run Mitype."""

    def __init__(self):
        """Initialize the application class."""
        # Start the parser
        self.text, self.text_id = resolve_commandline_arguments()
        self.tokens = self.text.split()

        # Squash multiple spaces, tabs, newlines to single space
        self.text = " ".join(self.tokens)
        self.text_backup = self.text

        # Current typed word and entire string
        self.current_word = ""
        self.current_string = ""

        self.key = ""
        # First valid key press
        self.first_key_pressed = False
        # Stores keypress, time tuple
        self.key_strokes = []

        self.mistyped_keys = []

        # Time at which test started
        self.start_time = 0
        # Time at which test ended
        self.end_time = 0

        # Keep track of the token index in text
        self.token_index = 0
        # mode = 0 when in test
        # mode = 1 when in replay
        self.mode = 0

        self.window_height = 0
        self.window_width = 0

        self.number_of_lines_to_print_text = 0

        # Restrict current word length to a limit
        # Used to highlight once the limit is reached
        self.current_word_limit = 25

        self.test_complete = False

        # Real-time speed, the value at the end of the test is the result
        # And a few other stats
        self.current_speed_wpm = 0
        self.accuracy = 0
        self.time_taken = 0

        self.total_chars_typed = 0
        self.text_without_spaces = self.text_backup.replace(" ", "")

        sys.stdout = sys.__stdout__

        # Set ESC delay to 0 (default 1 on linux)
        os.environ.setdefault("ESCDELAY", "0")

        # Start curses on main
        curses.wrapper(self.main)

    def main(self, win):
        """Respond to user inputs.

        This is where the infinite loop is executed to continuously serve events.

        Args:
            win (any): Curses window object.
        """
        # Initialize windows
        self.initialize(win)

        while True:
            # Typing mode
            key = self.keyinput(win)

            if not self.first_key_pressed:
                if is_escape(key) or is_ctrl_c(key):
                    sys.exit(0)

                if is_left_arrow_key(key):
                    self.switch_text(win, -1)

                if is_right_arrow_key(key):
                    self.switch_text(win, 1)

            # Test mode
            if self.mode == 0:
                self.typing_mode(win, key)

            # Again mode
            else:
                # Tab to retry last test
                if is_tab(key):
                    win.clear()
                    self.reset_test()
                    self.setup_print(win)
                    self.update_state(win)

                # Replay
                if is_enter(key):
                    self.replay(win)

                # Tweet result
                if is_ctrl_t(key):
                    self.share_result()

            # Refresh for changes to show up on window
            win.refresh()

    def initialize(self, win):
        """Configure the initial state of the curses interface.

        Args:
            win (any): Curses window.
        """
        self.window_height, self.window_width = self.get_dimensions(win)

        # This works by adding extra spaces to the text where needed
        self.text = word_wrap(self.text, self.window_width)

        # Check if we can fit text in current window after adding word wrap
        self.screen_size_check()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)

        class Color:
            GREEN = curses.color_pair(1)
            RED = curses.color_pair(2)
            BLUE = curses.color_pair(3)
            YELLOW = curses.color_pair(4)
            CYAN = curses.color_pair(5)
            MAGENTA = curses.color_pair(6)
            BLACK = curses.color_pair(7)

        self.Color = Color

        # This sets input to be a non-blocking call and will block for 100ms
        # Returns -1 if no input found at the end of time
        win.nodelay(True)
        win.timeout(100)

        self.setup_print(win)

    def setup_print(self, win):
        """Print setup text at beginning of each typing session.

        Args:
            win (any): Curses window object.
        """
        win.addstr(0, 0, " ID:{} ".format(self.text_id), self.Color.CYAN)
        win.addstr(0, self.window_width // 2 - 4, " MITYPE ", self.Color.CYAN)

        # Text is printed BOLD initially
        # It is dimmed as user types on top of it
        win.addstr(2, 0, self.text, curses.A_BOLD)

        self.print_realtime_wpm(win)

        # Set cursor position to beginning of text
        win.move(2, 0)

    def clear_line(self, win, line):
        """Clear a line on the window.

        Args:
            win (any): Curses window.
            line (int): Line number.
        """
        # Cursor advances to next cell after the character is printed
        # This causes scroll with addstr on the last line which is disabled
        # Hence using insstr instead
        win.insstr(line, 0, " " * self.window_width)

    def update_state(self, win):
        """Report on typing session results.

        Args:
            win (any): Curses window.
        """
        self.clear_line(win, self.number_of_lines_to_print_text)
        self.clear_line(win, self.number_of_lines_to_print_text + 2)
        self.clear_line(win, self.number_of_lines_to_print_text + 4)

        # Highlight in RED if word reaches the word limit length
        if len(self.current_word) >= self.current_word_limit:
            win.addstr(
                self.number_of_lines_to_print_text, 0, self.current_word, self.Color.RED
            )
        else:
            win.addstr(self.number_of_lines_to_print_text, 0, self.current_word)

        # Text is printed BOLD initially
        # It is dimmed as user types on top of it
        win.addstr(2, 0, self.text, curses.A_BOLD)
        win.addstr(2, 0, self.text[0 : len(self.current_string)], curses.A_DIM)

        index = first_index_at_which_strings_differ(self.current_string, self.text)
        # Check if difference was found
        if index < len(self.current_string):
            self.mistyped_keys.append(len(self.current_string) - 1)

        win.addstr(
            2 + index // self.window_width,
            index % self.window_width,
            self.text[index : len(self.current_string)],
            self.Color.RED,
        )

        # End of test, all characters are typed out
        if index == len(self.text):
            self.test_end(win)

        win.refresh()

    def test_end(self, win):
        # Highlight mistyped characters
        for i in self.mistyped_keys:
            win.addstr(
                2 + i // self.window_width,
                i % self.window_width,
                self.text[i],
                self.Color.RED,
            )

        curses.curs_set(0)

        # Calculate stats at the end of the test
        if self.mode == 0:
            self.current_speed_wpm = speed_in_wpm(self.tokens, self.start_time)
            total_chars_in_text = len(self.text_without_spaces)
            wrongly_typed_chars = self.total_chars_typed - total_chars_in_text
            self.accuracy = accuracy(self.total_chars_typed, wrongly_typed_chars)
            self.time_taken = get_elapsed_seconds_since_first_keypress(self.start_time)

            self.mode = 1
            # Find time difference between the key strokes
            # The key_strokes list is storing the time at which the key is pressed
            for k in range(len(self.key_strokes) - 1, 0, -1):
                self.key_strokes[k][0] -= self.key_strokes[k - 1][0]

            self.key_strokes[0][0] = 0

        win.addstr(self.number_of_lines_to_print_text, 0, " Your typing speed is ")
        win.addstr(" " + self.current_speed_wpm + " ", self.Color.MAGENTA)
        win.addstr(" WPM ")

        win.addstr(
            self.number_of_lines_to_print_text + 2, 1, " Enter ", self.Color.BLACK
        )
        win.addstr(" to see replay, ")

        win.addstr(" Tab ", self.Color.BLACK)
        win.addstr(" to retry.")

        win.addstr(
            self.number_of_lines_to_print_text + 3, 1, " Arrow keys ", self.Color.BLACK
        )
        win.addstr(" to change text.")

        win.addstr(
            self.number_of_lines_to_print_text + 4, 1, " CTRL+T ", self.Color.BLACK
        )
        win.addstr(" to tweet result.")

        self.print_stats(win)

        self.first_key_pressed = False
        self.end_time = time.time()
        self.current_string = ""
        self.current_word = ""
        self.token_index = 0

        self.start_time = 0
        if not self.test_complete:
            win.refresh()
            save_history(
                self.text_id, self.current_speed_wpm, "{:.2f}".format(self.accuracy)
            )
            self.test_complete = True

    def typing_mode(self, win, key):
        """Start recording typing session progress.

        Args:
            win (any): Curses window.
            key (str): First typed character of the session.
        """
        # Note start time when first valid key is pressed
        if not self.first_key_pressed and is_valid_initial_key(key):
            self.start_time = time.time()
            self.first_key_pressed = True

        if is_resize(key):
            self.resize(win)

        if not self.first_key_pressed:
            return

        self.key_strokes.append([time.time(), key])

        self.print_realtime_wpm(win)

        self.key_printer(win, key)

    @staticmethod
    def keyinput(win):
        """Retrieve next character of text input.

        Args:
            win (any): Curses window.

        Returns:
            str: Value of typed key.
        """
        key = ""
        try:
            key = win.get_wch()
            if isinstance(key, int):
                if key in (curses.KEY_BACKSPACE, curses.KEY_DC):
                    return "KEY_BACKSPACE"
                if key == curses.KEY_RESIZE:
                    return "KEY_RESIZE"
            return key
        except curses.error:
            return ""

    def key_printer(self, win, key):
        """Print required key to terminal.

        Args:
            win (any): Curses window object.
            key (str): Individual characters are returned as 1-character
                strings, and special keys such as function keys
                return longer strings containing a key name such as
                KEY_UP or ^G.
        """
        # Reset test
        if is_escape(key):
            self.reset_test()

        elif is_ctrl_c(key):
            sys.exit(0)

        # Handle resizing
        elif is_resize(key):
            self.resize(win)

        # Check for backspace
        elif is_backspace(key):
            self.erase_key()

        elif is_ctrl_backspace(key):
            self.erase_word()

        # Ignore spaces at the start of the word (Plover support)
        elif key == " " and len(self.current_word) < self.current_word_limit:
            if self.current_word != "":
                self.check_word()

        elif is_valid_initial_key(key):
            self.appendkey(key)
            self.total_chars_typed += 1

        # Update state of window
        self.update_state(win)

    def resize(self, win):
        """Respond to window resize events.

        Args:
            win (any): Curses window.
        """
        win.clear()

        self.window_height, self.window_width = self.get_dimensions(win)
        self.text = word_wrap(self.text_backup, self.window_width)

        self.screen_size_check()

        self.print_realtime_wpm(win)
        self.setup_print(win)
        self.update_state(win)

    def print_stats(self, win):
        """Print the bottom stats bar after each run.

        Args:
            win (any): Curses window.
        """
        win.addstr(
            self.window_height - 1,
            0,
            " WPM: " + str(self.current_speed_wpm) + " ",
            self.Color.MAGENTA,
        )

        win.addstr(
            " Time: " + "{:.2f}".format(self.time_taken) + "s ",
            self.Color.GREEN,
        )

        win.addstr(
            " Accuracy: " + "{:.2f}".format(self.accuracy) + "% ",
            self.Color.CYAN,
        )

    def print_realtime_wpm(self, win):
        """Print realtime wpm during the test.

        Args:
            win (any): Curses window.
        """
        current_wpm = 0
        total_time = mitype.timer.get_elapsed_seconds_since_first_keypress(
            self.start_time
        )
        if total_time != 0:
            current_wpm = 60 * len(self.current_string.split()) / total_time

        win.addstr(
            0,
            self.window_width - 14,
            " " + "{:.2f}".format(current_wpm) + " ",
            self.Color.CYAN,
        )
        win.addstr(" WPM ")

    def replay(self, win):
        """Play out a recording of the user's last session.

        Args:
            win (any): Curses window.
        """
        win.clear()
        self.print_stats(win)
        win.addstr(self.number_of_lines_to_print_text + 2, 0, " " * self.window_width)
        curses.curs_set(1)

        win.addstr(
            0,
            self.window_width - 14,
            " " + str(self.current_speed_wpm) + " ",
            self.Color.CYAN,
        )
        win.addstr(" WPM ")

        self.setup_print(win)

        win.timeout(10)
        for j in self.key_strokes:
            time.sleep(j[0])
            key = self.keyinput(win)
            if is_escape(key) or is_ctrl_c(key):
                sys.exit(0)
            self.key_printer(win, j[1])
        win.timeout(100)

    def share_result(self):
        """Open a twitter intent on a browser."""
        message = (
            "My typing speed is "
            + self.current_speed_wpm
            + " WPM! Know yours on mitype."
            + "\nhttps://pypi.org/project/mitype/ by @MithilPoojary"
            + "\n#TypingTest"
        )

        # URL encode message
        message = message.replace("\n", "%0D").replace("#", "%23")
        url = "https://twitter.com/intent/tweet?text=" + message
        webbrowser.open(url, new=2)

    def reset_test(self):
        """Reset the data for current typing session."""
        self.mode = 0
        self.current_word = ""
        self.current_string = ""
        self.first_key_pressed = False
        self.key_strokes = []
        self.mistyped_keys = []
        self.start_time = 0
        self.token_index = 0
        self.current_speed_wpm = 0
        self.total_chars_typed = 0
        self.accuracy = 0
        self.time_taken = 0
        curses.curs_set(1)

    def switch_text(self, win, value):
        """Load next or previous text snippet from database.

        Args:
            win (any): Curses window.
            value (int): value to increase or decrement the text ID by.
        """
        if isinstance(self.text_id, str):
            return

        win.clear()

        self.text_id += value
        self.text = load_from_database(self.text_id)[0]
        self.tokens = self.text.split()

        self.text = " ".join(self.tokens)
        self.text_backup = self.text

        self.reset_test()
        self.setup_print(win)
        self.update_state(win)

    @staticmethod
    def get_dimensions(win):
        """Get the height and width of terminal.

        Args:
            win (any): Curses window object.

        Returns:
            (int, int): Tuple of height and width of terminal window.
        """
        dimension_tuple = win.getmaxyx()

        return dimension_tuple

    def screen_size_check(self):
        """Check if screen size is enough to print text."""
        self.number_of_lines_to_print_text = (
            number_of_lines_to_fit_text_in_window(self.text, self.window_width) + 2 + 1
        )
        if self.number_of_lines_to_print_text + 7 >= self.window_height:
            curses.endwin()
            sys.stdout.write("Window too small to print given text")
            sys.exit(1)

    def appendkey(self, key):
        """Append a character to the end of the current word.

        Args:
            key (key): Character to append.
        """
        if len(self.current_word) < self.current_word_limit:
            self.current_word += key
            self.current_string += key

    def erase_key(self):
        """Erase the last typed character."""
        if len(self.current_word) > 0:
            self.current_word = self.current_word[0 : len(self.current_word) - 1]
            self.current_string = self.current_string[0 : len(self.current_string) - 1]

    def erase_word(self):
        """Erase the last typed word."""
        if len(self.current_word) > 0:
            index_word = self.current_word.rfind(" ")
            diff = len(self.current_word) - index_word
            if index_word == -1:
                self.current_string = self.current_string[: -len(self.current_word)]
                self.current_word = ""
            else:
                self.current_word = self.current_word[:-diff]
                self.current_string = self.current_string[:-diff]

    def check_word(self):
        """Accept finalized word."""
        spc = get_space_count_after_ith_word(len(self.current_string), self.text)
        if self.current_word == self.tokens[self.token_index]:
            self.token_index += 1
            self.current_word = ""
            self.current_string += spc * " "
        else:
            self.current_word += " "
            self.current_string += " "
