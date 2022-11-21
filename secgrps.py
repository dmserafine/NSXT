######################### Createempty Security Groups in NSX-T 3.2
### NOTE: This script uses Python3 and the Policy API to add Security groups in bulk
###       The script takes the values for Security Display Name followed by one or more tags in a comma separated
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
# userNSX = input("Enter the Policy API username for NSX: ")
# passwordNSX = getpass.getpass('Enter the password for the NSX user: ')
# urlNSX = 'https://nsxtlmg.serafine.home'
urlNSX = 'https://nsxtgm.serafine.home'
userNSX = 'admin'
passwordNSX ='brg*zwc1vwm3kuc2XNR'

domainID = 'default'

data_file = open('testIPData.txt','r')

data_lines = csv.reader(data_file)

trbl_file = open("trbl.txt", "w")

Headers = {"Content-Type": "application/json"}

for line in data_lines:
	Secgrp = line[0]
	addSecGrpUrl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/groups/" + Secgrp

	sgdata = {
				"description": Secgrp,
				"display_name": Secgrp,
				"_revision":0
			}

	addSecGrp = requests.patch(addSecGrpUrl, auth=(userNSX,passwordNSX), verify = False, json = sgdata, headers = Headers)
	
	print('Security Group: ',Secgrp, file=trbl_file)
	print(addSecGrp, file=trbl_file)


data_file.close()