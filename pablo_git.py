#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime
import sys
import os
import random
from subprocess import call
import subprocess 
import pyvona # amazon ivona

print "PAB4PAB rev 6.  GPIO %s %s" %(GPIO.VERSION, GPIO.RPI_REVISION)

salut_num=3
salut=\
{0:"bonjour pablo",\
 1:"salut pablo",\
 2:"sa va bien  pablo",\
 3:"coucou pablo"
}


mpc = [ "mpc play 1","mpc play 3","mpc play 5","mpc play 7", "mpc play 9"]
num_channel = 4   # start from 0
channel = ["station spaciale", "controle de mission", "espace profond", "grouve", "annee soixante disse" ]


pin_ultrason_trigger=23
pin_ultrason_echo=24
pin_halt=12

led_L_R=19
led_L_G=26
led_L_B=13
led_R_R=17
led_R_G=22
led_R_B=27

# in cm
dist_radio_on_high=4.0
dist_animal_low=6.0
dist_animal_high=30.0
dist_radio_off_low=40.0
dist_radio_off_high=70.0  # do not detect ceiling


GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_halt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_ultrason_trigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_ultrason_echo,GPIO.IN)

GPIO.setup(led_L_R, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_L_G, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_L_B, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_R_R, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_R_G, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_R_B, GPIO.OUT, initial=GPIO.LOW)

# amazon TTS ivona voice celine hardcoded in library
voice=pyvona.create_voice('', '')

# espeakl mbrola  voice1 male voice2 female
voice1 = "espeak -v mb/mb-fr1 -q --pho \"%s\"  | mbrola -t 1.7 -f 0.7  -e -C \"n n2\" /usr/share/mbrola/voices/fr3 - -.au | aplay"
voice2 = "espeak -v mb/mb-fr4 -q --pho \"%s\"  | mbrola -t 1.7 -f 0.7  -e -C \"n n2\" /usr/share/mbrola/voices/fr4 - -.au | aplay"

# pico TTS android
def pico(text):
	s="pico2wave -l fr-FR -w /home/pi/ramdisk/a.wav \"" + text +"\""
        print s
        os.system(s)
        os.system("aplay /home/pi/ramdisk/a.wav")

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

test=0
def test_mp3():
	if (test==3):
		call (["mpg123", "-n", "600", "-q", "/home/pi/pablo/mp3/VACHE.mp3"])
		pico("VACHE")
	if (test==1):
		call (["mpg123", "-n", "600", "-q", "/home/pi/pablo/mp3/CHEVAL.mp3"])
		pico("CHEVAL")
	if (test==2):
		call (["mpg123", "-n", "600", "-q", "/home/pi/pablo/mp3/dromadaire.mp3"])
		pico("dromadaire")
	if (test==4):
		pico("CODE CODE CODE")
		pico("Piton")
		
def pablo_mp3(dir):
	list = os.listdir(dir)
	animalmp3= random.choice (list)
	file = dir + animalmp3	
	print file	
	call (["mpg123", "-n", "600", "-q", file])
	animal = animalmp3.split(".")[0]
	print animal
	pico(animal)
	voice.speak(animal)

def rand_led():
	GPIO.output(led_R_R, random.randint(0,1))
	GPIO.output(led_R_G, random.randint(0,1))
	GPIO.output(led_R_B, random.randint(0,1))
	GPIO.output(led_L_R, random.randint(0,1))
	GPIO.output(led_L_G, random.randint(0,1))
	GPIO.output(led_L_B, random.randint(0,1))

def low_led(led):
	GPIO.output(led, GPIO.LOW)

def high_led(led):
	GPIO.output(led, GPIO.HIGH)

def blink_led(led,delay):
	high_led(led)
	time.sleep(delay)
	low_led(led)	

def low_all_led():
	low_led(led_R_R)
	low_led(led_R_G)
	low_led(led_R_B)
	low_led(led_L_R)
	low_led(led_L_G)
	low_led(led_L_B)

def chenillard (delay,cycle):
	for i  in range(cycle):
		low_all_led()
		blink_led(led_R_R,delay)
		blink_led(led_R_G,delay)
		blink_led(led_R_B,delay)
		blink_led(led_L_R,delay)
		blink_led(led_L_G,delay)
		blink_led(led_L_R,delay)

def do_halt(channel):
        GPIO.remove_event_detect(pin_halt)
        print "event detect will halt", channel
	low_all_led()
	high_led(led_R_R)
	high_led(led_L_R)
	pico("au revoir pablo")
	call (["sudo","halt"])

#   ---------------  START ---------------------------------------
os.system("mpc stop")
random.seed()

git="open source"
voice.speak(git)
pico(git)
os.system(voice2 % git)


#ping = subprocess.check_output("ping -c 1 192.168.1.1", shell=True)
ping=os.system("ping -c1 192.168.1.1")
print "ping:   ", ping
if (ping == 0):
	pico("ouifi OK")
else:
	os.system(voice1 % "ouifi PAS OK")

ping=os.system("ping -c1 8.8.8.8")
print "ping:   ", ping
if (ping == 0):
	pico("internette OK")
else:
	os.system(voice2 % "internette PAS OK")

for i in range(20):
	rand_led()
	time.sleep(0.05)

#salutation
pico(salut[random.randint(0,salut_num)])
#call (["/home/pi/pablo/tts/voice1.sh",salut[random.randint(0,6)]])

last_distance=0
mpc_channel=0
GPIO.add_event_detect(pin_halt, GPIO.FALLING, callback=do_halt, bouncetime=1000)

periodic=0  # periodic message 

try:
	while 1:
		periodic +=1
		blink_led(led_L_G,0.03)
		blink_led(led_R_G,0.03)
		current_distance = pulse ()
		print "curent and last distance in cm:  ", current_distance, last_distance

#		if (abs(current_distance - last_distance) > 20):
		if (current_distance < dist_radio_on_high):
			print "MPC" , mpc_channel
			pico("radio internet")
			pico(channel[mpc_channel])
			os.system(mpc[mpc_channel])
			if (mpc_channel == num_channel):
				mpc_channel=0
			else:
				mpc_channel +=1
					
		if ((current_distance > dist_animal_low) and (current_distance < dist_animal_high)):
			chenillard(0.1,2)
			pablo_mp3("/home/pi/pablo/mp3/")
	
		if (current_distance > dist_radio_off_low  and current_distance < dist_radio_off_high):
			os.system("mpc stop")
			mpc_channel=0

		if (periodic==30):
			periodic=0
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
	os.system("mpc stop")
	GPIO.cleanup()

exit(0)



