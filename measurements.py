import os, platform, numpy, datetime, time, threading, queue, math, xml.etree.ElementTree as ET 
cwd = os.path.dirname(os.path.realpath(__file__))
dataq = queue.Queue(1)
##actual measuring
def data():
    while True:
        with open(cwd+'/data.xml', 'r') as sett:
            stuff = ET.parse(sett)
            root = stuff.getroot()
            for element in root.findall("./dummy"):
                dataq.put({"voltage": element.attrib['voltage'],\
                             "current":element.attrib['current'],\
                             "n": element.text\
                             })
        dataq.join()
msThread = threading.Thread(target=data)
msThread.start()
##main loop
x = 0
try:
    sett = open(cwd+'/measurements.xml', 'r')
    sett.close()
except IOError:
    sett = open(cwd+'/measurements.xml', 'w')
    sett.write("<measurements></measurements>")
    sett.close()
while True:
    x+=1
    with open(cwd+'/measurements.xml', 'r') as sett:
        now = datetime.datetime.now()
        msFile = ET.parse(sett)
        root = msFile.getroot()
        msData = dataq.get()
        dataq.task_done()
        root.append(ET.Element("plot",{'voltage':str(msData["voltage"]),'current':str(msData["current"]), 'variation':str(30), 'date': now.strftime("%m/%d/%Y %H:%M:%S"), 'n': str(x)}))
        with open (cwd + '/measurements.xml', 'wb') as settw:
            msFile.write(settw)
            settw.close()
    time.sleep(1)
