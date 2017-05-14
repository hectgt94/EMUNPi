import requests
import time

######################################################
# Data Update at Track-mypower.tk

def updatePT(user, password):
  interval = 10
  requestUrl = "http://" + user + ":" + password + "@track-mypower.tk/measurements/meteorological/new/wunderground"
  u = requests.get(requestUrl)
  response = u.text
  return response

while True:
  try:
    user = "admin"
    password = "uninorte"
    res = updatePT(user, password)
    print(res)
    time.sleep(299)
  except:
    pass