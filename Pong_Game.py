from ball import *
import random as rand
from math import *
from Mapping_for_Tkinter import Mapping_for_Tkinter


class racket:
    def __init__(self, mapping, canvas, x, y):  ### racket constructor
        self.mapping = mapping
        self.canvas = canvas
        self.x = x
        self.y = y
        self.myracket = canvas.create_rectangle(mapping.get_i(self.x - 30), mapping.get_j(self.y + 5),
                                                mapping.get_i(self.x + 30), mapping.get_j(self.y - 5),
                                                fill="black")  ### creates racket rectangle

    def shift_left(self, canvas):  ### method for shifting racket to the left
        xmin = (-canvas.winfo_width() / 2) + 2  ### defines xmin
        if self.x == xmin + 30:  ### accounts for case in which racket cannot shift due to bounds
            return None
        else:
            canvas.move(self.myracket, -30, 0)  ### shifts racket
            self.x -= 30

    def shift_right(self, canvas):  ### method for shifting racket to the right
        xmax = (canvas.winfo_width() / 2) - 2  ### defines xmas
        if self.x == xmax - 30:  ### accounts for case in which racket cannot shift due to bounds
            return None
        else:
            canvas.move(self.myracket, 30, 0)  ### shifts racket
            self.x += 30

    def activate(self, canvas, raccy):  ### creates method to change active racket to red
        self.canvas.itemconfig(raccy.myracket, fill="red")

    def deactivate(self, canvas, raccy):  ### creates method to change inactive racket to black
        self.canvas.itemconfig(raccy.myracket, fill="black")


def main():
    game1_check = 1  ### variables for ball file to account for the ball hitting racket instead of bound
    game2_check = 1
    mapping = Mapping_for_Tkinter(-300, 300, -300, 300, 600)  ### imports mappign specifications
    root = Tk()
    w = 600
    h = 600
    canvas = Canvas(root, width=mapping.get_width(), height=mapping.get_height(),
                    bg="white")  ### creates and packs canvas
    canvas.pack()
    raccy1 = racket(mapping, canvas, 0, mapping.get_ymin() + 5)  ### makes "raccy" racket objects
    raccy2 = racket(mapping, canvas, 0, mapping.get_ymax() - 5)
    v = 300  ### sets velocity and angle
    theta = 45
    ball1 = ball(mapping, canvas, 0, mapping.get_ymin() + 14, v, theta)  ### creates ball object

    ############################################
    ####### start simulation
    ############################################
    t = 0  # real time between event
    t_total = 0  # real total time
    count = 0  # rebound_total=0

    raccy1.deactivate(canvas, raccy1)  ### sets top racket to be active by default
    raccy2.activate(canvas, raccy2)
    canvas.bind("<Button-1>", lambda e: raccy2.shift_left(canvas))  ### makes left click shift racket left
    canvas.bind("<Button-3>", lambda e: raccy2.shift_right(canvas))  ### makes right click shift racket right

    while True:
        t = t + 0.01  # real time between events- in second
        t_total = t_total + 0.01  # real total time- in second
        side = ball1.update_xy(t, game1_check, game2_check)  # Update ball position and return collision event
        root.update()  # update the graphic (redraw)
        if side != 0:  ### when ball hits a bound
            if ball1.y == mapping.get_ymax() - 14:  ### makes ball bounce off racket at random angle
                ball1.angle = rand.uniform(-170, -10)
            if ball1.y == mapping.get_ymin() + 14:  ### makes ball bounce off racket at random angle
                ball1.angle = rand.uniform(10, 170)
            if ((
                    ball1.x > raccy2.x - 30 and ball1.x < raccy2.x + 30) and ball1.y == mapping.get_ymax() - 14):  ### activates bottom racket
                canvas.bind("<Button-1>", lambda e: raccy1.shift_left(canvas))  ### makes left click shift racket left
                canvas.bind("<Button-3>",
                            lambda e: raccy1.shift_right(canvas))  ### makes right click shift racket right
                raccy1.activate(canvas, raccy1)
                raccy2.deactivate(canvas, raccy2)
            elif ((
                          ball1.x > raccy1.x - 30 and ball1.x < raccy1.x + 30) and ball1.y == mapping.get_ymin() + 14):  ### activates top racket
                raccy1.deactivate(canvas, raccy1)
                raccy2.activate(canvas, raccy2)
                canvas.bind("<Button-1>", lambda e: raccy2.shift_left(canvas))  ### makes left click shift racket left
                canvas.bind("<Button-3>",
                            lambda e: raccy2.shift_right(canvas))  ### makes right click shift racket right

            count = count + 1  # increment the number of rebounds
            t = 0  # reinitialize the local time
        time.sleep(0.01)  # wait 0.01 second (simulation time)
        if ((
                ball1.x < raccy1.x - 30 or ball1.x > raccy1.x + 30) and ball1.y == mapping.get_ymin() + 14):  ### if racket 1 misses the ball
            print("Game Over for Racket 1!")
            break  # stop the simulation
        if ((
                ball1.x < raccy2.x - 30 or ball1.x > raccy2.x + 30) and ball1.y == mapping.get_ymax() - 14):  ### if racket 2 misses the ball
            print("Game Over for Racket 2!")
            break


main()
