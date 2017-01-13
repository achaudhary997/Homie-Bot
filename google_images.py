from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json
import sys

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

query = ' '.join(map(str, sys.argv[1:]))
image_type="file"
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)

ActualImages=[]
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)

for i , (img , Type) in enumerate(ActualImages):
    req = urllib2.Request(img, headers={'User-Agent' : header})
    raw_img = urllib2.urlopen(req).read()
    cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
    if len(Type)==0:
        f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
    else :
        f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')
    f.write(raw_img)
    f.close()