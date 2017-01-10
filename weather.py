import pyowm
import sys

owm = pyowm.OWM('8e47cb932d1448c4049c3506aca77f87')
place = sys.argv[1]
observation = owm.weather_at_place(place)
w = observation.get_weather()
complete_temp = w.get_temperature('celsius') 
for i in complete_temp:
	if(i=="temp"):
		print str(complete_temp[i]) + chr(248) + "C"