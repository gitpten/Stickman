from time import sleep
from tkinter import Canvas, PhotoImage, Tk, mainloop


W, H = 500, 500
SPD = 5

class Game:
    def __init__(self) -> None:
        self.win = Tk()
        self.canvas = Canvas(self.win, width=W, height=H)
        self.canvas.pack()
        self.run = True
        self.sprites = self.get_plathforms() + [Stickman(self)]
    
    def tick(self):
        for sprite in self.sprites:
            sprite.update()
        self.canvas.update()
        sleep(0.02)
    
    def get_plathforms(self):
        pp = []
        pp.append(Plathform(self, 2, 8))
        pp.append(Plathform(self, 8, 7))
        pp.append(Plathform(self, 4, 5, width=2))
        pp.append(Plathform(self, 7, 4, width=2))
        pp.append(Plathform(self, 2, 2, width=3))
        return pp

class Sprite:
    def __init__(self, g: Game, x = W / 2, y = H / 2, speedx = 0, speedy = 0) -> None:
        self.game = g
        self.canvas = g.canvas
        self.x, self.y = x, y
        self.speedx, self.speedy = speedx, speedy
        self.obj = None
    
    def update(self):
        self.move()

    def move(self):
        self.x += self.speedx
        self.y -= self.speedy
        self.canvas.coords(self.obj, self.x, self.y)

class Plathform(Sprite):
    def __init__(self, g: Game, x, y, speedx=0, speedy=0, width=1) -> None:
        super().__init__(g, x * W / 10, y * H / 10, speedx, speedy)   
        self.img = PhotoImage(file=f"P{width}.png")
        self.obj = self.canvas.create_image(self.x, self.y, image = self.img, anchor='center')
        self.width = width * 30

class Stickman(Sprite):
    def __init__(self, g: Game, x = W / 2, y = H / 2, speedx=0, speedy=0) -> None:
        super().__init__(g, x, y, speedx, speedy)
        self.costumes = self.get_costumes()
        self.frame = 0
        self.flying = True
        self.obj = self.canvas.create_image(self.x, self.y, image = self.costumes[-1], anchor='center')
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
        imgs.append(PhotoImage(file=f"LJ1.png"))
        imgs.append(PhotoImage(file=f"LJ2.png"))
        imgs.append(PhotoImage(file=f"RJ1.png"))
        imgs.append(PhotoImage(file=f"RJ2.png"))        
        imgs.append(PhotoImage(file=f"Stand.png"))
        return imgs
    
    def force(self, event):
        key = event.keysym
        if key == "Left":
            self.speedx = -SPD
        if key == "Right":
            self.speedx = SPD   
        if key == "Up":
            if not self.flying:
                self.flying = True
                self.speedy = 20 

    def unforce(self, event):
        key = event.keysym
        if key == "Left":
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
        
        right = self.speedx > 0
        down = self.speedy < 0
        if self.flying:
            self.switchcostume(-5 + 2 * right + down)
        else:
            self.switchcostume(self.frame % 15 + 15 * right)
    
    def check(self):
        while self.collide() or self.y > H - 15:
            self.speedy = 0
            self.flying = False
            self.y -= 1
        self.canvas.coords(self.obj, self.x, self.y)
    
    def collide(self):
        for plathform in self.game.sprites:
            if plathform == self:
                continue
            mytop = self.y - 15
            mybottom = self.y + 15
            left = plathform.x - plathform.width / 2
            right = plathform.x + plathform.width / 2
            if mytop < plathform.y < mybottom and left < self.x < right:
                return True
        return False

g = Game()
while g.run:
    g.tick()

mainloop()