#########################Enter bulk NAT entries in a T1 gateway
### NOTE: This script uses Python3 and the Policy API to configure NAT rules on a T0 or T1 gateway
###       The script takes a text file with the values for sequence number, display name,
###       action, source IP(destination IP for DNAT) and translated IP separated by a space called "nat.txt"
###       Place this file in the same directory and run using "python3 nat.py"
###       By default all rules will be enabled, logged and bypass firewall




import os
import getpass

routerID = input("Enter the ID of the Tier1 router: ")
urlNSX = input("Enter the FQDN of the NSX manager API: ")
userNSX = input("Enter the Policy API username for NSX: ")
passwordNSX = getpass.getpass('Enter the password for the NSX user: ')

gatewayType = ()
routerType = ()

validInput = False
   
while (validInput == False):

   gatewayType = input("T1 or T0? ")

   if (gatewayType == "T1" or gatewayType == "T0"):
      validInput = True

   else:
      continue


if gatewayType == "T1":

   routerType = "tier-1s"

else:

   routerType = "tier-0s"

my_file = open("nat.txt", "r")

#for loop for curl requests
for line in my_file.readlines():

    
   sequenceNum, displayName, Action, sourceNetwork, translatedNetwork = line.strip().split(" ")

   if Action == "DNAT": 
      
      data = {
      "sequence_number": sequenceNum,
      "action": Action,
      "destination_network": sourceNetwork,
      "translated_network": translatedNetwork,
      "enabled": "true",
      "logging": "true",
      "firewall_match": "BYPASS",
      "display_name": displayName
      }

   else:

      data = {
      "sequence_number": sequenceNum,
      "action": Action,
      "source_network": sourceNetwork,
      "translated_network": translatedNetwork,
      "enabled": "true",
      "logging": "true",
      "firewall_match": "BYPASS",
      "display_name": displayName
      }

   dataString = str(data).replace("'", "\"")

   cmd = "curl -k -u \'" + userNSX + "\':\'" + passwordNSX + "\' -H \"Content-Type: application/json\" -X PATCH https://\'" + urlNSX + "\'/policy/api/v1/infra/\'" + routerType + "\'/\'" + routerID + "\'/nat/USER/nat-rules/\'" + displayName +"\' -d \'" + dataString + "\'"

   os.system(cmd)
   
   print(cmd)

my_file.close()
