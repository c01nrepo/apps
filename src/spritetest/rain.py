from badge import oled, btn
from time import sleep_ms
from utils import loadPBM
import framebuf
from random import random, randint

def app_start():
	oled.fill(0)
	sprites = loadPBM('./sprites.pbm')
	oled.blit(sprites,0,0)

	sprites = []
	for i in range(6): # split sprites
		fbuf = framebuf.FrameBuffer(bytearray(32), 16, 16, framebuf.MONO_HLSB)
		for yy in range(16):
			for xx in range(16):
				if oled.pixel(i*16+xx,yy): fbuf.pixel(xx,yy,1)
		sprites.append(fbuf)

	objs = []
	for i in range(randint(5, 15)): objs.append([0,0,65,1]) # sprite,x,y,vy

	while btn.B.value():
		oled.fill(0)
		for o in objs:
			o[2] += o[3]
			if o[2] > 64: # reset obj
				o[0] = randint(0,5)
				o[1] = randint(0,110)
				o[2] = -16
				o[3] = randint(1,10)
			oled.blit(sprites[o[0]], o[1], o[2], 0)
		oled.fill_rect(20,55,90,8,0)
		oled.hctext('[B] to Quit',56,1)
		oled.show()
		sleep_ms(10)