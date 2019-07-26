#!/usr/bin/python
#test comment
import requests
import urllib3
import sys
import json
import re
import os
import random
#Gets IP and create Fixed IPs / including DELETE function
#the script ping the IP before creating it, and it generates a random mac address in case the user don't know it

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.Session()
session.auth = ('admin', 'infoblox')
session.verify = False
url = 'https://10.55.34.16/wapi/v2.6.1/'

def rand_mac():   #function to generate random mac address in case that user doesn't know it
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def create_host(namehost, ip_addr, mac_addr): #function to create fixed IP, it will be called from different parts of code
host_data = {'mac': mac_addr, 'name': namehost, 'ipv4addr': ip_addr}
data=json.dumps(host_data)
resul = session.post(url + 'fixedaddress', data = data)
print resul.content
print "Congratulations, your IP was created!"

def create_process(ip_addr):
    r = session.get(url + 'ipv4address?status=USED&ip_address=' + ip_addr)
    urlFile = r.content
    resp_dict = json.loads(urlFile)


    if urlFile == "[]":
        print "Available!"
        print "Creating Fixed IP..."
        user_mac = raw_input("Please specify MAC address, example 01:0C:F1:DE:A9:40, leave it blank for random MAC: ")
        if user_mac == "":
            user_mac = rand_mac()
            user_hostname = raw_input("Please specify hostname: ")
            create_host(user_hostname, user_input, user_mac)
        else:
            user_hostname = raw_input("Please specify hostname: ")
            create_host(user_hostname, user_input, user_mac)

    else:
            #print "it seems to be available... Checking"
        for i in resp_dict:
            if i['status'] == "USED":
                print "Sorry, this IP is already in Use."
                user_input2 = raw_input("Would you like to get the next available IP? (y/n): ")
                if user_input2 == "y":
                    print "Checking..."
                    rea = session.get(url + 'network?network=' + i['network'])  #this will get the network reference to post next available
                    urlget = rea.content
                    resp_dict2 = json.loads(urlget)
                    for x in resp_dict2:
                        refe = x['_ref']  #we need to take only the ref code to insert it in the url
                        start = refe.find('n')
                        end = refe.find(':', start)
                        reas = session.post(url + refe[start:end] + '?_function=next_available_ip')
                        available_ip = reas.content
                        available_redable = json.loads(available_ip)

                        for i in available_redable.values():
                            print "This is your IP: " ,i[0], "would you like to create a host? (y/n): "
                            user_input3 = raw_input()
                            if user_input3 == "y":
                                print "Creating Fixed IP..."
                                user_mac_2 = raw_input("Please specify MAC address, example 01:0C:F1:DE:A9:40, leave it blank for random MAC: ")
                                if user_mac_2 == "":
                                    user_mac_2 = rand_mac()
                                    user_hostname_2 = raw_input("Please specify hostname: ")
                                    create_host(user_hostname_2, i[0], user_mac_2)
                                else:
                                    print "Specify mac address TEST"
                            else:
                                print "Closing program..."
                else:
                    print "What a pity, please run the script again to allocate another IP"
            else:
                print "IP seems to be available! Please report it to Network Admin first"

#def search(myDict, lookup):
    #for key, value in myDict.items():
        #    if lookup
            #    return key
    #return None
#End of creation function, application starts here
while True:
    print ""
    print "Infoblox IP Script"
    print ""
    print "What option do you want?: "
    print ""
    print "1: Search IP Status"
    print "2: Create IP address"
    print "3: Delete IP address"
    input_option = raw_input("Option: ")
    if input_option == "1":
        print ""
        user_input = raw_input("What IP address do you want to check?: ")
        r = session.get(url + 'ipv4address?status=USED&ip_address=' + user_input)
        urlFile = r.content
        resp_dict = json.loads(urlFile)
        if urlFile == "[]":
            print ""
            print ""
            print "Status: IP not in use!"
            print ""
            print ""
        else:
            print ""
            print ""
            print "Status: This IP is in use"
            print ""
            print ""
    if input_option == "2":
        print ""
        print "What option do you want?: "
        print "1: Create specific or random IP"
        print "2: List available subnets before creating IP"
        CreationOption = raw_input("Option: ")
        if CreationOption == "1":
            ip_addr = raw_input("What IP address do you want to check?: ")
            create_process(ip_addr)
        elif CreationOption == "2":
            print ""
            print ""
            SubnetRequest = raw_input("What env do you want to list? (DEV/TEST/STG): ")
            if SubnetRequest == "TEST" or SubnetRequest == "DEV" or SubnetRequest == "STG":
                r = session.get(url + 'network')
                urlFile = r.content
                resp_dict = json.loads(urlFile)

                for i in resp_dict:
                    #print i[0]
                    for k, v in i.iteritems():
                        if SubnetRequest in v:
                         print v
                         print i['network']
                         print ""
            else:
                print "Please type a valid environment"
