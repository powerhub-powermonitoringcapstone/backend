from xml.dom import minidom
import xml.etree.ElementTree as ET
import os, platform, numpy
cwd = os.path.dirname(os.path.realpath(__file__))
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
try:
    sett = open(cwd+'/settings.xml', 'r')
    sett.close()
except IOError:
    sett = open(cwd+'/settings.xml', 'w')
    sett.write("<settings></settings>")
    sett.close()
def readSettings():
    with open(cwd +'/settings.xml', 'r') as sett:
        settings = ET.parse(sett)
        root = settings.getroot()
        x = 0
        d = {'IsSetup':0,'DataLogging':1,'SensitivityThreshold':2,'Debug':3, 'NodeName':4,'Version':5,'NodeType':6,'Permanence':7}
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
    
                
