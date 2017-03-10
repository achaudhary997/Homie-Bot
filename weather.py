import pyowm
import sys
import speech_recognition as sr
import pyttsx

owm = pyowm.OWM('8e47cb932d1448c4049c3506aca77f87')

flag = 0
r = sr.Recognizer()
while True:
	with sr.Microphone() as source:
		
		if(flag == 0):
			engine = pyttsx.init()
			engine.say('What place do you want to know the temperature of?')
			engine.runAndWait()
		audio = r.listen(source)
	#query = ' '.join(map(str, sys.argv[1:]))
	try:
		place = r.recognize_google(audio)
		engine = pyttsx.init()
		engine.say("Finding the temperature of ")
		engine.say(place)
		engine.say(" for you.")
		engine.runAndWait()
		break
	except sr.UnknownValueError:
		engine = pyttsx.init()
		engine.say('Sorry, could you please repeat')
		flag = 1
		engine.runAndWait()
	except sr.RequestError as e:
		engine = pyttsx.init()
		engine.say('Sorry, could you please repeat')
		flag = 1
		engine.runAndWait()

#print place
#place = ' '.join(map(str, sys.argv[1:]))
observation = owm.weather_at_place(place)
w = observation.get_weather()
complete_temp = w.get_temperature('celsius') 
for i in complete_temp:
	if(i=="temp"):
		engine = pyttsx.init()
		engine.say("The temperature is ")
		engine.say(str(complete_temp[i]))
		engine.say(" degree Celcius")
		engine.runAndWait()
		#print str(complete_temp[i]) + chr(248) + "C"