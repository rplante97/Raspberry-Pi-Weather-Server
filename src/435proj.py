#!/usr/bin/python
import json
import urllib2
import sys
import socket
import os
import MySQLdb
import datetime
import time
import subprocess


#Pulls weather data for Orono, ME from web
def get_orono_temp():
	#define a few strings that will be needed to build our url
	city_Code_Orono = '4974313' #openweathermap code for Orono, ME
	api_key = '956dd23bd442f244da4f5dbc974dfd62' #our unique api key
	unit = 'imperial'
	api = 'http://api.openweathermap.org/data/2.5/weather?id='
	
	full_url = api + city_Code_Orono + '&mode=json&units=' + unit + '&APPID=' + api_key #full request


	url = urllib2.urlopen(full_url) #open our url
	output = url.read() #read contents of page, this will be in json format
	output_dict = json.loads(output) #create a json dictionary from our output
	url.close() #Important! We can't forget to close the connection, otherwise our api key may be suspended!
	
	
	temp_current = output_dict.get('main').get('temp') #Access 'temp' readout of the 'main' section of the dictionary
	pressure = output_dict.get('main').get('pressure')
	humidity = output_dict.get('main').get('humidity')
	description = output_dict['weather'][0]['description']
	print humidity
	print pressure
	print description
	print 'Current Temp: ' + str(temp_current) #For now we just print our current temp
	return {'temp_current':temp_current, 'humidity':humidity, 'pressure':pressure, 'description':description}#Return our values so they can be used by other functions

	
#Gets current datetime
def getDateTime():
	dateandtime = time.time() #Gets the current time in seconds elapsed since Linux epoch
	print dateandtime
	return dateandtime #We'll need this value later
	
#Opens C Func and Retreives return value
def getIndoorTemp():
	indoorTemp = subprocess.check_output("./temp_1wire")
	indoorTemp = float(indoorTemp) #Convert returned string to float
	print(indoorTemp)
	indoorTemp = (indoorTemp*(1.8)) + 32 #Convert to Farhenheit
	print indoorTemp
	return indoorTemp
	

#Takes current datetime, indoor temp, and outdoor temp and adds it to database
def database_modify():
	db = MySQLdb.connect(host="localhost",
						user="root",       #This is bad, change to local user later
						passwd="ECE435", 
						db="weatherdata")   #name of the database
	
	#Access the various datapoints returned by the functions above
	date = getDateTime()
	outsideTemp = get_orono_temp().get('temp_current')
	humidity = get_orono_temp().get('humidity')
	pressure = get_orono_temp().get('pressure')
	description = get_orono_temp().get('description')
	
	insideTemp = getIndoorTemp()
	
	cursor = db.cursor() #Creates a cursor object that we can modify our database with
	
	#The id column is null as it is declared as auto increment
	mysqlStatement = "INSERT INTO weather (id, datetime, outsidetemp, insidetemp) VALUES (NULL, '%f', %f, %f)" % \
	(date, outsideTemp, insideTemp) #Inserts the date, outdoor temp, and indoor temp int the sql table	
	
	mysqlStatement2 = "UPDATE weathercards SET humidity=%i, pressure=%i, tempnow=%f, description='%s' WHERE id = 1;" % \
	(humidity, pressure, outsideTemp, description) #Updates the weathercards table to hold the most recent weather data
	
	
	cursor.execute(mysqlStatement) #Execute our query
	cursor.execute(mysqlStatement2)
	db.commit(); #Commit our table changes
	db.close(); #Close the db connection. For security reasons its best to close this whenever we can, even if we know we will be using the db again later.
	
if __name__ == "__main__":
	while(1):
		database_modify()
		time.sleep(60*5) #Run add new data to the database once every 5 minutes forever
