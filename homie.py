import speech_recognition as sr 
import os
import pyowm
from lxml import html
import requests
import time
from datetime import datetime
r=sr.Recognizer()

def weather():
	owm = pyowm.OWM('8e47cb932d1448c4049c3506aca77f87')
	while True:
		with sr.Microphone() as source:
			print("say something")
			audio=r.listen(source)

			
		try:
			os.system('./speech.sh ' + "Finding the temperature in " + r.recognize_google(audio)) 
			break
		except sr.UnknownValueError:
			os.system('./speech.sh ' + "Could you please repeat that")
			print("error")


		except sr.RequestError as e:
			print"error"
			os.system('./speech.sh ' + "Could you please repeat that")

	place = r.recognize_google(audio)
	observation = owm.weather_at_place(place)
	w = observation.get_weather()
	complete_temp = w.get_temperature('celsius') 
	for i in complete_temp:
		if(i=="temp"):
			os.system('./speech.sh ' + "The temperature is " + str(complete_temp[i]) + " Degrees celsius ")

def news_for_today():
	response = requests.get('https://news.google.com/news/section?cf=all&pz=1&topic=b&siidp=b458d5455b7379bd8193a061024cd11baa97&ict=ln')
	if (response.status_code == 200):
		pagehtml = html.fromstring(response.text)
		news = pagehtml.xpath('//h2[@class="esc-lead-article-title"] \
		                      /a/span[@class="titletext"]/text()')
		for i in news:
			os.system('./speech.sh ' + i)
		#print("\n \n".join(news))



def current_time():
	d=str(datetime.now().time())
	d=d[:5]
	d=datetime.strptime(d, "%H:%M")
	d=d.strftime("%I:%M %p")
	os.system('./speech.sh ' + d)

def reminder():
	

#news_for_today()
#current_time()



