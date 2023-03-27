import pyxel
import numpy as np
# from Cursor import Cursor
# from BDFRenderer import BDFRenderer
# from copy import deepcopy as dc

font_path1 = "assets/misaki_gothic.bdf"

#pyuni = PyxelUnicode(basedir+"/font/misaki_ttf/misaki_gothic.ttf", original_size=8)

num2item = {(0,1):"海", (0,2):"平地",(0,3):"森", (0,4):"山"}
num2color = {(0,1):12, (0,2):11,(0,3):3, (0,4):4}
        
c_list2 = [{"name":"sea", "r_range":[0.0,0.20], "color":(0,1)},   # dodgerblue
           {"name":"plain", "r_range":[0.20,0.45], "color":(0,2)},  # springgreen
           {"name":"forest", "r_range":[0.45,0.70], "color":(0,3)}, # green
           {"name":"montain", "r_range":[0.70,1.0], "color":(0,4)}] # maroon


class BDFRenderer:
    BORDER_DIRECTIONS = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]

    def __init__(self, bdf_filename):
        self.fonts = self._parse_bdf(bdf_filename)
        # self.screen_ptr = pyxel.screen.data_ptr()
        # self.screen_width = pyxel.width

    def _parse_bdf(self, bdf_filename):
        fonts = {}
        code = None
        bitmap = None
        with open(bdf_filename, "r") as f:
            for line in f:
                if line.startswith("ENCODING"):
                    code = int(line.split()[1])
                elif line.startswith("BBX"):
                    bbx_data = list(map(int, line.split()[1:]))
                    font_width, font_height = bbx_data[0], bbx_data[1]
                elif line.startswith("BITMAP"):
                    bitmap = []
                elif line.startswith("ENDCHAR"):
                    fonts[code] = (font_width, font_height, bitmap)
                    bitmap = None
                elif bitmap is not None:
                    hex_string = line.strip()
                    bin_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)
                    bitmap.append(int(bin_string[::-1], 2))
        return fonts

    def _draw_font(self, x, y, font, color):
        font_width, font_height, bitmap = font
        # screen_ptr = self.screen_ptr
        # screen_width = self.screen_width
        for j in range(font_height):
            for i in range(font_width):
                if (bitmap[j] >> i) & 1:
                    pyxel.pset(x+i, y+j, color)
                    #screen_ptr[(y + j) * screen_width + x + i] = color

    def draw_text(self, x, y, text, color=7, border_color=None):
        for char in text:
            code = ord(char)
            if code not in self.fonts:
                continue
            font = self.fonts[code]
            if border_color is not None:
                for dx, dy in self.BORDER_DIRECTIONS:
                    self._draw_font(
                        x + dx,
                        y + dy,
                        font,
                        border_color,
                    )
            self._draw_font(x, y, font, color)
            x += font[0] + 1


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


class App:
    def __init__(self):
        self.width = 128
        self.height = 148
        pyxel.init(self.width, self.height, fps=60, title="map_and_cursor")

        pyxel.load("assets/map.pyxres")
        self.bdf1 = BDFRenderer(font_path1)

        self.c_x = 0
        self.c_y = 0

        self.msize_x = 48
        self.msize_y = 32
        self.minimap = np.zeros([self.msize_x, self.msize_y],dtype=int)
        arr = create_middle_map(self.msize_x,self.msize_y,15,kp_base=2)
        set_color_map(self, arr, c_list2)

        self.cursor = Cursor(lim_x=self.msize_x * 8, lim_y=self.msize_y*8)

        pyxel.run(self.update, self.draw)

    def reset(self):
        #self.cursor = Cursor(lim_x=256, lim_y=128)
        arr = create_middle_map(48,32,15,kp_base=2)
        set_color_map(self, arr, c_list2)
        # self.px = 10
        # self.py = 10
        # pyxel.rect(self.px, self.py, 5, 5, 6)

    def update(self):
        if(pyxel.btnr(pyxel.KEY_R)):
            self.reset()

        self.cursor.update()

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

    def draw_control2(self):
        pyxel.blt(16, self.height-32, 0, 0, 16, 16, 16)
        pyxel.blt(0, self.height-16, 0, 0, 48, 16, 16)
        pyxel.blt(16, self.height-16, 0, 0, 32, 16, 16)
        pyxel.blt(32, self.height-16, 0, 0, 64, 16, 16)

    def draw_minimap(self, c_x, c_y):
        #pyxel.rect(self.width - 50, self.height - 34, 48, 32,0)
        y, x = self.minimap.shape
        xy = self.cursor.coordinate()

        print(xy[0]*8 - c_x)
        if xy[0]*8 - c_x < (self.width / 2):
            pyxel.rect(c_x + self.width - 51, c_y + 1, 50, 34, 10)
            for i in range(y):
                for j in range(x):
                    pyxel.pset(c_x + i + self.width - 50, c_y + j + 2, self.minimap[i,j])
            pyxel.pset(c_x + xy[0] + self.width - 50, c_y + xy[1] + 2,7)
        else:
            pyxel.rect(c_x + 1, c_y + 1, 50, 34, 10)
            for i in range(y):
                for j in range(x):
                    pyxel.pset(c_x + i + 2 , c_y + j + 2, self.minimap[i,j])
            pyxel.pset(c_x + xy[0] + 2, c_y + xy[1] + 2, 7)

    def draw(self):
        # クリア
        pyxel.cls(0)

        n = 2
        c_px, c_py = self.cursor.get_position()
        if c_px > self.c_x + (self.width - 8*(n+1)) and c_px <= self.msize_x * 8 - (8*(n+1)):
            self.c_x = c_px - (self.width - 8*(n+1))
        if c_px < self.c_x + 8*n and c_px >= 8*n:
            self.c_x = c_px -  8*n

        if c_py > self.c_y + (self.height - 20 - 8*(n+1)) and c_py <= self.msize_y * 8 - (8*(n+1)):
            self.c_y = c_py - (self.height - 20 - 8*(n+1))
        if c_py < self.c_y + 8*n and c_py >= 8*n:
            self.c_y = c_py -  8*n

        #c_x = (pyxel.frame_count // 30)*8 % 240
        #c_x = 0
        pyxel.camera(self.c_x, self.c_y)
 
        # マップの表示
        pyxel.bltm(0, 0, 1, 0, 0, 48*8, 32*8, 0)

        # ミニマップの表示
        self.draw_minimap(self.c_x, self.c_y)

       # 下領域の描画
        pyxel.rect(self.c_x, self.c_y + self.height -20, self.width, 20, 7)
        self.draw_control1(self.c_x + 10, self.c_y -2)
        pyxel.text(self.c_x + 50, self.c_y + self.height-18, "R:Restart", 0)
        
        # ゲーム部の描画
        self.cursor.draw()

        xy = self.cursor.coordinate()
        pyxel.text(self.c_x + 96, self.c_y + self.height-18, f'({xy[0]}, {xy[1]})', 0)
        map_item_tpl = pyxel.tilemap(1).pget(xy[0], xy[1])
        self.bdf1.draw_text(self.c_x + 100, self.c_y + self.height-10, num2item[map_item_tpl], color=0)
        #pyuni.text(self.c_x + 100, self.c_y + self.height-10, num2item[map_item_tpl], color=0)

        #pyxel.rect(self.px, self.py, 5, 5, 6)
        #self.draw_control2()



def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def create_middle_map(y, x, grad, kp_base=6):
    height_map = np.zeros([y,x], dtype=float)
    kp_num = kp_base + np.random.randint(4)
    keypoints = [[np.random.randint(y),np.random.randint(x)] for _ in range(kp_num)]
    for kp in keypoints:
        height_map[kp[0], kp[1]] = 0.99
    
    while len(keypoints) > 0:
        next_kp = []
        for kp in keypoints:
            for i,j in zip([-1,1,0,0],[0,0,-1,1]):
                if 0 <= kp[0]+i < y and 0 <= kp[1]+j < x:
                    h_next = height_map[kp[0],kp[1]] - np.random.randint(grad) / 100
                    if h_next > height_map[kp[0]+i,kp[1]+j]:
                        height_map[kp[0]+i,kp[1]+j] = h_next
                        if not [kp[0]+i, kp[1]+j] in next_kp:
                            next_kp.append([kp[0]+i, kp[1]+j])

        keypoints = next_kp

    return height_map



def set_color_map(self, arr, c_list):
    y, x = arr.shape
    cmap = np.zeros([y,x], dtype=int)
    
    for i in range(y):
        for j in range(x):
            for c in c_list:
                if c["r_range"][0] <= arr[i,j] < c["r_range"][1]:
                    cmap[i,j] = num2color[c["color"]]
                    pyxel.tilemap(1).pset(i, j, c["color"])

    self.minimap = cmap
App()
