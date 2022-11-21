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
import getpass

# user input of NSX LM URL, Username and password
urlNSX = input("Enter the FQDN of the NSX manager API: ")
userNSX = input("Enter the Policy API username for NSX: ")
passwordNSX = getpass.getpass('Enter the password for the NSX user: ')

data_file = open('servicegroupdata.txt','r')

data_lines = csv.reader(data_file)

for line in data_lines:
	ServiceGrpName = line[0]
	serviceEntries = len(line) - 1
	print("Service name: ",ServiceGrpName," ","Service Entries: ",serviceEntries)

	addService = urlNSX + "/global-manager/api/v1/global-infra/services/" + ServiceGrpName
	Headers = {"Content-Type": "application/json"}

# 	Routine to handle service with only one service entry
	if serviceEntries == 1:
		service = line[1]
		seName = service + "entry"
		nestedPath = "/global-infra/services/" + service
		data = {
			  "description": ServiceGrpName,
			  "display_name": ServiceGrpName,
			  "_revision": 0,
			  "service_entries": [
			      {
			          "resource_type": "NestedServiceServiceEntry",
			          "display_name": seName,
			          "nested_service_path": nestedPath
			      }
			  ]
			}			
		svcAdd = requests.patch(addService, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
		print(ServiceGrpName," service: ",service," display_name: ",service)
		exit

# 	Routine to handle service with more than one service entry
	else:
		for service in line[1:]:
			seName = service + "entry"
			nestedPath = "/global-infra/services/" + service
			data2 = {
			  "description": ServiceGrpName,
			  "display_name": ServiceGrpName,
			  "_revision": 0,
			  "service_entries": [
			      {
		          "resource_type": "NestedServiceServiceEntry",
		          "display_name": seName,
		          "nested_service_path": nestedPath
			      }
			  ]
			}		

			svcAdd = requests.patch(addService, auth=(userNSX,passwordNSX), verify = False, json = data2, headers = Headers)
			print(ServiceGrpName," service: ",service)

data_file.close()
