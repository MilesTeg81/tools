# read a directory structure with all files and paths
import os
import shutil
import sys
import subprocess
#from subprocess import Popen, PIPE



#Source directory
dir1="cmp_src_tmp"

header="datatreecmp.py by MilesTeg 2013"

Usage="datatreecmp.py"

def saveFile(filename, txtContent):
	outputFile = open( filename, 'w' )
	outputFile.write(txtContent)
	print filename," saved"

#creates a csv file and returns the content as a string.
def createCSV(finishedlist, minElements=0):
	csvData=""
	for y in finishedlist:
		if len(y)>minElements:
			for x in y:
				csvData+=x+","
			csvData+="\n"
	return csvData

def createListTXT(finishedlist):
	content=""
	for y in finishedlist:
				content+=y+"\n"
	return content

#saves file and directory trees
def dirsave(dir):
	filelist =[]
	#csvData=""
	dirTree=[]
	for root, dirs, files in os.walk(dir, topdown=False):
		#gives us all filenames including rel. dir path	
		for name in files:
			fullpath = os.path.join(root, name)
			md5sum=subprocess.check_output(""+"md5sum.exe \""+ fullpath +"\"")
			md5sum=md5sum.split("*")[0]
			md5sum=md5sum.replace("\\","").strip()
			filelist.append( [fullpath, md5sum] )
			
		#gives us the directory structure
		for name in dirs:
			dirTree.append(os.path.join(root, name).replace(dir+"\\","") )
	#for dataset in filelist:
	#	csvData += dataset[0]+", "+dataset[1]+"\n"
	return filelist, dirTree

#comparism code
def comparism(DirOne, DirTwo):
	result=[]
	unknown=[]
	for dest in DirTwo:
		#multiple occurences of a file in source directory will be just ignored (found)
		found=False
		for source in DirOne:
			#source md5 vs destination md5
			if (source[1] == dest[1]) and not found:
				#add source, destination, md5
				#tmp directories are removed - you get pure and relative path to a file :)
				result.append([   source[0].replace(dir1+"\\",""),  dest[0].replace(dir2+"\\",""),  source[1] ])
				found=True;
		if not found:
			unknown.append([  dest[0].replace(dir2+"\\",""),  dest[1] ])
	return result, unknown

if len(sys.argv) < 2:
	print '\nNOTE: No Parameters given.\n'
	sys.exit()
try:
	open(sys.argv[1])
except IOError:
	print'\nNOTE: Cannot find file!\n'
	sys.exit()


#mod filename
modFilename =sys.argv[1].replace("\"","")

#install directory (the one you'll have to edit)
dir2=".\\"+os.path.splitext(modFilename)[0]

#check directory
noDir2=False
try:
	if not os.path.isdir(os.path.basename(dir2)):
		noDir2=True
		command = ur'7z.exe x "' + modFilename + '" -o\"'+dir2+'\" -y -aoa'
		print "=============================================================="
		print "Starting 7zip => "+command
		print "=============================================================="
		subprocess.call(command,shell=True)
		print ""
		print "\nNOTE: Sorry :( couldn't find the directory for your installed mod\n"
		print "It needs to be named \"", dir2,"\" for this tool."
		print "I have now extracted the mod into \"", dir2,"\" for you."
		print "Please make some changes e.g. run an installer, move files."
		print "Then run this tool again. See you later..."
	else:
		command = ur'7z.exe x "' + modFilename + '" -o\"'+dir1+'\" -y -aoa'
		print "=============================================================="
		print "Starting 7zip => "+command
		print "=============================================================="
		subprocess.call(command,shell=True)
		print "\n\n\n\n\n\n"
		print "Comparing fresh extraction (from temp dir) with your changed \"", dir2, "\" (This might take a while)",
		print "please wait...\n"
		
		fileList1, dirTreeSrc =dirsave(dir1)
		fileList2, dirTreeDst =dirsave(dir2)

		sourceDestList, unknownFiles = comparism( fileList1, fileList2 )

		#7z might use this later...
		excludeList=[]
		for x in fileList1:
			found=False
			for y in sourceDestList:
				if os.path.basename(x[0]) == os.path.basename(y[0]):
					found=True
					continue
			if not found:
				excludeList.append(os.path.basename(x[0]))

		#print excludeList
		
		saveFile( modFilename+"_copyCommands.csv",  createCSV(sourceDestList,2) )
		if len(unknownFiles)>0:
			saveFile( modFilename+"_unknown.csv",  createCSV(unknownFiles) )
		saveFile( modFilename+"_dirTreeSrc.txt",  createListTXT(dirTreeSrc) )
		saveFile( modFilename+"_dirTreeDst.txt",  createListTXT(dirTreeDst) )
		#use this 7z listfile with a command like ths:
		#7z.exe x yourmodfile.7z -oEXTRACTIONDIR -xr@Listfile.txt
		saveFile( modFilename+"_7zExcludeListfile.txt",  createListTXT(excludeList) )
		print "Deleting temporary folders"
		shutil.rmtree("cmp_src_tmp")
		print "\n\nNOTE: all done :)\n"
except IOError:
	print'\nNOTE: Error!\n'
	sys.exit()
