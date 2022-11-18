#########################create distributed firewall rules in bulk in NSX-T 3.2
### NOTE: This script uses Python3 to creat a rule per row in a source excel
###       The script takes the entire worksheet as a data array
###		  from a file named "ruledata.xlsx"
###		  Column headers should be in order:category,policysection,rulename,sources,destinations,services,action,applyto
###		  This script does not use applyto for today - future product enhancement
###		  This script places security rules in the default domain 
###		  The URL is for a Global Manager and Global groups
###       Place this file in the same directory and run using "python3 rules2.py"
###		  This python script requires the csv, requests, json, getpass and pandas modules
###		  This script will create two files; error.txt and trbl.txt
###		  error.txt is a file listing all of the group and services objects not found in NSX-T
###		  trbl.txt is a file containing all datagrams, urls and response codes for API calls

import csv
import requests
import json
import getpass
import pandas as pd

## uncomment for user input
## urlNSX = input("Enter the FQDN of the NSX manager API? ")
## userNSX = input("Enter the Policy API username for NSX? ")
## passwordNSX = getpass.getpass("Enter the password for the NSX user? ")

urlNSX = 'https://nsxtgm.serafine.home'
userNSX = 'admin'
passwordNSX ='brg*zwc1vwm3kuc2XNR'

domainID = 'default'

Headers = {"Content-Type": "application/json"}

getgroupsurl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/groups"
getserviceurl = urlNSX + "/global-manager/api/v1/global-infra/services"
getsectionurl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/security-policies"

error_file = open("error.txt", "w")
trbl_file = open("trbl.txt", "w")

# Uses excel data file 
data_file = pd.read_excel('ruledata.xlsx')

# headers for columns in data file in order, exact name follows "row."
for row in data_file.itertuples():
	sequencenum = row.sequence
	category = row.category
	sections = row.policysection
	name = row.rulename
	source = row.sources
	destination = row.destinations
	service = row.services
	action = row.action
	applyto = row.applyto

# converts multiple entries in source, destination and service field to JSON format list
	sourcelist = source.strip(" ").split(",")
	sourcedata = []
	destinationlist = destination.strip(" ").split(",")
	destinationdata = []
	servicelist = service.strip(" ").split(",")
	servicedata = []

# check to see if section exists
	item_found = False
	getsection = requests.get(getsectionurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
	sectiondata = getsection.json()
	for section in sectiondata['results']:
		sectionName = section['display_name']
		sectionID = section['id']
		if sections == sectionName:
			item_found = True
		else:
			sectiondata = {
				    "description": sections,
				    "display_name": sections,
				    "category": category
					}
			addsectionurl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/security-policies/" + sections
			addsection = requests.put(addsectionurl, auth=(userNSX,passwordNSX), verify=False, json = sectiondata, headers = Headers)
			print("Added Section: ",section, file=trbl_file)
			print(addsection.text, file=trbl_file)


# Check groups in the source field to get grouppath if exist
	for item in sourcelist:
		item_found = False

# If only one entry exists check if entry is "any" or group name
		if len(sourcelist) == 1:
			if item == "any":
				sourcedata = "any"

# Verify group name against existing groups in NSX-T and add group as source
			else:
				getgroup = requests.get(getgroupsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
				groupdata = getgroup.json()
				for group in groupdata['results']:
					groupName = group['display_name']
					groupPath = group['path']
					if item == groupName:
						sourcedata = groupPath
						item_found = True

# If group does not exist print out rule sequence number and group name							
				if item_found == False:
					print("Item not found: ",sequencenum,": ",item, file=error_file)


# If multiple entries exists check if each entry is valid and combine to array
		else:
			getgroup = requests.get(getgroupsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
			groupdata = getgroup.json()
			for group in groupdata['results']:
				groupName = group['display_name']
				groupPath = group['path']
				if item == groupName:
					sourceentry = groupPath
					sourcedata.append(sourceentry)
					item_found = True

# If group does not exist print out rule sequence number and group name					
			if item_found == False:
				print("Item not found: ",sequencenum,": ",item, file=error_file)


# Check groups in the destination field to get grouppath if exist
	for item in destinationlist:
		item_found = False

# If only one entry exists check if entry is "any" or group name
		if len(destinationlist) == 1:
			if item == "any":
				destinationdata = "any"

# Verify group name against existing groups in NSX-T and add group as destination				
			else:
				getgroup = requests.get(getgroupsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
				groupdata = getgroup.json()
				for group in groupdata['results']:
					groupName = group['display_name']
					groupPath = group['path']
					if item == groupName:
						destinationdata = groupPath
						item_found = True

# If group does not exist print out rule sequence number and group name							
				if item_found == False:
					print("Item not found: ",sequencenum,": ",item, file=error_file)

# If multiple entries exists check if each entry is valid and combine to array
		else:
			getgroup = requests.get(getgroupsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
			groupdata = getgroup.json()
			for group in groupdata['results']:
				groupName = group['display_name']
				groupPath = group['path']
				if item == domainName:
					destinationentry = domainPath
					destinationdata.append(destinationentry)
					item_found = True

# If group does not exist print out rule sequence number and group name						
			if item_found == False:
				print("Item not found: ",sequencenum,": ",item, file=error_file)


# Check services in the service field to get path if exist
	for item in servicelist:
		item_found = False

# If only one entry exists check if entry is "any" or service name
		if len(servicelist) == 1:
			if item == "any":
				servicedata = ["any"]

# Verify group name against existing groups in NSX-T and add group as service				
			else:
				getservice = requests.get(getserviceurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
				servicejson = getservice.json()
				for service in servicejson['results']:
					serviceName = service['display_name']
					servicePath = service['path']
					if item == serviceName:
						servicedata = servicePath
						item_found = True

# If service does not exist print out rule sequence number and service name							
				if item_found == False:
					print("Item not found: ",sequencenum,": ",item, file=error_file)

# If multiple entries exists check if each entry is valid and combine to array
		else:
			getservice = requests.get(getserviceurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
			servicejson = getservice.json()
			for service in servicejson['results']:
				serviceName = service['display_name']
				servicePath = service['path']
				if item == serviceName:
					serviceentry = servicePath
					servicedata.append(serviceentry)
					item_found = True

# If service does not exist print out rule sequence number and service name						
			if item_found == False:
				print("Item not found: ",sequencenum,": ",item, file=error_file)

	if sourcedata == []:
		sourcedata = "any"
	if destinationdata == []:
		destinationdata = "any"
	if servicedata == []:
		servicedata = ["any"]

# build data array for each rule
	data = {
		  "action": action.upper(),	
		  "resource_type": "Rule",
		  "id": name,
		  "display_name": name,
#		  "rule_id": ruleid,
		  "sequence_number": sequencenum,
		  "source_groups": [sourcedata],
		  "destination_groups": [destinationdata],
		  "services": servicedata,
		  "profiles": ["any"],
		  "logged": 'true',		  		  	  
		  "scope": ["any"],
		  "disabled": 'false'
		}
	print(data, file = trbl_file)
	
# URL used to add or create rules
	addruleurl = urlNSX + "/global-manager/api/v1/global-infra/domains/" + domainID + "/security-policies/" + sections + "/rules/" + name

	print(addruleurl, file = trbl_file)
	
# API call to add rule
	addrule = requests.patch(addruleurl, auth=(userNSX,passwordNSX), verify=False, json = data, headers = Headers)

	print(addrule.text, file = trbl_file)
	
