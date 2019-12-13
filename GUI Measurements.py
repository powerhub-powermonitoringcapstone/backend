import tkinter as tk, threading, tkinter.messagebox as messagebox, subprocess, sys
import os, platform, numpy, datetime, time, threading, queue, math, xml.etree.ElementTree as ET, tkinter as tk, serial, settingsHandler as sh
cwd = os.path.dirname(os.path.realpath(__file__))
dataq = queue.Queue(1)
datathread = msthread = msdata = readoutsthread = 0
threadstop = [False,False,False] ##saving, data collection, readings update
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
        self.butt2 = tk.Button(self.viewf, text="Email / Notifications", command=self.settings)
        self.butt2.pack(side="left")
        self.butt3 = tk.Button(self.viewf, text="Server", command=self.teardown)
        self.butt3.pack(side="left")
        self.butt4 = tk.Button(self.viewf, text="About", command=self.about_)
        self.butt4.pack(side="left")
        self.viewf.pack()
        self.measurements()
    def teardown(self):
        try:
            measurements_.frame.destroy()
            set_.settings.destroy()
            about__.aboutfr.destroy()
        except (NameError, AttributeError) as e:
            pass
    def measurements(self):
        global measurements_
        self.teardown()
        measurements_ = measurements(self.parent)
    def settings(self):
        global set_
        self.teardown()
        set_ = sett(self.parent)
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

class sett(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.settings = tk.Frame(self.parent)
        self.settext = tk.Label(self.settings, text="HowerPub")
        self.settext.pack(side="top")
        self.settings.pack()

class about(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.aboutfr = tk.Frame(self.parent)
        self.abouttx = tk.Label(self.aboutfr, text="PowerHub is a prototype created \n\
        for the partial fulfillment of the Capstone Experience Program.")
        self.abouttx.pack(side="top")
        self.aboutfr.pack()

def data():
    global threadstop
    port = serial.Serial(measurements_.serialentry.get(), 9600)
    while threadstop[1] == False:
##        dataq.join()
##        dataq.put({"voltage": 230,\ ## Debugging Latency Tester
##                   "current": 4,\
##                   "pf": 1,\
##                   "date": datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y %H:%M:%S")\
##                   }) 
##        time.sleep(1) ##End of Latency Tester
        if (port.read(1)==b'-'):
            dataq.join()
            stuff = port.read(36).decode('ascii').split('-')[0].split('\r\n')[1:6]
            port.flushInput()
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
            except ValueError:
                pass
    sys.exit()
def readouts():
    global threadstop, msData
    while threadstop[2]==False:
        measurements_.voltage.config(text='Voltage: ' + str(msData['voltage']) + " V")
        measurements_.current.config(text='Current: ' + str(msData['current']) + " A")
        measurements_.pf.config(text='Power Factor: ' + str(msData['pf']))
        measurements_.wattage.config(text='Wattage: ' + str(msData['voltage'] * msData['current'] * msData['pf'])[:4] + " W")
        time.sleep(1)
    sys.exit()
def saving():
    global threadstop, msthread, msData, readoutsthread
    msthread = threading.Thread(target=data)
    msthread.start()
    readoutsthread = threading.Thread(target=readouts)
    x = wsigma = insig = sig =  0
    cv_ = float(sh.readSettings()[2])
    while threadstop[0]==False:
        if (dataq.full()):
            msData = dataq.get()
            dataq.task_done()
            x+=1
            if (x==1):
                readoutsthread.start()
            with open(cwd+'/measurements.xml', 'r') as sett:
                notify = "False"
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
                    msFile.write(settw)
                    settw.close()
                time.sleep(1)
    threadstop[1] = True
    threadstop[2] = True
    sys.exit()



class connect():
    def __init__(self):
        global datathread
        self.permissions = subprocess.run("chmod 666 " + measurements_.serialentry.get(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        self.output = [self.permissions.returncode, self.permissions.stdout, self.permissions.stderr]
        if (self.output[0] == 1):
            messagebox.showerror("An error occured.", self.output[2])
        else:
            if (datathread == 0):
                datathread = threading.Thread(target=saving)
            if (not datathread.isAlive()):
                datathread = threading.Thread(target=saving)
                datathread.start()
def stopconnect():
    global threadstop
    threadstop[0] = True

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
    if os.geteuid() == 0:
        wh = MainInterface(root)
        root.mainloop()
    else:
        root.withdraw()
        messagebox.showerror("You're not superuser", "Superuser privileges are required in order to start measurements")
