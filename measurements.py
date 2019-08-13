import xml.etree.ElementTree as ET
import os, platform, numpy, datetime
cwd = os.path.dirname(os.path.realpath(__file__))
##main loop
try:
    sett = open(cwd+'/measurements.xml', 'r')
    sett.close()
except IOError:
    sett = open(cwd+'/measurements.xml', 'w')
    sett.write("<measurements></measurements>")
    sett.close()
    
with open(cwd+'/measurements.xml', 'r') as sett:
    now = datetime.datetime.now()
    measurements = ET.parse(sett)
    root = measurements.getroot()
    root.append(ET.Element("plot",{'voltage':str(230),'current':str(5), 'variation':str(30), 'date': now.strftime("%m/%d/%Y %H:%M")}))
    settw = open (cwd + '/measurements.xml', 'wb')
    measurements.write(settw)
    settw.close()
