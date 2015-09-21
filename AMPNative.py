#--finds only AMPNative folders--#
import os

ampFolders = []

#myDir = 'C:\\Python27\\MINE\\mydir\\'
myDir='/var/lib/jenkins/jobs/'

for folderName in os.listdir(myDir):
    if folderName[:10] == 'AMPNative-':
        ampFolders.append(folderName)

print 'ampFolders:'
for ampFolderName in ampFolders:
    print ampFolderName
print '\n'
#______________________#



#--generates paths of AmpNative Jobs--#
ampPaths = []

for ampFolderName in ampFolders:
    ampPaths.append(myDir+ampFolderName)
#_____________#
 
 
 
#--gets list of files in subdirs--#
#--validates data leaving only dates--#
#--date format: 'YYYY-MM-DD_HH-MM-SS'--#
#--loads xml file--#
#--updates startTime tag--#
 
import xml.etree.ElementTree as ET
import time
import re

# example data:
# ampFolderName == 'AMPNative-4.3'
# ampFiles == '2013-11-12_14-31-44'
# tmpDir == 'AMPNative-4.3\2013-11-12_14-31-44'
# xmlFileName == 'AMPNative-4.3\2013-11-12_14-31-44\build.xml'

for ampFolderName in ampPaths:
    for ampFiles in os.listdir(ampFolderName):
        if re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[0-9][0-9]-[0-9][0-9]-[0-9][0-9]', ampFiles):
            tmpDir = ampFolderName+'/'+ampFiles
            print 'processing directory: '+tmpDir
            xmlFileName = tmpDir+'/'+'build.xml'
            tree = ET.parse(xmlFileName)
            print 'parsing xml file: '+xmlFileName
            root = tree.getroot()
            tmpTimestamp = int(time.mktime(time.strptime(ampFiles, '%Y-%m-%d_%H-%M-%S'))) - time.timezone
            timestampExists = tree.find('timestamp')
            if timestampExists is None: #jesli wczesniej nie istnial tag <timestamp>
                addedTag = ET.SubElement(root, 'timestamp') #dodaje nowy tag na koncu pliku
                addedTag.text = str(tmpTimestamp) #ustawia jego tekst
                print 'there is no <timestamp> tag. It has been added.'
            else:##jesli wczesniej juz istnial tag <timestamp>
                for xmlTag in root.iter('timestamp'):
                    if xmlTag.text == '0':##zmieniamy tylko jesli wczesniej zawieral 0
                        print '<timestamp> is now: 0. changing.'
                        xmlTag.text = str(tmpTimestamp)
                        print '<timestamp> tag is now: '+xmlTag.text
            tree.write(xmlFileName) 
