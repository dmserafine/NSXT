#########################create tag membership criteria for security groups in NSX-T 3.2
### NOTE: This script uses Python3 to pull service items in a list 
###       The script takes the first item as "Security Group Name" and all other items in each row as a tag
###		  comma separated from a file named "tagdata.txt"
###		  This script places security groups in the default domain 
###		  The URL is for a Global Manager and Global groups
###	 	  To create local groups use "/policy/api/v1/infra/domains/"
###       Place this file in the same directory and run using "python3 secgrptag2.py"
###		  This python script requires the csv, requests and json modules

import csv
import requests
import json
import getpass

##  user input
urlNSX = input("Enter the FQDN of the NSX manager API: ")
userNSX = input("Enter the Policy API username for NSX: ")
passwordNSX = getpass.getpass("Enter the password for the NSX user: ")

# domainID = input("Enter the domain where the groups will be located: ")
domainID = 'default'

data_file = open('tagdata.txt','r')

data_lines = csv.reader(data_file)


# Read in lines from file
for line in data_lines:
	Secgrp = line[0]
		
	Headers = {"Content-Type": "application/json"}

# create URL for API call
	addTagsurl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/groups/" + Secgrp
	

# API call buld for only one item in tag list
	if len(line) == 2:
		tag = line[1]

		data =  {
				   "expression": [
								      {
								          "resource_type": "Condition",
								          "member_type": "VirtualMachine",
								          "value": tag,
								          "key": "Tag",
								          "operator": "EQUALS",
								          "_protection": "NOT_PROTECTED"
								      }
								  ]
					}		
			
		putTag = requests.patch(addTagsurl, auth=(userNSX,passwordNSX), verify=False, json = data, headers = Headers)
		exit

# API call buld for more than one item in tag list
	else:
		exprdata = []
		operator = "AND"
		tag = line[1]
		condata = {}
		newdata = {}
		
		newdata['member_type'] = 'VirtualMachine'
		newdata['key'] = 'Tag'
		newdata['operator'] = 'EQUALS'
		newdata['value'] = tag
		newdata['resource_type'] = 'Condition'
		exprdata.append(newdata)

		
		for tag in line[2:]:
			  
			condata['conjunction_operator'] = operator
			condata['resource_type'] = 'ConjunctionOperator'
			exprdata.append(condata)

			newdata = {}
			newdata['member_type'] = 'VirtualMachine'
			newdata['key'] = 'Tag'
			newdata['operator'] = 'EQUALS'
			newdata['value'] = tag
			newdata['resource_type'] = 'Condition'
			exprdata.append(newdata)

			finaldata = {}
			finaldata['expression'] = exprdata
			print(finaldata)

			putTag = requests.patch(addTagsurl, auth=(userNSX,passwordNSX), verify=False, json = finaldata, headers = Headers)



data_file.close()
