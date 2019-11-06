import os, platform, numpy, datetime, time, threading, queue, math, xml.etree.ElementTree as ET, tkinter as tk, settingsHandler as sh, serial
cwd = os.path.dirname(os.path.realpath(__file__))
dataq = queue.Queue(1)
port = serial.Serial('/dev/ttyACM0', 9600) ## first USB port
##actual measuring
def data():
    n = 0
    while True:
        n += 1
        if (port.read(1)==b'-'):
            stuff = port.read(36).decode('ascii').split('-')[0].split('\r\n')[1:6]
            try:
                voltage = float(stuff[0])
                current = float(stuff[1])
                pf = float(stuff[4])
                dataq.put({"voltage": voltage,\
                           "current": current,\
                            "pf": pf,\
                            "n": n\
                           })
            except ValueError:
                pass
        dataq.join()                
##        with open(cwd+'/data.xml', 'r') as sett:
##            stuff = ET.parse(sett)
##            root = stuff.getroot()
##            for element in root.findall("./dummy"):
##                dataq.put({"voltage": element.attrib['voltage'],\
##                             "current":element.attrib['current'],\
##                           "pf":element.attrib['pf'],
##                             "n": element.text\
##                             })
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
    if (dataq.full()):
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
            try:
                cv /= (wsigma/x)    
            except ZeroDivisionError:
                pass
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
