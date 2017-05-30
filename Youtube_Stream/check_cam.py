from datetime import datetime
import os

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
  try:
    os.kill(pid, 0)
  except OSError:
    return False
  else:
    return True

while True:
	try:
		with open("log_Img.txt",'r') as file:
			lines = file.readlines()
			pid   = (lines[0]) 
			time  = datetime.strptime(lines[1], '%Y-%m-%d %H:%M:%S')

		now = datetime.now()
		delta_t = now - time
		tot_min = delta_t.total_seconds()/60
		check = check_pid(pid)

		if (tot_min > 5) and (check == True):
			os.system("sudo kill " + pid)
			os.system("sudo python /home/pi/EMUNPi/Youtube_Stream/Img_stream.py &")
	except:
		pass