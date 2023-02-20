import pyxel
base_assets = "./assets/command_line.pyxres"

class App:
    def __init__(self):
        self.width = 100
        self.height = 100

        self.text = ""
        self.result_text = []
        self.tone = 0

        pyxel.init(self.width, self.height, fps=60, title="Command Line")

        pyxel.load(base_assets)

        for i in range(4):
            pyxel.sound(i).speed = 5

        pyxel.run(self.update, self.draw)


    def reset(self):
        self.text = ""
        self.result_text = []

    def update(self):
        if pyxel.input_keys == [8]: #BackSpaceキー
            self.text = self.text[:-1]
        if pyxel.input_keys == [13]: #Enterキー
            self.result_text.append(self.text)
            self.text = ""

        if pyxel.input_text == "R":
            self.reset()

        if pyxel.input_text != "":
            self.text += pyxel.input_text


    def draw_control1(self, x=0, y=0):
        be = 16 if pyxel.btn(pyxel.KEY_E) else 0
        bs = 16 if pyxel.btn(pyxel.KEY_S) else 0
        bd = 16 if pyxel.btn(pyxel.KEY_D) else 0
        bf = 16 if pyxel.btn(pyxel.KEY_F) else 0

        pyxel.blt(8+x, self.height-16+y, 0, 0+be, 0, 8, 8) # E 
        pyxel.blt(0+x, self.height-8+y, 0, 0+bs, 8, 8, 8) # S
        pyxel.blt(8+x, self.height-8+y, 0, 8+bd, 0, 8, 8) # D
        pyxel.blt(16+x, self.height-8+y, 0, 8+bf, 8, 8, 8) # F
       
            
    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 80, self.width, self.height, 7)

        # if pyxel.input_keys != []:
        #     print(pyxel.input_keys)

        for i, line in enumerate(self.result_text[::-1]):
            pyxel.text(10, 50-10*i, line, 7)
            if i == 6:
                break

        pyxel.rectb(7, 58, 86, 10, 7)
        pyxel.text(10, 60, "> "+self.text, 7)

        pyxel.rect(0, 80, self.width, self.height, 7)
        pyxel.text(50, 82, "R:Restart", 0)        
       
        #self.draw_control1(10, -2)
        
App()