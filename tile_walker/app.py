from Tkinter import *
from PIL import Image, ImageTk
import constants
import sprites
import string

class Application(Frame):
    selected_square=None
    def make_water(self):
        s=self.selected_square
        s.passable=False
        s.square_type='water'
        self.screen.canvas.itemconfig(s.representation, fill='blue')
        self.selected_square=None
    def make_grass(self):
        s=self.selected_square
        s.passable=True
        s.square_type='grass'
        self.screen.canvas.itemconfig(s.representation, fill='green')
        self.selected_square=None
    def edit_square(self, event):
        row = int(event.y/constants.grid_size)
        column = int(event.x/constants.grid_size)
        o = string.Template('Right Clicked {x:$column, y:$row}').substitute({'column':column, 'row': row})
        print o
        ss = self.screen
        s = ss.grid[row][column]
        self.selected_square = s
        print s.square_type
        if s.square_type == 'grass':
            self.popup.entryconfig('Make Grass', state='disabled')
            self.popup.entryconfig('Make Water', state='normal')
        elif s.square_type == 'water':
            self.popup.entryconfig('Make Water', state='disabled')
            self.popup.entryconfig('Make Grass', state='normal')
        print s.passable
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup.grab_release()

    def keypress(self, event):
        h = constants.bounds["y"][1]
        w = constants.bounds["x"][1]
        g = constants.grid_size

        # for d in event.__dict__.keys():
        #     print d
        # print event.keycode

        c = self.screen.canvas

        p=c.coords(self.tux.sprite)

        current_row = int((p[1]-4)/g)
        current_column = int((p[0]-4)/g)
        max_row = int(h/g)-1
        max_column = int(w/g)-1

        # o = string.Template('In {x:$column, y:$row}').substitute({
        #     'column':current_column, 
        #     'row': current_row
        #     })
        # print o

        if event.keycode == 8320768: 
            if current_row > 0:
                # o = string.Template('Moving to: {x:$column, y:$row}').substitute({
                #     'column':current_column, 
                #     'row': current_row-1
                #     })
                # print o
                # print self.screen.grid[current_row-1][current_column].square_type

                if self.screen.grid[current_row-1][current_column].passable:
                    self.screen.canvas.move(self.tux.sprite,0,-g)
        elif event.keycode == 8255233: 
            if current_row < max_row:
                if self.screen.grid[current_row+1][current_column].passable:
                    self.screen.canvas.move(self.tux.sprite,0,g)
        elif event.keycode == 8124162: 
            if current_column > 0:
                if self.screen.grid[current_row][current_column-1].passable:
                    self.screen.canvas.move(self.tux.sprite,-g,0)
        elif event.keycode == 8189699: 
            if current_column < max_column:
                if self.screen.grid[current_row][current_column+1].passable:
                    self.screen.canvas.move(self.tux.sprite,g,0)
        elif event.keycode == 262248:
            print "harvest"
        else:
            print event.keycode

    def addSprites(self):
        self.tux = sprites.Sprite(self)
        self.screen.monsters=[]
        for i in range(0,10):
            self.screen.monsters.append(sprites.Monster(self))
        sprites.Trees(self)

    def display_inventory(self):
        self.inventory = {
            "wood": {"display": "Wood", "qty" : 1},
            "spears":{"display": "Spears", "qty": 10}
            }
        si=self.inventory
        row=0;
        for key in self.inventory:    
            si[key]["s"]=StringVar()
            si[key]["s"].set(self.inventory[key]["qty"])
            si[key]["l1"]=Label(self.frame2, text=si[key]["display"]+": ", bg="gray")
            si[key]["l2"]=Label(self.frame2, textvariable=si[key]["s"], bg="gray")
            si[key]["l1"].grid(row=row, column=0, sticky="we")
            si[key]["l2"].grid(row=row, column=1, sticky="we")
            row+=1

    def createWidgets(self):
        global root
        self.frame = Frame(root)
        self.frame2 = Frame(root)
        self.frame.pack(fill=BOTH, expand=1, side="left")

        self.screen = sprites.Screen(self)
        self.addSprites()
        self.screen.canvas.pack(fill=BOTH, expand=1)
        self.display_inventory()
        self.frame2.pack(fill=BOTH, expand=1, side="right")


        self.screen.canvas.focus_set()
        self.screen.canvas.bind("<Key>", self.keypress)
        # menubar = Menu(root)
        # filemenu = Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Bigger", command=self.make_balls_bigger)
        # filemenu.add_command(label="Smaller", command=self.make_balls_smaller)
        # menubar.add_cascade(label="Size", menu=filemenu)
        # root.config(menu=menubar)

    def create_popups(self):
        self.popup = Menu(root, tearoff=0)
        self.popup.add_command(label="Make Grass", command=self.make_grass) # , command=next) etc...
        self.popup.add_command(label="Make Water", command=self.make_water)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.create_popups()
        # self.animate()

root = Tk()
app = Application(master=root)
app.mainloop()
try: 
    root.destroy()
except:
    print "Couldn't destroy root. Maybe try a bigger drill?"