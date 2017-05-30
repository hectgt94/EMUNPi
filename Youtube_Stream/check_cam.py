from datetime import datetime
import os

while True:
	try:
		with open("log_Img.txt",'r') as file:
			lines = file.readlines()
			pid   = (lines[0]) 
			time  = datetime.strptime(lines[1], '%Y-%m-%d %H:%M:%S')

		now = datetime.now()
		delta_t = now - time
		tot_min = delta_t.total_seconds()/60

		if tot_min > 1:
			os.system("sudo kill " + pid)
			os.system("python /home/pi/EMUNPi/Youtube_Stream/Img_stream.py &")
	except:
		pass