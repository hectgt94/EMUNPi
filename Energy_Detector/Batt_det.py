import RPi.GPIO as GPIO
import time

def notif(estado, msg, tp):
  titles     = ["System Reboot","Davis Console","WeatherUnderground"]
  messages   = ["Energy restored: Working with Battery","Energy restored: Working with Wall Adapter","USB not detectec","USB connection restored","Problem sending to WUN","Data send to WUN"]
  notif_type = ["INFO","ERROR"]

  notification = [titles[estado], messages[msg], notif_type[tp]]
  
  return notification

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
GPIO.setup(3, GPIO.OUT)

message = "Energia reestablecida"
print(message)

if GPIO.input(27):
  print("CARGADOR")
  notif1 = notif(0,1,0)
  print(notif1)
  ##AQUI SE ENVIA A TMP.TK
else:
  print("BATERIA")
  notif1 = notif(0,0,0)
  print(notif1)
  ##AQUI SE ENVIA A TMP.TK

while True:
  try:
    if GPIO.input(27):
      GPIO.output(3, 0)
    else:
      GPIO.output(3, 1)
    time.sleep(0.01)
  except:
    pass  
