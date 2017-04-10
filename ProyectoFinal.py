#!/usr/bin/env python

import serial
import time
import math
import subprocess
import os
import datetime
import requests
import logging
from collections import OrderedDict
######################################################
#Configuracion del logfile

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('emunpi_error.log')
file_handler.setFormatter(formatter)

file_handler2 = logging.FileHandler('emunpi_total.log')
file_handler2.setFormatter(formatter)

logger.addHandler(file_handler)
logger2.addHandler(file_handler2)

######################################################

def configPrt(device, baud):
  # Configuracion del puerto
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

def leerInfo(data_req):
  # Solicitar datos usando LOOP2
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

######################################################

def decodeMeteo(resp):

  data = OrderedDict()
  raw = resp.encode('hex')
  # Separar datos
  i = raw.index("4c4f4f")                     #indice donde empieza la trama de 100 bytes LOOP2

  bar        = (raw[i+16:i+18] + raw[i+14:i+16])             #Presion Barometrica
  in_temp    = (raw[i+20:i+22] + raw[i+18:i+20])
  in_hum     = (raw[i+22:i+24])
  out_temp   = (raw[i+26:i+28] + raw[i+24:i+26])
  wind_sp    = (raw[i+28:i+30])
  wind_dir   = (raw[i+34:i+36] + raw[i+32:i+34])
  wind_gust  = (raw[i+46:i+48] + raw[i+44:i+46])
  dew_pnt    = (raw[i+62:i+64] + raw[i+60:i+62])
  out_hum    = (raw[i+66:i+68])
  rain_rate  = (raw[i+84:i+86] + raw[i+82:i+84])
  uv         = (raw[i+86:i+88])
  solar_rad  = (raw[i+90:i+92] + raw[i+88:i+90])
  daily_rain = (raw[i+102:i+104] + raw[i+100:i+102])

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

#  print(bar)
#  print(in_temp)
#  print(in_hum)
#  print(out_temp)
#  print(wind_sp)
#  print(wind_dir)
#  print(wind_gust)
#  print(dew_pnt)
#  print(out_hum)
#  print(rain_rate)
#  print(uv)
#  print(solar_rad)
#  print(daily_rain)
  print("Data decoded...")
  return data

######################################################

def envioWUN(data):
  interval = 10
  requestUrl = 'http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php'
  nowUtc = datetime.datetime.utcnow()
  parameters = {
    'action'         : 'updateraw',
    'ID'             : 'IATLNTIC4',                              # ID de la estacion en wunderground.com
    'PASSWORD'       : 'mauro97',                                # Contrasena wunderground.com
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
    'windgustmph'    : data['wind_gust']                         # 
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

dev = "/dev/ttyUSB0"
baud = 19200
print("Inicializando programa...")
time.sleep(5)
while True:
  error_USB = 0
  try:
    try:
      logger2.info('Conexion')
      port = configPrt(dev, baud)
    except:
      error_USB = error_USB + 1
      if error_USB < 100
        logger.info('Intentar cambio de puerto USB')
        if dev == "/dev/ttyUSB0":
          dev = "/dev/ttyUSB1"
        else:
          dev = "/dev/ttyUSB0"
      else:
        logger.error('USB no conectado')
        error_USB = 0
    error_TEST = 0
    while True:
      logger2.info('TEST')
      data_req = "TEST\n"
      resp = leerInfo(data_req)
      if "TEST" in resp:
        error_LOOP = 0
        error_WUN = 0
        while True:
          try:
            subprocess.call("./tiempo.sh")
          except:
            logger.error("Error al setear fecha y hora")
          logger2.info('LOOP')
          data_req = "LPS 2 1\n"
          resp = leerInfo(data_req)
          if "LOO" in resp:
            weath_data = decodeMeteo(resp)
            logger2.info('WUN')
            resWun = envioWUN(weath_data)
            if not('success' in resWun):
              logger.debug('Envio incorrecto a WUN')
              error_WUN = error_WUN + 1
              if error_WUN == 10:
                logger.error('No se esta enviando correctamente a WUN')
                break
          else:
            error_LOOP = error_LOOP + 1
            logger.debug('Recepcion incorrecta de la informacion')
            if error_LOOP == 100:
              logger.warning('No se esta recibiendo correctamente la informacion')
              break
      else:
        error_TEST = error_TEST + 1
        if error_count == 3:
          logger.warning('No se pudo probar la conexion')
          break
  except:
    pass

