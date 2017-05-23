import RPi.GPIO as GPIO
import time
import sys
import requests
from bs4 import BeautifulSoup
import socket
import fcntl
import struct

######################################################
# Get IP address

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


######################################################
# Notification set to Track-My-Power

def notif(title, text, type_):
  IP = get_ip_address('wlan0')
  print(IP)
  titles     = ["System Reboot","Davis Console","WeatherUnderground"]
  messages   = ["Energy restored: Working with Battery, IP: " + IP,"Energy restored: Working with Wall Adapter IP: " + IP,"USB not detectec","USB connection restored","Problem sending to WUN","Data send to WUN"]
  notif_type = ["info","error","warning"]

  notification = [titles[title], messages[text], notif_type[type_]]
  
  return notification

######################################################
# Notification send to Track-mypower.tk

def send_notf(title,text,type_):
  URL = 'http://track-mypower.tk/login'
  NOTF_URL = 'http://admin:uninorte@track-mypower.tk/source/RaspberryPi/notifications/new'

  log_data = {
    'session[email]'    : 'raspberrypi',
    'session[password]' : 'raspberrypi1234',
    'authenticity_token': ' '
  }

  notf_data = {
    'type'  : type_,
    'title' : title,
    'text'  : text
  }

  with requests.Session() as s:
    log    = s.get(URL)
    cookie = s.cookies
    soup   = BeautifulSoup(log.content)
    token  = soup.select('meta[name="csrf-token"]')[0]['content']
    log_data['authenticity_token'] = token
    log1   = s.post(URL, cookies=cookie, data=log_data)
    notf   = s.get(NOTF_URL, params=notf_data)

######################################################
# Main code

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
GPIO.setup(3, GPIO.OUT)


if GPIO.input(14):
  notif1 = notif(0,1,0)
  send_notf(notif1[0],notif1[1],notif1[2])
  ##AQUI SE ENVIA A TMP.TK
else:
  notif1 = notif(0,0,2)
  send_notf(notif1[0],notif1[1],notif1[2])
  ##AQUI SE ENVIA A TMP.TK

while True:
  try:
    if GPIO.input(14):
      GPIO.output(3, 0)
    else:
      GPIO.output(3, 1)
    time.sleep(0.01)
  except:
    pass  
