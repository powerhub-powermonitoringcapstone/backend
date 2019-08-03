from xml.dom import minidom
import xml.etree.ElementTree as ET
import os, platform, numpy, datetime
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
sett = open(cwd + '/logins.xml', 'r')
settings = ET.parse(sett)
root = settings.getroot()
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
def isLogin(fgt):
    now = datetime.datetime.utcnow()
    nowString = now.strftime("%m/%d/%Y %H:%M")
    x = 0
    for element in root.findall('login'):
        try:
            c = root[x].attrib[fgt]
            x +=1
        except KeyError:
            pass
        if (datetime.datetime.strptime(root[x].attrib['expires'], '%m/%d/%Y %H:%M') < now):
            print(False)
def newLogin(fgt):
    now = datetime.datetime.utcnow()
    nowString = now.strftime("%m/%d/%Y %H:%M")
    x = 0
    for element in root.findall('login'):
        try:
            c = root[x].attrib[fgt]
            x +=1
        except KeyError:
            pass
        root[x].set('expires', 'never')
        settw = open(cwd + '/logins.xml', 'wb')
        settings.write(settw)
        settw.close()
        ##if (datetime.datetime.strptime(root[x].attrib['expires'], '%m/%d/%Y %H:%M') < now):
##            print(False)
##    x = 0
##    for element in root:
##        try:
##            c = root[x].attrib[fgt]
##            x +=1
##        except KeyError:
##            pass
##        if (datetime.datetime.strptime(root[x].attrib['expires'], '%m/%d/%Y %H:%M') < now):
##            return False
        
def mntnLogin():
    print("Unimplemented yet!") ##purges lapsed login records
    
                
