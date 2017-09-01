from Tkinter import *
import random

class Application(Frame):
    MIN = 1
    MAX = 10
    guesses=0
    def guess(self):
        text = self.entry_text.get()
        try:
            i=int(text)
            self.guesses+=1
            if i<self.n:
                text="Higher"
            elif i>self.n:
                text="Lower"
            else:
                text="You guessed it in " + str(self.guesses) + " guesses."
        except:
            text="Invalid input"
        self.entry_text.set("")
        self.o.set(text)

    def start_game(self):
        self.n = int(random.randrange(self.MIN,self.MAX,1))
        self.o.set("I'm thinking of a number between 1 and 10")
        self.guesses=0

    def createWidgets(self):
        self.o = StringVar()
        self.Output = Label(self, textvariable=self.o)
        self.Output.pack()

        self.entry_text = StringVar()
        self.e = Entry(self, width=50, textvariable=self.entry_text)
        self.e.pack()

        self.start = Button(self)
        self.start["text"] = "Start",
        self.start["command"] = self.start_game
        self.start.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Guess",
        self.hi_there["command"] = self.guess
        self.hi_there.pack({"side": "left"})

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["foreground"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})
        

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()