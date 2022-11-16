#########################create distributed firewall rules in bulk in NSX-T 3.2
### NOTE: This script uses Python3 to creat a rule per row in a source excel
###       The script takes the entire worksheet as a data array
###		  from a file named "ruledata.xlsx"
###		  Column headers should be in order:sequence,category,policysection,rulename,sources,destinations,services,action,applyto
###		  This script does not use applyto for today - future product enhancement
###		  This script places security rules in the default domain 
###		  The URL is for a Global Manager and Global groups
###      	  Place this file in the same directory and run using "python3 rules2.py"
###		  This python script requires the csv, requests, json, getpass and pandas modules

import csv
import requests
import json
import getpass
import pandas as pd

### user input
urlNSX = input("Enter the FQDN of the NSX manager API? ")
userNSX = input("Enter the Policy API username for NSX? ")
passwordNSX = getpass.getpass("Enter the password for the NSX user? ")


domainID = 'default'

Headers = {"Content-Type": "application/json"}


# Uses excel data file 
data_file = pd.read_excel('ruledata.xlsx')

# headers for columns in data file in order, exact name follows "row."
for row in data_file.itertuples():
	sequencenum = row.sequence
	category = row.category
	section = row.policysection
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

# Check domains in the source field to get domainpath if exist
	for item in sourcelist:

# If only one entry exists check if entry is "any" or domain name	
		if len(sourcelist) == 1:
			if item == "any":
				sourcedata = "any"
			else:
				getdomain = requests.get(getdomainsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
				domaindata = getdomain.json()
				for domain in domaindata['results']:
					domainName = domain['display_name']
					domainPath = domain['path']
					if item == domainName:
						sourcedata = domainpath
					else: 
						print("No Domain Found For:" + item)
#						sourcedata = "/global-infra/domains/" + item

# If multiple entries exists check if each entry is valid and combine to array
		else:
			getdomain = requests.get(getdomainsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
			domaindata = getdomain.json()
			for domain in domaindata['results']:
				domainName = domain['display_name']
				domainPath = domain['path']
				if item == domainName:
					sourceentry = domainPath
					sourcedata.append(sourceentry)
				else: 
					print("No Domain Found For:" + item)
#					sourceentry = "/global-infra/groups/" + item
#					sourcedata.append(sourceentry)

# If only one entry exists check if entry is "any" or domain name
	for item in destinationlist:

		if len(destinationlist) == 1:
			if item == "any":
				destinationdata = "any"
			else:
				getdomain = requests.get(getdomainsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
				domaindata = getdomain.json()
				for domain in domaindata['results']:
					domainName = domain['display_name']
					domainPath = domain['path']
					if item == domainName:
						destinationdata = domainpath
					else:
						print("No Domain Found For:" + item) 
#						destinationdata = "/global-infra/domains/" + item

# If multiple entries exists check if each entry is valid and combine to array
		else:
			getdomain = requests.get(getdomainsurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
			domaindata = getdomain.json()
			for domain in domaindata['results']:
				domainName = domain['display_name']
				domainPath = domain['path']
				if item == domainName:
					destinationentry = domainPath
					destinationdata.append(destinationentry)
				else: 
					print("No Domain Found For:" + item) 
#					destinationentry = "/global-infra/groups/" + item
#					destinationdata.append(destinationentry)

# Check services in the service field to get path if exist
	for item in servicelist:

# If only one entry exists check if entry is "any" or service name
		if len(servicelist) == 1:
			if item == "any":
				servicedata = "any"
			else:
				getservice = requests.get(getserviceurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
				domaindata = getdomain.json()
				for domain in domaindata['results']:
					domainName = domain['display_name']
					domainPath = domain['path']
					if item == domainName:
						servicedata = domainpath
					else:
						print("No Domain Found For:" + item) 
#						servicedata = "/global-infra/domains/" + item

# If multiple entries exists check if each entry is valid and combine to array
		else:
			getservice = requests.get(getserviceurl, auth=(userNSX,passwordNSX), verify=False, headers = Headers)
			domaindata = getdomain.json()
			for domain in domaindata['results']:
				domainName = domain['display_name']
				domainPath = domain['path']
				if item == domainName:
					serviceentry = domainPath
					servicedata.append(serviceentry)
				else: 
					print("No Domain Found For:" + item)
#					serviceentry = "/global-infra/groups/" + item
#					servicedata.append(serviceentry)

# build data array for each rule
	data = {
		  "description": name,
		  "display_name": name,
		  "source_groups": [
		      sourcedata
		  ],
		  "logged": "true",
		  "destination_groups": [
		      destinationdata
		  ],
		  "scope": [
		      "ANY"
		  ],
		  "action": action,
		  "services": servicedata
		}
	print(data)	

# URL used to add or create rules
	addruleurl = userNSX + "/global-manager/api/v1/infra/domains/" + domainID + "/security-policies/" + section + "/rules/" name

	print(addruleurl)

# API call to add rule	
	addrule = requests.put(addruleurl, auth=(userNSX,passwordNSX), verify=False, json = data, headers = Headers)

	print(addrule.text)


