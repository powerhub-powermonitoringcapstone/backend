from xml.dom import minidom
import xml.etree.ElementTree as ET
import os, platform, numpy
cwd = os.path.dirname(os.path.realpath(__file__))
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
d = {'IsSetup':0,'DataLogging':1,'SensitivityThreshold':2\
     ,'Debug':3, 'NodeName':4, 'Version':5 , 'NodeType':6,\
     'Permanence':7, 'CarbonFootprint':8, 'RefreshRate':9}
try:
    sett = open(cwd+'/settings.xml', 'r')
    sett.close()
except IOError:
    with open(cwd+'/settings.xml', 'w') as sett: 
        sett.write("<settings></settings>")
        sett.close()
def riteSettings(f, g): ##index number, pamalit na value
    with open(cwd + '/settings.xml', 'r') as sett:
        settings = ET.parse(sett)
        root = settings.getroot()
        x = 0
        f = int(f)
        for element in root:
            if (f == d[root[x].attrib['name']]):
                root[x].text = g
            x+=1
        with open(cwd + '/settings.xml', 'wb') as settw:
            settings.write(settw)
            settw.close()
        ## wala pang data validity checker ah
def readSettings():
    with open(cwd +'/settings.xml', 'r') as sett:
        settings = ET.parse(sett)
        root = settings.getroot()
        x = 0
        for element in root:
            try:
                c = d[root[x].attrib['name']]
                setArray[c] = root[x].text
            except KeyError:
                pass
            x +=1
        #sanity checks here
        return setArray

    
                
