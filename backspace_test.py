import curses

def main(win):
    while True:
        try:
            key = win.get_wch()
            win.addstr(str(key))
            win.addstr(str(key=="\x7f"))
        except:
            pass

curses.wrapper(main)