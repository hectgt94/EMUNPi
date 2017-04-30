import RPi.GPIO as GPIO
import time

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

GPIO.setmode(GPIO.BCM)
stat=10
GPIO.setup(10,GPIO.OUT)
while True:
  led_status("USBError", 10)
