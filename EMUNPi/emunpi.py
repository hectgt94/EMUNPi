#!/usr/bin/env python

import serial
import time
import math
import subprocess
import os
import datetime
import requests
import logging
import RPi.GPIO as GPIO
from collections import OrderedDict
import sys
from bs4 import BeautifulSoup

######################################################
# Envio de notificaciones a Track-mypower.tk

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
# Configuracion del puerto serial USB

def configPrt(device, baud):
  port =serial.Serial(
      device,
      baud,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      writeTimeout = 0,
      timeout = 10,
      rtscts=False,
      dsrdtr=False,
      xonxoff=False
  )
  return port

######################################################
# Extrauer datos de la consola dependiendo del REQUEST hecho

def leerInfo(data_req):
  while True:
    if port.isOpen():
        print("Port opened...")
        port.write(data_req)
        resp=port.read(200)
        break
    else:
        port.open()
  print("Data extracted...")
  return resp

######################################################
#Decodificacion de los datos LOOP extraidos

def decodeMeteo(resp):

  data = OrderedDict()
  raw = resp.encode('hex')
  # Separar datos
  i = raw.index("4c4f4f")                     #indice donde empieza la trama de 100 bytes LOOP2

  bar        = (raw[i+16:i+18] + raw[i+14:i+16])             # Presion Barometrica
  in_temp    = (raw[i+20:i+22] + raw[i+18:i+20])             # Temperatura Interna
  in_hum     = (raw[i+22:i+24])                              # Humedad Interna
  out_temp   = (raw[i+26:i+28] + raw[i+24:i+26])             # Temperatura Externa
  wind_sp    = (raw[i+28:i+30])                              # Velocidad del viento
  wind_dir   = (raw[i+34:i+36] + raw[i+32:i+34])             # Direccion del viento
  wind_gust  = (raw[i+46:i+48] + raw[i+44:i+46])             # Rafagas de viento
  dew_pnt    = (raw[i+62:i+64] + raw[i+60:i+62])             # Punto de rocio
  out_hum    = (raw[i+66:i+68])                              # Humedad Externa
  rain_rate  = (raw[i+84:i+86] + raw[i+82:i+84])             # Tasa de lluvia
  uv         = (raw[i+86:i+88])                              # Indice UV
  solar_rad  = (raw[i+90:i+92] + raw[i+88:i+90])             # Radiacion Solar
  daily_rain = (raw[i+102:i+104] + raw[i+100:i+102])         # Lluvia diaria

  bar        = float.fromhex(bar)/1000
  in_temp    = float.fromhex(in_temp)/10
  in_hum     = float.fromhex(in_hum)
  out_temp   = float.fromhex(out_temp)/10
  wind_sp    = float.fromhex(wind_sp)
  wind_dir   = float.fromhex(wind_dir)
  wind_gust  = float.fromhex(wind_gust)
  dew_pnt    = float.fromhex(dew_pnt)
  out_hum    = float.fromhex(out_hum)
  rain_rate  = float.fromhex(rain_rate)
  uv         = float.fromhex(uv)/10
  solar_rad  = float.fromhex(solar_rad)
  daily_rain = float.fromhex(daily_rain)

  data['bar']        = "%.2f" % bar
  data['in_temp']    = "%.2f" % in_temp
  data['in_hum']     = "%.2f" % in_hum
  data['out_temp']   = "%.2f" % out_temp
  data['wind_sp']    = "%.2f" % wind_sp
  data['wind_dir']   = "%.2f" % wind_dir
  data['wind_gust']  = "%.2f" % wind_gust
  data['dew_pnt']    = "%.2f" % dew_pnt
  data['out_hum']    = "%.2f" % out_hum
  data['rain_rate']  = "%.2f" % rain_rate
  data['uv']         = "%.2f" % uv
  data['solar_rad']  = "%.2f" % solar_rad
  data['daily_rain'] = "%.2f" % daily_rain

  print("Data decoded...")
  return data

######################################################
# Envio de datos a WeatherUnderground

def envioWUN(data,wun_user,wun_pass):
  interval = 10
  requestUrl = 'http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php'
  nowUtc = datetime.datetime.utcnow()
  parameters = {
    'action'         : 'updateraw',
    'ID'             : wun_user,                                 # ID de la estacion en wunderground.com
    'PASSWORD'       : wun_pass,                                 # Contrasena wunderground.com
    'dateutc'        : nowUtc.strftime( '%Y-%m-%d %H:%M:%S' ),   # Estampa de tiempo
    'tempf'          : data['out_temp'],                         # Temperatura externa [F]
    'humidity'       : data['out_hum'],                          # Porcentaje de humedad [0-100%]
    'dewptf'         : data['dew_pnt'],                          # Punto de rocio [F]
    'baromin'        : data['bar'],                              # Presion barometrica [inches]
    'windspeedmph'   : data['wind_sp'],                          # velocidad del viendo [mph]
    'winddir'        : data['wind_dir'],                         # Direccion del viento [0-360]
    'rainin'         : data['rain_rate'],                        # Lluvia en la ultima hora
    'dailyrainin'    : data['daily_rain'],                       # Lluvia en el dia
    'solarradiation' : data['solar_rad'],                        # Radiacion solar
    'UV'             : data['uv'],                               # Radiacion UV
    'windgustmph'    : data['wind_gust']                         # Rafagas de viento
  }
  if interval <= 10:
    parameters['realtime'] = 1
    parameters['rtfreq'] = interval
    requestUrl = 'http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php'

  print "sending to wunderground...",
  u = requests.post(requestUrl, data=parameters)
  response = u.text
  if "success" in response:
    print "success."
  else:
    print "error."
    print 'url:', u.url
    print 'response:', response
  return response

######################################################
#Parpadeo del LED dependiendo del estado

def led_status(estado,stat):
  if (estado == "Envio"):
    GPIO.output(stat, 1)
    time.sleep(1)
    GPIO.output(stat, 0)
  elif (estado == "USBError"):
    GPIO.output(stat, 1)
    time.sleep(0.2)
    GPIO.output(stat, 0)
    time.sleep(0.2)
    GPIO.output(stat, 1)
    time.sleep(0.2)
    GPIO.output(stat, 0)
    time.sleep(0.2)
    GPIO.output(stat, 1)
    time.sleep(0.2)
    GPIO.output(stat, 0)
  elif (estado == "SENDError"):
    GPIO.output(stat, 1)
    time.sleep(0.1)
    GPIO.output(stat, 0)
    time.sleep(0.1)    
    GPIO.output(stat, 1)
    time.sleep(0.1)
    GPIO.output(stat, 0)
    time.sleep(0.4)
    GPIO.output(stat, 1)
    time.sleep(0.1)
    GPIO.output(stat, 0)
    time.sleep(0.1)
    GPIO.output(stat, 1)
    time.sleep(0.1)
    GPIO.output(stat, 0)

######################################################
# Leer datos de configuracion

def config_data():
  f = open("/home/pi/EMUNPi/Config/config.txt","r")
  lines = f.readlines()
  wun_user = lines[15].replace('\n','')
  wun_pass = lines[17].replace('\n','')
  wun_freq = lines[19].replace('\n','')
  wun = [wun_user,wun_pass,wun_freq]
  return wun

######################################################
# Notificacion a Track-My-Power

def notif(title, text, type_):
  titles = ["System Reboot","Davis Console","WeatherUnderground"]
  messages = ["Energy restored: Working with Battery","Energy restored: Working with Wall Adapter","USB not detected","USB connection restored","Problem sending to WUN","Data send to WUN"]
  notif_type = ["info","error","warning"]

  notification = [titles[title], messages[text], notif_type[type_]]

  return notification

######################################################
# Codigo fuente

GPIO.setmode(GPIO.BCM)
stat=10
GPIO.setup(stat, GPIO.OUT)

dev = "/dev/ttyUSB0"
baud = 19200
print("Inicializando programa...")
time.sleep(5)
error_USB = 0
TMP_notf = 0
WUN_notf = 0
while True:
  wun_data = config_data()
  try:
    try:
      port = configPrt(dev, baud)
      if TMP_notf == 1:
        notif2 = notif(1,3,0)
        TMP_notf = 0
        send_notf(notif2[0],notif2[1],notif2[2])
    except:
      error_USB = error_USB + 1
      estado = "USBError"
      led_status(estado,stat)
      if error_USB < 10:
        if dev == "/dev/ttyUSB0":
          dev = "/dev/ttyUSB1"
        else:
          dev = "/dev/ttyUSB0"
      else:
        if TMP_notf == 0:
          notif2 = notif(1,2,1)
          TMP_notf = 1
          send_notf(notif2[0],notif2[1],notif2[2])
          ###########################################
          #Espacio para enviar error a PowerTracking#
          ###########################################
        error_USB = 0
    error_TEST = 0
    while True:
      data_req = "TEST\n"
      resp = leerInfo(data_req)
      if "TEST" in resp:
        error_LOOP = 0
        error_WUN = 0
        while True:
          try:
            subprocess.call("./tiempo.sh")
          except:
            pass
          data_req = "LPS 2 1\n"
          resp = leerInfo(data_req)
          if "LOO" in resp:
            weath_data = decodeMeteo(resp)
            if (float(weath_data['out_temp']) >= 150 or float(weath_data['out_hum']) >= 100 or float(weath_data['solar_rad']) >= 1500 or float(weath_data['uv']) >= 50):
              break
            resWun = envioWUN(weath_data,wun_data[0],wun_data[1])
            if not('success' in resWun):
              error_WUN = error_WUN + 1
              estado = "SENDError"
              led_status(estado,stat)
              if error_WUN >= 10:
                if WUN_notf == 0:
                  notif3 = notif(2,4,1)
                  WUN_notf = 1
                  send_notf(notif3[0],notif3[1],notif3[2])
                  ###########################################
                  #Espacio para enviar error a PowerTracking#
                  ###########################################
                error_WUN = 0
                break
            else:
              if WUN_notf == 1:
                notif3 = notif(2,5,0)
                WUN_notf = 0
                send_notf(notif3[0],notif3[1],notif3[2])
                ###########################################
                #Espacio para enviar error a PowerTracking#
                ###########################################
              estado = "Envio"
              led_status(estado,stat)
              time.sleep(int(wun_data[2]))
          else:
            error_LOOP = error_LOOP + 1
            if error_LOOP == 10:
              error_LOOP = 0
              break
      else:
        error_TEST = error_TEST + 1
        if error_TEST == 3:
          error_TEST = 0
          break
  except:
    pass
