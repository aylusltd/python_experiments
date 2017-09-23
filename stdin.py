import sys
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setraw(sys.stdout.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
# with open('help.txt', 'wb') as myfile:
#     h = help(sys.stdin)
#     myfile.write(h)
#     myfile.close()

buff = []
EXIT=False

match_b = False
match_y = False
match_e = False

last_4=[]

while not EXIT:
    c = getch()
    if c == "\x03":
        buff.extend(last_4)
        EXIT = True
    last_4.append(c)
    if len(last_4)>4:
        buff.append(last_4.pop(0))
    if last_4 == ["b","y","e","\r"]:
        print "\nbye"
        EXIT = True
    # if c != "\r":
    sys.stdout.write(c)
    # print last_4
    # else:
s = str(buff)
print s
