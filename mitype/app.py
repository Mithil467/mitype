import curses
import os
import curses.ascii
import time
import math
import random
import platform
import sqlite3


class App:

    CurrentWord, CurrentString, key, TEXT = '', '', '', ''
    TOK = []
    FirstKeyPressed = False
    start_time = i = mode = end_time = 0

    winWidth = 0

    LineCount = 0
    CurrWPM = 0
    KeyStrokes = []

    def DirectoryPath(self):
        path = os.path.abspath(__file__)
        LastIndex = 0
        SlashCharacter1 = '\\'
        SlashCharacter2 = '/'
        for j in range(len(path)):
            if path[j] == SlashCharacter1 or path[j] == SlashCharacter2:
                LastIndex = j
        return path[0:LastIndex+1]

    def search(self, id):
        pathStr = self.DirectoryPath()+"data.db"
        conn = sqlite3.connect(pathStr)
        cur = conn.cursor()
        cur.execute("SELECT txt FROM data where id=?", (id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def generate(self):
        NumberOfTextEntries = 6000
        s = self.search(random.randrange(1, NumberOfTextEntries + 1))
        return s[0][0]

    def ChangeIndex(self, a, b):
        if len(a) == 0:
            return 0
        length = min(len(a), len(b))
        for i in range(length):
            if a[i] != b[i]:
                return i
        return length

    def getWPM(self, TXT, start_time):
        TimeTaken = 60 * len(TXT) / self.getTimeElasped(start_time)
        return "{0:.2f}".format(TimeTaken)

    def getTimeElasped(self, start_time):
        return (time.time() - start_time)

    def CountLines(self, s, winWidth):
        return math.ceil(len(s) / winWidth)

    def is_escape(self, key):
        if len(key) == 1:
            return ord(key) == curses.ascii.ESC
        return False

    def is_backspace(self, key):
        if key == 'KEY_BACKSPACE':
            return True
        if len(key) == 1:
            ord(key) == curses.ascii.BS or key == '\b'
        return False

    def getDimensions(self, win):
        return win.getmaxyx()[1]

    def Init(self):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    def SetupPrint(self, win):
        win.addstr(0, 0, ' '*(self.winWidth), curses.color_pair(3))
        win.addstr(0, 0, ' Made by Mithil', curses.color_pair(3))
        win.addstr(2, 0, self.TEXT, curses.A_BOLD)

    def KeyPrinter(self, win, key):
        if self.is_escape(key):
            exit(0)

        elif self.is_backspace(key):
            if len(self.CurrentWord) > 0:
                self.CurrentWord = self.CurrentWord[0:len(self.CurrentWord)-1]
                self.CurrentString = self.CurrentString[0:len(
                    self.CurrentString)-1]

        elif key == ' ':
            if self.CurrentWord == self.TOK[self.i]:
                self.i += 1
                self.CurrentWord = ''
            else:
                self.CurrentWord += ' '
            self.CurrentString += ' '

        elif len(key) == 1:
            self.CurrentWord += key
            self.CurrentString += key

        win.addstr(self.LineCount, 0, ' '*self.winWidth)
        win.addstr(self.LineCount, 0, self.CurrentWord)

        win.addstr(2, 0, self.TEXT, curses.A_BOLD)
        win.addstr(2, 0, self.TEXT[0:len(self.CurrentString)], curses.A_DIM)

        index = self.ChangeIndex(self.CurrentString, self.TEXT)
        win.addstr(2+index//self.winWidth, index % self.winWidth,
                   self.TEXT[index:len(self.CurrentString)], curses.color_pair(2))

        if index == len(self.TEXT):
            win.addstr(self.LineCount, 0, "Your typing speed is ")
            if self.mode == 0:
                self.CurrWPM = self.getWPM(self.TOK, self.start_time)
            win.addstr(self.CurrWPM,
                       curses.color_pair(1))
            win.addstr(' WPM ')

            win.addstr(self.LineCount+2, 0,
                       "Press enter to see a replay!", curses.color_pair(6))

            if self.mode == 0:
                self.mode = 1
                for k in range(len(self.KeyStrokes)-1, 0, -1):
                    self.KeyStrokes[k][0] -= self.KeyStrokes[k-1][0]
            self.KeyStrokes[0][0] = 0
            self.FirstKeyPressed = False
            self.end_time = time.time()
            self.CurrentString = ''
            self.CurrentWord = ''
            self.i = 0
            # for k in range(len(self.KeyStrokes)):
            #     self.KeyStrokes[k][0] -= self.start_time

            self.start_time = 0

    def main(self, win):
        curses.initscr()
        self.Init()
        win.nodelay(True)
        self.TEXT = self.generate()
        self.TOK = self.TEXT.split()

        self.winWidth = self.getDimensions(win)

        self.LineCount = self.CountLines(self.TEXT, self.winWidth) + 2 + 1

        self.SetupPrint(win)

        while(True):

            if self.mode == 0:
                try:
                    key = win.getkey()
                except Exception:
                    continue

                if self.FirstKeyPressed == False:
                    self.start_time = time.time()
                    self.FirstKeyPressed = True

                self.KeyStrokes.append([time.time(), key])

                self.KeyPrinter(win, key)

            elif self.mode == 1:
                # self.mode = 3
                key = ''
                try:
                    key = win.getkey()
                except Exception:
                    pass
                if key == '\n':
                    win.addstr(self.LineCount+2, 0, ' '*self.winWidth)
                    self.SetupPrint(win)
                    for j in self.KeyStrokes:
                        time.sleep(j[0])
                        self.KeyPrinter(win, j[1])
                        keyWithinReplay = ''
                        try:
                            keyWithinReplay = win.getkey()
                        except Exception:
                            pass
                        if self.is_escape(keyWithinReplay):
                            exit(0)
                        win.refresh()

                elif self.is_escape(key):
                    exit(0)

            win.refresh()

    def start(self):
        curses.wrapper(self.main)
