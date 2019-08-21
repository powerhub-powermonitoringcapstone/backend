import xml.etree.ElementTree as ET 
import os, platform, numpy, datetime, time, threading, queue, math
cwd = os.path.dirname(os.path.realpath(__file__))
rawdata = queue.Queue(360)

##implement as separate thread
def data():
    while True:
        with open(cwd+'/data.xml', 'r') as sett:
            stuff = ET.parse(sett)
            root = stuff.getroot()
            for element in root.findall("./dummy"):
                rawdata.put({"voltage": element.attrib['voltage'],\
                             "current":element.attrib['current'],\
                             "n": element.text\
                             })
        rawdata.join()
        time.sleep(0.5)
msThread = threading.Thread(target=data)
msThread.start()
##main loop
try:
    sett = open(cwd+'/measurements.xml', 'r')
    sett.close()
except IOError:
    sett = open(cwd+'/measurements.xml', 'w')
    sett.write("<measurements></measurements>")
    sett.close()

while True:
    with open(cwd+'/measurements.xml', 'r') as sett:
        now = datetime.datetime.now()
        msFile = ET.parse(sett)
        root = msFile.getroot()
        msData = rawdata.get()
        rawdata.task_done()
        root.append(ET.Element("plot",{'voltage':str(msData["voltage"]),'current':str(msData["current"]), 'variation':str(30), 'date': now.strftime("%m/%d/%Y %H:%M:%S")}))
        settw = open (cwd + '/measurements.xml', 'wb')
        msFile.write(settw)
        settw.close()
