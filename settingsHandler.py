from xml.dom import minidom
import xml.etree.ElementTree as ET
import os, platform, numpy
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
sett = open(cwd + '/settings.xml', 'r+')
settings = ET.parse(sett)
root = settings.getroot()
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
def settFile():
    return sett
def retCwd():
    return cwd
def readSettings():
    x = y = 0
    d = {'IsSetup':0,'DataLogging':1,'SensitivityThreshold':2,'Debug':3, 'NodeName':4,'Version':5,'NodeType':6}
    for element in root:
        try:
            c = d[root[x].attrib['name']]
            setArray[c] = root[x].text
            x +=1
        except KeyError:
            pass
    #sanity checks here
    return setArray
def riteSettings():
    print("Unimplemented yet!")
def readLogin():
    print("Unimplemented yet!") ##returns logins from logins.xml
def mntnLogin():
    print("Unimplemented yet!") ##purges lapsed login records
    
                
