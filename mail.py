#test
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from encrypt import *

browser = webdriver.Firefox()
browser.get('https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier')

username = browser.find_element_by_id("Email")
username.send_keys("scrypting101@gmail.com")
browser.find_element_by_id("next").click()

time.sleep(1)

password = browser.find_element_by_id("Passwd")
password.send_keys(decrpyt("Homie_bot","1UZVUTKUg.! \x1d\x1a"))
browser.find_element_by_id("signIn").click()

time.sleep(4)

browser.find_element_by_xpath("//div[@role='button' and @class='T-I J-J5-Ji T-I-KE L3']").click()

time.sleep(1)

email_address = browser.find_element_by_xpath("//textarea[@rows='1']")	
email_address.send_keys("yashit16123@iiitd.ac.in")

email_subject = browser.find_element_by_xpath("//input[@name='subjectbox']")	
email_subject.send_keys("Location of your Object")

email_body = browser.find_element_by_xpath("//div[@class='Am Al editable LW-avf' and @hidefocus='true']")	
email_body.send_keys("This is a test mail.")

browser.find_element_by_xpath("//div[@class='T-I J-J5-Ji aoO T-I-atl L3']").click()	

#http://askubuntu.com/questions/11925/a-command-line-clipboard-copy-and-paste-utility
