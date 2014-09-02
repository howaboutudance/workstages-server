# (c) Michael Penhallegon released under GPL v3
#
# simple server written in bottle, does the basic utilities of workstages.

from bottle import request, abort, get, delete, post, Bottle, template, debug
from stageserver.controllers import StageContrl
import json, uuid, datetime

# create bottle app
debug(mode=True)
app = Bottle()
contl = StageContrl()
# opens shelve that will be used for data persistence
stages = []

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
	
	if contl.in_stage() == True:
		return contl.get_last()
	else:
		return {"in_pomodoro":False, "success":False }
	
@app.post('/latest/')
def post_entry():
	# constructor to add a stage, checkes datastore via list comprhension for a currently running
	# stage, and if not found, create new stage object and send to be added to datastore, if currently
	# in stage returns a 404
	
	return contl.write_stage(request.forms)
		
@app.delete("/latest/")
def stop_stage():
	#used to stop stage, queries datastore via list comprhension if found removes via remove method of datastore
	
	if contl.in_stage() == True:
		s = contl.get_last()
		s.stopped = True;
		contl.write_stage(s)
		
@app.get('/report/<limit:int>')
def report(limit=100):
	# contructor for report returns data from datastore via get_stages function
	return json.dumps([contl.get_data(x) for x in contl.get_stages(limit)])

@app.get('/summary')
def summary():
	# computes statistics about stages and returns them
	total_stages = len(stages)
	work_sum = sum([x.get_interval() for x in stages if x.get_type() == 'work'])
	break_sum = sum([x.get_interval() for x in stages if x.get_type() == 'break'])
	return json.dumps({"hours_worked":work_sum, "total_stages":total_stages, "hours_break":break_sum})

# Dashboard
@app.get('/dash')
@app.get('/')
def get_dashboard():
	tpl = template('templates/simple_dashboard')
	return tpl
