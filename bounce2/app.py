from Tkinter import *
from ball import ball 
from detect_collisions import detect_collisions
from point import point
import constants

class Application(Frame):
    def animate(self):
        w = constants.bounds["x"][1]
        h = constants.bounds["y"][1]
        for ball in self.balls:
            b=ball.representation
            p=self.canvas.coords(b)

            if not ball.frozen:
                # Apply Drag
                for d in ['x', 'y']:
                    ball.speed[d] -= constants.DRAG
                    if ball.speed[d] < 0:
                        ball.speed[d] = 0

            if p[3] >= h:
                ball.direction.y = -1
                self.canvas.move(b, 0, -(p[3]-h))
            elif p[1] <= 0:
                ball.direction.y = 1
                self.canvas.move(b, 0, -p[1])
            if p[2] >= w:
                ball.direction.x = -1
                self.canvas.move(b, -(p[2]-(w)), 0)
            elif p[0] <= 0:
                ball.direction.x = 1
                self.canvas.move(b, -p[0], 0)

            if not ball.frozen:
                # Apply Drag
                for d in ['x', 'y']:
                    ball.speed[d] -= constants.DRAG
                    if ball.speed[d] < 1:
                        ball.speed[d] = 0

                if not ball.at_rest:
                    if ball.direction.y == 1:
                        if p[3] < h:
                            ball.speed.y += constants.gravity
                    else:
                        ball.speed.y -= constants.gravity
                    
                    if ball.speed.y < 0:
                        ball.speed.y *=-1
                        ball.direction.y*=-1

                    if 7.2 > ball.speed.y > h-p[3]:
                        ball.speed.y = h-p[3]
                
                for d in ['x','y']:
                    if ball.speed[d] <= 7:
                        ball.speed[d] = 0
                    ball.velocity[d] = ball.speed[d] * ball.direction[d]
                

                if ball.moved:
                    delta_x = ball.last_move.x
                    delta_y = ball.last_move.y
                    if delta_x < 0:
                        ball.speed.x = -delta_x
                        ball.direction.x = -1
                    else:
                        ball.speed.x = delta_x
                        ball.direction.x = 1
                    if delta_y < 0:
                        ball.speed.y = -delta_y
                        ball.direction.y = -1
                    else:
                        ball.speed.y = delta_y
                        ball.direction.y = 1
                    ball.moved = False
                else:
                    ball.velocity.x=int(ball.velocity.x)
                    ball.velocity.y=int(ball.velocity.y)
                    delta_x = ball.velocity.x
                    delta_y = ball.velocity.y

                self.canvas.move(ball.representation,delta_x, delta_y)
            else:
                print str(ball.id_number) + " is frozen"
        detect_collisions(self.balls, self.canvas)
        self.canvas.update()
        root.after(constants.INTERVAL,self.animate)

    def click(self,event):
        selected=False
        for ball in self.balls:
            b=ball.representation
            c=self.canvas
            pos = c.coords(b)
            if pos[0] <= event.x <= pos[2] and pos[1] <= event.y <= pos[3]:
                # click in ball
                if selected is False:
                    self.clicked_ball = ball
                    ball.frozen = True
                    selected = True
                print "In ball " + str(ball.id_number)
        if selected is False:
            self.clicked_ball = None

    def release(self, event):
        if self.clicked_ball is not None:
            print "Releasing ball " + str(self.clicked_ball.id_number)
            self.clicked_ball.frozen = False
            self.clicked_ball.at_rest = False
            print self.clicked_ball.at_rest
            self.clicked_ball.prev_pos = None

    def drag(self, event):
        if constants.bounds["x"][0] > event.x or event.x > constants.bounds["x"][1]-20:
            print event.x
            print constants.bounds["x"][0]
            print constants.bounds["x"][1]
            return None 
        if constants.bounds["y"][0] > event.y or event.y> constants.bounds["y"][1]-20:
            print event.y
            print constants.bounds["y"][0]
            print constants.bounds["y"][1]
            return None

        if self.clicked_ball is not None:
            ball = self.clicked_ball
            b=ball.representation
            c=self.canvas
            pos = c.coords(b)
            
            if ball.prev_pos is not None:
                prev_pos = ball.prev_pos
                if prev_pos.x != event.x or prev_pos.y != event.y:
                    delta_x = event.x - prev_pos.x
                    delta_y = event.y - prev_pos.y
                    c.move(b, delta_x, delta_y)
                    ball.last_move = point(delta_x, delta_y) * 2
                    ball.velocity = point(delta_x, delta_y) * 2
                    ball.moved = True
            ball.prev_pos = point(event.x, event.y)


    def createWidgets(self):
        self.frame = Frame(root)
        self.frame.pack(fill=BOTH, expand=1)
        self.canvas=Canvas(self.frame, height=constants.bounds["y"][1]+10, width=constants.bounds["x"][1]+10)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.balls =[]
        for i in range(1,5):
            self.balls.append(ball(self.canvas, cx=i*100, vx=i*10))
        self.canvas.pack(fill=BOTH, expand=1)
        # self.animate()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.animate()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()