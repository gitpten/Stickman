from email.mime import image
<<<<<<< HEAD
from time import sleep
from tkinter import Canvas, PhotoImage, Tk, mainloop


W, H = 500, 500
=======
from math import ceil
from telnetlib import GA
from time import sleep
from tkinter import Canvas, PhotoImage, Tk, mainloop

W = 500
H = 500
>>>>>>> prepare
SPD = 5

class Game:
    def __init__(self) -> None:
        self.win = Tk()
        self.canvas = Canvas(self.win, width=W, height=H)
        self.canvas.pack()
        self.run = True
<<<<<<< HEAD
        self.sprites = [Stickman(self)]
    
    def tick(self):
        for sprite in self.sprites:
            sprite.move()
        self.canvas.update()
        sleep(0.02)


class Sprite:
    def __init__(self, g: Game, x = W / 2, y = H / 2, speedx = 0, speedy = 0) -> None:
        self.game = g
        self.canvas = g.canvas
        self.x, self.y = x, y
        self.speedx, self.speedy = speedx, speedy
        self.obj = None
    
    def move(self):
        self.canvas.move(self.obj, self.speedx, self.speedy)

class Stickman(Sprite):
    def __init__(self, g: Game, x=W / 2, y=H / 2, speedx=0, speedy=0) -> None:
        super().__init__(g, x, y, speedx, speedy)
        self.costumes = [
            PhotoImage(file="figure-L1.png"),
            PhotoImage(file="figure-R1.png"),
        ]
        self.obj = self.canvas.create_image(self.x, self.y, image = self.costumes[1], anchor='center')
=======
        self.sprites = [Stickman(self, (20, H - 20))]

    def tick(self):
        for sprite in self.sprites:
            sprite.move()
            self.canvas.update()



class Sprite:
    def __init__(self, game: Game, coords = (W / 2, H / 2), speed = (0, 0)) -> None:
        self.game = game
        self.canvas = self.game.canvas
        self.coords = coords
        self.speed = speed
        self.obj = None
    
    def move(self):
        sx, sy = self.speed
        self.canvas.move(self.obj, sx, sy)


class Stickman(Sprite):
    def __init__(self, game: Game, coords=(W / 2, H / 2), speed=(0, 0)) -> None:
        super().__init__(game, coords, speed)
        self.images = [
            PhotoImage(file='figure-L1.png'),
            PhotoImage(file='figure-R1.png')
        ]
        x, y = self.coords
        self.obj = self.canvas.create_image(x, y, image=self.images[0])
>>>>>>> prepare
        self.canvas.bind_all("<KeyPress>", self.force)
        self.canvas.bind_all("<KeyRelease>", self.unforce)
    
    def force(self, event):
        key = event.keysym
<<<<<<< HEAD
        if key == "Left":
            self.speedx = -SPD
            self.switchcostume(0)
        if key == "Right":
            self.speedx = SPD     
            self.switchcostume(1)       

    def unforce(self, event):
        key = event.keysym
        if key == "Left":
            self.speedx = 0            
        if key == "Right":
            self.speedx = 0                 

    def switchcostume(self, num):
        self.canvas.itemconfig(self.obj, image = self.costumes[num])       
=======
        sx, sy = self.speed
        if key == "Left":
            self.speed = (-SPD, sy)
            self.canvas.itemconfig(self.obj, image = self.images[0])
        if key == "Right":
            self.speed = (SPD, sy)
            self.canvas.itemconfig(self.obj, image = self.images[1])

    def unforce(self, event):
        key = event.keysym
        sx, sy = self.speed
        if key == "Left":
            self.speed = (0, sy)
        if key == "Right":
            self.speed = (0, sy)
>>>>>>> prepare

g = Game()
while g.run:
    g.tick()
<<<<<<< HEAD
=======
    sleep(0.02)
>>>>>>> prepare

mainloop()