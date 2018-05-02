#!/usr/bin/env python3
# File : sparkRun.py
# Desc : Python script to remote control a Onion Omega II IoT device using a Cisco WebEx Spark room
# Author : Joe McManus josephmc@alumni.cmu.edu 
# version :  1.0 2018.05.01
#
# Copyright (C) 2018 Joe McManus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import subprocess
from ciscosparkapi import CiscoSparkAPI

import configparser
import time
import argparse
from datetime import datetime
from os import path

parser = argparse.ArgumentParser(description='A program to receive messages from Cisco Spark on Omega')
parser.add_argument('--pid', help="Create a pid file in /var/run/sparkRun.pid",  action="store_true")
parser.add_argument('--delay', help="Number of seconds to wait between readings, default 30", default=30, type=int, action="store")
parser.add_argument('--log', help="Create a log file in /tmp/sparkRun.log",  action="store_true")
parser.add_argument('--config', help="Specify an alternate location of the config file, default ./spark.cfg", default='spark.cfg',  action="store")

args=parser.parse_args()

if args.pid:
	from os import getpid
	print("Creating PID file.")
	fh=open("/var/run/sparkRun.pid", "w")
	fh.write(str(getpid()))
	fh.close()

if args.log:
	import logging
	logFile=args.log
	logging.basicConfig(filename='/tmp/sparkRun.log', level=logging.DEBUG)
	logging.debug("{}:  Started App".format(datetime.now()))

#read API key 
configFile=args.config
if path.isfile(configFile):
	print("Reading config in " + configFile) 
else:
	print("ERROR: Can't read config file " + configFile) 
	quit()

config=configparser.ConfigParser()
config.read(configFile)
apiKey=config['apiKey']['key']
roomName=config['apiKey']['room']
api = CiscoSparkAPI(access_token=apiKey)

def getRoomID(api, roomName):
	rawRooms=api.rooms.list()
	rooms=[room for room in rawRooms if room.title == roomName]
	if len(rooms) == 0:
		print("No roomID found for {}, creating: ".format(roomName))
		room=api.rooms.create(roomName)
		roomID=room.id
	else:	
		for room in rooms:
			roomID=(room.id)
	if len(rooms) > 1:
		print("Found multiple rooms with name {} , using newest room.\n -You may want to delete some of the rooms".format(roomName))

	return roomID

roomID=getRoomID(api, roomName)
print("Connected, using roomID : "  + roomID)
logging.debug("{}:Connected to Spark Room : {}".format(messageTime, message.text))

#Initialize an empty message and timestamp, so we don't run old commands
lastMessageID=''
lastMessageTime=datetime.now()

while True:
	try:
		messages = api.messages.list(roomID)
	except:
		messages()
	for message in messages: 
		#Check to see if we print a message on the OLED or run a command
		if message.text[:3] == "run" or message.text[:4] == "oled":
			messageTime=(message.created.split(".")[0])
			messageTime=datetime.strptime(messageTime, '%Y-%m-%dT%H:%M:%S')
			if message.id != lastMessageID and messageTime > lastMessageTime:
				if args.log:
					logging.debug("{}: Received Message: {}".format(messageTime, message.text))
				if message.text[:3] == "run":
					command=message.text[3:]
					oledMsg="Command: " + command
					oledMsg="oled-exp -i -c write \"{}\"".format(oledMsg)
					sendMsg=(subprocess.Popen(oledMsg, shell=True, stdout=subprocess.PIPE).stdout.read()).strip()
					commandOutput=subprocess.getoutput(command)
					api.messages.create(roomID,text="Output: \n" + commandOutput)
				else: 
					oledMsg="oled-exp -i -c write \"{}\"".format(message.text[4:])
					sendMsg=(subprocess.Popen(oledMsg, shell=True, stdout=subprocess.PIPE).stdout.read()).strip()
					api.messages.create(roomID,text="OLED Updated")

				lastMessageID=message.id
				lastMessageTime=messageTime	
				break
	time.sleep(args.delay)
