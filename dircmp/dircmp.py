import os
import sys
from os.path import join, getsize

rootdir = "C:\\boost"
#sys.argv[1]
print "test"

def walkthrough(root, subFolders, files):
    for folder in subFolders:
	print folder
	outfileName = os.path.join(rootdir, folder) + "\\py-outfile.txt" # hardcoded path
	folderOut = open( outfileName, 'w' )
	folderOut.write( folder + "\n" )
	print "outfileName is " + outfileName
	"""
	for file in files:
		filePath = rootdir + '/' + file 
		#f = open( filePath, 'r' )
		#toWrite = f.read()
		print "Logging " + filePath  + '\n'
		fileOut = open( outfileName, 'w' )
		folderOut.write( filePath +"\n" )
		print folderOut.read()
		# os. /or \
		#f.close()"""
	folderOut.close()
	

for root, subFolders, files in os.walk(rootdir):
#print "root" + root
#print "subf"+ subFolders
    walkthrough(root, subFolders, files)
