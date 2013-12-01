import urllib2
import os
import sys
import csv
import string
from os.path import join, getsize

MAXSEC=12
VERS="2.2.7"
CHARNR=66

bookmarks = open( "bookmarks.html", 'w' )

htmlcode = unicode("")

htmlcode += u"<!DOCTYPE NETSCAPE-Bookmark-file-1><META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">"
htmlcode += u"<TITLE>STEP Bookmarks</TITLE>"
htmlcode += u"<H1>STEP Menu </H1>"
response = urllib2.urlopen('http://wiki.step-project.com/Special:Ask/-5B-5BIsCore::true-5D-5D/-3FSourceID%3DNexus-20ID/-3FSection/format%3Dcsv/offset%3D0')
inputfile = csv.reader(response, delimiter=',', quotechar='|')

linkpart="<DT><A HREF=\"http://skyrim.nexusmods.com/mods/"
linkpart.strip()
skipfirst = 0
Section=[""]
for i in range(MAXSEC):
	Section.append("")

for iterator in range(MAXSEC):
	#if content!="":
	Section[iterator]+= u"<p><DT><DL><H3 >STEP {0} Section 2.".format(VERS)
	Section[iterator]+= chr(iterator+CHARNR)
	Section[iterator]+= u".</H3><DL><p>\n"

for row in inputfile:
	if skipfirst == 0:
		skipfirst=1;
	else:
		buffer =""
		buffer += linkpart
		buffer += row[1].strip()
		buffer += u"\">"
		buffer += row[0].replace(u"\"",u"")
		buffer +=  u"</A>\n"
		print "buffer: ", row[2], buffer
		Section[ord(row[2])-CHARNR]+= buffer
		# 'A' == 1
		#print ord(row[2])-64
		#Section[ord(row[2])-64]="buffer"

for iterator in range(MAXSEC):
	Section[iterator]+= u"</DL>\n"
	#print Section[iterator]
htmlcode+= u"</DL><p>\n"

for i in range(MAXSEC):
	htmlcode+=  Section[i]

print htmlcode
bookmarks.write( htmlcode )