import pyxel
import numpy as np
from Cursor import Cursor
from BDFRenderer import BDFRenderer
#from copy import deepcopy as dc

font_path1 = "assets/misaki_gothic.bdf"
bdf1 = BDFRenderer(font_path1)

#pyuni = PyxelUnicode(basedir+"/font/misaki_ttf/misaki_gothic.ttf", original_size=8)


num2item = {(0,1):"海", (0,2):"平地",(0,3):"森", (0,4):"山"}
        
c_list2 = [{"name":"sea", "r_range":[0.0,0.20], "color":(0,1)},   # dodgerblue
           {"name":"plain", "r_range":[0.20,0.45], "color":(0,2)},  # springgreen
           {"name":"forest", "r_range":[0.45,0.70], "color":(0,3)}, # green
           {"name":"montain", "r_range":[0.70,1.0], "color":(0,4)}] # maroon

class App:
    def __init__(self):
        self.width = 128
        self.height = 148
        pyxel.init(self.width, self.height, fps=60, title="map_and_cursor")

        pyxel.load("assets/mr.pyxres")

        self.c_x = 0
        self.c_y = 0

        self.msize_x = 48
        self.msize_y = 32
        arr = create_middle_map(self.msize_x,self.msize_y,15,kp_base=2)
        set_color_map(arr, c_list2)

        self.cursor = Cursor(lim_x=self.msize_x * 8, lim_y=self.msize_y*8)

        pyxel.run(self.update, self.draw)

    def reset(self):
        #self.cursor = Cursor(lim_x=256, lim_y=128)
        arr = create_middle_map(48,32,15,kp_base=2)
        set_color_map(arr, c_list2)
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

       # 下領域の描画
        pyxel.rect(self.c_x, self.c_y + self.height -20, self.width, 20, 7)
        self.draw_control1(self.c_x + 10, self.c_y -2)
        pyxel.text(self.c_x + 50, self.c_y + self.height-18, "R:Restart", 0)
        
        # ゲーム部の描画
        self.cursor.draw()

        xy = self.cursor.coordinate()
        pyxel.text(self.c_x + 96, self.c_y + self.height-18, f'({xy[0]}, {xy[1]})', 0)
        map_item_tpl = pyxel.tilemap(1).pget(xy[0], xy[1])
        bdf1.draw_text(self.c_x + 100, self.c_y + self.height-10, num2item[map_item_tpl], color=0)
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



def set_color_map(arr, c_list):
    y, x = arr.shape
    #cmap = np.zeros([y,x,3], dtype=int)
    
    for i in range(y):
        for j in range(x):
            for c in c_list:
                if c["r_range"][0] <= arr[i,j] < c["r_range"][1]:
                    #cmap[i,j] = c["color"]
                    pyxel.tilemap(1).pset(i, j, c["color"])

App()
