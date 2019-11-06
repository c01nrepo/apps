from badge import oled,btn
from time import sleep_ms
from random import randint, random
import math

def app_start():
	g = 0.1
	jerk = 0.3
	ball = [64,-10,1,0,7] #x,y,vx,vy,r
	while btn.B.value():
		if not btn.A.value():
			ball[0] = randint(ball[4], 128-ball[4])
			ball[1] = randint(ball[4], 63-ball[4])
			ball[2] = 3*(random()-0.5)
			ball[3] = 3*(random()-0.5)
			sleep_ms(250)
		oled.fill(0)
		if ball[1] > 60-ball[4] and ball[2]**2 + ball[3]**2 < 0.1: oled.hctext("Press [A]",30,1)
		oled.fill_circle(round(ball[0]),round(ball[1]),ball[4],1)
		oled.show()
		if not btn.U.value(): ball[3] -= jerk
		if not btn.D.value(): ball[3] += jerk
		if not btn.L.value(): ball[2] -= jerk
		if not btn.R.value(): ball[2] += jerk
		ball[3] += g
		ball[0] += ball[2]
		ball[1] += ball[3]
		ball[2] *= 0.999
		ball[3] *= 0.999
		if ball[1] > 63-ball[4]:
			ball[3] *= -0.9
			ball[1] = 64-ball[4]
		if ball[0] > 128-ball[4]:
			ball[2] *= -0.9
			ball[0] = 127-ball[4]
		if ball[0] < ball[4]:
			ball[2] *= -0.9
			ball[0] = ball[4]