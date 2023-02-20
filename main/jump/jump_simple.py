import pyxel
class App:
  def __init__(self):
    pyxel.init(100, 100)
    self.a_box = Player(5,5,8,8,7)
    self.floor = Wall_box(0,80,100,20,3)
    global obj_box
    obj_box = []
    obj_box.append(self.floor)

    pyxel.run(self.update, self.draw)

  def update(self):
    if pyxel.btn(pyxel.KEY_S):
      self.a_box.left()
    if pyxel.btn(pyxel.KEY_F):
      self.a_box.right()
    if pyxel.btnp(pyxel.KEY_K):
      self.a_box.jump()

    self.a_box.update()

  def draw(self):
    pyxel.cls(0)
    self.a_box.draw()
    self.floor.draw()
    pyxel.text(5, 100-18, "S:<-", 7)
    pyxel.text(5, 100-8, "F:->", 7)
    pyxel.text(25, 100-18, "K:Jump", 7)
    pyxel.text(25, 100-8, "ESC:End", 7)

  def get_obj_box(self):
     return self.obj_box 

class Box:
  def __init__(self, x, y, w, h, col):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.col = col

class Player(Box):
  def __init__(self, x, y, w, h, col):
    super().__init__(x, y, w, h, col)
    self.col = col

    self.vx = 0.0
    self.vy = 0.0

    self.gravity_1 = 0.5

    self.touch_ground = False

  def draw(self):
    pyxel.rect(self.x,self.y,self.w,self.h,self.col)

  def left(self):
    self.x += -1

  def right(self):
    self.x += 1

  def check_touch_ground(self, temp_y):
    limit_y0 = temp_y
    self.touch_ground = False
    for a_obj in obj_box:
      if temp_y + self.h >= a_obj.y:
        limit_y0 = a_obj.y
        self.touch_ground = True

    return limit_y0

  def jump(self):
    if self.touch_ground == False:
      pass
    else:
      self.vy += -5.0 # ここを変えるとジャンプの高さが変わる

  def update(self):
    temp_vy = self.vy + self.gravity_1
    temp_y = int(self.y + temp_vy)
    limit_y0 = self.check_touch_ground(temp_y)

    if self.touch_ground == False:
      self.vy += self.gravity_1
      self.y += int(self.vy)
    else:
      self.vy = 0
      self.y = limit_y0 - self.h
  


class Wall_box(Box):
  def __init__(self, x, y, w, h, col):
    super().__init__(x, y, w, h, col)
    
  def draw(self):
    pyxel.rectb(self.x,self.y,self.w,self.h,self.col)


App()
