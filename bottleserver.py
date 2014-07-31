# (c) Michael Penhallegon relased under GPL v3
#
# simple server written in bottle, does the basic utilities of workstages.

from bottle import request, abort, get, delete, post, Bottle, template 
from models import Stage

import json 

#constants
DEBUG = True
RELOADER = True
# create bottle app
app = Bottle()

# opens shelve that will be used for data persistence
stages = []
	
# Helper Functions

def write_to_stages(stage):
	# add stage to local datastore and syncs with shelve
	
	stages.append(stage)

def get_stages(limit, start=0):
	# provides list of stages history
	data = [x.get_data() for x in stages]
	if len(data) >= limit:
		data = data[start:limit]
	return data

# Routes

@app.get('/entries/<name>')
def get_by_id(name):
	#used to get stages by uuid
	
	result =  [x.dump() for x in stages if x.get_uuid() == name]
	if len(result) < 1:
		abort(404, "stage dosen't exist")
	else:
		return result[0]
	
@app.delete('/entries/<name>')
def delete_by_id(name):
	# used to delete stage if not available will return a 404
	
	try:
		stage = [x for x in stages if x.get_uuid() == name][0]
		stages.remove(stage)
		stage.set_stop_status()
	except ValueError:
		abort(404, "stage dosen't exist")
		
@app.get('/latest/')
def get_latest():
	# return status of current stage and the data from that stage 
	
	if len(stages) >= 1:
		return stages[-1].dump()
	else:
		return {"in_pomodoro":False, "success":False }
	
@app.post('/latest/')
def post_entry():
	# constructor to add a stage, checkes datastore via list comprhension for a currently running
	# stage, and if not found, create new stage object and send to be added to datastore, if currently
	# in stage returns a 404
	
	q = [x for x in stages if x.get_current() == True]
	if len(q) == 0:
		current_stage = Stage(request.forms['startTimeStamp'], request.forms['interval'], stagetype=request.forms['type'])
		write_to_stages(current_stage)
	else:
		abort(404, "stage already in progress")
		
@app.delete("/latest/")
def stop_stage():
	#used to stop stage, queries datastore via list comprhension if found removes via remove method of datastore
	
	q = [x for x in stages if x.get_current == True]
	if len(q) != 0:
		for s in q:
			stages.remove(s)
		s.set_stop_status()
		write_to_stages(s)
		
@app.get('/report/<limit:int>')
def report(limit=100):
	# contructor for report returns data from datastore via get_stages function
	return json.dumps(get_stages(limit))

@app.get('/summary')
def summary():
	# computes statistics about stages and returns them
	total_stages = len(stages)
	work_sum = sum([x.get_interval() for x in stages if x.get_type() == 'work'])
	break_sum = sum([x.get_interval() for x in stages if x.get_type() == 'break'])
	return json.dumps({"hours_worked":work_sum, "total_stages":total_stages, "hours_break":break_sum})

# Dashboard
@app.get('/dash')
def get_dashboard():
	tpl = template('templates/simple_dashboard')
	return tpl

