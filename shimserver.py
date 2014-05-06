# (c) 2014 Michael Penhallegon

import web
import json
from models import Stage

urls = (
  '/test/(.*)', 'latest',
  '/latest/(.*)', 'latest',
  '/entries/(.*)', 'by_id',
  '/report/(.*)', 'report'
  )
stages = []


app = web.application(urls, globals())

class by_id:
  def GET(self, name):
    result =  [x.dump() for x in stages if x.get_uuid() == name]
    if len(result) < 1:
      web.notfound()
    else:
      return result[0]
  def DELETE(self, name):
    try:
     stage = [x for x in stages if x.get_uuid() == name][0]
     stages.remove(stage)
     stage.set_stop_status()
     stages.append(stage)
    except ValueError:
      abort(404, "stage dosen't exist")
class latest:
    def GET(self, name):
      if len(stages) >= 1:
        return stages[-1].dump()
      else:
        response = json.dumps({"in_pomodoro":False})
        return response
    def POST(self, message):
      data = web.input()
      q = [x for x in stages if x.get_current() == True]
      if len(q) == 0:
        print("q is 0")
        stages.append(Stage(data.startTimeStamp, data.interval))
      else:
        web.notfound("please wait till "+q[0].get_endTimestamp().isoformat())
      
class report:
    def GET(self, message):
        data = [x.get_data() for x in stages]
        return json.dumps(data)
if __name__ == "__main__":
  app.run()