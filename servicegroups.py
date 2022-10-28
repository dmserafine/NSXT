#########################create service group definitions in NSX-T 3.2
### NOTE: This script uses Python3 to pull service items in a list 
###       The script takes the first item as "Service Name" and all other items in each row as a "protocol(port)" format
###		  comma separated from a file named "servicedata.txt"
###       Place this file in the same directory and run using "python3 itemWsubs.py"
###		  This python script requires the csv, requests and json modules

##	Import the modules needed
import csv
import json
import requests

# uncomment for user input of NSX LM URL, Username and password
# urlNSX = input("Enter the FQDN of the NSX manager API: ")
# userNSX = input("Enter the Policy API username for NSX: ")
# passwordNSX = getpass.getpass('Enter the password for the NSX user: ')
urlNSX = 'https://nsxtlmg.serafine.home'
userNSX = 'admin'
passwordNSX ='brg*zwc1vwm3kuc2XNR'

data_file = open('servicegroupdata.txt','r')

data_lines = csv.reader(data_file)

for line in data_lines:
	ServiceName = line[0]
	serviceEntries = len(line) - 1
	print("Service name: ",ServiceName," ","Service Entries: ",serviceEntries)
	
	addService = urlNSX + "/policy/api/v1/infra/services/" + ServiceName
	appendService = urlNSX + "/policy/api/v1/infra/services/" + ServiceName
	findservice = urlNSX + "/policy/api/v1/global-infra/services/"
	Headers = {"Content-Type": "application/json"}

#	find existing service entry for services



# 	Routine to handle service with only one service entry
	item = line[1]
	
	data = {
		  "description": ServiceName,
		  "display_name": ServiceName,
		  "_revision": 0,
		  "service_entries": [
		      {
		          "resource_type": "NestedServiceServiceEntry",
		          "display_name": ServiceName + "Entry",
		          "children": item
		      }
		  ]
		}			
	svcAdd = requests.put(addService, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
	print(ServiceName," proto: ",proto," port: ",portNum)
	exit
# 	Routine to handle service with more than one service entry
	else:
		item = line[1]:

		data = {
			  "description": ServiceName,
			  "display_name": ServiceName,
			  "_revision": 0,
			  "service_entries": [
			      {
		          "resource_type": "NestedServiceServiceEntry",
		          "display_name": ServiceName + "Entry",
		          "children": item
			      }
			  ]
			}

		svcAdd = requests.put(addService, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
		print(ServiceName," proto: ",proto," port: ",portNum)

		for item in line[1:]:
			proto = item[0:3]
			port = item[3:]
			portNum = port.strip("()")
			data = {
				  "description": ServiceName,
				  "display_name": ServiceName,
				  "_revision": 1,
				  "service_entries": [
				      {
		          "resource_type": "NestedServiceServiceEntry",
		          "display_name": ServiceName + "Entry",
		          "children": item
				      }
				  ]
				}		
			
			svcAdd = requests.patch(appendService, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
			print(ServiceName," proto: ",proto," port: ",portNum)

data_file.close()