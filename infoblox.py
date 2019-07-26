import requests
import urllib3
import sys
import json
import re

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



session = requests.Session()
session.auth = ('apiuser', 'infoblox')
session.verify = False
url = 'https://{infoblox_IP}/wapi/v2.6.1/'
urlFile = "[]"

Status = True

def checkIpStatus(hostname):
global HostIpRemove
result = session.get(url + 'lease?_return_fields=binding_state,hardware,client_hostname&client_hostname~=' + hostname)
print result.content
print result.status_code
if result.status_code == 200:
print "Request OK"
urlget = result.content
IpResultList = json.loads(urlget)
for x in IpResultList:
refe = x['_ref']  #we need to take only the ref code to insert it in the url
start = refe.find(':')
end = refe.find('/', start)
HostIp = refe[start:end]
HostIpRemove = HostIp.replace(":", "")
print hostname + " IP address is " + HostIpRemove
return HostIpRemove
else:
print "exiting"


#def createHostRecord(ip_address, namehost, comment):
#host = (namehost + ".msdev.dom")
#data1 = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "' + ip_address + '"}],"name": "' + host + '", "comment": "'+ comment + '" }'
#print data1 for debugging purposes
#result = session.post(url + 'record:host', data = data1)
#print resul.content for debugging purposes
#print resul.status_code for debugging purposes
#if result.status_code == 201:
#print "Congratulations, your IP was created!"
#else:
#print "Something went wrong, please try again"

#def nextAvailable

#def subnetStatus

#def createSubnet

#def deleteHostRecord



while True:

print "Please select any of the following options: "
print ""
print "1 to check a host IP"
print "2 to check a subnet Status, add or delete a subnet"
print ""
userInput = raw_input("Option: ")
if userInput == "1":
IpCounter = 0
#HostList = []
class Host(object):
def __init__(self, hostname, ip):
self.hostname = hostname
self.ip = ip
print "Make sure you have DHCP enable in your new host!"
print ""
userHostName = raw_input("Please enter your hostname as it is in the VM: ")
checkIpStatus(userHostName)
IpCounter += 1
#HostList[0] = HostIpRemove
print "PRUEBA" + HostIpRemove
print IpCounter
HostIpRemove2 = HostIpRemove.encode('ascii')
Hosts = [Host(userHostName,HostIpRemove2)]
HostDic = dict([(h.hostname,h.ip) for h in Hosts])
print HostDic
#HostList.append(HostIpRemove)
#print type(HostList[0])

#print HostList
while True:
moreIps = raw_input("Would you like to look for another host?(y/n): ")
if moreIps == "y":
userNextOption = raw_input("Please enter your hostname as it is in the VM: ")
checkIpStatus(userNextOption)
IpCounter += 1
HostIpRemove2 = HostIpRemove.encode('ascii')
HostDic[userNextOption] = HostIpRemove2
print HostDic
else:
print ""
print ""
print "OK. Your host/s List is as follows: "
print ""
print HostDic
print ""
UserLbConf = raw_input("Would you like to create these hosts and a Pool for these hosts?(y/n): " )

break


elif userInput == "2":
userNextOption = raw_input("Please specify IP address: ")
else:
print ""
print "Not a valid Option! please select any of the following numbers 1-7"
print ""
#Please specify your option:

