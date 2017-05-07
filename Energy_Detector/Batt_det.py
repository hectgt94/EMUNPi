import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
GPIO.setup(3, GPIO.OUT)

message = "Energia reestablecida"

while True:
  GPIO.output(3, 1)

while True:
  try:
    if GPIO.input(27):
      print("CARGADOR")
      GPIO.output(3, 1)
      ##### AQUI SE ENVIA LA NOTIFICACION DE RED A TRACK-MYPOWER.TK
    else:
      print("BATERIA")
      GPIO.output(3, 0)
      ##### AQUI SE ENVIA LA NOTIFICACION DE BAT A TRACK-MYPOWER.TK
    time.sleep(0.01)
  except:
    pass  
