from badge import oled, wlan, connectWifi, btn
from time import sleep_ms
from uikit import selectVList
import urequests

def app_start():
	connectWifi()
	oled.fill(0)
	oled.fill_rect(0,0,128,10,1)
	oled.hctext('SGP Weather',1,0)

	if not wlan.isconnected():
		oled.hctext('No WiFi :(',24,1)
		oled.hctext('Connection',32,1)
		oled.hctext('[B] to Quit',56,1)
		oled.show()
		while(btn.B.value()):
			sleep_ms(100)
		return 1

	oled.hctext('Connecting to',24,1)
	oled.hctext('data.gov.sg',32,1)
	oled.show()
	r1 = urequests.get('https://api.data.gov.sg/v1/environment/24-hour-weather-forecast')
	r2 = urequests.get('https://api.data.gov.sg/v1/environment/2-hour-weather-forecast')
	d1 = r1.json()
	d2 = r2.json()

	forecast = d1['items'][0]['general']['forecast']
	rhumid = d1['items'][0]['general']['relative_humidity']
	temp = d1['items'][0]['general']['temperature']
	wind = d1['items'][0]['general']['wind']
	oled.fill(0)
	oled.fill_rect(0,0,128,10,1)
	oled.hctext('24 Hour Forecast',1,0)
	oled.text(forecast,0,17,1)
	oled.text('RH '+str(rhumid['low'])+'-'+str(rhumid['high'])+' %',0,32,1)
	oled.text('Temp '+str(temp['low'])+'-'+str(temp['high'])+' C',0,40,1)
	oled.text('Wind Dir '+str(wind['direction']),0,48,1)
	oled.text(' @ '+str(wind['speed']['low'])+'-'+str(wind['speed']['high'])+' km/h',0,56,1)
	oled.show()

	while btn.A.value() and btn.B.value(): sleep_ms(100)
	sleep_ms(200)

	forecasts = []
	for area in d2['items'][0]['forecasts']: forecasts.extend([area['area'][:16],area['forecast'][:16],''])
	sid = 0
	while True: 
		sid = selectVList('2 Hour Nowcast',forecasts,sid,1)
		if sid == -1: return 0