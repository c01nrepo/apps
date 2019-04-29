from badge import oled, wlan, connectWifi, btn
from time import sleep_ms
from uikit import selectVList
import urequests

def psidescriptor(psi):
	if psi <= 50: return "Good"
	if psi <= 100: return "Moderate"
	if psi <= 200: return "Unhealthy"
	if psi <= 300: return "Very Unhealthy"
	return "Hazardous"

def app_start():
	connectWifi()
	oled.fill(0)
	oled.fill_rect(0,0,128,10,1)
	oled.hctext('SGP Environment',1,0)

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
	psi = urequests.get('https://api.data.gov.sg/v1/environment/psi')
	psi = psi.json()

	psi_24 = psi['items'][0]['readings']['psi_twenty_four_hourly']
	pm10_24 = psi['items'][0]['readings']['pm10_twenty_four_hourly']
	pm25_24 = psi['items'][0]['readings']['pm25_twenty_four_hourly']
	#psi3 = psi['items'][0]['readings']['psi_three_hourly']


	oled.fill(0)
	oled.fill_rect(0,0,128,10,1)
	oled.hctext('SGP Environment',1,0)
	oled.hctext('24 hour values:',17,1)
	oled.text('PSI   '+str(psi_24['national']),0,32,1)
	oled.hctext('(%s)'%psidescriptor(psi_24['national']),40,1)
	oled.text('PM10  %d ug/m^3'%pm10_24['national'],0,48,1)
	oled.text('PM2.5 %d ug/m^3'%pm25_24['national'],0,56,1)
	#oled.text(' @ '+str(wind['speed']['low'])+'-'+str(wind['speed']['high'])+' km/h',0,56,1)
	oled.show()

	while btn.A.value() and btn.B.value(): sleep_ms(100)
	sleep_ms(200)
	return
	#forecasts = []
	#for area in d2['items'][0]['forecasts']: forecasts.extend([area['area'][:16],area['forecast'][:16],''])
	#sid = 0
	#while True:
	#	sid = selectVList('2 Hour Nowcast',forecasts,sid,1)
	#	if sid == -1: return 0
