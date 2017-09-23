import constants
from Tkinter import *
import random
import string
from PIL import Image, ImageTk

    

class Square(constants.correction):
    def debug_click(self, event):
        row = int(event.y/constants.grid_size)
        column = int(event.x/constants.grid_size)
        o = string.Template('Clicked {x:$column, y:$row}').substitute({'column':column, 'row': row})
        print o
        s = self.app.screen.grid[row][column]
        print "Type: " + s.square_type
        print "Passable: " +str(s.passable)
        print "Occupied: " + str(s.occupied)

    def __init__(self, row, column, canvas, app, g=constants.grid_size, square_type='grass'):
        if canvas is not None:
            self.canvas = canvas
            if square_type == 'grass':
                fill='green'
                self.passable=True
            elif square_type == 'water':
                fill='blue'
                self.passable = False
            self.representation = canvas.create_rectangle(
                (column*g)+5, 
                (row*g)+5, 
                ((column+1)*g)+5, 
                ((row+1)*g)+5,
                fill=fill)
            self.canvas.bind("<Button-1>", self.debug_click)
            self.canvas.bind("<Control-Button-1>", app.edit_square)
        self.square_type = square_type
        self.row=row
        self.column=column
        self.app = app
        self.occupied=False

class Sprite(constants.correction):
    def __init__(self,app):
        constants.l('test',{})
        h = constants.bounds["y"][1]
        w = constants.bounds["x"][1]
        g = constants.grid_size
        cx = w/(2*g)
        cy = h/(2*g)
        img = Image.open("sprites/sm_tux.gif")

        # self.p= PhotoImage(file="sprites/tux.gif")
        # img.thumbnail((g,g))
        self.p_sprite = ImageTk.PhotoImage(img)
        self.row=cy
        self.column=cx
        original_cx = cx

        s=app.screen.grid[cy][cx]
        tries=0
        # s.square_type='water'
        # s.passable=False
        while (s.square_type != 'grass') and (tries < 20):
            constants.l('Moving from {x:$x, y:$y}', {'x':cx,'y':cy})
            if cx>0:
                cx-=1
            else:
                cx=original_cx
                cy-=1
            tries+=1
            s=app.screen.grid[cy][cx]
        if tries == 20:
            app.screen=Screen(app)


        self.sprite = app.screen.canvas.create_image(((cx+0.5)*g)+5, ((cy+0.5)*g)+5, image=self.p_sprite)
        app.screen.grid[cy][cx].occupied=True

class Monster(constants.correction):
    def __init__(self,app):
        constants.l('Placing Monster',{})
        h = constants.bounds["y"][1]
        w = constants.bounds["x"][1]
        g = constants.grid_size
        cx = w/(2*g)+1
        cy = h/(2*g)
        img = Image.open("sprites/sm_monster.gif")

        # self.m= PhotoImage(file="sprites/monster.gif")
        # img.thumbnail((g,g))
        self.m_sprite = ImageTk.PhotoImage(img)
        self.row=cy
        self.column=cx
        original_cx = cx

        s=app.screen.grid[cy][cx]
        tries=0
        # s.square_type='water'
        # s.passable=False
        while (s.passable is False or s.occupied is True) and (tries < 20):
            constants.l('Moving from {x:$x, y:$y}', {'x':cx,'y':cy})
            if cx<(w/g)-2:
                cx+=1
            else:
                cx=original_cx
                cy+=1
            tries+=1
            s=app.screen.grid[cy][cx]

        self.sprite = app.screen.canvas.create_image(((cx+0.5)*g)+5, ((cy+0.5)*g)+5, image=self.m_sprite)
        app.screen.grid[cy][cx].occupied=True

def Trees(app):
    constants.l('Placing Trees',{})
    h = constants.bounds["y"][1]
    w = constants.bounds["x"][1]
    g = constants.grid_size
    img = Image.open("sprites/sm_tree.gif")
    # app.t= PhotoImage(file="sprites/tree.gif")
    img.thumbnail((g,g))
    app.t_sprite = ImageTk.PhotoImage(img)

    for row in app.screen.grid:
        for s in row:
            t=random.randint(0,12)%3 == 0
            if (t and s.square_type == "grass" and not s.occupied):
                s.tree_sprite = app.screen.canvas.create_image(((s.column+0.5)*g)+5, ((s.row+0.5)*g)+5, image=app.t_sprite)                    
                s.has_tree=True



class Screen(constants.correction):
    def __init__(self,app, height=constants.bounds["y"][1], width=constants.bounds["x"][1], grid=constants.grid_size):
        h=height
        g=grid
        w=width
        self.canvas=Canvas(app.frame, height=h+10, width=w+10, background="green")
        self.grid = []
        for i in range(0,(h/g)):
            self.grid.append([])
            # print app.grid[i]
            for j in range(0,(w/g)):
                r = random.randint(0,12)
                if r%4 == 0:
                    square_type = 'water'
                else:
                    square_type = 'grass'
                s = Square(i,j, self.canvas, app=app, square_type=square_type)
                self.grid[i].append(s)


class Map(constants.correction):
    def __init__(self, screens_height, screens_width):
        print "Map"


