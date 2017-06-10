import requests
import json

class hc2(object):
    bien=0;
    def __init__(self, user,password,ip):
        self.user = user
        self.password = password
        self.iphc2=ip
    def setvariable(self,vari,data):
        url = 'http://'+self.user+':'+self.password+'@'+self.iphc2+'/api/globalVariables/'+vari
        payload = {"value":"{}".format(data),"invokeScenes":True}
        data = json.dumps(payload)
        headers = {"content-type": "application/json", "Authorization": "<auth-key>" }
        r = requests.put(url, data, headers=headers)
        #print(r)
    def getvariable(self,vari):
        url = 'http://'+self.user+':'+self.password+'@'+self.iphc2+'/api/globalVariables/'+vari
        reponse = requests.get(url)
        return reponse
    def setswitch(self,id_switch,value):
        if value=="1":
            value="turnOn"
        else :
            value="turnOff"
        url = 'http://'+self.user+':'+self.password+'@'+self.iphc2+'/api/callAction?deviceID='+id_switch+'&name='+value
        reponse = requests.get(url)
        return reponse
    def setRGB(self,id_RGB,mauR,mauG,mauB,mauW):
        url = 'http://'+self.user+':'+self.password+'@'+self.iphc2+'/api/callAction?deviceID='+id_RGB+'&name=setColor&arg1='+mauR+'&arg2='+mauG+'&arg3='+mauB+'&arg3='+mauW
        reponse = requests.get(url)
        return reponse
    def startRGB(self,id_RGB,program):
        url = 'http://'+self.user+':'+self.password+'@'+self.iphc2+'/api/callAction?deviceID='+id_RGB+'&name=startProgram&arg1='+program
        reponse = requests.get(url)
        return reponse
