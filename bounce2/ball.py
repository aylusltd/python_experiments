import constants
from point import point, boundary
balls=0

class ball(constants.correction):
    frozen=False
    selected=False
    prev_pos=None
    moved=False
    mass=1.0
    at_rest=False
    last_move = point(0,0)

    def __init__(self, canvas=None, cx=20, cy=20, rx=20, ry=20, vx=0, vy=0, fill="red"):
        global balls
        balls+=1
        self.id_number = balls
        self.c=point(cx,cy)
        self.r=point(rx,ry)
        self.direction=point(1,1)
        self.velocity=point(vx,vy)
        self.speed = point(0,0)
        self.v_to_s()           
        
        # assert(self.velocity == self.speed * self.direction)
        if canvas is not None:
            self.representation = canvas.create_oval(cx-rx,cy-ry,cx+rx,cy+ry, tags='ball', fill=fill)
            self.canvas = canvas
            canvas.pack()
        else:
            self.representation = 0

    def v_to_s(self):
        for d in self.velocity.__dict__.keys():
            if self.velocity[d] >= 0:
                self.speed[d] = self.velocity[d]
                self.direction[d] = 1
            else:
                self.speed[d] = -self.velocity[d]
                self.direction[d] = -1
        
    def s_to_v(self):
        self.velocity = self.speed * self.direction

    def get_boundaries(self):
        if self.canvas is not None:
            return boundary(self.canvas.coords(self.representation))
        else:
            return None