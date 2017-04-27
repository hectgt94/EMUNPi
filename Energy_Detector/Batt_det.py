import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

message = "Energia reestablecida"

while True:
  try:
    if GPIO.input(27):
      print("CARGADOR")
      ##### AQUI SE ENVIA LA NOTIFICACION DE RED A TRACK-MYPOWER.TK
    else:
      print("BATERIA")
      ##### AQUI SE ENVIA LA NOTIFICACION DE BAT A TRACK-MYPOWER.TK
    time.sleep(0.01)
  except:
    pass  
