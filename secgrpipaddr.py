#########################Add IP Addresses to Security Group membership in NSx-T 3.2
### NOTE: This script uses Python3 and the Policy API to add IP Adresses to Security groups in bulk
###       The script takes the values for VM Display Name followed by one or more tags in a comma separated
###		  format from a file named "testIPdata.txt"
###       Place this file in the same directory and run using "python3 tagvms.py"
###		  This python script requires the csv, requests and json modules

##	Import the modules needed
import csv
import requests
import json
import getpass

# uncomment for user input of NSX LM URL, Username and password
# urlNSX = input("Enter the FQDN of the NSX manager API: ")
urlGNSX = input("Enter the FQDN of the Global NSX manager API: ")
userNSX = input("Enter the Policy API username for NSX: ")
passwordNSX = getpass.getpass('Enter the password for the NSX user: ')


domainID = 'default'

data_file = open('testIPData.txt','r')

data_lines = csv.reader(data_file)

Headers = {"Content-Type": "application/json"}

for line in data_lines:
	Secgrp = line[0]
	addSecGrpUrl = urlGNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/groups/" + Secgrp

	sgdata = {
				"description": Secgrp,
				"display_name": Secgrp,
				"_revision":0
			}

	addSecGrp = requests.put(addSecGrpUrl, auth=(userNSX,passwordNSX), verify = False, json = sgdata, headers = Headers)
	
	print('Security Group: ',Secgrp)
	ips = len(line) - 1
	print('Number of IP Adresses: ', ips)

	expressID = Secgrp + "ipset"
	addIPUrl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/groups/" + Secgrp + "/ip-address-expressions/" + expressID
	appendIPUrl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/groups/" + Secgrp + "/ip-address-expressions/" + expressID + "?action=add"
	

	if len(line) == 2:
		print('Only one IP')
		ips = line[1]
		data = {
		          "ip_addresses": [ips],
		          "resource_type": "IPAddressExpression",
      			  "id" : expressID
				}				
		ipAdd = requests.patch(addIPUrl, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
		print("Security Group: ",Secgrp," IP Adresses: ",ips)
		exit
	else:
		print('More than one IP')
		firstip = line[1]
		data = {
          "ip_addresses": [firstip],
          "resource_type": "IPAddressExpression",
			  "id" : expressID
		}				
		ipAdd = requests.patch(addIPUrl, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)

		listips = line[2:]
		data = {
        	 	 "ip_addresses": listips,
				}	
	
		ipAdd = requests.post(appendIPUrl, auth=(userNSX,passwordNSX), verify = False, json = data, headers = Headers)
		print("Security Group: ",Secgrp," IP Adresses: ",ips)

data_file.close()
