#Capture live stream from website http://www.insecam.org/
import urllib.request
import re
import os
import cv2
import time
import PIL.Image
from apscheduler.schedulers.background import BackgroundScheduler  

#analyze the html of the website and extract the url of movie
print("Recording video...")
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
website = input('please type in the url of the website: ')
req = urllib.request.Request(url=website, headers=headers)
response = urllib.request.urlopen(req)
html = response.read()
imgre = re.compile(r'img id="image0" src="(.*)" class')
html=html.decode('utf-8')#python3
url = imgre.findall(html)[0]
img_root = ''
fps = 1
fourcc = cv2.VideoWriter_fourcc(*'MP42')

#get the size of the picture
req2 = urllib.request.Request(url=url)
response2 = urllib.request.urlopen(req2)
buffer = response2.read()
filename = 'IMAGE.jpg'
with open(filename,'wb') as f:
            f.write(buffer)
im = PIL.Image.open(filename)
videoWriter = cv2.VideoWriter('liveStream.mp4',fourcc,fps,im.size)

#function of read images from url and write into a mp4 file
def extract():
    try:
        req2 = urllib.request.Request(url=url)
        response2 = urllib.request.urlopen(req2)
        buffer = response2.read()
        if not buffer:
            return
        filename = 'IMAGE.jpg'
        with open(filename,'wb') as f:
            f.write(buffer)
            frame = cv2.imread(img_root + filename)
            videoWriter.write(frame)
    except Exception as e:
        print(e)

#apply multiple threads to implement extracting images every 1 second
scheduler = BackgroundScheduler()
scheduler.add_job(extract, 'interval',seconds = 1)

scheduler.start()  
print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))  
  
try:  
    while True:
        time.sleep(2)  
except (KeyboardInterrupt, SystemExit):  
    scheduler.shutdown()
    videoWriter.release()
    os.remove('IMAGE.jpg')
