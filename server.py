# (c) Michael Penhallegon released under GPL v3
#
# simple server written in bottle, does the basic utilities of workstages.

from bottle import request, abort, get, delete, post, Bottle, template, debug
from stageserver.models import Stage, StageObj
from google.appengine.ext import ndb
import json, uuid, datetime

# create bottle app
debug(mode=True)
app = Bottle()

# opens shelve that will be used for data persistence
stages = []
	
# Helper Functions

def write_to_stages(request):
	# add stage to local datastore and syncs with shelve
    user_name = "mpenhall"
    stagetype = 0
    if request.get("type") == "work":
        stagetype = 1
    newstage = StageObj(
        parent=ndb.Key("User","mpenhall"),
        starttime=datetime.datetime.fromtimestamp(int(request.get('startTimeStamp'))/1000.0),
        interval=int(request.get('interval'))/60,
        worktype=bool(stagetype),
        uuid = str(uuid.uuid4()))
    newstage.put()
def get_stages(limit, start=0):
	# provides list of stages history
    user_name = "mpenhall"
    ancestor_key = ndb.Key("User", user_name or "*nouser*")
    return StageObj.query_user(ancestor_key).fetch(limit)

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
	
		write_to_stages(request.forms)
		
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
