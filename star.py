from turtle import Turtle, Screen 
from math import gcd, sin, radians
from time import sleep 

class Star:
    def __init__(self, p, radius):
        self.p = p
        self.radius = radius
        self.angles = self.q_angles(p)

    @staticmethod    
    def q_angles(p):
        angs = dict()
        for q in range(2, p//2 + p%2):
            ang = (180/p) * (p-2*q)
            angs[q] = ang
        return angs
    
    @staticmethod
    def beta(q, p):
        return (q-1)*180/p

    @staticmethod
    def gamma(q, p):
        return q*360/p

    @staticmethod
    def chord(radius, gamma):
        return 2 * radius * sin(radians(gamma/2))

    @staticmethod
    def side(radius, p):
        return 2 * radius * sin(radians(180/p))

    def draw(self, t, q, center = (0,0), pointing_angle = 90):
        if self.p < 5: return
        t.penup()
        t.goto(center) # center of the star
        # direction of a point, measured from the center 
        t.setheading(pointing_angle)
        t.forward(self.radius)
        t.right(180-self.angles[q]/2)
        t.pendown()
        n = gcd(self.p, q)
        
        # star in one pass
        length = self.chord(self.radius, self.gamma(q, self.p))
        if n == 1:
            t.begin_fill()
            for _ in range(self.p):
                t.forward(length)
                t.right(180-self.angles[q])
            t.end_fill() 
        else:
            # star in n passess since {p/q} = n {p'/q'}
            # 1st {p'/q'}
            t.begin_fill()
            for _ in range(int(self.p/n)):
                t.forward(length)
                t.right(180-self.angles[q])
            t.end_fill() 

           # remaining n-1 of {p'/q'}
            angle_beta = self.beta(q,self.p)
            side_length = self.side(self.radius, self.p)
            for _ in range(1, n):
                    # move to the correct position before drawing {p'/q'}
                    t.penup()
                    t.left(angle_beta)
                    t.forward(side_length)
                    t.right(180-angle_beta-self.angles[q])
                    t.pendown()
                    t.begin_fill()
                    for _ in range(int(self.p/n)):
                        t.forward(length)
                        t.right(180-self.angles[q])
                    t.end_fill() 
        
      
    def draw_all(self,t, center=(0,0), pointing_angle=90):
           for q in self.angles.keys():
               self.draw(t, q, center, pointing_angle)
               sleep(1)
               t.clear()


if __name__ == '__main__':
    t = Turtle()
    Screen().bgcolor('black')
    t.color('yellow')
    t.speed('fast')
    t.hideturtle()

    radius = 100
    for p in range(5, 20):
        star = Star(p, radius)
        # draw all possible stars
        star.draw_all(t)
