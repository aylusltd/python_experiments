from Tkinter import *

# import random

class Application(Frame):
    bounds = {
        "x": [0,1000],
        "y": [0,500]
    }
    velocity = {
        "x":0,
        "y":0
    }

    direction = {
        "down" : 1,
        "up": -1,
        "left":-1,
        "right":1
    }

    FRAME_RATE = 70
    INTERVAL = 1000 / FRAME_RATE

    DRAG = 1
    x_dir = 'left'
    y_dir = 'down'

    # 50 px = 1m
    # 50 fps
    gravity = 50 * 9.8 / FRAME_RATE
    def configure(self, event):
        w,h = event.width, event.height
        self.bounds["x"][1] = w
        self.bounds["y"][1] = h

    def animate(self):
        w = self.bounds["x"][1]
        h = self.bounds["y"][1]
        d = self.direction
        b = self.balls[0]["ball"]

        if self.balls[0].get("frozen", None) is None:        
            self.velocity["x"] -= self.DRAG
            self.velocity["y"] -= self.DRAG
        
        c = self.canvas.coords(b)
        #(left, top, right, bottom)

        g=self.gravity
        
        if c[3] >= self.bounds["y"][1]:
            self.y_dir = 'up'
            self.canvas.move(b, 0, -(c[3]-h))
            # g=self.gravity * 0            
        elif c[1] <= 0:
            self.y_dir = 'down'
            self.canvas.move(b, 0, -c[1])
        if c[2] >= w:
            self.x_dir = 'left'
            self.canvas.move(b, -(c[2]-(w)), 0)
        elif c[0] <= 0:
            self.x_dir = 'right'
            self.canvas.move(b, -c[0], 0)

        if self.balls[0].get("frozen", None) is None:        
            if self.y_dir == "up":
                self.velocity["y"] -= g
            else:
                self.velocity["y"] += g

            if self.velocity["x"] < 0:
                self.velocity["x"] = 0
            if self.velocity["y"] < 0:
                self.velocity["y"] = 0
                if c[3] < h-self.gravity and self.y_dir == "up":
                    self.y_dir="down"
            if self.balls[0]["props"]["moved"]:
                x_move = self.balls[0]["props"]["last_move"]["x"] * 2
                y_move = self.balls[0]["props"]["last_move"]["y"] * 2
                if x_move <0:
                    self.x_dir="left"
                    self.velocity["x"] = -x_move
                else:
                    self.x_dir="right"
                    self.velocity["x"] = x_move
                if y_move <0:
                    self.y_dir="up"
                    self.velocity["y"] = -y_move
                else:
                    self.y_dir="down"
                    self.velocity["y"] = y_move
                self.balls[0]["props"]["moved"] = False
            else:
                x_move = int(self.velocity["x"] * d[self.x_dir] *10)/10
                y_move = int(self.velocity["y"] * d[self.y_dir] *10)/10             

            self.canvas.move(b,x_move, y_move)
            self.canvas.update()
        root.after(self.INTERVAL,self.animate)

    def animate2(self):
        for ball in self.balls:
            pos = self.canvas.coords(ball.ball)
            ball.props["v"]["x"]

    def make_ball_bigger(self, event=None):
        b = self.balls[0]["ball"]
        c = self.canvas
        p = c.coords(b)
        print p
        if (p[2]-p[0]) < 100:
            p[0]-=10
            p[1]-=10
        c.coords(b, p[0], p[1], p[2], p[3])

    def make_ball_smaller(self, event=None):
        b = self.balls[0]["ball"]
        c = self.canvas
        p = c.coords(b)
        if (p[2]-p[0]) > 10:
            p[0]+=10
            p[1]+=10
        c.coords(b, p[0], p[1], p[2], p[3])

    def keypress(self, event):
        print "Test"
        print event

    def createWidgets(self):
        global root
        self.frame = Frame(root)
        self.frame.pack(fill=BOTH, expand=1)
        self.canvas=Canvas(self.frame, height=self.bounds["y"][1], width=self.bounds["x"][1])
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.balls =[]
        ball1=self.canvas.create_oval(10,10,50,50, tags='ball', fill='red')
        self.balls.append({"ball": ball1, "props":{"last_move":{"x":0,"y":0}, "moved":False}})
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.bind("<Configure>", self.configure)
        self.canvas.focus_set()
        self.canvas.bind("<Mod1-equal>", self.make_ball_bigger)
        self.canvas.bind("<Mod1-minus>", self.make_ball_smaller)
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Bigger", command=self.make_ball_bigger)
        filemenu.add_command(label="Smaller", command=self.make_ball_smaller)
        menubar.add_cascade(label="Size", menu=filemenu)
        root.config(menu=menubar)
        self.animate()

    def click(self, event):
        selected=False
        for ball in self.balls:
            b=ball["ball"]
            c=self.canvas
            pos = c.coords(b)
            if pos[0] <= event.x <= pos[2] and pos[1] <= event.y <= pos[3]:
                # click in ball
                if selected is False:
                    self.clicked_ball = ball
                    selected = True
                # print "In ball"
        if selected is False:
            self.clicked_ball = None

    def drag(self, event):
        if self.bounds["x"][0] > event.x or event.x > self.bounds["x"][1]-20:
            print event.x
            print self.bounds["x"][0]
            print self.bounds["x"][1]
            return None 
        if self.bounds["y"][0] > event.y or event.y> self.bounds["y"][1]-20:
            print event.y
            print self.bounds["y"][0]
            print self.bounds["y"][1]
            return None

        if self.clicked_ball is not None:
            ball = self.clicked_ball
            b=ball["ball"]
            c=self.canvas
            pos = c.coords(b)
            
            if ball.get("prev_position", None) is not None:
                prev_position = ball["prev_position"]
                if prev_position["x"] != event.x or prev_position["y"] != event.y:
                    delta_x = event.x - prev_position["x"]
                    delta_y = event.y - prev_position["y"]
                    c.move(b, delta_x, delta_y)
                    ball["props"]["last_move"]["x"] = delta_x
                    ball["props"]["last_move"]["y"] = delta_y
                    ball["props"]["moved"] = True
            ball["prev_position"] = {"x":event.x, "y":event.y}
            ball["frozen"] = True

    def release(self, event):
        for ball in self.balls:
            ball["frozen"] = None
            ball["prev_position"] = None

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()