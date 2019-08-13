import xml.etree.ElementTree as ET
import os, platform, numpy, datetime, time, threading, queue, math
cwd = os.path.dirname(os.path.realpath(__file__))
rawdata = queue.Queue(360)

##implement as separate thread
def peakVoltage():
    measarray = []
    if (rawdata.full()):
        while (not rawdata.empty()):
            measarray.append(rawdata.get())
            rawdata.task_done()
        return(max(measarray)/math.sqrt(2), min(measarray)/math.sqrt(2))
def measure():
    x = 0
    while True:
        time.sleep(0.0166666666667)
        x += (0.0166666666667)
        y = math.sin(x)
        v = 325.2691193 * y
        rawdata.put(v)
##        if (x%2 == 0):
##            rawdata.join()
        if (rawdata.full()):
            return(peakVoltage())
            break
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
    root.append(ET.Element("plot",{'voltage':str(230),'current':str(5), 'variation':str(30), 'date': now.strftime("%m/%d/%Y %H:%M:%S")}))
    settw = open (cwd + '/measurements.xml', 'wb')
    measurements.write(settw)
    settw.close()
