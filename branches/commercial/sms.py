#! /usr/bin/env python
#-*-coding:utf8-*-
import httplib
import urllib2
from xml.etree import ElementTree as ET

class AvisoSMS:
    server = 'api.avisosms.ru'
#    server = '127.0.0.1:8097'
    path = '/sms/xml'

    def __init__(self, username, password, proxy = None):
        self.username = username
        self.password = password
#        self.connection = httplib.HTTPConnection(self.server)
        self.protocol = 'http://'
        self.proxy = proxy

    def getXML(self, params, values):
        result = ''
        for i in xrange(len(params)):
            result += '<'+params[i]+'>'+str(values[i])+'</'+params[i]+'>\n'
        return result

    def getHost(self):
        return self.protocol+self.server+self.path

    def request(self, method, params = [], params_values = []):
        content = self.getXML(['smsUser', 'password'], [self.username, self.password])
        content += self.getXML(params, params_values)
        request = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <'''+method+' xmlns="'+self.server+self.path+'">'+content+'</'+method+'''>
  </soap:Body></soap:Envelope>'''
        headers = {'Content-Type': 'text/xml; charset=utf-8', 'Content-Length': str(len(request))}
        req = urllib2.Request(url = self.protocol + self.server + self.path, data = request, headers = headers)
        if self.proxy:
            req.set_proxy(self.proxy, 'http')
        response = urllib2.urlopen(req).read()
        try:
            data = ET.XML(response)
            data = data.find('.//{'+self.getHost()+'}'+method+'Response').getchildren()
        except:
            return response
        answer = {}
        for e in data:
            text = e.text.replace(" ", "").replace("\n", "")
            if text:
                answer[e.tag[len(self.getHost())+2:]] = text
#            if 'messageId' in e.tag:
#                result = []
#                for child in e.getchildren():
#                    result.append(child.text.replace(" ", "").replace("\n", ""))
#                answer[e.tag[len(self.getHost())+2:]] = result
        return answer
            
    def getBalance(self):
        return self.request('GetCreditBalance')
    
    def sendMessage(self, dst, data, src = 'AvisoSMS', report = True, flash = False, period = 60):
        params = ['destinationAddress', 'messageData', 'sourceAddress', 'deliveryReport', 'flashMessage', 'validityPeriod']
        params_values = [dst, data, src, report, flash, period]
        return self.request('SendTextMessage', params, params_values)
        
    def getState(self, messageId):
        return self.request('GetMessageState', ['messageId'], [messageId])
if __name__=="__main__":
    sms = AvisoSMS('kmkap', 'rBpTW8zCIHwwZVxP')
    print sms.getBalance()
    print sms.sendMessage('79529603429', 'KMKAP worked', 'KMKAP')
    #print sms.getState('59E5281E')
