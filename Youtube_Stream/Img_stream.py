import requests
import time
import get_ip
import json
import subprocess
import shutil
import time

#FILE INFO
PATH = "snapshot.jpg"

#CAM INFO
IPCAM_TOKEN = '8c585b83-17389eb66cbc49c7b243706'
DEVICE_ID = 'FFFFDE8C8D867E29EC642E15FCE34D1D00004492'
url = 'https://use1-wap.tplinkcloud.com/?token=' + IPCAM_TOKEN
data = {"method":"passthrough","params":{"requestData":{"command":"GET_EXTRA_INFO","content":0},"deviceId":DEVICE_ID}}
headers = {'Content-type': 'application/json'}
IP = "0.0.0.0"
attempt = 1

tokenURL = "https://www.tplinkcloud.com/init3.php"
paramstoken = {
    'DATA[account]'  : "mpardo@uninorte.edu.co",
    'DATA[password]' : "I6iIyjcCbSaUC2o%2Bo4ktopFtInNE5DS6VKi05tinApCcuXtqko9VZVUXVJMXpernCtTmBX8xo2TEyuzqyIRuT30t%2Bgrh39D2FbdxKZ%" + "2F38iqzZWXKVDwrJWEQ4pW2Nrr1n9yv2ngMGN9V2auU3SUxvJ8FfVM0SH2ReLZfRq0qwnc%3D",
    'REQUEST'        : "LOGIN"
    }
    
postTOKEN = requests.post(tokenURL,data=paramstoken)

while True:
    try:
        while IP == "0.0.0.0":
            print("Attempt " + str(attempt) + ": Finding IP...")
            IP_RESPONSE = requests.post(url, data=json.dumps(data), headers=headers)
            IP = get_ip.from_camera(IP_RESPONSE.text)
            print(IP_RESPONSE.text)
            time.sleep(10)
            attempt = attempt + 1

        print("Camera's IP found: " + IP)
        PORT = '8080'
        USER = 'admin'
        PASS = 'YWRtaW4xMjM0'
        FILENAME = 'snapshot.jpg'
        IMG_PATH='stream/' + FILENAME
        REQUEST_URL = "http://" + USER + ":" + PASS + "@" + IP + ":" + PORT +"/" + IMG_PATH
        SAVE_URL = 'http://admin:uninorte@track-mypower.tk/stream/new?url='
        
        while True:
            #INITIATE STREAMING
            try:
                try:
                    r = requests.get(REQUEST_URL, stream=True)
                    if r.status_code == 200:
                        with open('snapshot.jpg', 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
		    else:
			IP = "0.0.0.0"
			break
                except:
                    IP = "0.0.0.0"
                    break
                post_img = requests.post('http://uploads.im/api?upload', files= dict(fileupload=open('snapshot.jpg', 'rb')))
                img_response = json.loads(post_img.text)
                img_url = str(img_response["data"]["img_url"]).replace('\\', '')
                r=requests.get(SAVE_URL+img_url)
                print(img_url)
                print("-------------------")
                time.sleep(0.4)
            except:
                print("Se jodio en el 2do try ")
                IP = "0.0.0.0"
                break
    except:
        pass
