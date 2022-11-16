#########################create distributed firewall rules in bulk in NSX-T 3.2
### NOTE: This script uses Python3 to creat a rule per row in a source excel
###       The script takes the entire worksheet as a data array
###		  from a file named "ruledata.xlsx"
###		  Column headers should be in order:category,policysection,rulename,sources,destinations,services,action,applyto
###		  This script does not use applyto for today - future product enhancement
###		  This script places security rules in the default domain 
###		  The URL is for a Global Manager and Global groups
###       Place this file in the same directory and run using "python3 rules2.py"
###		  This python script requires the pandas, csv, requests and json modules

import csv
import requests
import json
import pandas as pd

## uncomment for user input
## urlNSX = input("Enter the FQDN of the NSX manager API? ")
## userNSX = input("Enter the Policy API username for NSX? ")
## passwordNSX = input("Enter the password for the NSX user? ")

urlNSX = 'https://nsxtgm.serafine.home'
userNSX = 'admin'
passwordNSX ='brg*zwc1vwm3kuc2XNR'

domainID = 'default'

Headers = {"Content-Type": "application/json"}

data_file = pd.read_excel('ruledata.xlsx')

for row in data_file.itertuples():
	category = row.category
	section = row.policysection
	name = row.rulename
	source = row.sources
	destination = row.destinations
	service = row.services
	action = row.action
	applyto = row.applyto


	sourcelist = source.strip(" ").split(",")
	sourcedata = []
	destinationlist = source.strip(" ").split(",")
	destinationdata = []
	servicelist = service.strip(" ").split(",")
	servicedata = []

	for item in sourcelist:

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

	for item in servicelist:

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

	addruleurl = userNSX + "/global-manager/api/v1/infra/domains/" + domainID + "/security-policies/" + section + "/rules/" name

	print(addruleurl)

	addrule = requests.put(addruleurl, auth=(userNSX,passwordNSX), verify=False, json = data, headers = Headers)

	print(addrule.text)


