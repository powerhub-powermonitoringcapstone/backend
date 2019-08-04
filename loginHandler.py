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
    found = root.find(".//logind/[@fgt={}]".format("\""+fgt+"\""))
    if (found == None):
        return False
    else:
        if (datetime.datetime.strptime(found.attrib['expires'], '%m/%d/%Y %H:%M') < now):
            return(False)
def newLogin(fgt):
    mntnLogin()
    now = datetime.datetime.utcnow()
    nowString = (now + datetime.timedelta(minutes = 10)).strftime("%m/%d/%Y %H:%M")
    found = root.find(".//logind/[@fgt={}]".format("\""+fgt+"\""))
    if (found == None):
        root.append(ET.Element("logind", {'expires': nowString, 'fgt': fgt, 'interval':"10"}))
    else:
        found.set('expires', nowString)
    settw = open(cwd + '/logins.xml', 'wb')
    settings.write(settw)
    settw.close()
def mntnLogin():
    found = root.findall(".logind")[19:]
    for elem in found:
        root.remove(elem)
    settw = open (cwd + '/logins.xml', 'wb')
    settings.write(settw)
    settw.close()
    
                
