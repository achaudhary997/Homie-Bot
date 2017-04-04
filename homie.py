import speech_recognition as sr 
import os
import pyowm
from lxml import html
import requests
import time
from datetime import datetime

#settings
mic_name = "USB Device 0x46d:0x825: Audio (hw:1,0)"
sample_rate = 48000
chunk_size = 2048

r=sr.Recognizer()
r.energy_threshold = 50
mic_list = sr.Microphone.list_microphone_names()

for i,microphone_name in enumerate(mic_list):
	if microphone_name == mic_name:
		device_id=i

def input_speech():
	while True:
		print "trying to listen"
		with sr.Microphone(device_index=device_id, sample_rate = sample_rate, chunk_size=chunk_size) as source:
			print "okay say something"
			audio=r.listen(source)
			print "sup"
		try:
			text=r.recognize_google(audio)
			print text
			break
		except:
			os.system('./speech.sh ' + "could you please repeat that? I did not quite understand you.")

	#text = r.recognize_google(audio)
	return text

def weather():
	owm = pyowm.OWM('8e47cb932d1448c4049c3506aca77f87')
	os.system("./speech.sh " + "Which place?")
	place = input_speech()
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



def current_time():
	d=str(datetime.now().time())
	d=d[:5]
	d=datetime.strptime(d, "%H:%M")
	d=d.strftime("%I:%M %p")
	os.system('./speech.sh ' + d)

def determine(ans):
	option1a="news"
	option1b="News"
	option2a="Weather"
	option2b="weather"
	option3a="time"
	option3b="Time"
	if option1a in ans or option1b in ans:
		news_for_today()
	elif option2a in ans or option2b in ans:
		weather()
	elif option3a in ans or option3b in ans:
		current_time()

#news_for_today()
#current_time()

if __name__ == "__main__":
	os.system("./speech.sh " + "Hey there! Whats up? ")
	print "hello"
	ans = input_speech()
	print ans
	determine(ans)


