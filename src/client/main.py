import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("resources/wizard.pyxel")
       
        self.x = 0
        self.y = 0
        
        # Character animation
        self.moved = False
        self.char_height = 16
        self.char_width = 8
        self.char_animation_length = 7 #indices, starts at 0
        self.char_current_anim = 0
        
        
        pyxel.run(self.update, self.draw)
        

        

    def update(self):
        
        self.update_location()
        if self.moved:
            self.char_move_cycle()

    def draw(self):
        pyxel.cls(0)
        self.draw_map()
        pyxel.blt(self.x, self.y, 0, self.char_current_anim, 0, 8, 16, 0)
        
        
    def draw_map(self):
        pyxel.bltm(0, 0, 0, 0, 0,pyxel.height, 30, 30)
        
        
    def update_location(self):
        self.moved = False
        if pyxel.btn(pyxel.KEY_UP):
            self.y = (self.y - 1) % pyxel.height
            self.moved = True
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = (self.y + 1) % pyxel.height
            self.moved = True
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = (self.x - 1) % pyxel.width
            self.moved = True
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = (self.x + 1) % pyxel.width
            self.moved = True
    
    def char_move_cycle(self):
        self.char_current_anim = (self.char_width + self.char_current_anim) % (self.char_animation_length * self.char_width)

App()