"""This is the Mitype main app script"""

import curses
import os
import sys
import time

import mitype.calculations
import mitype.commandline
import mitype.keycheck

from datetime import datetime, timedelta
import signal


class App:

    """Class for enclosing all methods required to run Mitype"""

    def __init__(self):

        # Start the parser
        self.text = mitype.commandline.main()[0]
        self.text_id = mitype.commandline.main()[1]
        self.tokens = self.text.split()

        # Convert multiple spaces, tabs, newlines to single space
        self.text = " ".join(self.tokens)
        self.ogtext = self.text

        self.current_word = ""
        self.current_string = ""

        self.key = ""
        self.first_key_pressed = False
        self.key_strokes = []

        self.start_time = 0
        self.end_time = 0

        self.i = 0
        self.mode = 0

        self.window_height = 0
        self.window_width = 0
        self.line_count = 0

        self.current_speed_wpm = 0

        sys.stdout = sys.__stdout__

        # Set ESC delay to 0 (default 1 on linux)
        os.environ.setdefault("ESCDELAY", "0")

        # Start curses on main
        curses.wrapper(self.main)

    def main(self, win):
        """Main function. This is where the infinite loop is executed to
        continuously serve events.

        Args:
            win (object): Curses window object.
        """

        # Initialize windows
        self.initialize(win)

        # Signal logic
        def signal_handler(sig, frame):
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            # Typing mode
            key = self.keyinput(win)

            # Exit when escape key is pressed and test hasn't started
            if mitype.keycheck.is_escape(key) and self.start_time == 0:
                sys.exit(0)

            # Test mode
            if self.mode == 0:
                self.typing_mode(win, key)

            # Replay mode
            elif self.mode == 1 and mitype.keycheck.is_enter(key):
                # Start replay if enter key is pressed
                self.replay(win)

            # Refresh for changes to show up on window
            win.refresh()

    def typing_mode(self, win, key):
        # Note start time when first valid key is pressed
        if not self.first_key_pressed and mitype.keycheck.is_valid_initial_key(key):
            self.start_time = time.time()
            self.first_key_pressed = True

        if mitype.keycheck.is_resize(key):
            self.resize(win)

        if not self.first_key_pressed:
            return

        self.key_strokes.append([time.time(), key])

        self.key_printer(win, key)

    def initialize(self, win):

        # Find window dimensions
        self.window_height, self.window_width = self.get_dimensions(win)

        # Adding word wrap to text
        self.text = self.word_wrap(self.text, self.window_width)

        # Find number of lines required to print text
        self.line_count = (
            mitype.calculations.number_of_lines_to_fit_string_in_window(
                self.text, self.window_width
            )
            + 2  # Top 2 lines
            + 1  # One empty line after text
        )

        # If required number of lines are more than the window height, exit
        # +3 for printing stats at the end of the test
        if self.line_count + 3 > self.window_height:
            self.size_error()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

        win.nodelay(False)

        self.setup_print(win)

    @staticmethod
    def get_dimensions(win):
        """Get the width of terminal.

        Args:
            win (object): Curses window object.

        Returns:
            (integer): Return width of terminal window.
        """
        dimension_tuple = win.getmaxyx()

        return dimension_tuple

    def setup_print(self, win):
        """Print setup text at beginning of each typing session.

        Args:
            win (object): Curses window object.
        """

        # Top strip
        # Display text ID
        win.addstr(0, 0, " ID:{} ".format(self.text_id), curses.color_pair(3))

        # Display Title
        win.addstr(0, int(self.window_width / 2) - 4, " MITYPE ", curses.color_pair(3))

        # Print text in BOLD from 3rd line
        win.addstr(2, 0, self.text, curses.A_BOLD)

    def key_printer(self, win, key):
        """Print required key to terminal.

        Args:
            win (object): Curses window object.
            key (string): Individual characters are returned as 1-character
                          strings, and special keys such as function keys
                          return longer strings containing a key name such as
                          KEY_UP or ^G.
        """

        # Reset test
        if mitype.keycheck.is_escape(key):
            self.reset_test()

        # Handle resizing
        elif mitype.keycheck.is_resize(key):
            self.resize(win)

        # Check for backspace
        elif mitype.keycheck.is_backspace(key):
            self.erase_key()

        # Check for space
        elif key == " ":
            self.check_word()

        # Check for any other typable characters
        elif mitype.keycheck.is_valid_initial_key(key):
            self.appendkey(key)

        # Update state of window
        self.update_state(win)

    def keyinput(self, win):
        key = ""
        while key == "":
            try:
                if sys.version_info[0] < 3:
                    key = win.getkey()
                    return key

                key = win.get_wch()
                if isinstance(key, int):
                    if key in (curses.KEY_BACKSPACE, curses.KEY_DC):
                        return "KEY_BACKSPACE"
                    if key == curses.KEY_RESIZE:
                        return "KEY_RESIZE"
            except curses.error:
                continue
        return key

    def erase_key(self):
        if len(self.current_word) > 0:
            self.current_word = self.current_word[0 : len(self.current_word) - 1]
            self.current_string = self.current_string[0 : len(self.current_string) - 1]

    def check_word(self):
        spc = mitype.calculations.get_space_count_after_ith_word(
            len(self.current_string), self.text
        )
        if self.current_word == self.tokens[self.i]:
            self.i += 1
            self.current_word = ""
            self.current_string += spc * " "
        else:
            self.current_word += " "
            self.current_string += " "

    def appendkey(self, key):
        self.current_word += key
        self.current_string += key

    def update_state(self, win):
        win.addstr(self.line_count, 0, " " * self.window_width)
        win.addstr(self.line_count, 0, self.current_word)

        win.addstr(2, 0, self.text, curses.A_BOLD)
        win.addstr(2, 0, self.text[0 : len(self.current_string)], curses.A_DIM)

        index = mitype.calculations.first_index_at_which_strings_differ(
            self.current_string, self.text
        )
        win.addstr(
            2 + index // self.window_width,
            index % self.window_width,
            self.text[index : len(self.current_string)],
            curses.color_pair(2),
        )

        if index == len(self.text):
            win.addstr(self.line_count, 0, " Your typing speed is ")
            if self.mode == 0:
                self.current_speed_wpm = mitype.calculations.speed_in_wpm(
                    self.tokens, self.start_time
                )

            win.addstr(" " + self.current_speed_wpm + " ", curses.color_pair(1))
            win.addstr(" WPM ")

            win.addstr(self.line_count + 2, 0, " Press ")

            win.addstr(" Enter ", curses.color_pair(6))

            win.addstr(" to see a replay! ")

            if self.mode == 0:
                self.mode = 1
                for k in range(len(self.key_strokes) - 1, 0, -1):
                    self.key_strokes[k][0] -= self.key_strokes[k - 1][0]
            self.key_strokes[0][0] = 0
            self.first_key_pressed = False
            self.end_time = time.time()
            self.current_string = ""
            self.current_word = ""
            self.i = 0

            self.start_time = 0
        win.refresh()

    def reset_test(self):
        self.current_word = ""
        self.current_string = ""
        self.first_key_pressed = False
        self.key_strokes = []
        self.start_time = 0
        self.i = 0
        self.current_speed_wpm = 0

    def replay(self, win):

        win.addstr(self.line_count + 2, 0, " " * self.window_width)

        self.setup_print(win)

        for j in self.key_strokes:
            time.sleep(j[0])

            self.key_printer(win, j[1])

    @staticmethod
    def word_wrap(text, width):

        """Based on the window width, return text with extra spaces
        which makes the string word wrap.

        Args:
            text (string): Text to wrap.
            width (integer): Width to wrap around.

        Returns:
            (string): Return altered text.
        """
        # For the end of each line, move backwards until you find a space.
        # When you do, append those many spaces after the single space.
        for x in range(
            1,
            mitype.calculations.number_of_lines_to_fit_string_in_window(text, width)
            + 1,
        ):
            if not (x * width >= len(text) or text[x * width - 1] == " "):
                i = x * width - 1
                while text[i] != " ":
                    i -= 1
                text = text[:i] + " " * (x * width - i) + text[i + 1 :]
        return text

    def resize(self, win):
        win.clear()
        self.window_height, self.window_width = self.get_dimensions(win)

        self.text = self.word_wrap(self.ogtext, self.window_width)
        self.line_count = (
            mitype.calculations.number_of_lines_to_fit_string_in_window(
                self.text, self.window_width
            )
            + 2
            + 1
        )
        self.setup_print(win)
        self.update_state(win)

    @staticmethod
    def size_error():
        sys.stdout.write("Window too small to print given text")
        curses.endwin()
        sys.exit(4)
