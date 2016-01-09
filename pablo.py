#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime
import sys
import os
import random
from subprocess import call
import subprocess 


print "PAB4PAB rev 5.  GPIO %s %s" %(GPIO.VERSION, GPIO.RPI_REVISION)


salut=\
{0:"bonjour pablo",\
 1:"salut pablo",\
 2:"saa va pablo",\
 3:"elo pablo",\
 4:"coucou pablo",\
 5:"yo pablo", \
 6:"bisou pablo"
}

mpc = [ "mpc play 1","mpc play 2","mpc play 3","mpc play 4","mpc stop" ]


pin_ultrason_trigger=11
pin_ultrason_echo=8
pin_halt=23

pin_R_1=18
pin_G_1=17
pin_B_1=22

pin_R_2=26
pin_G_2=13
pin_B_2=5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_halt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_ultrason_trigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_ultrason_echo,GPIO.IN)

GPIO.setup(pin_R_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_R_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_B_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_B_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_G_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_G_2, GPIO.OUT, initial=GPIO.LOW)

voice1 = "espeak -v mb/mb-fr1 -q --pho \"%s\"  | mbrola -t 1.7 -f 0.7  -e -C \"n n2\" /usr/share/mbrola/voices/fr3 - -.au | aplay"
voice2 = "espeak -v mb/mb-fr4 -q --pho \"%s\"  | mbrola -t 1.7 -f 0.7  -e -C \"n n2\" /usr/share/mbrola/voices/fr4 - -.au | aplay"

def pulse():
	GPIO.output(pin_ultrason_trigger, False)
	time.sleep(0.5)
	# Send 10us pulse to trigger
	GPIO.output(pin_ultrason_trigger, True)
	time.sleep(0.00001)
	GPIO.output(pin_ultrason_trigger, False)
	start = time.time()
	while GPIO.input(pin_ultrason_echo)==0:
	  	start = time.time()

	while GPIO.input(pin_ultrason_echo)==1:
  		stop = time.time()
	elapsed = stop-start
	#330m/sec
	distance = elapsed * 330*100 / 2
	#in cm
	return(distance)

def pablo_mp3(dir):
	list = os.listdir(dir)
	animalmp3= random.choice (list)
	file = dir + animalmp3	
	print file	
	call (["mpg123", "-n", "600", "-q", file])
	animal = animalmp3.split(".")[0]
	print animal
#	os.system(voice2 % animal )
#use pico
	s="pico2wave -l fr-FR -w /home/pi/ramdisk/a.wav \"" + animal +"\""
	print s
	os.system(s)
	os.system("aplay /home/pi/ramdisk/a.wav")

def rand_led():
	GPIO.output(pin_R_1, random.randint(0,1))
	GPIO.output(pin_R_2, random.randint(0,1))
	GPIO.output(pin_G_1, random.randint(0,1))
	GPIO.output(pin_G_2, random.randint(0,1))
	GPIO.output(pin_B_1, random.randint(0,1))
	GPIO.output(pin_B_2, random.randint(0,1))

def blink_led(led,delay):
	GPIO.output(led, GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(led, GPIO.LOW)
	
def low_led(led):
	GPIO.output(led, GPIO.LOW)

def low_all_led():
	low_led(pin_R_1)
	low_led(pin_R_2)
	low_led(pin_G_1)
	low_led(pin_G_2)
	low_led(pin_B_1)
	low_led(pin_B_2)

def chenillard (delay,cycle):
	for i  in range(cycle):
		low_all_led()
		GPIO.output(pin_R_1, GPIO.HIGH)
		time.sleep(delay)
		low_led(pin_R_1)
		GPIO.output(pin_R_2, GPIO.HIGH)
		time.sleep(delay)
		low_led(pin_R_2)

		GPIO.output(pin_G_1, GPIO.HIGH)
		time.sleep(delay)
		low_led(pin_G_1)
		GPIO.output(pin_G_2, GPIO.HIGH)
		time.sleep(delay)
		low_led(pin_G_2)

		GPIO.output(pin_B_1, GPIO.HIGH)
		time.sleep(delay)
		low_led(pin_B_1)
		GPIO.output(pin_B_2, GPIO.HIGH)
		time.sleep(delay)
		low_led(pin_B_2)

def do_halt(channel):
        GPIO.remove_event_detect(pin_halt)
        print "event detect will halt", channel
	low_all_led()
	GPIO.output(pin_R_2, GPIO.HIGH)
	GPIO.output(pin_R_1, GPIO.HIGH)
	s="pico2wave -l fr-FR -w /home/pi/ramdisk/a.wav \"au revoir pablo\" "
	print s
	os.system(s) 
	os.system("aplay /home/pi/ramdisk/a.wav")
#	os.system(voice2 % "au revoir pablo")
	call (["sudo","halt"])


#   ---------------  START ---------------------------------------


os.system(mpc[4])

random.seed()

#ping = subprocess.check_output("ping -c 1 192.168.1.1", shell=True)
ping=os.system("ping -c1 192.168.1.1")
print "ping:   ", ping
if (ping == 0):
	os.system(voice1 % "ouifi OK")
else:
	os.system(voice1 % "ouifi PAS OK")

ping=os.system("ping -c1 8.8.8.8")
print "ping:   ", ping
if (ping == 0):
	os.system(voice2 % "internet OK")
else:
	os.system(voice2 % "internet PAS OK")

for i in range(20):
	rand_led()
	time.sleep(0.05)

#epeak mbrola
#call (["/home/pi/pablo/tts/voice1.sh",salut[random.randint(0,6)]])

s="pico2wave -l fr-FR -w /home/pi/ramdisk/a.wav \"" + salut[random.randint(0,6)]+"\""
print s
os.system(s)
os.system("aplay /home/pi/ramdisk/a.wav")


#if (random.randint(0,1) == 0):
#	os.system(voice1 % salut[random.randint(0,6)])
#else:
#	os.system(voice2 % salut[random.randint(0,6)])

last_distance=0
cycle_count=0
mpc_channel=0

GPIO.add_event_detect(pin_halt, GPIO.FALLING, callback=do_halt, bouncetime=1000)

try:
	while 1:
		cycle_count=cycle_count+1
		blink_led(pin_G_1,0.03)
		blink_led(pin_G_2,0.03)
		current_distance = pulse ()
		print "curent and last distance cm:  ", current_distance, last_distance

#		if (abs(current_distance - last_distance) > 20):
		if (current_distance < 5):

			print "MPC" , mpc_channel
			os.system(mpc[mpc_channel])
			if (mpc_channel == 4):
				mpc_channel=0
			else:
				mpc_channel = mpc_channel+1
					
		if (current_distance > 10 and current_distance < 30):
			chenillard(0.1,2)
			pablo_mp3("/home/pi/pablo/mp3/")
		
		if (current_distance > 30 and current_distance < 50):
			os.system(mpc[4])
			mpc_channel=0

		if (cycle_count==30):
			cycle_count=0
			if (mpc_channel==0):
				if (random.randint(0,1) == 0):
					os.system(voice1 % "on continue")

				else:
					os.system(voice2 % "encore")

		last_distance=current_distance
		low_all_led()
		time.sleep(1)

except KeyboardInterrupt:
	print "/nPablo Cleanup"
	os.system(mpc[4])
	GPIO.cleanup()

exit(0)




