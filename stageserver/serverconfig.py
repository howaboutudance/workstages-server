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
	filename = 'server.ini'
	config = configparser.ConfigParser()
	config.readfp(open(filename))
	SERVER_ADDRESS = config.get('server', 'server_address')
	SERVER_PORT = config.get('server','server_port')
	SERVER_DEBUG = config.get('server','server_debug')
	
except(IOError):
	#default constants
	SERVER_ADDRESS = "127.1.1.1"
	SERVER_PORT = "8080"
	DEBUG = True
	RELOADER = True

STATIC_FILE_PATH = '/home/crimson/Downloads/develop/workstages/server/static'
LIB_FILE_PATH = '/home/crimson/Downloads/develop/workstages/lib'

if __name__ == '__main__':
		config.write('server.ini')
		address = raw_input("Server Address (as '127.1.1.1' or 'google.com')> ")
		port = raw_input('Server Port (like 8080 or 80)> ')
		debug = None
		while (debug == None):
			port_raw = raw_input('Debug on or off> ')
			port_raw = port_raw.lower()
			if (port_raw == 'true') or (port_raw == 'yes') or (port_raw == 'y') or (port_raw == 'on'):
				debug = True
			elif (port_raw == 'false') or (port_raw == 'no') or (port_raw ==  'n') or (port_raw == 'off'):
				debug = False
		config.add_section("server")
		config.set('server','server_address',str(address))
		config.set('server','server_port',str(port))
		config.set('server','server_debug',str(debug))
				
