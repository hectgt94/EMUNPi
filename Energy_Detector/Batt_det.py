import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
GPIO.setup(3, GPIO.OUT)

message = "Energia reestablecida"
print(message)

if GPIO.input(27):
  print("CARGADOR")
  ##AQUI SE ENVIA A TMP.TK
else:
  print("BATERIA")
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
