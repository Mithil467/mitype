"""This is the Mitype main app script"""

import curses
import os
import random
import sys
import time

from mitype import calculations
from mitype import database
from mitype import keycheck


class App:

    """Class for enclosing all methods required to run Mitype"""

    def __init__(self):
        self.current_word, self.current_string = "", ""
        self.key, self.text = "", ""
        self.tokens = []
        self.first_key_pressed = False
        self.start_time = self.i = self.mode = self.end_time = 0

        self.win_width = 0

        self.line_count = 0
        self.curr_wpm = 0
        self.key_strokes = []

    @staticmethod
    def get_dimensions(win):
        """Get the width of terminal.

        Args:
            win (object): Curses window object.

        Returns:
            (integer): Return width of terminal window.
        """
        return int(win.getmaxyx()[1])

    def initialize(self, win):
        """Initialize curses"""
        curses.initscr()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        win.nodelay(True)
        self.tokens = self.text.split()

        self.win_width = self.get_dimensions(win)

        self.text = self.word_wrap(self.text, self.win_width)

        self.line_count = calculations.count_lines(self.text, self.win_width) + 2 + 1

        self.setup_print(win)

    def setup_print(self, win):
        """Print setup text at beginning of each typing session.

        Args:
            win (object): Curses window object.
        """
        win.addstr(0, 0, " " * (self.win_width), curses.color_pair(3))
        win.addstr(0, 0, " Made by Mithil", curses.color_pair(3))
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
        if keycheck.is_escape(key):
            sys.exit(0)

        elif keycheck.is_resize(key):
            # TODO handle resize
            pass

        elif keycheck.is_backspace(key):
            self.EraseKey()

        elif key == " ":
            self.check_word()

        elif len(key) == 1:
            self.appendkey(key)

        self.UpdateState(win)

    def main(self, win):
        """Main function. This is where the infinite loop is executed to
        continuously serve events.

        Args:
            win (object): Curses window object.
        """
        self.initialize(win)

        while True:
            # Typing mode
            if self.mode == 0:
                key = self.keyinput(win)

                if keycheck.is_escape(key):
                    sys.exit(0)

                if not self.first_key_pressed:
                    if keycheck.is_valid_initial_key(key):
                        self.start_time = time.time()
                        self.first_key_pressed = True
                    else:
                        continue

                self.key_strokes.append([time.time(), key])

                self.key_printer(win, key)
            # Replay mode
            elif self.mode == 1:
                key = self.keyinput(win)
                if keycheck.is_enter(key):
                    self.Replay(win)

                elif keycheck.is_escape(key):
                    sys.exit(0)

            win.refresh()

    def keyinput(self, win):
        key = ""
        while key == "":
            try:
                key = win.getkey()
            except curses.error:
                continue
        return key

    def EraseKey(self):
        if len(self.current_word) > 0:
            self.current_word = self.current_word[0 : len(self.current_word) - 1]
            self.current_string = self.current_string[0 : len(self.current_string) - 1]

    def check_word(self):
        spc = calculations.get_spc_count(len(self.current_string), self.text)
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

    def UpdateState(self, win):
        win.addstr(self.line_count, 0, " " * self.win_width)
        win.addstr(self.line_count, 0, self.current_word)

        win.addstr(2, 0, self.text, curses.A_BOLD)
        win.addstr(2, 0, self.text[0 : len(self.current_string)], curses.A_DIM)

        index = calculations.change_index(self.current_string, self.text)
        win.addstr(
            2 + index // self.win_width,
            index % self.win_width,
            self.text[index : len(self.current_string)],
            curses.color_pair(2),
        )

        if index == len(self.text):
            win.addstr(self.line_count, 0, "Your typing speed is ")
            if self.mode == 0:
                self.curr_wpm = calculations.get_wpm(self.tokens, self.start_time)
            win.addstr(self.curr_wpm, curses.color_pair(1))
            win.addstr(" WPM ")

            win.addstr(
                self.line_count + 2,
                0,
                "Press enter to see a replay!",
                curses.color_pair(6),
            )

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

    def Replay(self, win):
        win.addstr(self.line_count + 2, 0, " " * self.win_width)
        self.setup_print(win)
        for j in self.key_strokes:
            time.sleep(j[0])
            self.key_printer(win, j[1])
            key_within_replay = ""
            try:
                key_within_replay = win.getkey()
            except curses.error:
                pass
            if keycheck.is_escape(key_within_replay):
                sys.exit(0)
            win.refresh()

    def start(self):
        """Start app. Starts main in curses wrapper."""

        self.parse()
        os.environ.setdefault("ESCDELAY", "0")
        curses.wrapper(self.main)

    def parse(self):
        opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
        args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
        if "-f" in opts:
            try:
                self.text = open(args[0]).read()
            except:
                print("Cannot open file -", args[0])
                sys.exit(0)
        elif "-d" in opts:
            try:
                limit = int(args[0])
            except:
                print("Expected an integer")
                sys.exit(0)
            if limit not in range(1, 6):
                print("Please enter a difficulty level between 1 and 5")
                sys.exit(0)

            # total entries in db = 6000
            # 5 sections of each difficulty
            self.text = database.generate(limit * 1200)
        else:
            # Default difficulty when no parameters are passed
            limit = 3
            self.text = database.generate(limit * 1200)

    def word_wrap(self, text, width):
        x = 1
        while x <= calculations.count_lines(text, width):
            if x * width >= len(text):
                pass
            elif text[x * width - 1] == " ":
                pass
            else:
                i = x * width - 1
                while text[i] != " ":
                    i -= 1
                text = text[:i] + " " * (x * width - i) + text[i + 1 :]
            x += 1
        return text
