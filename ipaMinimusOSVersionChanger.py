# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
import zipfile
from pprint import pprint

try:
	import plist
except ImportError:
	raise ImportError(u'python-plist package should be installed in your system.')

def extractFile(ipaFileName, errors):	
	if not zipfile.is_zipfile(os.path.realpath(ipaFileName)) or ipaFileName.find('.ipa') == -1:
		errors.append(u'Wrong file type or file doesn\'t exist. Must be .ipa')
		return None

	with zipfile.ZipFile(ipaFileName) as ipaFile:
		for ipaContent in ipaFile.filelist:
			if ipaContent.filename.find('Info.plist') > -1:
				plFileName = ipaFile.extract(ipaContent.filename)

		ipaFile.close()

		if not plFileName:
			errors.append(u'File wasn\'t found')
			return None
		else:
			return plFileName


def buildDataTree(plFileName, xml, errors):
	with open(plFileName, 'rb') as plFile:
		binData = plFile.read()

	if binData[0] == b'<':
		dataTree = plist.plist.Structure_from_xml(binData)
	else:
		dataTree = plist.plist.Structure_from_bin(binData)
		xml = False

	if not dataTree['MinimumOSVersion']:
		errors.append('Minimum OS Version requirement isn\'t setted up. Breaking.')
		return None

	return dataTree


def changeValueInFile(dataTree, plFileName, xml, errors):
	print 'Current OS version requirement: %s' % dataTree['MinimumOSVersion'].get_value()

	osVersion = raw_input('Enter new OS Version requirement or leave blank to prevent changes:')

	if not re.compile(r"^\d{1}(\.\d){1,2}$").match(osVersion):
		osVersion = '3.1.3'

	dataTree['MinimumOSVersion'].set_value(osVersion)

	binData = dataTree.to_xml() if xml else dataTree.to_bin()

	try:
		with open(plFileName, 'w+') as plFile:
			plFile.write(binData)
	except (OSError, IOError), e:
		errors.append(e.__str__())


def saveAndRemoveTemp(plFileName, ipaFileName, errors):
	length = len(os.getcwd())
	appendFileName = plFileName[length + 1:]

	with zipfile.ZipFile(ipaFileName, 'a') as ipaFile:
		ipaFile.write(appendFileName)
		ipaFile.close()

	delimiter = '/' if os.name == 'posix' else '\\'

	shutil.rmtree(appendFileName[len(delimiter) - 1:].split(delimiter)[0])

	print 'Done!'
	

def Do(name, errors):
	xml = True
	ipaFileName = sys.argv[1]

	plFileName = extractFile(ipaFileName, errors)

	if not len(errors):
		dataTree = buildDataTree(plFileName, xml, errors)
	else:
		return None

	if not len(errors):
		changeValueInFile(dataTree, plFileName, xml, errors)
	else:
		return None

	if not len(errors):
		saveAndRemoveTemp(plFileName, ipaFileName, errors)
		return True
	else:
		return None	

if __name__ == "__main__":
	errors = []

	if len(sys.argv) < 2:
		errors.append(u'File name should be specified')
		pprint(errors)
	else:
		if not Do(sys.argv[1], errors):
			pprint(errors)