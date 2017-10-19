import requests
import time
import get_ip
import json
import subprocess
import shutil
import os
import datetime
import sys, traceback
import urllib2

#FILE INFO
PORT = '8080'
USER = 'admin'
PASS = 'YWRtaW4xMjM0'
FILENAME = 'snapshot.jpg'
IMG_PATH='stream/' + FILENAME

#CAM INFO
IPCAM_TOKEN = '8c585b83-17389eb66cbc49c7b243706'
DEVICE_ID = 'FFFFDE8C8D867E29EC642E15FCE34D1D00004492'
url = 'https://use1-wap.tplinkcloud.com/?token=' + IPCAM_TOKEN
data = {"method":"passthrough","params":{"requestData":{"command":"GET_EXTRA_INFO","content":0},"deviceId":DEVICE_ID}}
headers = {'Content-type': 'application/json'}
IP = "0.0.0.0"
attempt = 1

#PROCESS ID
pid = os.getpid()
print("Process ID: " + str(pid))

#STREAMING CODE
while True:
    try:
        #Looking for the IP
        while IP == "0.0.0.0":
            print("Attempt " + str(attempt) + ": Finding IP...")
            IP_RESPONSE = requests.post(url, data=json.dumps(data), headers=headers, timeout=1.50)
            IP = get_ip.from_camera(IP_RESPONSE.text)
            print(IP_RESPONSE.text)
            time.sleep(10)
            attempt = attempt + 1
        print("Camera's IP found: " + IP)

        #Assembling request and save url
        REQUEST_URL = "http://" + USER + ":" + PASS + "@" + IP + ":" + PORT +"/" + IMG_PATH
        SAVE_URL = 'http://admin:uninorte@track-mypower.tk/stream/new?url='
        
        #Initiate streaming
        while True:
            try:
                #Getting image from camera
                start = 0
                end = 0
                try:
                    r = urllib2.urlopen(REQUEST_URL)                    
                    if r.getcode() == 200:                        
                        output = open(FILENAME, 'wb')
                        start = time.time()
                        output.write(r.read())
                        end = time.time()
                        output.close()
                        print("Elapsed timeout0: " + str(end-start))
                    else:
                        print ("break 1")
                        traceback.print_exc()
                        print("Elapsed timeout0: " + str(end-start))
                        IP = "0.0.0.0"
                        break
                except:
                    print ("break 2")                    
                    traceback.print_exc()
                    print("Elapsed timeout0: " + str(end-start))
                    IP = "0.0.0.0"
                    break
                #Uploading image to Uploads.im and getting URL
                post_img = requests.post('http://uploads.im/api?upload', files= dict(fileupload=open('snapshot.jpg', 'rb')), timeout=1.50)
                print("Elapsed timeout1: " + str(post_img.elapsed.total_seconds()))
                img_response = json.loads(post_img.text)
                img_url = str(img_response["data"]["img_url"]).replace('\\', '')
                
                #Updating URL in track-mypower.tk stream database
                r = requests.get(SAVE_URL+img_url, timeout=0.80)
                print("Elapsed timeout2: " + str(r.elapsed.total_seconds()))
                print(img_url)
                print("-------------------")
                #time.sleep(0.4)
            except:
                print ("break 3")
                traceback.print_exc()
                IP = "0.0.0.0"
                break
    except:
        print ("pass 1")
        traceback.print_exc()
        pass
