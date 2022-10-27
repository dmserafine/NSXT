#########################Tag Multiple VMs in NSx-T 3.2
### NOTE: This script uses Python3 and the Policy API to add tags to Virtual Machines in bulk
###       The script takes the values for VM Display Name followed by one or more tags in a comma separated
###		  format from a file named "vmtestdata.txt"
###       Place this file in the same directory and run using "python3 tagvms.py"
###		  This python script requires the csv, requests and json modules

##	Import the modules needed
import csv
import requests
import json
import getpass

# uncomment for user input of NSX LM URL, Username and password
urlNSX = input("Enter the FQDN of the NSX manager API: ")
userNSX = input("Enter the Policy API username for NSX: ")
passwordNSX = getpass.getpass('Enter the password for the NSX user: ')

getLDomainsUrl = urlNSX + "/policy/api/v1/infra/domains"
	
getDomains = requests.get(getLDomainsUrl, auth=(userNSX,passwordNSX), verify = False)
domainData = getDomains.json()

for domain in domainData['results']:
	domainName = domain['display_name']
	domainID = domain['id']

	print(domainName, domainID)

domainID = 'default'

# uncomment to specify domain_id of VMs
# domainID = input("Enter the domain of the virtual machines: ")

data_file = open('vmtestdata.txt','r')

data_lines = csv.reader(data_file)

for line in data_lines:
	vmName = line[0]
	apivmName = ""
	apivmID = ""
	vmID = ""

	print('VM: ',vmName)
	tags = len(line) - 1
	print('Number of Tags: ', tags)

	getVMIDUrl = urlNSX + "/api/v1/fabric/virtual-machines"
	addTagUrl = urlNSX + "/api/v1/fabric/virtual-machines?action=add_tags"
	Headers = {"Content-Type": "application/json"}

	response = requests.get(getVMIDUrl, auth=(userNSX,passwordNSX), verify = False)

	vmdata = response.json()

	for vm in vmdata['results']:

		apivmName = vm['display_name']
		apivmID = vm['external_id']
	
		if apivmName == vmName:
			vmID = apivmID

#			print('from API:',apivmName,apivmID)

			for tag in line:
				if tag != vmName:
					data = {
							    "external_id": vmID,
							    "tags": [
							    	{"scope": "", "tag": tag}
								]
							}
#					print('from loop',vmName, tag)
#					print('from API',apivmName, apivmID)	
					
					tagAdd = requests.post(addTagUrl, auth=(userNSX,passwordNSX), verify = False, json = data, headers=Headers)
					
					print(tagAdd.text)
					print(tagAdd.headers)

data_file.close()
