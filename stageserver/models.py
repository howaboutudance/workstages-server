# (c) 2014 Michael Penhallegon

import uuid, time, json
from datetime import datetime, timedelta
from sqlalchemy import Column, ForeignKey, Integer, String, CHAR, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

base = declarative_base()

class db_Stage(base):
	__tablename__ = 'stages'
	stage_id = Column(CHAR(32), primary_key=True)
	start_time = Column(DateTime())
	end_time = Column(DateTime())
	interval = Column(Float())
	
engine = create_engine('sqlite:///stages.db')
class Stage():
  def __init__(self, starttime, interval, stagetype="work"):
    self.stopped = False
    self.uuid = uuid.uuid4()
    self.startTime = datetime.fromtimestamp(int(starttime)/1000.0)
    self.interval = timedelta(0, float(interval)*60)
    if stagetype == 'break':
      self.is_break = True
    else:
      self.is_break = False
  def set_stop_status(self):
    self.stopped = True
  def get_stop_status(self):
    return self.stopped
  def set_type(self, stagetype):
    self.type = stagetype
  def get_type(self):
    if self.is_break:
      return "break"
    else:
      return "work"
  def get_uuid(self):
      return str(self.uuid)
  def get_interval(self):
    return self.interval.seconds / 60.0
  def get_startTime(self):
      return time.mktime(self.startTime.timetuple()) * 1000
  def get_endTimestamp(self):
    return (self.startTime + self.interval).time()
  def get_endTime(self):
    return time.mktime((self.startTime + self.interval).timetuple()) * 1000
  def get_current(self):
    if (datetime.now() < (self.startTime + self.interval)) and (self.get_stop_status() != True):
      return True
    else:
      return False
  def get_data(self):
    data_dict = {
      "stage_id": self.get_uuid(),
      "end_time": self.get_endTime(),
      "start_time":self.get_startTime(),
      "interval":self.get_interval(),
      "type": self.get_type(),
      "stopped":self.get_stop_status()
      }
    return data_dict
  def dump(self):
    props = self.get_data()
    newdata = {"current":self.get_current(), "properties": props}
    return json.dumps(newdata)
