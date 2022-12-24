import pygame,sys
import pygame.locals

pygame.init()
joy = pygame.joystick.Joystick(0)      
joy.init()

SCREEN_SIZE = (570, 600)

screen = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.Font(None,30)
infoPosX = 150
infoPosY = 300

shiftBasePosX = 130
shiftBasePosY = 300
shiftDistanceX = 150 
shiftDistanceY = 50

isSideBrake = True
isAllowSideBrake = True
beforeInputHat = ""
shiftPosX = shiftBasePosX + shiftDistanceX
shiftPosY = shiftBasePosY + shiftDistanceY

isStart = True 
isAllowStart = True

while True:
  pygame.display.update()
  screen.fill((0,0,0))


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
  #上から延ばす
  pygame.draw.rect(screen,(0,150,0),(50,50,50,clutchPower))
  #screen.blit(font.render('Cpower : ' + str(clutchPower) , True, (255, 255, 255)), [infoPosX, infoPosY+150]) 

  #-----------------

  pygame.draw.rect(screen,(100,100,100),(450,50,50,200))
  pygame.draw.rect(screen,(0,0,0),(451,51,48,198))

  acceleratorPower = (joy.get_axis(5)+1)*100
  #上から延ばす
  pygame.draw.rect(screen,(0,0,150),(450,50,50,acceleratorPower))
  #screen.blit(font.render('Apower : ' + str(acceleratorPower) , True, (255, 255, 255)), [infoPosX, infoPosY+170]) 

  #-----------------
  #ブレーキメーター
  #-----------------
  pygame.draw.rect(screen,(100,100,100),(350,50,50,100))
  pygame.draw.rect(screen,(0,0,0),(351,51,48,98))

  brakePower = -joy.get_axis(4)*100 # 0 -> -1
  #上から延ばす
  pygame.draw.rect(screen,(150,0,0),(350,50,50,brakePower))
  #screen.blit(font.render('brakepower : ' + str(brakePower) , True, (255, 255, 255)), [infoPosX, infoPosY+190]) 


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
  #screen.blit(font.render('joy.get_button(4) : ' + str(joy.get_button(4)) , True, (255, 255, 255)), [10, 50]) 
  pygame.draw.rect(screen,(100,100,100),(5,150,20,200))
  pygame.draw.rect(screen,(0,0,0),(6,151,18,198))
  #screen.blit(font.render('joy.get_button(4) : ' + str(joy.get_button(4)) , True, (255, 255, 255)), [10, 50]) 

  if joy.get_button(4) == 1:
    if isAllowSideBrake and isSideBrake == False:
      isSideBrake = True
    elif isAllowSideBrake:
      isSideBrake = False
    isAllowSideBrake = False 

  else: 
    isAllowSideBrake = True

  if isSideBrake:
    pygame.draw.rect(screen,(150,100,100),(6,151,18,198))

  #screen.blit(font.render('isAllowSideBrake : ' + str(isAllowSideBrake) , True, (255, 255, 255)), [10, 50]) 
  #screen.blit(font.render('isSideBrake : ' + str(isSideBrake) , True, (255, 255, 255)), [10, 70]) 

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

  if isStart:
    dispMessage = "ON"
  else:
    dispMessage = "OFF"

  screen.blit(font.render(dispMessage, True, (200,200,200)),[150,50]) 

 
  #キー入力処理
  for event in pygame.event.get():
    if event.type == pygame.locals.KEYDOWN: 
      #終了処理
      if event.key == pygame.locals.K_ESCAPE:
        pygame.quit()
        sys.exit()
