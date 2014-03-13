# (c) 2014 Michael Penhallegon

import web
import json

urls = ('/(.*)', 'test')

def not_found():
    return json.dumps({'ok':0, 'errcode': 404})
def found():
    return json.dumps({'ok':1, 'messaage':'success'})

app = web.application(urls, globals())

class test:
    def GET(self, name):
        response =  found()
        return response
    def POST(self, message):
        if message:
          return message
        else:
          return not_found()
if __name__ == "__main__":
  app.run()