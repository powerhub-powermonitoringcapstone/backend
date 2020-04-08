from xml.dom import minidom
import xml.etree.ElementTree as ET, portalocker, os, platform, numpy
cwd = os.path.dirname(os.path.realpath(__file__))
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
d = {'IsSetup':0,'DataLogging':1,'SensitivityThreshold':2\
     ,'Debug':3, 'NodeName':4, 'Version':5 , 'NodeType':6,\
     'Permanence':7, 'CarbonFootprint':8, 'RefreshRate':9, 'KilowattLimit':10, 'KilowattLimitEnabled':11,\
     'EmailAddress1':12, 'EmailAddress2':13, 'EmailAddress3':14, 'EmailAddress4':15, 'EmailAddress5':16, \
     'EmailAddress6':17, 'EmailAddress7':18, 'EmailAddress8':19, 'EmailAddress9':20, 'EmailAddress10':21,} ##Email Addresses on 12
try:
    sett = open(cwd+'/settings.xml', 'r')
    sett.close()
except IOError:
    with open(cwd+'/settings.xml', 'w') as sett: 
        sett.write("<settings></settings>")
        sett.close()
def riteSettings(f, g): ##index number, pamalit na value
    lock = False
    while lock == False:
        try:
            with portalocker.Lock(cwd + '/settings.xml', 'r') as settfile:
                lock = True
                settings = ET.parse(settfile)
                root = settings.getroot()
                x = y = 0
                f = int(f)
                for element in root:
                    try:
                        if (f == d[root[x].attrib['name']]):
                            root[x].text = g
                    except KeyError:
                        pass
                    x+=1## wala pang data validity checker ah
                with open(cwd+'/settings.xml', 'wb') as sett:             
                    settings.write(sett)
        except portalocker.exceptions.LockException:
            pass
def readSettings():
    lock = False
    while lock == False:
        try:
            with portalocker.Lock(cwd +'/settings.xml', 'r') as settfile:
                lock = True
                settings = ET.parse(settfile)
                root = settings.getroot()
                x = 0
                for element in root:
                    try:
                        setArray[d[root[x].attrib['name']]] = root[x].text
                    except KeyError:
                        pass
                    x+=1
        except portalocker.exceptions.LockException:
            pass
    #sanity checks here
    return setArray

    
                
