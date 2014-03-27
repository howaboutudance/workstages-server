# (c) 2014 Michael Penhallegon

import uuid, time, json
from datetime import datetime, timedelta

class Stage:
  def __init__(self, starttime, interval):
    self.uuid = uuid.uuid4()
    self.startTime = datetime.fromtimestamp(int(starttime)/1000.0)
    self.interval = timedelta(minutes=int(interval))
  def get_uuid(self):
      return str(self.uuid)
  def get_interval(self):
    return self.interval.seconds / 60.0
  def get_startTime(self):
      return time.mktime(self.startTime.timetuple()) * 1000
  def get_endTime(self):
    return time.mktime((self.startTime + self.interval).timetuple()) * 1000
  def get_data(self):
    data_dict = {
      "pomodoro_id": self.get_uuid(),
      "end_time": self.get_endTime(),
      "start_time":self.get_startTime(),
      "interval":self.get_interval()
      }
    return data_dict
  def dump(self):
    props = self.get_data()
    if (self.startTime + self.interval) > datetime.now():
      in_pom = True
    else:
        in_pom = False
    newdata = {"in_pomodoro":in_pom, "properties": props}
    return json.dumps(newdata)