'''
Created on May 17, 2014

@author: crimson
'''

# exception handling for python3 configparser lib for python 2.7.x
try:
	import configparser
except(ImportError):
	import ConfigParser as configparser

#tries to parse config file if not will set default constants
try:
	config = configparser.ConfigParser()
	config.readfp(open('server.ini'))
	
except(IOError):
	#default constants
	SERVER_ADDRESS = "127.1.1.1"
	SERVER_PORT = "8080"
	DEBUG = True
	RELOADER = True
	STATIC_FILE_PATH = '/home/crimson/Downloads/develop/workstages/server/static'
	LIB_FILE_PATH = '/home/crimson/Downloads/develop/workstages/lib'

if __name__ == '__main__':
		pass