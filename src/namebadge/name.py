from badge import oled,btn,readConfig
import framebuf as fb
from time import sleep_ms,ticks_ms
from uikit import inputAlphanumeric,msgBox

def app_start():
	msgBox('Name Badge',['','[B] will launch','a keyboard to','enter name','','[\n] to Submit'])
	name = ' %s '%inputAlphanumeric()
	_W = len(name)*8
	_H = 8
	fbuf = fb.FrameBuffer(bytearray(_W*_H//8),_W,_H,fb.MONO_HLSB)
	fbuf.text(name,0,0,1)
	ix = 0
	while btn.B.value():
		oled.fill(0)
		for x in range(16):
			for y in range(8):
				if fbuf.pixel((x+ix)%_W,y): oled.fill_rect(x*8,y*8,8,8,1)
		oled.show()
		ix+=1
		sleep_ms(50)