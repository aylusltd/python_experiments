import constants

class boundary(constants.correction):
    def __init__(self, l):
        self.left=l[0]
        self.right=l[2]
        self.top=l[1]
        self.bottom=l[3]
        self.cx = (self.left+self.right)/2
        self.cy = (self.top+self.bottom)/2
        self.rx = self.right - self.cx
        self.ry = self.bottom - self.cy

    def hits(self, other):
        return ( self.left <= other.right and
             self.right >= other.left and
             self.top <= other.bottom and
             self.bottom >= other.top
            )

    def circles_hit(self, other):
        side1 = self.cx - other.cx
        side2 = self.cy - other.cy
        side3 = self.rx + other.rx
        return side1**2 + side2**2 <= side3**2

    def is_left_of(self,other):
        return self.left<=other.left

class point(constants.correction):
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __add__(self, other):
        a = point(self.x, self.y)
        a.x += other.x
        a.y += other.y

        return a

    def __sub__(self, other):
        a = point(self.x, self.y)
        a.x -= other.x
        a.y -= other.y

        return a

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y

        return self

    def __str__(self):
        s = "{x:" + str(self.x) +", y:" + str(self.y)+"}"
        return s

    def __div__(self, other):
        a = point(self.x, self.y)
        a.x = a.x/other
        a.y = a.y/other

        return a
        
    def __mul__(self, other):
        a = point(self.x, self.y)
        if isinstance(other, point):
            a.x*=other.x
            a.y*=other.y
        else:
            a.x *= other
            a.y *= other

        return a

    def __eq__(self,other):
        retVal = False
        if isinstance(other, point):
            retVal = other.x == self.x and other.y == self.y
        return retVal

    def total(self):
        return self.x+self.y