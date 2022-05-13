from time import sleep
from tkinter import Canvas, PhotoImage, Tk, mainloop


W, H = 500, 500
SPD = 5

class Game:
    def __init__(self) -> None:
        self.win = Tk()
        self.canvas = Canvas(self.win, width=W, height=H)
        self.canvas.pack()
        self.level = 1
        self.run = True
        self.sprites = self.get_plathforms() + [Stickman(self)]
    
    def newlevel(self):
        if self.level == 2:
            self.gameover()
            return
        self.canvas.delete('all')
        self.level += 1
        self.stickman = Stickman(self)
        self.sprites = self.get_platforms() + [self.stickman]
    
    
    def tick(self):
        for sprite in self.sprites:
            sprite.update()
        self.canvas.update()
        sleep(0.02)
    
    def get_plathforms(self):
        pp = []
        if self.level == 1:
            pp.append(Plathform(self, 2, 8))
            pp.append(Plathform(self, 8, 7))
            pp.append(Plathform(self, 4, 5, width=2))
            pp.append(Plathform(self, 7, 4, width=2))
            pp.append(Plathform(self, 2, 2, width=3))
        elif self.level == 2:
            pp.append(Plathform(self, 8, 4, width=2))
            pp.append(PlathformKiller(self, 7, 8))
            pp.append(Plathform(self, 3, 2, width=3))
            pp.append(Plathform(self, 4, 7, width=2))
            pp.append(Plathform(self, 1, 2))                
        pp.insert(0, Door(pp[-1]))
        return pp
    
    def newlevel(self, level = -1):
        self.level = self.level + 1 if level == -1 else level
        if self.level == 3:
            self.gameover()
            return
        
        self.canvas.delete('all')
        self.sprites = self.get_plathforms() + [Stickman(self)]
    
    def gameover(self):
        self.run = False
        self.canvas.create_text(W / 2, H / 2, font = ('Arial', 30), text = 'Game over', \
            anchor='center')



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
    
class PlathformKiller(Plathform):
    def __init__(self, g: Game, x, y, speedx=0, speedy=0, width=1) -> None:
        super().__init__(g, x, y, speedx, speedy, width)
        self.img = PhotoImage(file=f"P{width} green.png")
        self.canvas.itemconfig(self.obj, image = self.img)
        



class Door(Sprite):
    def __init__(self, p: Plathform) -> None:
        super().__init__(p.game, p.x, p.y, 0, 0)
        self.img_opened = PhotoImage(file=f"door2.png")
        self.img_closed = PhotoImage(file=f"door1.png")
        self.obj = self.canvas.create_image(self.x, self.y, image = self.img_opened, anchor='s')
        self.width = 30




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
        imgs.append(PhotoImage(file=f"dead.png"))
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
        sprite = self.collide()
        if type(sprite) is Door:
            self.game.newlevel()
            return
        if type(sprite) is PlathformKiller:
            self.kill()
            return
        while self.collide() or self.y > H - 15:
            self.speedy = 0
            self.flying = False
            self.y -= 1
        self.canvas.coords(self.obj, self.x, self.y)

    
    def collide(self):
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            mytop = self.y - 15
            mybottom = self.y + 15
            left = sprite.x - sprite.width / 2
            right = sprite.x + sprite.width / 2
            if self.speedy <= 0 and mytop < sprite.y < mybottom and left < self.x < right:
                return sprite
        return False
    
    def kill(self):
        self.switchcostume(-6)
        self.canvas.update()
        sleep(1)
        self.game.newlevel(1)



g = Game()
while g.run:
    g.tick()

mainloop()