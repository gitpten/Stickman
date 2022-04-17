from tkinter import *
import time

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('Stickman')
        self.tk.resizable(0, 0)
        self.tk.wm_attributes('-topmost', 1)
        self.canvas_width = 500
        self.canvas_height = 500
        self.canvas = Canvas(self.tk, width = self.canvas_width, height = self.canvas_height, highlightthickness = 0)
        self.canvas.pack()
        self.tk.update()
        self.bg = PhotoImage(file = "background.png")
        w = self.bg.width()
        h = self.bg.height()
        for x in range(self.canvas_width // w):
            for y in range(self.canvas_height // h):
                self.canvas.create_image(x * w, y * h, image = self.bg, anchor = 'nw')
        
        self.sprites = []
        self.running = True
    
    def mainloop(self):
        while True:
            if self.running:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def within_x(c1, c2):
    return (c1.x1 > c2.x1 and c1.x2 < c2.x2) or \
        (c1.x2 > c2.x1 and c1.x1 < c2.x2) or \
        (c2.x1 > c1.x1 and c2.x2 < c1.x2) or \
        (c2.x2 > c1.x1 and c2.x1 < c1.x2)

def within_y(c1, c2):
    return (c1.y1 > c2.y1 and c1.y2 < c2.y2) or \
        (c1.y2 > c2.y1 and c1.y1 < c2.y2) or \
        (c2.y1 > c1.y1 and c2.y2 < c1.y2) or \
        (c2.y2 > c1.y1 and c2.y1 < c1.y2)
        
def collided_left(c1, c2):
    return within_y(c1, c2) and c2.x1 <= c1.x1 <= c2.x2

def collided_right(c1, c2):
    return within_y(c1, c2) and c2.x1 <= c1.x2 <= c2.x2

def collided_top(c1, c2):
    return within_x(c1, c2) and c2.y1 <= c1.y1 <= c2.y2

def collided_buttom(y, c1, c2):
    _y = c1.y2 + y
    return within_x(c1, c2) and c2.y1 <= _y <= c2.y2

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coords = None
    def move(self):
        pass
    def get_coords(self):
        return self.coords

class Platform(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        super().__init__(game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image = self.photo_image, anchor = 'nw')
        self.coords = Coords(x, y, x + width, y + height)

class StickManSprite(Sprite):
    def __init__(self, game):
        super().__init__(game)
        self.images_left = [
            PhotoImage(file="figure-L1.png"),
            PhotoImage(file="figure-L2.png"),
            PhotoImage(file="figure-L3.png")
        ]
        self.images_right = [
            PhotoImage(file="figure-R1.png"),
            PhotoImage(file="figure-R2.png"),
            PhotoImage(file="figure-R3.png")
        ]
        self.image = game.canvas.create_image(200, 470, image = self.images_left[0], anchor = 'nw')
        self.dx = -2
        self.dy = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coords = Coords()

        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)
    
    def turn_left(self, event):
        if self.dy == 0:
            self.dx = -2
    
    def turn_right(self, event):
        if self.dy == 0:
            self.dx = 2
    
    def jump(self, event):
        if self.dy == 0:
            self.dy = -4
            self.jump_count = 0
    
    def animate(self):
        if self.dx != 0 or self.dy != 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.dx < 0:
            if self.dy != 0:
                self.game.canvas.itemconfig(self.image, image = self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image = self.images_left[self.current_image])
        
        if self.dx > 0:
            if self.dy != 0:
                self.game.canvas.itemconfig(self.image, image = self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image = self.images_right[self.current_image])
    
    def get_coords(self):
        coords = self.game.canvas.coords(self.image)
        self.coords.x1 = coords[0]
        self.coords.y1 = coords[1]
        self.coords.x2 = coords[0] + 27
        self.coords.y2 = coords[1] + 30
        return self.coords
    
    def move(self):
        self.animate()
        if self.dy < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.dy = 4
        
        if self.dy > 0:
            self.jump_count -=1

        coords = self.get_coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        if self.dy > 0 and coords.y2 >= self.game.canvas_height:
            self.dy = 0
            bottom = False
        elif self.dy < 0 and coords.y2 <= 0:
            self.dy = 0
            top = False
        
        if self.dx > 0 and coords.x2 >= self.game.canvas_width:
            self.dx = 0
            right = False
        elif self.dx < 0 and coords.x2 <= 0:
            self.dx = 0
            left = False        

        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_coords = sprite.get_coords()
            if top and self.dy < 0 and collided_top(coords, sprite_coords):
                self.dy *= 1
                top = False
            if bottom and self.dy > 0 and collided_buttom(self.dy, coords, sprite_coords):
                self.dy = sprite_coords.y1 - coords.y2
                if self.dy < 0:
                    self.dy = 0
                bottom = False
                top = False
            if bottom and falling and self.dy == 0 and coords.y2 < self.game.canvas_height \
                 and collided_buttom(1, coords, sprite_coords):
                 falling = False
            if left and self.dx < 0 and collided_left(coords, sprite_coords):
                self.dx = 0
                left = False
                if sprite.endgame:
                    self.game.running = False
            if right and self.dx > 0 and collided_right(coords, sprite_coords):
                self.dx = 0
                right = False
                if sprite.endgame:
                    self.game.running = False
        if falling and bottom and self.dy == 0 and coords.y2 < self.game.canvas_height:
            self.dy = 4
        self.game.canvas.move(self.image, self.dx, self.dy)
        
class DoorSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        super().__init__(game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image = photo_image, anchor = 'nw')
        self.coords = Coords(x, y, x + (width / 2), y + height)
        self.endgame = True

g = Game()
g.sprites.append(Platform(g, PhotoImage(file = "platform-1.png"), 0, 480, 100, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-1.png"), 150, 440, 100, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-1.png"), 300, 160, 100, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-1.png"), 300, 400, 100, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-2.png"), 175, 350, 66, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-2.png"), 50, 300, 66, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-2.png"), 170, 120, 66, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-2.png"), 45, 60, 66, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-3.png"), 170, 250, 32, 10))
g.sprites.append(Platform(g, PhotoImage(file = "platform-3.png"), 230, 200, 32, 10))
door = DoorSprite(g, PhotoImage(file = "door1.png"), 45, 30, 40, 35)
g.sprites.append(door)
stickman = StickManSprite(g)
g.sprites.append(stickman)
g.mainloop()
