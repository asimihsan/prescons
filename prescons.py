# presentation console
# - a python interpreter for "pseudo-interative" demos
#
# usage: $ python prescons.py <filename>
#
# <filename> should be a file that contains python code as would be entered
# directly in a terminal - see example.py
#
# while running, press 'space' to move through the code
#
# github.com/inglesp/prescons

from code import InteractiveConsole
from StringIO import StringIO
import sys, termios, tty

# get character from stdin
# based on http://code.activestate.com/recipes/134892/
# *nix only, and doesn't handle arrow keys well
def getch(ch=None):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        while True:
            tty.setraw(fd)
            gotch = sys.stdin.read(1)
            if ch is None or gotch == ch:
                break
            if ord(gotch) == 3:
                raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# subclasses InteractiveConsole from code module
class PresentationConsole(InteractiveConsole):
    def __init__(self, path):
        self.file = open(path)
        InteractiveConsole.__init__(self)

    def raw_input(self, prompt=''):
        self.write(prompt)
        if prompt == sys.ps1:
            try:
                getch(' ')
            except KeyboardInterrupt:
                print "KeyboardInterrupt"
                exec "import ipdb; ipdb.set_trace()" in self.locals
        line = self.file.readline()
        if len(line) == 0:
            self.file.close()
            raise EOFError
        self.write(line)
        return line.rstrip()

    def runcode(self, code):
        sys.stdout = StringIO()
        InteractiveConsole.runcode(self, code)
        output = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__
        if len(output) > 0:
            getch(' ')
            self.write(output)

if __name__ == '__main__':
    path = sys.argv[1]
    console = PresentationConsole(path)
    console.interact()
