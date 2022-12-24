import pygame,sys
import pygame.locals

pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()

SCREEN_SIZE = (545, 450)

screen = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.Font(None,30)
#サイドブレーキ
isSideBrake = True
isAllowSideBrake = True

#シフトレバー
infoPosX = 150
infoPosY = 300

shiftBasePosX = 130
shiftBasePosY = 300
shiftDistanceX = 150 
shiftDistanceY = 50

beforeInputHat = ""
shiftPosX = shiftBasePosX + shiftDistanceX*2
shiftPosY = shiftBasePosY + shiftDistanceY*2

#エンジン
isStart = False
isAllowStart = True

#ウインカー
beforeLeft = 0
beforeRight = 0
left = 0
right = 0

while True:
  pygame.display.update()
  screen.fill((0,0,0))

  #---------
  #エンジン
  #---------
  if joy.get_button(7) == 1:
    if isAllowStart and isStart == True:
      isStart = False 
    elif isAllowStart:
      isStart = True
    isAllowStart = False
  else:
    isAllowStart = True

  if isStart: dispMessage = "ON"
  else:  dispMessage = "OFF"

  screen.blit(font.render(dispMessage, True, (200,200,200)),[250,20]) 

  #-----------
  #ウインカー
  #-----------
  #LEFT
  pygame.draw.rect(screen,(100,100,100),(50,10,50,30))
  pygame.draw.rect(screen,(0,0,0),(51,11,48,28))
  
  if beforeLeft != joy.get_button(4):
    if joy.get_button(4) == 1:
      if left == 0:
        left = 1
      else:
        left = 0
    beforeLeft = joy.get_button(4) 
  if left == 1:
    pygame.draw.rect(screen,(255,212,0),(51,11,48,28))

  #RIGHT
  pygame.draw.rect(screen,(100,100,100),(450,10,50,30))
  pygame.draw.rect(screen,(0,0,0),(451,11,48,28))
  if beforeRight != joy.get_button(5):
    if joy.get_button(5) == 1:
      if right == 0:
        right = 1
      else:
        right = 0
    beforeRight = joy.get_button(5) 

  if right == 1:
    pygame.draw.rect(screen,(255,212,0),(451,11,48,28))

  #--------
  #ハンドル
  #--------
  x0 = joy.get_axis(0)*95
  y0 = joy.get_axis(1)*95

  pygame.draw.circle(screen,(100,100,100),(225,150),100)
  pygame.draw.circle(screen,(0,0,0),(225,150),99)
  pygame.draw.circle(screen,(0,255,255),(225 + x0 ,150 + y0),10)
 
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
  pygame.draw.rect(screen,(100,100,100),(shiftBasePosX,shiftBasePosY, 300, 100))
  pygame.draw.rect(screen,(0,0,0),(shiftBasePosX+1,shiftBasePosY , shiftDistanceX -2, shiftDistanceY -1))
  pygame.draw.rect(screen,(0,0,0),(shiftBasePosX+shiftDistanceX+1,shiftBasePosY , shiftDistanceX -2, shiftDistanceY -1))
  
  pygame.draw.rect(screen,(0,0,0),(shiftBasePosX+1,shiftBasePosY+shiftDistanceY+1 , shiftDistanceX -2, shiftDistanceY -1))
  pygame.draw.rect(screen,(0,0,0),(shiftBasePosX+shiftDistanceX+1,shiftBasePosY+shiftDistanceY+1 , shiftDistanceX -2, shiftDistanceY -1))

  #-----------------
  #シフトレバー
  #-----------------
  inputHat = joy.get_hat(0)
  if beforeInputHat == "" or inputHat != beforeInputHat:
    if inputHat[0] == -1:
      shiftPosX = shiftPosX - shiftDistanceX
    if inputHat[0] == 1:
      shiftPosX = shiftPosX + shiftDistanceX
    if inputHat[1] == -1:
      shiftPosY = shiftPosY + shiftDistanceY
    if inputHat[1] == 1:
      shiftPosY = shiftPosY - shiftDistanceY
    beforeInputHat = joy.get_hat(0)

  pygame.draw.circle(screen,(200,200,200),(shiftPosX,shiftPosY),10)
  #screen.blit(font.render('inputHat : ' + str(inputHat) , True, (255, 255, 255)), [infoPosX, infoPosY+120]) 

  #-----------------
  #サイドブレーキ
  #-----------------
  pygame.draw.rect(screen,(100,100,100),(50,300,30,100))
  pygame.draw.rect(screen,(0,0,0),(51,301,28,98))

  if joy.get_button(6) == 1:
    if isAllowSideBrake and isSideBrake == False:
      isSideBrake = True
    elif isAllowSideBrake:
      isSideBrake = False
    isAllowSideBrake = False 

  else: 
    isAllowSideBrake = True

  if isSideBrake:
    pygame.draw.rect(screen,(150,100,100),(51,301,28,98))
 
  #キー入力処理
  for event in pygame.event.get():
    if event.type == pygame.locals.KEYDOWN: 
      #終了処理
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()
