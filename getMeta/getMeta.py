#!/usr/bin/python
import ConfigParser
import os
import sys
import glob
import subprocess


def getMeta():
	csvData=""
	#current dir is enough for now
	inputdir=""
	request = inputdir + '*.meta'
	print "Request:",request
	print "Result: ",glob.glob(request)
	for metafile in glob.glob(request):
		newData = ConfigParser.ConfigParser()
		newData.readfp(open(metafile))
		zipFilename=metafile.replace(".meta","")
		print inputdir+"md5sum.exe \""+ zipFilename+"\""
		md5sum=subprocess.check_output(inputdir+"md5sum.exe \""+ zipFilename+"\"")
		md5sum=md5sum.split("*")[0]
		row = [ zipFilename, md5sum ]
		wantedOptions = ["fileID", "modID", "Version", "name", "modName","newestVersion"]
		for x in wantedOptions:
			row.append(	newData.get("General", x) )
		print "Row: ", row
		for x in row:
			csvData += x+","
		csvData += "\n"
	csvFile = open( "result.csv", 'w' )
	csvFile.write(csvData)
	#for sectionList in newData.sections():
	#	for section in sectionList:
	#		print section
			#ConfigSectionMap("SectionOne")['name']
			#resultINI.add_section(section)
			
	#geninfo=config["General"]["name"];
	#Modname=config["General"]["modname"];
	#print(mystr);
	#file.write(ModList)
	
#disable parameter check for now	
'''if len(sys.argv) < 2:
	print 'No Parameters given.'
	sys.exit()
try:
	open(sys.argv[1])
except IOError:
	print'Cannot find file!'
	sys.exit()
'''
getMeta()
#getMeta("Original-4817-2-0.7z.meta")
