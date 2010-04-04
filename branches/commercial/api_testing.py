# -*- coding: utf-8 -*-

import httplib
import demjson

connection = httplib.HTTPConnection("marks.11infmat.ru")

body = '{"date":"2010-01-11","grade":[1],"subject":3,"task":"","teacher":2,"topic":"Электричество"}'
#body = file('./pup').read()
#body = '{"name":"Olosasasasaslo","saturday":0}'
#body = '{"saturday":1}'
#body = {'date': '2010-01-10', 'grade': 1, 'subject': 1, 'teacher': 2, 'topic': 'Bla-bla', 'school': 1}

connection.set_debuglevel(9)

connection.request("POST", "/api/lesson/", body, headers = {'HTTP_AUTHORIZATION': 'Basic ZW50cm9waXVzOmdoand0Y2NqaA=='})

r1 = connection.getresponse()



print "Status: %d" % r1.status
#print r1.read()
#print r1.getheader('location')
response = file('response.html', 'w')
response.write(r1.read())
response.close()

