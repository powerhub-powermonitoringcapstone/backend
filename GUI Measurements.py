import tkinter as tk, threading, tkinter.messagebox as messagebox, subprocess, sys
import os, platform, numpy, datetime, time, threading, queue, math, xml.etree.ElementTree as ET, tkinter as tk, serial, settingsHandler as sh, portalocker, smtplib, ssl
cwd = os.path.dirname(os.path.realpath(__file__))
dataq = queue.Queue(1)
##savingthread = msdata = readoutsthread = datagtest1thread = 0
threadactive = [False,False,False,False,False] ##data collection, saving, readings update, data gathering-pseudo data collection, email subprogram
refreshrate = 3600/int(sh.readSettings()[9])
class LabeledEntry(tk.Entry):
    def __init__(self, master, label, **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.label = label
        self.on_exit()
        self.bind('<FocusIn>', self.on_entry)
        self.bind('<FocusOut>', self.on_exit)

    def on_entry(self, event=None):
        if self.get() == self.label:
            self.delete(0, tk.END)
            self.insert(0, "/dev/ttyACM0")

    def on_exit(self, event=None):
        if not self.get():
            self.insert(0, self.label)

##MAIN INTERFACE STARTS HERE
class viewchanger(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.viewf = tk.Frame(self.parent)
        self.butt1 = tk.Button(self.viewf, text="Measurements", command=self.measurements)
        self.butt1.pack(side="left")
        self.butt2 = tk.Button(self.viewf, text="Data Gathering Tests", command=self.datagathering)
        self.butt2.pack(side="left")
        self.butt3 = tk.Button(self.viewf, text="Email / Notifications", command=self.notifs)
        self.butt3.pack(side="left")
        self.butt4 = tk.Button(self.viewf, text="Server", command=self.teardown)
        self.butt4.pack(side="left")
        self.butt5 = tk.Button(self.viewf, text="About", command=self.about_)
        self.butt5.pack(side="left")
        self.viewf.pack()
        self.measurements()
    def teardown(self):
        try:
            measurements_.frame.destroy()
        except (NameError, AttributeError) as e:
            pass
        try:
            datagathering_.frame.destroy()
        except (NameError, AttributeError) as e:
            pass
        try:
            notifs_.frame.destroy()
        except (NameError, AttributeError) as e:
            pass
        try:
            about__.frame.destroy()
        except (NameError, AttributeError) as e:
            pass
    def measurements(self):
        global measurements_
        self.teardown()
        measurements_ = measurements(self.parent)
    def datagathering(self):
        global datagathering_
        self.teardown()
        datagathering_ = datagathering(self.parent)
    def notifs(self):
        global notifs_
        self.teardown()
        notifs_ = notifs(self.parent)
    def about_(self):
        global about__
        self.teardown()
        about__ = about(self.parent)
        
class measurements(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.readoutsframe = tk.Frame(self.frame)
        self.serialframe = tk.Frame(self.frame)
        self.serialentry = LabeledEntry(self.serialframe, label="Serial port here")
        self.start = tk.Button(self.serialframe, text="Start", command=connect)#self.update)
        self.stop = tk.Button(self.serialframe, text="Stop", command=stopconnect)
        self.serialentry.grid(row=0,column=0)
        self.start.grid(row=0, column=1)
        self.stop.grid(row=0, column=2)
        self.serialframe.pack(side="top")
        self.voltage = tk.Label(self.readoutsframe, text="Voltage: --- V")
        self.voltage.pack(anchor=tk.W)
        self.current = tk.Label(self.readoutsframe, text="Current: --- A")
        self.current.pack(anchor=tk.W)
        self.pf = tk.Label(self.readoutsframe, text="Power Factor: ---")
        self.pf.pack(anchor=tk.W)
        self.wattage = tk.Label(self.readoutsframe, text="Wattage: --- W")
        self.wattage.pack(anchor=tk.W)
        self.notification = tk.Label(self.readoutsframe, text="Insignificant Load")
        self.notification.pack(anchor=tk.W)
        self.readoutsframe.pack(anchor=tk.N)
        self.frame.pack()

class datagathering(tk.Frame):
    def __init__(self,parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.test1 = tk.Label(self.frame, text="Notification Framework Test")
        self.test1b = tk.Button(self.frame, text="Start", command=datagtest1start)
        self.test1bs = tk.Button(self.frame, text="Stop", command=datagtest1stop)
        self.test1.grid(row=0,column=0)
        self.test1b.grid(row=0,column=1)
        self.test1bs.grid(row=0,column=2)
        self.frame.pack(anchor=tk.NW)

class notifs(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.text = tk.Label(self.frame, text="Email / Notification Settings")
        self.text.pack(side="top")
        self.frame.pack()

class about(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.text = tk.Label(self.frame, text="PowerHub is a prototype created \n\
        for the partial fulfillment of the Capstone Experience Program.\n\n\
        Authors of the Study:\n - Jericho Rejuso, layout and design\n - Khalil Ubalde, lead programmer")
        self.text.pack(side="top")
        self.frame.pack()

def datacollection():
    global threadactive, savingthread
    port = serial.Serial(measurements_.serialentry.get(), 9600)
    savingthread = threading.Thread(target=datasaving)
    savingthread.start()
    threadactive[0] = True
    while threadactive[0] == True:
        if (port.read(1)==b'-'):
            stuff = port.read(36).decode('ascii').split('-')[0].split('\r\n')[1:6]
            try:
                voltage = float(stuff[0])
                current = float(stuff[1])
                pf = float(stuff[4])
                if (not math.isnan(voltage)):
                    dataq.put({"voltage": voltage,\
                               "current": current,\
                               "pf": pf,\
                               "date": datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y %H:%M:%S")\
                               })
                    dataq.join()
            except ValueError:
                pass
        port.flushInput()
    print("Data collection stopping ...")
    threadactive[1] = False
    sys.exit()

def email(function):
    global threadactive, msData
    threadactive[4] = True
    context = ssl.create_default_context()
    print("should send email")
    if (function == "peak"):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:            
            server.login("powerhubwebmaster@gmail.com", "elyagayle")
            server.sendmail("powerhubwebmaster@gmail.com", "powerhubwebmaster@gmail.com", "Subject: Load Peak Detected at " + msData["date"]\
                                        + "\n\n" + "This message is to notify that a significant load peak was detected at"+ msData["date"]+".\n\n"\
                                        "---------------------------\nSystem-generated message. Please do not reply.")
    threadactive[4] = False

def datagatheringtest1():
    global threadactive, msData, notify, refreshrate
    x = wsigma = 0
    threadactive[3] = True
    readoutsthread = threading.Thread(target=readouts)
    while threadactive[3] == True:
        msData = {"voltage":230,"current":100,"pf":1,"date": datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y %H:%M:%S")}
        x+=1
        if (x==1):
            readoutsthread.start()
        if (x % 10 == 0):
            notify = "True"
        else:
            notify = "False"
        if (notify == "True"):
            emailthread = threading.Thread(target=email, args=["peak"])
            emailthread.start()
        lock = False
        while lock == False:
            try:
                with portalocker.Lock(cwd + '/measurements.xml', 'r') as sett:   
                    msFile = ET.parse(sett)
                    root = msFile.getroot()
                    cv = msData["voltage"] * msData["current"] * msData["pf"]
                    wsigma += cv
                    try:
                        cv /= (wsigma/x)
                        cv *= 100
                        cv -= 100
                    except ZeroDivisionError:
                        pass
                    root.append(ET.Element("plot",{'voltage':str(msData["voltage"]),'current':str(msData["current"]),\
                                                   'variation':str(cv), 'date': msData["date"],\
                                                   'n': str(x), 'mu': str(wsigma/x), 'notify': str(notify), 'pf':str(msData["pf"])}))
                    with open (cwd + '/measurements.xml', 'wb') as settw:
                        msFile.write(settw)
                        settw.close()
                lock = True
            except portalocker.exceptions.LockException:
                pass
        time.sleep(refreshrate)
    print("Data gathering test 1 stopping ...")
    threadactive[2] = False
    sys.exit()

def datagtest1start():
    global datagtest1thread
    try:
        datagtest1thread.isAlive()
    except NameError:
        datagtest1thread = threading.Thread(target=datagatheringtest1)
        datagtest1thread.start()
    if (not datagtest1thread.isAlive()):
        try:
            datagtest1thread.start()
        except RuntimeError:
            datagtest1thread = threading.Thread(target=datagatheringtest1)
            datagtest1thread.start()
        
def datagtest1stop():
    global threadactive
    threadactive[3] = False

def readouts():
    global threadactive, msData, notify
    threadactive[2]=True
    while threadactive[2]:
        try:
            measurements_.voltage.config(text='Voltage: ' + str(msData['voltage']) + " V")
            measurements_.current.config(text='Current: ' + str(msData['current']) + " A")
            measurements_.pf.config(text='Power Factor: ' + str(msData['pf']))
            measurements_.wattage.config(text='Wattage: ' + str(msData['voltage'] * msData['current'] * msData['pf'])[:4] + " W")
            if (notify == "True"):
                measurements_.notification.config(text='Significant Load')
            else:
                measurements_.notification.config(text='Insignificant Load')
        except tk.TclError:
            pass
        time.sleep(0.25)
    print("Readouts stopping ...")
    sys.exit()

def datasaving():
    global threadactive, msthread, msData, readoutsthread, notify, refreshrate
    readoutsthread = threading.Thread(target=readouts)
    x = wsigma = insig = sig =  0
    cv_ = float(sh.readSettings()[2])
    threadactive[1] = True
    while threadactive[1]==True:
        notify = "False"

        if (dataq.full()):
            msData = dataq.get()
            dataq.task_done()
            x+=1
            if (x==1):
                readoutsthread.start()
            lock = False
            while lock == False:
                try:
                    with portalocker.Lock(cwd + '/measurements.xml', 'r+') as measfile:
                        meas = ET.parse(measfile)
                        root = meas.getroot()
                        cv = msData["voltage"] * msData["current"] * msData["pf"]
                        wsigma += cv
                        try:
                            cv /= (wsigma/x)
                            cv *= 100
                            cv -= 100
                        except ZeroDivisionError:
                            pass
                        if (insig > 11):
                            insig = 0
                        if (cv >= cv_):
                            sig += 1
                        else:
                            insig += 1
                        if (sig >= 8 and insig <= 5):
                            sig = insig = 0
                            notify = "True"
                        root.append(ET.Element("plot",{'voltage':str(msData["voltage"]),'current':str(msData["current"]),\
                                                       'variation':str(cv), 'date': msData["date"],\
                                                       'n': str(x), 'mu': str(wsigma/x), 'notify': str(notify), 'pf':str(msData["pf"])}))
                        with open (cwd + '/measurements.xml', 'wb') as settw:
                            meas.write(settw)
                    lock = True
                except portalocker.LockException:
                    pass
            time.sleep(refreshrate)
    print("Data saving stopping ...")
    threadactive[2] = False
    sys.exit()

def connect():
    global datathread, threadactive
    if os.geteuid == 0:
        permissions = subprocess.run("chmod 666 " + measurements_.serialentry.get(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        output = [permissions.returncode, permissions.stdout, permissions.stderr]
        if (output[0] == 1):
            messagebox.showerror("An error occured.", self.output[2])
    try:
        datathread.isAlive()
    except NameError:
        datathread = threading.Thread(target=datacollection)
        datathread.start()
    if (not datathread.isAlive()):
        try:
            datathread.start()
        except RuntimeError:
            datathread = threading.Thread(target=datacollection)
            datathread.start()        
def stopconnect():
    global threadactive
    threadactive[0] = False

class MainInterface(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry("600x350")
        self.parent.title("PowerHub v0.1 beta")
        viewchanger(self.parent)
if __name__ == '__main__':
    root = tk.Tk()
##    root.protocol("WM_DELETE_WINDOW", stopconnect)
    if os.geteuid() != 0:
##        wh = MainInterface(root)
##        root.mainloop()
##    else:
        root.withdraw()
        messagebox.showerror("You're not superuser", "Issues may arise with serial read-write permissions.")
        root.deiconify()
    wh = MainInterface(root)
    root.mainloop()
