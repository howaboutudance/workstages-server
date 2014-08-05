from webtest import TestApp
from datetime import datetime

import unittest, time

import bottleserver

class latest_url(unittest.TestCase):
  def setUp(self):
    self.app = TestApp(stageserver.bottleserver.app)
    self.timestamp = time.mktime(datetime.now().timetuple())
  def test_post_request(self):
    response = self.app.post('/latest/', {"interval":0.25, "startTimeStamp":int(self.timestamp)})
    self.assertEqual(response.status_int, 200)
  def test_in_stage(self):
    self.app.post('/latest/', {"interval":25, "startTimeStamp":int(self.timestamp)})
    response = self.app.post('/latest/', {"interval":25, "startTimeStamp":int(self.timestamp)})
    self.assertEqual(response.status_int, 404)
    
if __name__ == "__main__":
  unittest.main()
