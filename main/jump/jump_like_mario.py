import pyxel
#import os
#basedir = ""
base_assets = "./assets/jump.pyxres"

class App:
    def __init__(self):
        self.width = 240
        self.height = 180
        pyxel.init(self.width, self.height, fps=30, title="jump")
        global obj_box
        obj_box = []

        pyxel.load(base_assets)

        self.c_x = 0
        self.c_y = 0

        self.a_box = Player(5,5,8,8,7)
        self.floor = self.create_wall(5,140,150,20,3)
        self.box_1 = self.create_wall(50,130,20,10,3)
        self.box_2 = self.create_wall(130,90,20,10,3)
        self.box_3 = self.create_wall(10,90,20,10,3)
        self.box_4 = self.create_wall(100,110,40,10,3,geotype="wall_nc")

        self.box_5_1 = self.create_wall(10,60,10,10,3)
        self.box_5_2 = self.create_wall(30,60,10,10,3)
        self.box_5_3 = self.create_wall(50,60,10,10,3)
        self.box_5_4 = self.create_wall(70,60,10,10,3)
        self.box_5_4 = self.create_wall(90,60,10,10,3)

        pyxel.run(self.update, self.draw)


    def update(self):
        self.a_box.keycheck()

        if pyxel.btn(pyxel.KEY_R):
            self.a_box.reset()

        self.a_box.update()

    def draw(self):
        pyxel.cls(0)

        pyxel.rect(self.c_x, self.c_y + self.height -20, self.width, 20, 7)
        self.draw_control1(self.c_x + 10, self.c_y -2)
        pyxel.text(self.c_x + 50, self.c_y + self.height-18, "R:Restart", 0)

        for a_obj in obj_box:
            a_obj.draw()
        self.a_box.draw()

    def get_obj_box(self):
        return self.obj_box 

    def create_wall(self, x, y, w, h, col, geotype="wall"):
        if geotype == "wall":
            a_wall = Wall_box(x, y, w, h, col)
        elif geotype == "wall_nc":
            a_wall = Wall_NC_box(x, y, w, h, col)
        obj_box.append(a_wall)
        return a_wall

    def draw_control1(self, x=0, y=0):
        be = 16 if pyxel.btn(pyxel.KEY_E) else 0
        bs = 16 if pyxel.btn(pyxel.KEY_S) else 0
        bd = 16 if pyxel.btn(pyxel.KEY_D) else 0
        bf = 16 if pyxel.btn(pyxel.KEY_F) else 0
        bj = 16 if pyxel.btn(pyxel.KEY_J) else 0
        bk = 16 if pyxel.btn(pyxel.KEY_K) else 0

        pyxel.blt(8+x, self.height-16+y, 0, 0+be, 0, 8, 8) # E 
        pyxel.blt(0+x, self.height-8+y, 0, 0+bs, 8, 8, 8) # S
        pyxel.blt(8+x, self.height-8+y, 0, 8+bd, 0, 8, 8) # D
        pyxel.blt(16+x, self.height-8+y, 0, 8+bf, 8, 8, 8) # F
        pyxel.blt(40+x, self.height-8+y, 0, 0+bj, 16, 8, 8) # J
        pyxel.blt(48+x, self.height-8+y, 0, 8+bk, 16, 8, 8) # K

class Box:
    def __init__(self, x, y, w, h, col):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col

class Geo(Box):
    def __init__(self, x, y, w, h, col, touchable=True, ridable=True):
        super().__init__(x, y, w, h, col)
        self.touchable = touchable
        self.ridable = ridable

class Player(Box):
    def __init__(self, x, y, w, h, col):
        super().__init__(x, y, w, h, col)

        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.4
        self.gravity_1 = 0.5
        self.gravity_2 = 0.3
        self.jump_button = False
        self.dash_button = False
        self.max_vx0 = 2.0
        self.max_vx1 = 4.0

        self.resist_1 = 0.15

        self.touch_ground = False
        self.touch_ceiling = False
        self.touch_wall = False

    def keycheck(self):
        if pyxel.btn(pyxel.KEY_S):
            self.left()
        if pyxel.btn(pyxel.KEY_F):
            self.right()
        if pyxel.btnp(pyxel.KEY_K):
            self.jump()
        if pyxel.btn(pyxel.KEY_K):
            self.jump_button = True
        else:
            self.jump_button = False
        if pyxel.btn(pyxel.KEY_J):
            self.dash_button = True
        else:
            self.dash_button = False        


    def draw(self):
        pyxel.rect(self.x,self.y,self.w,self.h,self.col)

    def reset(self):
        self.x = 10
        self.y = 10
        self.vx = 0.0
        self.vy = 0.0

    def left(self):
        if self.dash_button:
            max_vx = self.max_vx1
        else:
            max_vx = self.max_vx0

        if abs(self.vx) < max_vx:
            self.vx += -self.ax
        #self.x += -1

    def right(self):
        if self.dash_button:
            max_vx = self.max_vx1
        else:
            max_vx = self.max_vx0

        if abs(self.vx) < max_vx:
            self.vx += self.ax
        #self.x += 1

    def check_touch_ground(self, temp_y):
        limit_y0 = temp_y
        self.touch_ground = False
        for a_obj in obj_box:
            if self.x + self.w <= a_obj.x or self.x >= a_obj.x + a_obj.w:
                continue
            else:
                if self.y + self.h < a_obj.y + 3 and temp_y + self.h >= a_obj.y:
                    limit_y0 = a_obj.y
                    self.touch_ground = True

        return limit_y0

    def check_ylim(self, temp_y):
        limit_y0 = temp_y
        limit_y1 = temp_y
        self.touch_ground = False
        self.touch_ceiling = False
        for a_obj in obj_box:
            if self.x + self.w <= a_obj.x or self.x >= a_obj.x + a_obj.w:
                continue
            else:
                if a_obj.ridable == True:
                    if self.y + self.h < a_obj.y + 3 and temp_y + self.h >= a_obj.y:
                        limit_y0 = a_obj.y
                        self.touch_ground = True
                if a_obj.touchable == True:
                    if self.y >= a_obj.y + a_obj.h and temp_y < a_obj.y + a_obj.h:
                        limit_y1 = a_obj.y + a_obj.h
                        self.touch_ceiling = True

        return limit_y0, limit_y1

    def check_xlim(self, temp_x):
        limit_x0 = temp_x
        limit_x1 = temp_x
        self.touch_wall = False
        for a_obj in obj_box:
            if a_obj.touchable == False:
                continue
            if self.y + self.h <= a_obj.y or self.y >= a_obj.y + a_obj.h:
                continue
            else:
                if self.x + self.w <= a_obj.x and temp_x + self.w > a_obj.x:
                    limit_x0 = a_obj.x - self.w
                    self.touch_wall = True
                if self.x >= a_obj.x + a_obj.w and temp_x < a_obj.x + a_obj.w:
                    limit_x1 = a_obj.x + a_obj.w
                    self.touch_wall = True
        
        return limit_x0, limit_x1

    def jump(self):
        if self.touch_ground == False:
            pass
        else:
            self.vy += -1 * (5.0 + abs(self.vx) * 0.2)

    def update(self):
        if self.jump_button and self.vy < 0:
            gravity = self.gravity_2
        else:
            gravity = self.gravity_1

        temp_vy = self.vy + gravity
        temp_y = int(self.y + temp_vy)
        #limit_y0 = self.check_touch_ground(temp_y)
        limit_y0, limit_y1 = self.check_ylim(temp_y)

        if self.touch_ground == True and self.touch_ceiling == True:
            pass
        elif self.touch_ground == True:
            self.vy = 0
            self.y = limit_y0 - self.h
        elif self.touch_ceiling == True:
            self.vy = 0
            self.y = limit_y1
        else:
            self.vy += gravity
            self.y += int(self.vy)

        
        temp_x = int(self.x + self.vx)
        limit_x0, limit_x1 = self.check_xlim(temp_x)
        if self.touch_wall == False:
            if self.vx < 0:
                if self.touch_ground:
                    self.vx += self.resist_1
                else:
                    self.vx += self.resist_1 * 0.5
                if self.vx > 0:
                    self.vx = 0
            if self.vx > 0:
                if self.touch_ground:
                    self.vx -= self.resist_1
                else:
                    self.vx -= self.resist_1 * 0.5
                if self.vx < 0:
                    self.vx = 0

            self.x += int(self.vx)
        else:
            self.vx = 0
            if temp_x != limit_x0:
                self.x = limit_x0
            elif temp_x != limit_x1:
                self.x = limit_x1


class Wall_box(Geo):
    def __init__(self, x, y, w, h, col):
        super().__init__(x, y, w, h, col, touchable=True, ridable=True)
    
    def draw(self):
        pyxel.rect(self.x,self.y,self.w,self.h,self.col)

class Wall_NC_box(Geo):
    def __init__(self, x, y, w, h, col):
        super().__init__(x, y, w, h, col, touchable=False, ridable=True)
    
    def draw(self):
        pyxel.rectb(self.x,self.y,self.w,self.h,self.col)

App()
