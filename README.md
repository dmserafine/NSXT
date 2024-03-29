# VMware scripting tools for V2t and bulk import operations 


## Table of Contents
- [Abstract](#abstract)
- [Supported NSX-T Releases](#supported-nsx-t-releases)
- [Quick Start Guide](#quick-start-guide)
- [Script Files](#Contents-Scripts)
- [Example Data Files](#Contents-Example-Data-Files)
- [Run SDK Samples](#run-sdk-samples)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Repository Administrator Resources](#repository-administrator-resources)
- [VMware Resources](#vmware-resources)

## Abstract
This document describes the the various scripts within the repository.  These scripts are usefual when migrating from an NSXV envrionment to an NSX-T environment.  They are also useful when setting up a greenfield with large numbers of objects.  Each script will use a data file to pull in the info and then run associated API calls to NSX-T.

## Supported NSX-T Releases
NSX-T 3.2

## Quick Start Guide

## Contents Scripts
1. nat.py - This script applies gateway NAT rules in bulk to either a T0 or T1 gateway router
2. secgrpipaddr.py - This script applies ipaddresses in bulk to security groups for membership
3. secgrptag2.py - This script applies security tags to security groups for membership - deprecated Secgrptag.py
4. services2.py - Creates services with protocol(port) service definitions - deprecated services.py
5. servicegroups.py - Creates service groups with service membership
6. tagvms.py - Tags VM wih one or more security tags
7. rules2.py - create DFW rules in bulk with minor limitations(only validates first 1000 groups in NSX-T)
8. secgrps.py - create empty security groups in bulk
9. rules2woutV.py - rules2 but does not validate groups or services

## Contents Example Data Files
1. nat.txt - example data file for Nat.py
2. testipdata.txt - example data for file Secgrpipaddr.py
3. testdata.txt - example data file for Segrptag2.py
4. servicedata.txt - example data file for Services.py
5. serviegroupdata.txt - example data file for Servicegroups.py
6. vmtestdata - example data file for Tagvms.py
7. ruledata.xlsx - sample data for Rules2.py - not debugged - USE AT YOUR OWN RISK!

### Prepare a Python Development Environment

We recommend you to install latest [Python](http://docs.python-guide.org/en/latest/starting/installation/) and [pip](https://pypi.python.org/pypi/pip/) on your system.

A Python virtual environment is also highly recommended.
* [Install a virtual env for Python 3](https://docs.python.org/3/tutorial/venv.html)

### Installing Required Python Packages
SDK package installation commands may differ depending on the environment where it is being installed. The three installation options provided below are for different environments.
*pip* and *setuptools* are common requirements for these installation types, upgrade to the latest *pip* and *setuptools*.

##### 1. Typical Installation
This is the recommended way to install the SDK. The installation is done from [PyPI](https://pypi.org/) and [Automation SDK Python Github](https://github.com/vmware/vsphere-automation-sdk-python) repositories.

Install/Update latest pip from PyPI.
```cmd
pip install --upgrade pip
```
Install/Update request module
```cmd
pip install --upgrade requests
```
Instal/Upgrade csv module
```cmd
pip install --upgrade csv
```
Instal/Upgrade getpass module
```cmd
pip install --upgrade getpass
```
Instal/Upgrade json module
```cmd
pip install --upgrade json
```

##### 2. Execution of scripts

Place script in the same directory as the data file

## Run SDK Samples

Run Script
at a commnd prompt> python3 {scirpt filename with ".py" extension}

## API Documentation

### NSX API Documentation
* [NSX-T Data Center](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/index.html)
* [NSX Manager APIs](https://vmware.github.io/vsphere-automation-sdk-python/nsx/nsx/index.html) - API for managing NSX-T cluster and transport nodes for on-prem customers
* [NSX Policy](https://vmware.github.io/vsphere-automation-sdk-python/nsx/nsx_policy/index.html) - primary API for managing logical networks for on-prem customers
* [NSX VMC Policy](https://vmware.github.io/vsphere-automation-sdk-python/nsx/nsx_vmc_policy/index.html) - primary API for managing logical networks for VMC customers
* [NSX VMC AWS Integration APIs](https://vmware.github.io/vsphere-automation-sdk-python/nsx/nsx_vmc_aws_integration/index.html) - API for managing AWS underlay networks for VMC customers

## Troubleshooting

HTML Error codes from the API calls 
add Print(api call name) to the script immediately following the api call

## Repository Administrator Resources

### Board Members

Board members are volunteers from the SDK community and VMware staff members, board members are not held responsible for any issues which may occur from running of samples from this repository.

Members:
* David Serafine (VMware)

## VMware Resources

* [vSphere Automation SDK Overview](http://pubs.vmware.com/vsphere-65/index.jsp#com.vmware.vapi.progguide.doc/GUID-AF73991C-FC1C-47DF-8362-184B6544CFDE.html)
* [VMware Sample Exchange](https://code.vmware.com/samples) It is highly recommended to add any and all submitted samples to the VMware Sample Exchange
* [VMware Code](https://code.vmware.com/home)
* [VMware Developer Community](https://communities.vmware.com/community/vmtn/developer)
* VMware vSphere [REST API Reference documentation](https://developer.vmware.com/docs/vsphere-automation/latest/).
* [VMware Python forum](https://code.vmware.com/forums/7508/vsphere-automation-sdk-for-python)
