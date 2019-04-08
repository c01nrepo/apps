from badge import oled, btn
from machine import Pin
from time import sleep_ms, ticks_ms
import framebuf as fb
import urequests
from ubinascii import hexlify

def app_start():
	px = 64
	py = 32
	oled.fill(0)
	oled.show()
	fbuf = fb.FrameBuffer(bytearray(1024),128,64,fb.MONO_HLSB)
	sleep_ms(200)
	while True:
		oled.blit(fbuf,0,0)
		if(btn.A.value() == 0):
			fbuf.fill_rect(px,py,3,3,1)
		else:
			oled.fill_rect(px,py,3,3,int(ticks_ms()/100)%2)
		if(btn.B.value() == 0): 
			#urequests.get('http://ragulbalaji.com:3073/c01nsketch?g=%s'%hexlify(oled.buffer))
			return 0
		if(btn.U.value() == 0): py=(py-1)%64
		if(btn.D.value() == 0): py=(py+1)%64
		if(btn.L.value() == 0): px=(px-1)%128
		if(btn.R.value() == 0): px=(px+1)%128
		oled.show()