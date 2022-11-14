#########################create service definitions in NSX-T 3.2
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

# uncomment for user input of NSX LM URL, Username and password
# urlNSX = input("Enter the FQDN of the NSX manager API: ")
# userNSX = input("Enter the Policy API username for NSX: ")
# passwordNSX = getpass.getpass('Enter the password for the NSX user: ')
urlNSX = 'https://nsxtgm.serafine.home'
userNSX = 'admin'
passwordNSX ='brg*zwc1vwm3kuc2XNR'

data_file = open('servicedata.txt','r')

data_lines = csv.reader(data_file)

for line in data_lines:
	ServiceName = line[0]
	serviceEntries = len(line) - 1
	print("Service name: ",ServiceName," ","Service Entries: ",serviceEntries)
	
	addService = urlNSX + "/global-manager/api/v1/global-infra/services/" + ServiceName
	Headers = {"Content-Type": "application/json"}

# 	Routine to handle service with only one service entry
	if serviceEntries == 1:
		item = line[1]
		proto = item[0:3]
		port = item[3:]
		portNum = port.strip("()")
		seName = proto+portNum
		data = {
				  "description": ServiceName,
				  "display_name": ServiceName,
				  "_revision": 0,
				  "service_entries": [
				      {
				          "resource_type": "L4PortSetServiceEntry",
				          "display_name": seName,
				          "destination_ports": [
				              portNum
				          ],
				          "l4_protocol": proto
				      }
				  ]
				}			
		svcAdd = requests.patch(addService, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
		print(ServiceName," item: ",item," proto: ",proto," port: ",portNum)


# 	Routine to handle service with more than one service entry
	else:
		item = line[1]
		proto = item[0:3]
		port = item[3:]
		portNum = port.strip("()")
		seName = proto+portNum
		data = {
				  "description": ServiceName,
				  "display_name": ServiceName,
				  "_revision": 0,
				  "service_entries": [
				      {
				          "resource_type": "L4PortSetServiceEntry",
				          "display_name": seName,
				          "destination_ports": [
				              portNum
				          ],
				          "l4_protocol": proto
				      }
				  ]
				}		

		svcAdd = requests.patch(addService, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
		print(ServiceName,seName,addService," item: ",item," proto: ",proto," port: ",portNum)

#	Routine to add additional service entries
		for item in line[2:]:
			proto = item[0:3]
			port = item[3:]
			portNum = port.strip("()")
			seName = proto+portNum
			data2 = {
					  "resource_type": "L4PortSetServiceEntry",
					  "display_name": seName,
					  "destination_ports": [
					      portNum
					  ],
					  "l4_protocol": proto
					}		
			appendServiceEntry = urlNSX + "/global-manager/api/v1/global-infra/services/" + ServiceName + "/service-entries/" + seName
			svcAdd = requests.patch(appendServiceEntry, auth=(userNSX,passwordNSX), verify = False, json = data2, headers = Headers)	
			print(ServiceName," item: ",item," proto: ",proto," port: ",portNum)


data_file.close()
