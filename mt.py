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

  TAKO_L = (620,120)
  TAKO_R = (810,120)
  TAKO_RADIUS = 80 

  def init(self):
    self.rpm = 0
    self.initRpm = 0
    self.speed = 0

    self.carPosX = 500
    self.carPosY = 500
    self.carAngle = 0

    self.isJoin = False 
    self.joinCount = 0
    self.status = 'none'

    #シフトレバー
    self.beforeInputHat = ""
    self.leverPosX = 2
    self.leverPosY = 2
    self.gear = 0 

    self.shiftPosX = self.SHIFT_BASE_POS_X + self.SHIFT_DISTANCE_X*2
    self.shiftPosY = self.SHIFT_BASE_POS_Y + self.SHIFT_DISTANCE_Y*2

    #エンジン
    self.isStart = False
    self.isAllowStart = None 

    #サイドブレーキ
    self.isSideBrake = True
    self.isAllowSideBrake = True

    #ウインカー
    self.beforeLeft = 0
    self.beforeRight = 0
    self.left = 0
    self.right = 0

    #ハンドル
    self.distanceX = None
    self.angle = 90 

  def main(self):
    def distance_2points(x1, y1, x2, y2):
      d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
      return d

    def getSpeed(aPower,cPower,gear):
      return aPower/5000 * (60-cPower)/10

    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()

    #SCREEN_SIZE = (545, 450) #
    SCREEN_SIZE = (945, 650)

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
                                            ,(225,self.TIRE_INIT_POS_Y+self.TIRE_DISTANCE),width=1)

      self.angle = 90 - joy.get_axis(0) * 40 

      x = math.cos(math.radians(self.angle))*(self.TIRE_HEIGHT/2)
      y = math.sin(math.radians(self.angle))*(self.TIRE_HEIGHT/2)

      #タイヤの向き
      pygame.draw.rect(screen,(200,200,200),(self.TIRE_INIT_POS_X_L, self.TIRE_INIT_POS_Y,150,1))
      #left
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_L,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_L + x ,self.TIRE_INIT_POS_Y - y),width=1)
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_L,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_L - x ,self.TIRE_INIT_POS_Y + y),width=1)
      #right
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_R,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_R + x ,self.TIRE_INIT_POS_Y - y),width=1)
      pygame.draw.line(screen, (150,150,255),(self.TIRE_INIT_POS_X_R,self.TIRE_INIT_POS_Y)
                                            ,(self.TIRE_INIT_POS_X_R - x ,self.TIRE_INIT_POS_Y + y),width=1)

      #タイヤの向き
      pygame.draw.rect(screen,(200,200,200),(self.TIRE_INIT_POS_X_L, self.TIRE_INIT_POS_Y+self.TIRE_DISTANCE,150,1))
      pygame.draw.line(screen, (200,200,200),(self.TIRE_INIT_POS_X_L, self.TIRE_INIT_POS_Y-self.TIRE_HEIGHT/2+self.TIRE_DISTANCE)
                                            ,(self.TIRE_INIT_POS_X_L ,self.TIRE_INIT_POS_Y+self.TIRE_HEIGHT/2+self.TIRE_DISTANCE),width=1)
      pygame.draw.line(screen, (200,200,200),(self.TIRE_INIT_POS_X_R, self.TIRE_INIT_POS_Y-self.TIRE_HEIGHT/2+self.TIRE_DISTANCE)
                                            ,(self.TIRE_INIT_POS_X_R ,self.TIRE_INIT_POS_Y+self.TIRE_HEIGHT/2+self.TIRE_DISTANCE),width=1)
  
      #---------
      #エンジン
      #---------
      if joy.get_button(7) == 1:
        if self.isAllowStart == False and self.isStart == False:
          self.isStart = True
        elif self.isAllowStart == False and self.isStart:
          self.init()

      if joy.get_button(7) == 1:
        self.isAllowStart = True
      else:
        self.isAllowStart = False 

      #screen.blit(font.render('isStart : ' + str(self.isStart), True, (200,200,200)),(680,300)) 
      #screen.blit(font.render('isAllowStart : ' + str(self.isAllowStart), True, (200,200,200)),(680,320)) 
      

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

      # -1:0.99 = 0:200
      clutchPower = (joy.get_axis(2)+1)/2*100 #min:-1 max: 0.99
      pygame.draw.rect(screen,(0,150,0),(50,50,50,clutchPower * 2))
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
      
      pygame.draw.rect(screen,(0,0,0),(self.SHIFT_BASE_POS_X+1,self.SHIFT_BASE_POS_Y+self.SHIFT_DISTANCE_Y+1 
                                     ,self.SHIFT_DISTANCE_X -2, self.SHIFT_DISTANCE_Y -1))
      pygame.draw.rect(screen,(0,0,0),(self.SHIFT_BASE_POS_X+self.SHIFT_DISTANCE_X+1,self.SHIFT_BASE_POS_Y+self.SHIFT_DISTANCE_Y+1
                                     ,self.SHIFT_DISTANCE_X -2, self.SHIFT_DISTANCE_Y -1))

      #-----------------
      #シフトレバー
      #-----------------
      inputHat = joy.get_hat(0)
      if self.beforeInputHat == "" or inputHat != self.beforeInputHat and clutchPower >= 99:
        if inputHat[0] == -1 and self.leverPosX > 0 and self.leverPosY == 1:
          self.shiftPosX = self.shiftPosX - self.SHIFT_DISTANCE_X
          self.leverPosX = self.leverPosX - 1

        if inputHat[0] == 1 and self.leverPosX < 2 and self.leverPosY == 1:
          self.shiftPosX = self.shiftPosX + self.SHIFT_DISTANCE_X
          self.leverPosX = self.leverPosX + 1

        if inputHat[1] == -1 and self.leverPosY < 2:
          self.shiftPosY = self.shiftPosY + self.SHIFT_DISTANCE_Y
          self.leverPosY = self.leverPosY + 1

        if inputHat[1] == 1 and self.leverPosY > 0:
          self.shiftPosY = self.shiftPosY - self.SHIFT_DISTANCE_Y
          self.leverPosY = self.leverPosY - 1

        self.beforeInputHat = joy.get_hat(0)

      if self.leverPosY == 1:
        self.gear = 0
      elif self.leverPosX == 0:
        if self.leverPosY == 0:
          self.gear = 1
        else:
          self.gear = 2 
      elif self.leverPosX == 1:
        if self.leverPosY == 0:
          self.gear = 3
        else:
          self.gear = 4
      else:
        if self.leverPosY == 0:
          self.gear = 5
        else:
          self.gear = 9

      pygame.draw.circle(screen,(200,200,200),(self.shiftPosX,self.shiftPosY),10)

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

      
      #---------
      #速度制御
      #---------
      if self.isStart:
        if self.rpm < 20:
          self.initRpm = self.initRpm + 0.2
        self.rpm = acceleratorPower + self.initRpm

      #clutchPower 0 ~ 1.99
      #クラッチ40~60％かつアクセルを踏んでいる時に半クラッチ状態にする
      
      #クラッチ60%まではスピードは変わらない(100~60)...seed + 0 
      #クラッチ0だったらアクセル(100%)をスピードに伝える...

      if self.isStart and clutchPower >= 40 and  clutchPower <= 60 and acceleratorPower > 0 and self.gear == 1 and self.isJoin == False:
        self.status = "harf clutch"
        self.speed = self.speed + getSpeed(acceleratorPower,clutchPower,self.gear)

        if self.speed > 20:
          self.speed = 20

        self.joinCount = self.joinCount + 1
        if self.joinCount == 500:
          self.isJoin = True

      elif self.isJoin == True and acceleratorPower > 0 :
        self.status = "on join and accele on"

        if self.gear == 1 and self.speed > 20:
          self.speed = self.speed - 0.01
        elif self.gear == 2 and self.speed > 40:
          self.speed = self.speed - 0.01
          #self.speed = 40
        elif self.gear == 3 and self.speed > 60:
          self.speed = self.speed - 0.01
          #self.speed = 60
        elif self.gear == 4 and self.speed > 80:
          self.speed = self.speed - 0.01
          #self.speed = 80
        elif self.gear == 5 and self.speed > 100:
          self.speed = self.speed - 0.01
          #self.speed = 100
        else:

          if self.gear != 0 and self.gear != 9:
            if self.speed <= self.speed + getSpeed(acceleratorPower,clutchPower,self.gear)*0.5:
              self.speed = self.speed + getSpeed(acceleratorPower,clutchPower,self.gear)*0.5
            else:
              if self.speed > 0:
                self.speed = self.speed - 0.01 

      else:
        self.status = "else"
        if self.speed >= 0:
          self.speed = self.speed - 0.01 
          if self.speed < 0:
            self.speed = 0
            self.isJoin = False
            self.joinCount = 0

        if self.isJoin == False:
          self.joinCount = self.joinCount - 1
          if self.joinCount < 0:
            self.joinCount = 0

      screen.blit(font.render('GEAR : ' + str(self.gear), True, (200,200,200)),(50,440))
      screen.blit(font.render('JOIN COUNT : ' + str(self.joinCount), True, (200,200,200)),(50,480))
      screen.blit(font.render('IS JOIN : ' + str(self.isJoin), True, (200,200,200)),(50,520))
      #screen.blit(font.render('status : ' + str(self.status), True, (200,200,200)),(570,395))
      #screen.blit(font.render("tire angle -> " + str(self.angle), True, (200,200,200)),(520,150)) 
      #screen.blit(font.render('clutchPower : ' + str(clutchPower), True, (200,200,200)),(520,90))


      #------------------
      #タコメーターの描画
      #------------------
      pygame.draw.circle(screen,(200,200,200),self.TAKO_L, self.TAKO_RADIUS)
      pygame.draw.circle(screen,(0,0,0),self.TAKO_L, self.TAKO_RADIUS-1)
      pygame.draw.circle(screen,(200,200,200),self.TAKO_R,self.TAKO_RADIUS)
      pygame.draw.circle(screen,(0,0,0),self.TAKO_R,self.TAKO_RADIUS-1)

      pygame.draw.line(screen, (200,200,200),self.TAKO_L,(620,40),width=1)
      
      #7-8-9
      for i in range(0,4):
        x = math.cos(math.radians(i*30)) * self.TAKO_RADIUS
        y = math.sin(math.radians(i*30)) * self.TAKO_RADIUS
        pygame.draw.line(screen, (200,200,200),self.TAKO_L,(self.TAKO_L[0]+x,self.TAKO_L[1]-y),width=1)
        pygame.draw.line(screen, (200,200,200),self.TAKO_R,(self.TAKO_R[0]+x,self.TAKO_R[1]-y),width=1)

      #10
      x = math.cos(math.radians(30)) * self.TAKO_RADIUS
      y = math.sin(math.radians(30)) * self.TAKO_RADIUS
      pygame.draw.line(screen, (200,200,200),self.TAKO_L,(self.TAKO_L[0]+x,self.TAKO_L[1]+y),width=1)
      pygame.draw.line(screen, (200,200,200),self.TAKO_R,(self.TAKO_R[0]+x,self.TAKO_R[1]+y),width=1)

      #4,5,6
      for i in range(0,4):
        x = math.cos(math.radians(i*30)) * self.TAKO_RADIUS
        y = math.sin(math.radians(i*30)) * self.TAKO_RADIUS
        pygame.draw.line(screen, (200,200,200),self.TAKO_L,(self.TAKO_L[0]-x,self.TAKO_L[1]-y),width=1)
        pygame.draw.line(screen, (200,200,200),self.TAKO_R,(self.TAKO_R[0]-x,self.TAKO_R[1]-y),width=1)

      #0,1,2,3
      for i in range(0,4):
        x = math.cos(math.radians(i*30)) * self.TAKO_RADIUS
        y = math.sin(math.radians(i*30)) * self.TAKO_RADIUS
        pygame.draw.line(screen, (200,200,200),self.TAKO_L,(self.TAKO_L[0]-x,self.TAKO_L[1]+y),width=1)
        pygame.draw.line(screen, (200,200,200),self.TAKO_R,(self.TAKO_R[0]-x,self.TAKO_R[1]+y),width=1)

      #--------------------
      #速度・RPMの針の描画
      #--------------------
      pygame.draw.circle(screen,(0,0,0),self.TAKO_L, self.TAKO_RADIUS-8)
      pygame.draw.circle(screen,(0,0,0),self.TAKO_R, self.TAKO_RADIUS-8)

      if self.rpm < 180:
        x = math.cos(math.radians(90-self.rpm/2*3)) * self.TAKO_RADIUS
        y = math.sin(math.radians(90-self.rpm/2*3)) * self.TAKO_RADIUS
        pygame.draw.line(screen, (200,200,200),self.TAKO_L,(self.TAKO_L[0]-x,self.TAKO_L[1]+y),width=3)
      else:
        x = math.cos(math.radians(90-self.rpm/2*3)) * self.TAKO_RADIUS
        y = math.sin(math.radians(90-self.rpm/2*3)) * self.TAKO_RADIUS
        pygame.draw.line(screen, (200,200,200),self.TAKO_L,(self.TAKO_L[0]-x,self.TAKO_L[1]+y),width=3)

      if self.speed < 90:
        x = math.cos(math.radians(90-self.speed*3)) * self.TAKO_RADIUS
        y = math.sin(math.radians(90-self.speed*3)) * self.TAKO_RADIUS
        pygame.draw.line(screen, (200,200,200),self.TAKO_R,(self.TAKO_R[0]-x,self.TAKO_R[1]+y),width=3)
      else:
        x = math.cos(math.radians(90-self.speed*3)) * self.TAKO_RADIUS
        y = math.sin(math.radians(90-self.speed*3)) * self.TAKO_RADIUS
        pygame.draw.line(screen, (200,200,200),self.TAKO_R,(self.TAKO_R[0]-x,self.TAKO_R[1]+y),width=3)

      #--------
      #ブレーキ
      #--------
      #0~100
      if brakePower > 0.5 or self.speed > 0:
        self.speed = self.speed - brakePower/1000

      if self.speed < 0:
        self.speed = 0
  
      #--------
      #数値表示
      #--------
      if self.speed < 10:
        screen.blit(font.render(str(int(self.speed)), True, (200,200,200)),(self.TAKO_R[0]-5,self.TAKO_R[1]-30))
      elif self.speed < 100:
        screen.blit(font.render(str(int(self.speed)), True, (200,200,200)),(self.TAKO_R[0]-10,self.TAKO_R[1]-30))
      else:
        screen.blit(font.render(str(int(self.speed)), True, (200,200,200)),(self.TAKO_R[0]-15,self.TAKO_R[1]-30))

      #-----------------------
      #走行オブジェクトの描画
      #-----------------------
      #コースの描画
      pygame.draw.circle(screen,(0,255,200),(600,400),80)
      pygame.draw.circle(screen,(0,0,0),(600,400),79)
      pygame.draw.circle(screen,(0,255,200),(800,400),80)
      pygame.draw.circle(screen,(0,0,0),(800,400),79)
      pygame.draw.rect(screen,(0,255,200),(600,320,200,160))
      pygame.draw.rect(screen,(0,0,0),(600,321,200,158))

      #走行オブジェクトの描画
      pygame.draw.circle(screen,(150,150,255),(self.carPosX,self.carPosY),7)

      if  joy.get_axis(0) > 0.03 or joy.get_axis(0) < -0.03 :
        if self.speed > 0:
          self.carAngle = self.carAngle + joy.get_axis(0) * self.speed/10 
      x = math.cos(math.radians(self.carAngle)) 
      y = math.sin(math.radians(self.carAngle)) 

      pygame.draw.line(screen, (150,150,255),(self.carPosX,self.carPosY),(self.carPosX+x*25,self.carPosY+y*25),width=2)

      self.carPosX = self.carPosX + x*self.speed/20
      self.carPosY = self.carPosY + y*self.speed/20

      screen.blit(font.render('joy.get_axis(0) : ' + str(joy.get_axis(0)), True, (200,200,200)),(50,550))
      screen.blit(font.render('self.carPosX : ' + str(self.carPosX), True, (200,200,200)),(50,570))
      screen.blit(font.render('self.carPosY : ' + str(self.carPosY), True, (200,200,200)),(50,590))
      screen.blit(font.render('self.carAngle : ' + str(self.carAngle), True, (200,200,200)),(50,610))

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

