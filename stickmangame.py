from math import ceil
from time import sleep
from tkinter import Canvas, PhotoImage, Tk, mainloop
from turtle import speed

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
            sprite.update()
            self.canvas.update()



class Sprite:
    def __init__(self, game: Game, coords = (W / 2, H / 2), speed = (0, 0)) -> None:
        self.game = game
        self.canvas = self.game.canvas
        self.coords = coords
        self.speed = speed
        self.obj = None
    
    def update(self):
        self.move()

    def move(self):
        sx, sy = self.speed
        x, y = self.coords
        self.coords = (x + sx, y - sy)
        self.canvas.coords(self.obj, self.coords[0], self.coords[1])


class Stickman(Sprite):
    def __init__(self, game: Game, coords=(W / 2, H / 2), speed=(0, 0)) -> None:
        super().__init__(game, coords, speed)
        self.images = self.my_images(15)
        self.stand_img = PhotoImage(file=f"Stand.png")
        x, y = self.coords
        self.obj = self.canvas.create_image(x, y, image=self.stand_img)
        self.frame = 0
        self.canvas.bind_all("<KeyPress>", self.force)
        self.canvas.bind_all("<KeyRelease>", self.unforce)

    def my_images(self, num):
        img = []
        for i in range(num):
            img.append(PhotoImage(file=f"L{i + 1}.png"))
        for i in range(num):
            img.append(PhotoImage(file=f"R{i + 1}.png"))
        return img

    
    def force(self, event):
        key = event.keysym
        sx, sy = self.speed
        if key == "Left":
            self.speed = (-SPD, sy)     
        if key == "Right":
            self.speed = (SPD, sy)
        if key == "Up":
            self.speed = (sx, 20)     

    def unforce(self, event):
        key = event.keysym
        sx, sy = self.speed
        if key == "Left":
            self.speed = (0, sy)
            self.frame = 0
        if key == "Right":
            self.speed = (0, sy)
            self.frame = 0
    
    def update(self):
        super().update()
        sx, sy = self.speed
        self.speed = (sx, sy - 1)
        self.check()    
        self.frame += 1
        self.animate()

    def check(self):
        while(self.coords[1] > H - 15):
            self.speed = (self.speed[0], 0)
            self.coords = (self.coords[0], self.coords[1] - 1)
        self.canvas.coords(self.obj, self.coords) 

    def animate(self):
        if self.speed[0] == 0:
            self.canvas.itemconfig(self.obj, image=self.stand_img)
            return
        num = self.frame % 15 if self.speed[0] < 0 else self.frame % 15 + 15
        self.canvas.itemconfig(self.obj, image=self.images[num])


g = Game()
while g.run:
    g.tick()
    sleep(0.02)

mainloop()