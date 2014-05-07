# (c) Michael Penhallegon relased under GPL v3
#
# simple server written in bottle, does the basic utilities of workstages.

from bottle import route, run, request, abort, get, delete, post, Bottle, template, static_file
from models import Stage

import json, shelve

app = Bottle()

# opens shelve that will be used for data persistence
d = shelve.open("./data", writeback=True)
try:
	stages = d["stages"]
	
# if keyerror will open new list in data file named "stages"
except KeyError:
	d["stages"] = []
	stages = d["stages"]



def write_to_stages(stage):
	stages.append(stage)
	d["stages"].append(stage)
	d.sync()
	
@get('/entries/<name>')
def get_by_id(name=None):
	#used to get stages by uuid
	
	#
	result =  [x.dump() for x in stages if x.get_uuid() == name]
	if len(result) < 1:
		abort(404, "stage dosen't exist")
	else:
		return result[0]
	
@delete('/entries/<name>')
def delete_by_id(name):
	# used to delete stage if not available will return a 404
	try:
		stage = [x for x in stages if x.get_uuid() == name][0]
		stages.remove(stage)
		stage.set_stop_status()
		write_to_stages(stage)
	except ValueError:
		abort(404, "stage dosen't exist")
		
@get('/latest/')
# @get('/test/') depercrated
def get_latest():
	# return latest stage
	if len(stages) >= 1:
		return stages[-1].dump()
	else:
		return {"in_pomodoro":False, "success":False }
	
@post('/latest/')
# @post('/test/') depercrated
def post_entry():
	q = [x for x in stages if x.get_current() == True]
	if len(q) == 0:
		current_stage = Stage(request.forms['startTimeStamp'], request.forms['interval'], stagetype=request.forms['type'])
		write_to_stages(current_stage)
	else:
		abort(404, "stage already in progress")
		
@delete("/latest/")
def stop_stage():
	q = [x for x in stages if x.get_current == True]
	if len(q) != 0:
		for s in q:
			stages.remove(s)
		s.set_stop_status()
		write_to_stages(s)
		
@get('/report/')
def report():
	return json.dumps(get_stages())
def get_stages():
	# provides list of stages history
	data = [x.get_data() for x in stages]
	return data
@get('/dash')
def get_dashboard():
	tpl = template('simple_dashboard')
	return tpl
@route("/static/<filepath:path>")
def get_css_static(filepath):
	return static_file(filepath, root='/home/crimson/Downloads/develop/workstages/server/lib')
@route("/lib/<filename>")
def get_js_static(filename):
	return static_file(filename, root='/home/crimson/Downloads/develop/workstages/lib')
if __name__ == "__main__":
	run(host="127.1.1.1", port="8080", debug=True, reloader=True)
