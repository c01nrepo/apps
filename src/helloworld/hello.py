from badge import oled, btn
from time import sleep_ms

def app_start():
	oled.fill(0)
	oled.text('Hello',0,0,1)
	oled.text('World',0,8,1)
	oled.show()
	for y in range(2*8,-1,-1):
		oled.invert(y%2)
		for x in range(5*8,-1,-1):
			oled.fill_rect(x*3,y*3,3,3,oled.pixel(x,y))
			oled.show()
	oled.hctext('[B] to Quit',56,1)
	oled.show()
	while btn.B.value(): sleep_ms(20)

app_start()