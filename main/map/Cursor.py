import pyxel

class Cursor:
    def __init__(self, size=8, px=8, py=8, lim_x=128, lim_y=128):
        self.px = px
        self.py = py
        self.height = size
        self.width = size
        self.px_pre = px
        self.py_pre = py
        self.speed = 5 # 小さいほど速い

        self.margin_base = 8
        self.margin = self.margin_base
        self.moved = 0        
        self.moving = False
        self.music_wait = 0
        self.px_target = self.px
        self.py_target = self.py

        self.lim_x0 = 0
        self.lim_x1 = lim_x
        self.lim_y0 = 0
        self.lim_y1 = lim_y

        self.flag = False # チェック用

        self.mx = 0
        self.my = 0

        self.wait = 0

    def draw(self):
        if self.moving == False:
            self.sound()
        pyxel.rectb(self.px, self.py, self.height, self.width, 6)
        #pyxel.text(50, 92, str(self.moved), 0)
        #pyxel.text(56, 92, "True" if self.flag else "False", 0)

    def coordinate(self):
        #print(pyxel.tilemap(1).pget(self.px//8, self.py//8))
        xy = (self.px//8, self.py//8)
        #map_item_tpl = pyxel.tilemap(1).pget(self.px//8, self.py//8)
        #pyxel.text(self.lim_x0 + 100, self.lim_y1 + 2, str(map_item_tpl), 0)
        #pyxel.text(self.lim_x0 + 100, self.lim_y1 + 2, f'({self.px//8}, {self.py//8})', 0)
        return xy    
    
    def get_position(self):
        return self.px, self.py

    def update(self):
        if self.wait > 0:
          self.wait -= 1
          return


        #if pyxel.btn(pyxel.KEY_J) and self.moved == 2:
        if pyxel.btn(pyxel.KEY_J) and pyxel.btn(pyxel.KEY_K):
            self.speed = 1
        elif pyxel.btn(pyxel.KEY_J):
            self.speed = 2
        else:
            self.speed = 4

        # 加速中はmarginも短くする
        if pyxel.btn(pyxel.KEY_J):
            self.margin = 5
        else:
            self.margin = self.margin_base

        # 加速キーを離したら一旦止める
        if pyxel.btnr(pyxel.KEY_J):
            self.mx = 0
            self.my = 0
        
        # 方向キーも離したら一旦止める
        if self.moved == 2 and (pyxel.btnr(pyxel.KEY_S) or pyxel.btnr(pyxel.KEY_F)):
            self.mx = 0
        if self.moved == 2 and (pyxel.btnr(pyxel.KEY_E) or pyxel.btnr(pyxel.KEY_D)):
            self.my = 0

        # 動作のメイン処理
        if self.moving == False:
            self.move()
            self.move_check()

            if self.moved == 1 or self.moved == 2:
                self.moving = True
                self.anime1(self.px_pre, self.px, self.py_pre, self.py)
                #self.sound()
                self.anime()
        else:
            self.anime()
       

    def anime1(self, x0, x1, y0, y1):
        if abs(x1 - x0) == self.width:
            self.px_target = x1
            self.px = x0
        
        if abs(y1 - y0) == self.height:
            self.py_target = y1
            self.py = y0

        

    def anime(self):
        speed_x = self.width // self.speed
        if self.px_target > self.px:
            self.px += speed_x
            if self.px > self.px_target:
                self.px = self.px_target
        elif self.px_target < self.px:
            self.px += -speed_x
            if self.px < self.px_target:
                self.px = self.px_target
        
        speed_y = self.height // self.speed
        if self.py_target > self.py:
            self.py += speed_y
            if self.py > self.py_target:
                self.py = self.py_target
        elif self.py_target < self.py:
            self.py += -speed_y
            if self.py < self.py_target:
                self.py = self.py_target
        #print(self.px, self.py)

        if self.px_target == self.px and self.py_target == self.py:
            self.moving = False
            self.px_pre = self.px
            self.py_pre = self.py            

    def move(self):
        if(pyxel.btn(pyxel.KEY_F) and pyxel.btn(pyxel.KEY_S)):
            self.mx = 0
        else:
            if(pyxel.btn(pyxel.KEY_F)):
                self.mx += 1
            if(pyxel.btn(pyxel.KEY_S)):
                self.mx += -1
        if(pyxel.btn(pyxel.KEY_D) and pyxel.btn(pyxel.KEY_E)):
            self.my = 0
        else:
            if(pyxel.btn(pyxel.KEY_D)):
                self.my += 1
            if(pyxel.btn(pyxel.KEY_E)):
                self.my += -1

        # x軸移動処理
        if self.mx > self.margin and pyxel.btn(pyxel.KEY_F):
            self.px += 1 * self.width
        elif self.mx >= 1 and not pyxel.btn(pyxel.KEY_F):
            self.mx = 0
            self.px += 1 * self.width

        if self.mx < -self.margin and pyxel.btn(pyxel.KEY_S):
            self.px += -1 * self.width
        elif self.mx <= -1 and not pyxel.btn(pyxel.KEY_S):
            self.mx = 0
            self.px += -1 * self.width

        # y軸移動処理
        if self.my > self.margin and pyxel.btn(pyxel.KEY_D):
            self.py += 1 * self.height
        elif self.my >= 1 and not pyxel.btn(pyxel.KEY_D):
            self.my = 0
            self.py += 1 * self.height

        if self.my < -self.margin and pyxel.btn(pyxel.KEY_E):
            self.py += -1 * self.height
        elif self.my <= -1 and not pyxel.btn(pyxel.KEY_E):
            self.my = 0
            self.py += -1 * self.height


    def move_check(self):
        if self.px > self.lim_x1 - self.width:
            self.px = self.lim_x1 - self.width
        if self.px < self.lim_x0:
            self.px = self.lim_x0
        if self.py > self.lim_y1 - self.height:
            self.py = self.lim_y1 - self.height
        if self.py < self.lim_y0:
            self.py = self.lim_y0

        if self.px != self.px_pre or self.py != self.py_pre:
            self.flag = True
            if self.moved == 1:
                self.moved = 2
            elif self.moved == 0:
                self.moved = 1

        else:
            self.flag = False            
            if self.moved == 2:
                self.moved = 1
            else:
                self.moved = 0

    def sound(self):
        if self.moved == 1:
            pyxel.play(0, 1, False)
            self.music_wait = 0
        elif self.moved == 2:
            if self.music_wait > 0:
                self.music_wait -= 1
            elif self.music_wait == 0:
                pyxel.play(0, 2, False)
                self.music_wait = 1
        else:
            self.music_wait = 0

                

   