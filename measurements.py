import os, platform, numpy, datetime, time, threading, queue, math, xml.etree.ElementTree as ET, tkinter as tk, settingsHandler as sh
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
                           "pf":element.attrib['pf'],
                             "n": element.text\
                             })
        dataq.join()
msThread = threading.Thread(target=data)
msThread.start()
##main loop
x = wsigma = insig = sig =  0
cv_ = float(sh.readSettings()[2])
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
        notify = "False"
        now = datetime.datetime.now(datetime.timezone.utc)
        msFile = ET.parse(sett)
        root = msFile.getroot()
        msData = dataq.get()
        dataq.task_done()
        wsigma += float(msData["voltage"]) * float(msData["current"]) * float(msData["pf"])
        cv = float(msData["voltage"]) * float(msData["current"]) * float(msData["pf"])
        cv /= (wsigma/x)
        cv *= 100
        cv -= 100
        if (insig > 11):
            insig = 0
        if (cv >= cv_):
            sig += 1
        else:
            insig += 1
        if (sig >= 5 and insig <= 5):
            sig = insig = 0
            notify = "True"
        root.append(ET.Element("plot",{'voltage':str(msData["voltage"]),'current':str(msData["current"]),\
                                       'variation':str(cv), 'date': now.strftime("%m/%d/%Y %H:%M:%S"),\
                                       'n': str(x), 'mu': str(wsigma/x), 'notify': notify, 'pf':str(msData["pf"])}))
        with open (cwd + '/measurements.xml', 'wb') as settw:
            msFile.write(settw)
            settw.close()
    time.sleep(1)
