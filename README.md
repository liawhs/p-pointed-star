# Drawing a regular p-pointed star

![Regular star polygons](https://github.com/liawhs/p-pointed-star/blob/main/readme-imgs/Regular_star_polygons.png)
https://commons.wikimedia.org/wiki/File:Regular_star_polygons.svg


A regular star polygon {p/q}, with p, q positive integers, is a figure formed by connecting with straight lines every qth point out of p regularly spaced points lying on a circumference, where p and q are relatively prime and q > 1. Without loss of generality, take q < p/2 since {p/q} is equal to {p/p-q}. (Online reference: https://mathworld.wolfram.com/StarPolygon.html) 


Each straight line connects a pair of points. We can consider q as the number of sides of the polygon between a pair of points.


A star polygon can also be generalized to the star figure when the greatest common divisor (p,q) != 1. For such a figure, all points are not connected after the first pass. Then start with the first unconnected point and repeat the procedure. Repeat until all points are connected. For (p, q) != 1, the {p/q} symbol can be factored as {p/q} = n {p'/q'}. If q = 1, a regular polygon {p} is obtained. (Online reference: https://mathworld.wolfram.com/StarPolygon.html)


---
## Interior angle of a regular p-pointed star
The following star figure {10, 3} contained in a regular 10-sided polygon will be used to reach a general formula for the interior angle x of a regular p-pointed star.


![{10, 3} star contained in regular 10-sided polygon](https://github.com/liawhs/p-pointed-star/blob/main/readme-imgs/%7B10%2C3%7D_star_contained_n_regular_10-sided_polygon.png)


The interior angle <img src="https://render.githubusercontent.com/render/math?math=\alpha"> of a regular p-sided polygon is

<img src="https://render.githubusercontent.com/render/math?math=\alpha = {180\times(p-2)}/{p}">  ------  (1).


Consider the upper left segment of the figure above, the sum of the interior angles of the segment generally can be written as

<img src="https://render.githubusercontent.com/render/math?math=(q-1)\alpha \%2B 2\beta=180(q-1)">  ------  (2).


Substituting (1) into (2) and solving for <img src="https://render.githubusercontent.com/render/math?math=\beta">, we get

<img src="https://render.githubusercontent.com/render/math?math=\beta = \frac{180}{p}(q-1)">  ------  (3).


At a vertex, the interior angle <img src="https://render.githubusercontent.com/render/math?math=\alpha"> of a regular p-sided polygon is equal to the interior angle x of a regular p-pointed star plus 2<img src="https://render.githubusercontent.com/render/math?math=\beta">, as below:

<img src="https://render.githubusercontent.com/render/math?math=\alpha = x \%2B 2\beta">  ------  (4).


Substituting (1) and (3) into (4) and solving for x, we get the interior angle x of a regular p-pointed star

<img src="https://render.githubusercontent.com/render/math?math=\large x = \frac{180}{p}[p - 2q]">  ------  (5).



### Sample calculation for {10, 3}

<img src="https://render.githubusercontent.com/render/math?math=\alpha  = {180\times(p-2)}/{p} = {180\times(10-2)}/{10} = 144">


<img src="https://render.githubusercontent.com/render/math?math=\beta = 180(q -1)/p = 180(2)/10 = 36">


<img src="https://render.githubusercontent.com/render/math?math=x = \frac{180}{p}[p-2q] = \frac{180}{10}[10-2(3)] = 72">


All angles are in degrees.



---
## Implementation

The turtle module will be used to draw p-pointed stars. First, we need to import the turtle module and some functions or methods from other modules.

```
from turtle import Turtle, Screen 
from math import gcd, sin, radians
from time import sleep 
``` 
  
       
I use class to create a Star object. The \__init__ method takes p and the radius of the star object as arguments

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


The angles attribute is a dictionary of all possible values of q and the corresponding interior angles of the star object. These key-value pairs are determined by the q_angles method.


Prior to the draw method, which is used to draw a regular p-pointed star, I define the following simple methods.

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


The draw method takes four arguments: the turtle object, the q, the center of the star, and the pointing angle of the star. Setting the pointing angle to 90 degrees means one point of the star is on the y axis.

    def draw(self, t, q, center = (0,0), pointing_angle = 90):

The draw method checks the great common divisor of p and q. 
```
        n = gcd(self.p, q)
```

If it is equal to one, then we can draw the star figure in one pass.
```
        # star in one pass
        length = self.chord(self.radius, self.gamma(q, self.p))
        if n == 1:
            t.begin_fill()
            for _ in range(self.p):
                t.forward(length)
                t.right(180-self.angles[q])
            t.end_fill() 
```

Otherwise, we need to draw the star figure in n passes.
```
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
```

After the first {p'/q'} is drawn, before starting to draw the next {p'/q'}, we need to move the turtle to a correct location and set the turtle in a correct direction. 

I turn the turtle leftward an angle of beta, move forward along a side of the polygon to reach the next adjacent point of the star, and turn the turtle rightward an angle of (180 – beta – the interior angle of the star).

                    t.left(angle_beta)
                    t.forward(side_length)
                    t.right(180-angle_beta-self.angles[q])


Alternatively, you may let the turtle go to the center of the star, turn the turtle to a correct angle, move along the radius to reach the next adjacent point of the star, and turn the turtle to a correct direction.

---
## Sample output

 - 5-pointed stars pointing at various angles (0, 10, 20, ... 90 degrees)
 
 
 ![5-pointed star pointing at various angles](https://github.com/liawhs/p-pointed-star/blob/main/readme-imgs/5-pointed%20star%20pointing%20at%20various%20angles.png)


 - 5-, 6-, 7-, 8-, 9-, and 10-pointed stars


 ![5-, 6-, 7-, 8-, 9-, and 10-pointed stars](https://github.com/liawhs/p-pointed-star/blob/main/readme-imgs/5%20to%2010-pointed%20stars.png)


 - 11-, 12-, 13-, 14-, 15-,and 16-pointed stars


 ![11-, 12-, 13-, 14-, 15-,and 16-pointed stars](https://github.com/liawhs/p-pointed-star/blob/main/readme-imgs/11%20to%2016-pointed%20stars.png)


 - 17-, 18-, 19-, and 20-pointed stars


 ![17-, 18-, 19-, and 20-pointed stars](https://github.com/liawhs/p-pointed-star/blob/main/readme-imgs/17%20to%2020-pointed%20stars.png)
