import os
from getpass import getpass
import time

print(
"-----------------------------------------------------------------------------------\n"
"-----------------------------------------------------------------------------------\n"
"-------       EMUNPi: Estacion Meteorologica Universidad del Norte          -------\n"
"-------                                                                     -------\n"
"-------            Creado por: Hector Garcia & Jose Hernandez               -------\n"
"-------                                                                     -------\n"
"-------         Departamento de Ingenieria Electrica & Electronica          -------\n"
"-----------------------------------------------------------------------------------\n"
"-----------------------------------------------------------------------------------\n")

print("WeatherUnderground Configuration: ")
new_WUNID   = raw_input("ID: ")
new_WUNPASS = getpass("Password: ")
new_WUNFREQ = str(int(raw_input("Send freq (min): "))*60)
time.sleep(1)
print ("\033[A                                                                           \033[A")
print ("\033[A                                                                           \033[A")
print ("\033[A                                                                           \033[A")
print ("\033[A                                                                           \033[A")
print("Track-My-Power Configuration: ")
new_TMPUSER = raw_input("User: ")
new_TMPPASS = getpass("Password: ")
print ("\033[A                                                                           \033[A")
print ("\033[A                                                                           \033[A")
print ("\033[A                                                                           \033[A")
print ("\033[A                                                                           \033[A")

with open('config.txt', 'r') as input_file, open('config2.txt', 'w') as output_file:
  lines = input_file.readlines()
  for i in range(0,len(lines)):
  	if (lines[i-1] == '-ID_WUN:\n'):
  		output_file.write(new_WUNID + '\n')
  	elif (lines[i-1] == '-pass_WUN:\n'):
  		output_file.write(new_WUNPASS + '\n')
  	elif (lines[i-1] == '-frec_WUN:\n'):
  		output_file.write(new_WUNFREQ + '\n')
  	elif (lines[i-1] == '-user_TMP:\n'):
  		output_file.write(new_TMPUSER + '\n')
  	elif (lines[i-1] == '-pass_TMP:\n'):
  		output_file.write(new_TMPPASS + '\n')
  	else:
  		output_file.write(lines[i])

os.remove('config.txt')
os.rename('config2.txt','config.txt')