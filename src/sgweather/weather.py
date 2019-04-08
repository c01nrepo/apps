from badge import oled, wlan, connectWifi, btn
from time import sleep_ms
import urequests

def app_start():
	connectWifi()
	oled.fill(0)
	oled.fill_rect(0,0,128,7,1)
	oled.text('SGP Weather',0,0,0)
	
	if not wlan.isconnected():
		oled.hctext('No WiFi :(',16,1)
		oled.hctext('Connection',24,1)
		oled.show()
		while(btn.B.value()):
			sleep_ms(100)
		return 1
	
	oled.fill_rect(0,8,128,56,0)
	oled.text('Connecting to',0,16,1)
	oled.text('data.gov.sg',0,24,1)
	oled.show()

	r1 = urequests.get('https://api.data.gov.sg/v1/environment/24-hour-weather-forecast')
	d1 = r1.json()
	forecast = d1['items'][0]['general']['forecast']
	rhumid = d1['items'][0]['general']['relative_humidity']
	temp = d1['items'][0]['general']['temperature']
	wind = d1['items'][0]['general']['wind']

	oled.fill_rect(0,8,128,56,0)
	oled.text(forecast,0,8,1)
	oled.text('RH '+str(rhumid['low'])+'-'+str(rhumid['high'])+' %',0,24,1)
	oled.text('Temp '+str(temp['low'])+'-'+str(temp['high'])+' C',0,32,1)
	oled.text('Wind Dir '+str(wind['direction']),0,40,1)
	oled.text(' @ '+str(wind['speed']['low'])+'-'+str(wind['speed']['high'])+' km/h',0,48,1)
	oled.show()

	#TODO https://api.data.gov.sg/v1/environment/2-hour-weather-forecast

	while(btn.B.value()):
		sleep_ms(100)