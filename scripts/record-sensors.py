import sqlite3
import random
from Adafruit_BME280 import *
import Adafruit_ADS1x15
import smbus2
import bme280
import time
sensor = BME280(t_mode=4, p_mode=4, h_mode=4)


def addRecord(temp, press, humd, mois):
    """Add a new record to the database"""
    conn = sqlite3.connect("/home/pi/sensors.db")
    cur = conn.cursor()
    
    cur.execute("insert into sensors (temperature, pressure, humidity, moisture) values (?, ?, ?, ?)", (temp, press, humd, mois))
    conn.commit()
    conn.close()    

port=1
address = 0x76
bus = smbus2.SMBus(port)
#bme280.load_calibration_params(bus, address)

#data = bme280.sample(bus, address)    

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()


adc = Adafruit_ADS1x15.ADS1015()

GAIN =1

loops = 10
h=0
while loops>0:
	values=[0]*4
	for i in range(4):
		values[i] = adc.read_adc(i, gain=GAIN)

	h+=values[0]

	time.sleep(0.2)
	loops-=1


print("degrees:{0} \n pressure:{1} \n moisture: {2}".format(degrees, hectopascals, h/10))

addRecord(degrees, hectopascals, humidity, h/10)


