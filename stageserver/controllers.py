from stageserver.models import Stage, StageObj
from google.appengine.ext import ndb
import uuid, json
from datetime import timedelta, datetime

class StageContrl():
	def write_stage(self, request):
		# add stage to local datastore and syncs with shelve
	    user_name = "mpenhall"
	    stagetype = 0
	    if request.get("type") == "work":
	        stagetype = 1
	    newstage = StageObj(
	        parent = ndb.Key("User","mpenhall"),
	        starttime= datetime.fromtimestamp(int(request.get('startTimeStamp'))/1000.0),
	        interval = int(request.get('interval'))/60,
	        worktype = bool(stagetype),
	        uuid = str(uuid.uuid4()),
	        stopped = False)
	    newstage.put()
	    return "{'status':'sucess'}"
	def get_stages(self, limit, start=0):
		# provides list of stages history
	    user_name = "mpenhall"
	    ancestor_key = ndb.Key("User", user_name or "*nouser*")
	    return StageObj.query_user(ancestor_key).fetch(limit)
	def get_last(self):
		return self.get_stages(1)[0]
	def in_stage(self):
		lateststage = self.get_last()
		endofstage = lateststage.starttime + timedelta(minutes=lateststage.interval)
		if endofstage <= datetime.now():
			return False
		else:
			return True
	def get_data(self, s):
	 	props = {
	 		"stage_id": s.uuid,
	 		"end_time": str(s.starttime + timedelta(minutes=s.interval)),
	 		"start_time":str(s.starttime),
	 		"interval":s.interval,
	 		"type": s.worktype,
	 		"stopped":s.stopped
	 	}
	 	return props
	def dump(self, s):
	 	props = get_data(s)
	 	newdata = {"current":self.in_stage(), "properties": props}
	 	return newdata