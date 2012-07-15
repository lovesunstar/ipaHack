# -*- coding: utf-8 -*-

import plist, os, sys, shutil, re, zipfile
from pprint import pprint

xml = True
ipaFileName = None
ipaFile = None
plFileName = None
plFile = None
binData = None
dataTree = None

if len(sys.argv) == 0:
	raise ValueError(u'File name should be specified')
else:
	ipaFileName = sys.argv[1]

if not zipfile.is_zipfile(os.path.realpath(ipaFileName)):
	raise ValueError(u'Wrong file type or file doesn\'t exist. Must be .ipa')

with zipfile.ZipFile(ipaFileName) as ipaFile:
	for ipaContent in ipaFile.filelist:
		if ipaContent.filename.find('Info.plist') > -1:
			plFileName = ipaFile.extract(ipaContent.filename)

	if not plFileName:
		raise IOError(u'File wasn\'t found')

with open(plFileName, 'rb') as plFile:
	binData = plFile.read()

if binData[0] == b'<':
	dataTree = plist.plist.Structure_from_xml(binData)
else:
	dataTree = plist.plist.Structure_from_bin(binData)
	xml = False

print 'Current OS version requirement: %s' % dataTree['MinimumOSVersion'].get_value()

osVersion = raw_input('Enter new OS Version requirement or leave blank to prevent changes:')

if not re.compile(r"^\d{1}(\.\d){1,2}$").match(osVersion):
	osVersion = '3.1'

dataTree['MinimumOSVersion'].set_value(osVersion)

if xml:
	binData = dataTree.to_xml()
else:
	binData = dataTree.to_bin()

with open(plFileName, 'w+') as plFile:
	plFile.write(binData)

length = len(os.getcwd())
appendFileName = plFileName[length + 1:]

with zipfile.ZipFile(ipaFileName, 'a') as ipaFile:
	ipaFile.write(appendFileName)
	ipaFile.close()

delimiter = '/' if os.name == 'posix' else '\\'

shutil.rmtree(appendFileName[len(delimiter) - 1:].split(delimiter)[0])

print 'Done!'