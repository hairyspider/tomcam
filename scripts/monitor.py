import sqlite3
import random
import json
import threading
import RPi.GPIO as GPIO
import time
import os.path


class EventType:
	FAN = 1
	WATER = 2
	SETTINGS = 3

class Status:
	Fan = False
	Water = False
	last_settings_file_time = 0
	temp_thresh = 35
	fan_duration = 5

	soil_thresh = 0.5
	water_duration = 5
	
OPT_FILE = "/opt/irrigation/settings.conf"
	

def LoadSettings():
	cur_mod = os.path.getmtime(OPT_FILE)
	if cur_mod!=Status.last_settings_file_time:
		Status.last_settings_file_time = cur_mod
		
		AddEvent("Reloading settings", EventType.SETTINGS)
		
		with open(OPT_FILE) as f:
			o = json.load(f)
			Status.temp_thresh = int(o["temp"])
			Status.fan_duration = int(o["fan"])
			Status.soil_thresh = int(o["moist"])
			Status.water_duration = int(o["water"])
		
		
		AddEvent("Settings: temp:{0}, fan:{1}, soil:{2}, water:{3}".format(
					Status.temp_thresh, Status.fan_duration, 
					Status.soil_thresh, Status.water_duration), EventType.SETTINGS)

def AddEvent(description, type):
	conn = sqlite3.connect("/home/pi/sensors.db")
	cur = conn.cursor()
	cur.execute("insert into events (typeid, description) values (?,?)", (type, description))
	conn.commit()
	conn.close()


def GetSensorVals():
	conn = sqlite3.connect("/home/pi/sensors.db")
	cur = conn.cursor()
	sql = "select temperature, pressure, humidity, moisture from sensors order by time desc limit 1;"
	cur.execute(sql)
	rows = cur.fetchall()
	conn.close()
	print(rows[0])

	if rows:
		t = rows[0][0] #temperature
		h = rows[0][3] #moisture
		return (t, h)
	else:
		return 0


def StartFan():
	pin=22

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(pin, GPIO.OUT)
	
	AddEvent("Fan to go on for {0} minutes.".format(Status.fan_duration), EventType.FAN)
	
	GPIO.output(pin, 0)
	time.sleep(Status.fan_duration * 60)
	
	GPIO.output(pin, 1)		
	Status.Fan = False
	
	AddEvent("Fan is now off", EventType.FAN)
		
		
def StartWater():
	pin = 27

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	GPIO.setup(pin, GPIO.OUT)
	
	AddEvent("Water to go on for {0} minutes.".format(Status.water_duration), EventType.WATER)
	
	GPIO.output(pin, 0)
	time.sleep(Status.water_duration * 60)
	
	GPIO.output(pin, 1)		
	Status.Water = False
	
	AddEvent("Water is now off", EventType.WATER)		

	
while True:
	LoadSettings()
	
	vals = GetSensorVals()

	print(vals)

	if vals[0] > Status.temp_thresh:
		if not Status.Fan:
			print("Fan is about to start")
			Status.Fan = True
			AddEvent("Temperature too high, starting fan", EventType.FAN)
			t=threading.Thread(target=StartFan, args = ())
			t.start()
		else:
			print("Fan is currently running")
			
	else:
		print("Temperature is fine")

		
	if vals[1] > Status.soil_thresh:
		if not Status.Water:
			print("Water is about to start")
			Status.Water = True
			AddEvent("Moisture is too low, starting water", EventType.WATER)
			t=threading.Thread(target=StartWater, args = ())
			t.start()
		else:
			print("Water is currently running")
	else:
		print("Moisture is fine")
	
	print("Currently {0} threads running".format(threading.active_count()))
	
	print("sleeping for 10 minutes")
	time.sleep(600)
