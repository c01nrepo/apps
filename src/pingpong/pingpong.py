from badge import oled, btn
from time import sleep_ms
from random import getrandbits

ball = [] # x,y,r,vx,vy
playerPaddle = [] # x,y,w,h,vy
enemyPaddle = [] # x,y,w,h,vy
score = [0,0] # player, enemy

def randSpeed(a,p,m):
	return max(m,a*(getrandbits(p)/float(2**p)))*(1 if getrandbits(1) else -1)

def newGame():
	global ball,playerPaddle,enemyPaddle,score
	ball = [64,32,3,randSpeed(1,4,1),randSpeed(2,3,1)] 
	playerPaddle = [125,22,3,20,2] 
	enemyPaddle = [0,22,3,20,1.5]
	oled.hctext('ENEMY PLAYER',25,1)
	oled.hctext('%d   %d'%(score[1],score[0]),35,1)
	oled.hctext('[A] to Play',56,1)
	oled.show()
	while btn.A.value():
		if not btn.B.value(): return -1
		sleep_ms(100)
	drawObjects()
	sleep_ms(500)
	return 0

def drawBall(b):
	oled.fill_rect(int(b[0]-b[2]/2),int(b[1]-b[2]/2),b[2],b[2],1)

def drawPaddle(p):
	oled.fill_rect(p[0],int(p[1]),p[2],p[3],1)

def drawObjects():
	oled.fill(0)
	drawPaddle(playerPaddle)
	drawPaddle(enemyPaddle)
	drawBall(ball)
	oled.show()

def collideBallPaddle(b,p):
	if(b[0] > p[0] and b[0] < p[0]+p[2]):
		if(b[1] > p[1] and b[1] < p[1]+p[3]):
			return 1
	return 0

def app_start():
	oled.fill(0)
	global ball,playerPaddle,enemyPaddle,score
	newGame()
	while btn.B.value():
		if btn.U.value() == 0: playerPaddle[1]-=playerPaddle[4]
		if btn.D.value() == 0: playerPaddle[1]+=playerPaddle[4]

		enemyMiddle = enemyPaddle[1] + enemyPaddle[3]/2
		if abs(ball[1] - enemyMiddle) > 2: enemyPaddle[1] += enemyPaddle[4] * (1 if ball[1] > enemyMiddle else -1)

		ball[0] += ball[3]
		ball[1] += ball[4]
		if ball[0] < 0 or ball[0] > 128:
			score[0 if ball[0] < 0 else 1] += 1
			if newGame() == -1: return 0
		if ball[1] < 0 or ball[1] > 64:
			ball[1] = max(min(ball[1],64),0)
			ball[4] *= -1
		if collideBallPaddle(ball, playerPaddle) or collideBallPaddle(ball, enemyPaddle):
			ball[3] *= -1.1
			ball[4] *= 1.05

		drawObjects()
		sleep_ms(10)
	return 0