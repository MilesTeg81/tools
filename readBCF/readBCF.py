# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
# copied from Wrye Bashs "bosh.py" (V304.3)
# what it does: reads .BCF files as a standalone tool
# see http://sourceforge.net/projects/oblivionworks/files/Wrye%20Bash/
# for more info
# All credits go to the Wrye Bash Team!
# Small adjustments made by MilesTeg.
#
#
# This file is part of Wrye Bolt.
#
# Wrye Bolt is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Wrye Bolt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wrye Bolt; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Wrye Bolt copyright (C) 2005, 2006, 2007, 2008, 2009 Wrye
# =============================================================================
import time
# Imports ---------------------------------------------------------------------
import cPickle
import codecs
import StringIO
import codecs
import StringIO
import os
import re
import sys
import subprocess
from subprocess import Popen, PIPE
close_fds = True
from binascii import crc32


# sio - StringIO wrapper so it uses the 'with' statement, so they can be used
# in the same functions that accept files as input/output as well. Really,
# StringIO objects don't need to 'close' ever, since the data is unallocated
# once the object is destroyed.
#------------------------------------------------------------------------------
class sio(StringIO.StringIO):
        def __enter__(self): return self
        def __exit__(self,*args,**kwdargs): self.close()

class readBCF(object):
        #original was class InstallerConverter(object) in Wrye Bash code
        """Object representing a BAIN conversion archive, and its configuration"""
        #--Temp Files/Dirs
        def __init__(self,srcArchives=None, data=None, destArchive=None, BCFArchive=None, blockSize=None, progress=None):
                #--Persistent variables are saved in the data tank for normal operations.
                #--persistBCF is read one time from BCF.dat, and then saved in Converters.dat to keep archive extractions to a minimum
                #--persistDAT has operational variables that are saved in Converters.dat
                #--Do NOT reorder persistBCF,persistDAT,addedPersist or you will break existing BCFs!
                #--Do NOT add new attributes to persistBCF, persistDAT.
                self.persistBCF = ['srcCRCs']
                self.persistDAT = ['crc','fullPath']
                self.text = ""
                
                #--Any new BCF persistent variables are not allowed. Additional work needed to support backwards compat.
                #--Any new DAT persistent variables must be appended to addedPersistDAT.
                #----They must be able to handle being set to None
                self.addedPersistDAT = []
                self.srcCRCs = set()
                self.crc = None
                #--fullPath is saved in Converters.dat, but it is also updated on every refresh in case of renaming
                self.fullPath = u'BCF: Missing!'
                #--Semi-Persistent variables are loaded only when and as needed. They're always read from BCF.dat
                #--Do NOT reorder settings,volatile,addedSettings or you will break existing BCFs!
                self.settings = ['comments','espmNots','hasExtraData','isSolid','skipVoices','subActives']
                self.volatile = ['convertedFiles','dupeCount']
                #--Any new saved variables, whether they're settings or volatile must be appended to addedSettings.
                #----They must be able to handle being set to None
                self.addedSettings = ['blockSize',]
                self.convertedFiles = []
                self.dupeCount = {}
                self.load()
                self.text=""
                #--Else is loading from Converters.dat, called by __setstate__
        def load(self, fullLoad=False):
                #Loads BCF.dat
                startupinfo=None
                command = ur'"7z.exe" x ' + filename + ' BCF.dat -y -so'
                ins, err = Popen(command, stdout=PIPE, startupinfo=startupinfo).communicate()

                with sio(ins) as ins:
                        setter = object.__setattr__
                        # translate data types to new hierarchy
                        class _Translator:
                                        def __init__(self, streamToWrap):
                                                        self._stream = streamToWrap
                                        def read(self, numBytes):
                                                        return self._translate(self._stream.read(numBytes))
                                        def readline(self):
                                                        return self._translate(self._stream.readline())
                                        def _translate(self, s):
                                                        return re.sub(u'^(bolt|bosh)$', ur'bash.\1', s,flags=re.U)
                        translator = _Translator(ins)
                        #print translator
                        map(self.__setattr__, self.persistBCF, cPickle.load(translator))
                        #if fullLoad:
                        #        map(self.__setattr__, self.settings + self.volatile + self.addedSettings, cPickle.load(translator))
                        counter=0
                        arbit=0
                        for dataset in cPickle.load(translator)[6]:
                                for x in dataset:
                                        if counter==1:
                                                self.text+= str(x[0])+","
                                                self.text+= str(x[1])+","
                                                
                                        #print "data3", str(x[2])
                                        #print "data4", str(x[3])
                                        else:
                                                if counter ==2:
                                                        self.text+= x + "\n"
                                                else:
                                                        self.text+= str(x).strip(" ")+","
                                        counter=counter+1
                                counter=0
                        #for y in cPickle.load(translator)[6]:
                        #        print y;
                        if fullLoad:
                                        map(self.__setattr__, self.settings + self.volatile + self.addedSettings, cPickle.load(translator))
                        BCF=filename+".txt"
                        textfile = open(BCF, "w")        
                        textfile.write(self.text)
                        textfile.close
global filename
filename=""
if len(sys.argv) < 2:
        print 'No Parameters given. Use Standard BCF.7z'
        filename="noparam"
if filename =="noparam":
        filename="BCF.7z"
else:
        try:
                open(sys.argv[1])
        except IOError:
                print'BRC file not found'
                sys.exit()
        filename = sys.argv[1]
activeBCF = readBCF()
activeBCF.load()