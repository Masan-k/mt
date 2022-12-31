import pygame,sys
import pygame.locals
import math 
class Mt:
  #シフトレバー
  SHIFT_BASE_POS_X = 130
  SHIFT_BASE_POS_Y = 300
  SHIFT_DISTANCE_X = 150 
  SHIFT_DISTANCE_Y = 50

  TIRE_HEIGHT = 40
  TIRE_INIT_POS_X_L = 150
  TIRE_INIT_POS_X_R = 300 
  TIRE_INIT_POS_Y = 100 
  TIRE_DISTANCE = 100

  def init(self):
    #シフトレバー
    self.beforeInputHat = ""

    #エンジン
    self.isStart = False
    self.isAllowStart = True

    #サイドブレーキ
    self.isSideBrake = True
    self.isAllowSideBrake = True

    #ウインカー
    self.beforeLeft = 0
    self.beforeRight = 0
    self.left = 0
    self.right = 0

    #ハンドル
    self.beforePosX = None 
    self.beforePosY = None 
    self.beforeDistance = None 
    self.distanceX = None
    self.beforeDistanceX = None 
    self.angle = 90 

    self.shiftPosX = self.SHIFT_BASE_POS_X + self.SHIFT_DISTANCE_X*2
    self.shiftPosY = self.SHIFT_BASE_POS_Y + self.SHIFT_DISTANCE_Y*2

  def main(self):
    def distance_2points(x1, y1, x2, y2):
      d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
      return d

    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()

    #SCREEN_SIZE = (545, 450) #
    SCREEN_SIZE = (945, 450)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    font = pygame.font.Font(None,30)

    while True:
      pygame.display.update()
      screen.fill((0,0,0))

      #------------
      #ハンドル
      #------------
      #アナログスティック
      x0 = joy.get_axis(0) # min:-1.0 ~ max:0.9
      y0 = joy.get_axis(1)
      pygame.draw.circle(screen,(150,150,255),(225 + x0*10 ,self.TIRE_INIT_POS_Y + y0*10),5)
      pygame.draw.line(screen, (200,200,200),(225,self.TIRE_INIT_POS_Y)
                                            ,(225,self.TIRE_INIT_POS_Y+self.TIRE_DISTANCE),width=3)


      self.angle = 90 - joy.get_axis(0) * 40 
      screen.blit(font.render("angle -> " + str(self.angle), True, (200,200,200)),(520,10)) 

      x = math.cos(math.radians(self.angle))*(self.TIRE_HEIGHT/2)
      y = math.sin(math.radians(self.angle))*(self.TIRE_HEIGHT/2)

      #タイヤの向き
      pygame.draw.rect(screen,(200,200,200),(self.TIRE_INIT_POS_X_L, self.TIRE_INIT_POS_Y,150,2))
      #left
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_L,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_L + x ,self.TIRE_INIT_POS_Y - y),width=3)
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_L,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_L - x ,self.TIRE_INIT_POS_Y + y),width=3)
      #right
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_R,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_R + x ,self.TIRE_INIT_POS_Y - y),width=3)
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_R,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_R - x ,self.TIRE_INIT_POS_Y + y),width=3)

      #タイヤの向き
      pygame.draw.rect(screen,(200,200,200),(self.TIRE_INIT_POS_X_L, self.TIRE_INIT_POS_Y+self.TIRE_DISTANCE,150,2))
      pygame.draw.line(screen, (200,200,200),(self.TIRE_INIT_POS_X_L, self.TIRE_INIT_POS_Y-self.TIRE_HEIGHT/2+self.TIRE_DISTANCE)
                                            ,(self.TIRE_INIT_POS_X_L ,self.TIRE_INIT_POS_Y+self.TIRE_HEIGHT/2+self.TIRE_DISTANCE),width=3)
      pygame.draw.line(screen, (200,200,200),(self.TIRE_INIT_POS_X_R, self.TIRE_INIT_POS_Y-self.TIRE_HEIGHT/2+self.TIRE_DISTANCE)
                                            ,(self.TIRE_INIT_POS_X_R ,self.TIRE_INIT_POS_Y+self.TIRE_HEIGHT/2+self.TIRE_DISTANCE),width=3)
  
       #---------
      #エンジン
      #---------
      if joy.get_button(7) == 1:
        if self.isAllowStart and self.isStart == True:
          self.isStart = False 
          self.init()
        elif self.isAllowStart:
          self.isStart = True
        self.isAllowStart = False
      else:
        self.isAllowStart = True

      if self.isStart: dispMessage = "ON"
      else:  dispMessage = "OFF"
      screen.blit(font.render(dispMessage, True, (200,200,200)),[250,20]) 

      #-----------
      #ウインカー
      #-----------
      #LEFT
      pygame.draw.rect(screen,(100,100,100),(50,10,50,30))
      pygame.draw.rect(screen,(0,0,0),(51,11,48,28))
      
      if self.beforeLeft != joy.get_button(4):
        if joy.get_button(4) == 1:
          if self.left == 0:
            self.left = 1
          else:
            self.left = 0
        self.beforeLeft = joy.get_button(4) 
      if self.left == 1:
        pygame.draw.rect(screen,(255,212,0),(51,11,48,28))

      #RIGHT
      pygame.draw.rect(screen,(100,100,100),(450,10,50,30))
      pygame.draw.rect(screen,(0,0,0),(451,11,48,28))
      if self.beforeRight != joy.get_button(5):
        if joy.get_button(5) == 1:
          if self.right == 0:
            self.right = 1
          else:
            self.right = 0
        self.beforeRight = joy.get_button(5) 

      if self.right == 1:
        pygame.draw.rect(screen,(255,212,0),(451,11,48,28))

      #-----------------
      #クラッチメーター
      #-----------------
      pygame.draw.rect(screen,(100,100,100),(50,50,50,200))
      pygame.draw.rect(screen,(0,0,0),(51,51,48,198))

      #max押すと高さ100
      #開放状態：-1
      #押し込んだ状態：0.99
      #-1 < 0.99
      #input -> power
      # -1   -> 0
      # 0.99 -> 200
      clutchPower = (joy.get_axis(2)+1)*100
      pygame.draw.rect(screen,(0,150,0),(50,50,50,clutchPower))

      #-----------------
      #アクセルメーター
      #-----------------
      pygame.draw.rect(screen,(100,100,100),(450,50,50,200))
      pygame.draw.rect(screen,(0,0,0),(451,51,48,198))

      acceleratorPower = (joy.get_axis(5)+1)*100
      pygame.draw.rect(screen,(0,0,150),(450,50,50,acceleratorPower))

      #-----------------
      #ブレーキメーター
      #-----------------
      pygame.draw.rect(screen,(100,100,100),(350,50,50,100))
      pygame.draw.rect(screen,(0,0,0),(351,51,48,98))

      brakePower = -joy.get_axis(4)*100 # 0 -> -1
      pygame.draw.rect(screen,(150,0,0),(350,50,50,brakePower)) #上から延ばす

      #-----------------
      #シフトレバー(枠)
      #-----------------
      pygame.draw.rect(screen,(100,100,100),(self.SHIFT_BASE_POS_X,self.SHIFT_BASE_POS_Y, 300, 100))
      pygame.draw.rect(screen,(0,0,0),(self.SHIFT_BASE_POS_X+1,self.SHIFT_BASE_POS_Y , self.SHIFT_DISTANCE_X -2, self.SHIFT_DISTANCE_Y -1))
      pygame.draw.rect(screen,(0,0,0),(self.SHIFT_BASE_POS_X+self.SHIFT_DISTANCE_X+1,self.SHIFT_BASE_POS_Y , self.SHIFT_DISTANCE_X -2, self.SHIFT_DISTANCE_Y -1))
      
      pygame.draw.rect(screen,(0,0,0),(self.SHIFT_BASE_POS_X+1,self.SHIFT_BASE_POS_Y+self.SHIFT_DISTANCE_Y+1 , self.SHIFT_DISTANCE_X -2, self.SHIFT_DISTANCE_Y -1))
      pygame.draw.rect(screen,(0,0,0),(self.SHIFT_BASE_POS_X+self.SHIFT_DISTANCE_X+1,self.SHIFT_BASE_POS_Y+self.SHIFT_DISTANCE_Y+1 , self.SHIFT_DISTANCE_X -2, self.SHIFT_DISTANCE_Y -1))

      #-----------------
      #シフトレバー
      #-----------------
      inputHat = joy.get_hat(0)
      if self.beforeInputHat == "" or inputHat != self.beforeInputHat:
        if inputHat[0] == -1:
          self.shiftPosX = self.shiftPosX - self.SHIFT_DISTANCE_X
        if inputHat[0] == 1:
          self.shiftPosX = self.shiftPosX + self.SHIFT_DISTANCE_X
        if inputHat[1] == -1:
          self.shiftPosY = self.shiftPosY + self.SHIFT_DISTANCE_Y
        if inputHat[1] == 1:
          self.shiftPosY = self.shiftPosY - self.SHIFT_DISTANCE_Y
        self.beforeInputHat = joy.get_hat(0)

      pygame.draw.circle(screen,(200,200,200),(self.shiftPosX,self.shiftPosY),10)
      #screen.blit(font.render('inputHat : ' + str(inputHat) , True, (255, 255, 255)), [infoPosX, infoPosY+120]) 

      #-----------------
      #サイドブレーキ
      #-----------------
      pygame.draw.rect(screen,(100,100,100),(50,300,30,100))
      pygame.draw.rect(screen,(0,0,0),(51,301,28,98))

      if joy.get_button(6) == 1:
        if self.isAllowSideBrake and self.isSideBrake == False:
          self.isSideBrake = True
        elif self.isAllowSideBrake:
          self.isSideBrake = False
        self.isAllowSideBrake = False 

      else: 
        self.isAllowSideBrake = True

      if self.isSideBrake:
        pygame.draw.rect(screen,(150,100,100),(51,301,28,98))
 
      #キー入力処理
      for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN: 
          #終了処理
          if event.key == pygame.locals.K_ESCAPE:
            pygame.quit()
            sys.exit()

mt = Mt()
mt.init()
mt.main()

