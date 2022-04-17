from email.mime import image
from math import ceil
from telnetlib import GA
from time import sleep
from tkinter import Canvas, PhotoImage, Tk, mainloop

W = 500
H = 500
SPD = 5

class Game:
    def __init__(self) -> None:
        self.win = Tk()
        self.canvas = Canvas(self.win, width=W, height=H)
        self.canvas.pack()
        self.run = True
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
        self.canvas.bind_all("<KeyPress>", self.force)
        self.canvas.bind_all("<KeyRelease>", self.unforce)
    
    def force(self, event):
        key = event.keysym
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

g = Game()
while g.run:
    g.tick()
    sleep(0.02)

mainloop()