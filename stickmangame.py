<<<<<<< HEAD
=======
from math import ceil
>>>>>>> prepare
from time import sleep
from tkinter import Canvas, PhotoImage, Tk, mainloop
from turtle import speed


W, H = 500, 500
SPD = 5

class Game:
    def __init__(self) -> None:
        self.win = Tk()
        self.canvas = Canvas(self.win, width=W, height=H)
        self.canvas.pack()
        self.run = True
        self.sprites = [Stickman(self)]
    
    def tick(self):
        for sprite in self.sprites:
            sprite.update()
<<<<<<< HEAD
        self.canvas.update()
        sleep(0.02)
=======
            self.canvas.update()

>>>>>>> prepare


class Sprite:
    def __init__(self, g: Game, x = W / 2, y = H / 2, speedx = 0, speedy = 0) -> None:
        self.game = g
        self.canvas = g.canvas
        self.x, self.y = x, y
        self.speedx, self.speedy = speedx, speedy
        self.obj = None
    
    def update(self):
        self.move()
<<<<<<< HEAD
=======

    def move(self):
        sx, sy = self.speed
        x, y = self.coords
        self.coords = (x + sx, y - sy)
        self.canvas.coords(self.obj, self.coords[0], self.coords[1])
>>>>>>> prepare

    def move(self):
        self.x += self.speedx
        self.y -= self.speedy
        self.canvas.coords(self.obj, self.x, self.y)
        

class Stickman(Sprite):
<<<<<<< HEAD
    def __init__(self, g: Game, x = W / 2, y = H / 2, speedx=0, speedy=0) -> None:
        super().__init__(g, x, y, speedx, speedy)
        self.costumes = self.get_costumes()
        self.frame = 0
        self.obj = self.canvas.create_image(self.x, self.y, image = self.costumes[-1], anchor='center')
=======
    def __init__(self, game: Game, coords=(W / 2, H / 2), speed=(0, 0)) -> None:
        super().__init__(game, coords, speed)
        self.images = self.my_images(15)
        self.stand_img = PhotoImage(file=f"Stand.png")
        x, y = self.coords
        self.obj = self.canvas.create_image(x, y, image=self.stand_img)
        self.frame = 0
>>>>>>> prepare
        self.canvas.bind_all("<KeyPress>", self.force)
        self.canvas.bind_all("<KeyRelease>", self.unforce)

    def my_images(self, num):
        img = []
        for i in range(num):
            img.append(PhotoImage(file=f"L{i + 1}.png"))
        for i in range(num):
            img.append(PhotoImage(file=f"R{i + 1}.png"))
        return img

    
    def get_costumes(self):
        imgs = []
        for i in range(15):
            imgs.append(PhotoImage(file=f"L{i + 1}.png"))
        for i in range(15):
            imgs.append(PhotoImage(file=f"R{i + 1}.png"))
        imgs.append(PhotoImage(file=f"Stand.png"))
        return imgs
    
    def force(self, event):
        key = event.keysym
        if key == "Left":
<<<<<<< HEAD
            self.speedx = -SPD
        if key == "Right":
            self.speedx = SPD   
        if key == "Up":
            self.speedy = 20 
=======
            self.speed = (-SPD, sy)     
        if key == "Right":
            self.speed = (SPD, sy)
        if key == "Up":
            self.speed = (sx, 20)     
>>>>>>> prepare

    def unforce(self, event):
        key = event.keysym
        if key == "Left":
<<<<<<< HEAD
            self.speedx = 0  
            self.frame = 0          
        if key == "Right":
            self.speedx = 0
            self.frame = 0           

    def switchcostume(self, num):
        self.canvas.itemconfig(self.obj, image = self.costumes[num]) 

    def update(self):
        super().update()  
        self.speedy -= 1   
        self.check()   
        self.animate()
        self.frame += 1
    
    def animate(self):
        if self.speedx == 0:
            self.switchcostume(-1)
            return
        if self.speedx < 0:
            self.switchcostume(self.frame % 15)
        else:
            self.switchcostume(self.frame % 15 + 15)
    
    def check(self):
        while self.y > H - 15:
            self.speedy = 0
            self.y -= 1
        self.canvas.coords(self.obj, self.x, self.y)
=======
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

>>>>>>> prepare

g = Game()
while g.run:
    g.tick()

mainloop()