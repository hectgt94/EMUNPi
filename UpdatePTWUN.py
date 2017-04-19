import requests
import time

def updatePT(user, password):
  interval = 10
  requestUrl = "http://" + user + ":" + password + "@track-mypower.tk/measurements/meteorological/new/wunderground"
  #requestUrl = 'http://admin:admin1234@track-mypower.tk/measurements/meteorological/new/wunderground'
  u = requests.get(requestUrl)
  response = u.text
  print(requestUrl)
  return response

try: 
  while True:
    user = "admin"
    password = "admin1234"
    res = updatePT(user, password)
    print(res)
    time.sleep(60)
except:
  pass