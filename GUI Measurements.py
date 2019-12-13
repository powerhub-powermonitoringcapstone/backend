import tkinter as tk, threading, tkinter.messagebox as messagebox, subprocess, sys
import os, platform, numpy, datetime, time, threading, queue, math, xml.etree.ElementTree as ET, tkinter as tk, serial, settingsHandler as sh
cwd = os.path.dirname(os.path.realpath(__file__))
dataq = queue.Queue(1)
datathread = msthread = 0
threadstop = [False,False] ##saving, data collection
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
    def update(self):
        self.ozawa.config(text="Node name: " + self.req.json()['nodename'])
        self.name2.config(text="Node type: " + self.req.json()['nodetype'])
        print (self.req.text)

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
    port = serial.Serial('/dev/ttyACM0', 9600)
    while threadstop[1] == False:
        dataq.join()
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
                               })
            except ValueError:
                pass
    sys.exit()
def saving():
    global threadstop, msthread
    msthread = threading.Thread(target=data)
    msthread.start()
    x = wsigma = insig = sig =  0
    cv_ = float(sh.readSettings()[2])
    while threadstop[0]==False:
        if (dataq.full()):
            msData = dataq.get()
            dataq.task_done()
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
                print("yuh")
                measurements_.voltage.config(text='Voltage: ' + str(msData['voltage']) + " V")
                measurements_.current.config(text='Current: ' + str(msData['current']) + " A")
                measurements_.pf.config(text='Power Factor: ' + str(msData['pf']))
                measurements_.wattage.config(text='Wattage: ' + str(msData['voltage'] * msData['current'] * msData['pf']) + " W")
                root.append(ET.Element("plot",{'voltage':str(msData["voltage"]),'current':str(msData["current"]),\
                                               'variation':str(cv), 'date': now.strftime("%m/%d/%Y %H:%M:%S"),\
                                               'n': str(x), 'mu': str(wsigma/x), 'notify': notify, 'pf':str(msData["pf"])}))
                with open (cwd + '/measurements.xml', 'wb') as settw:
                    msFile.write(settw)
                    settw.close()
    threadstop[1] = True
    sys.exit()



class connect():
    def __init__(self):
        global datathread
        self.permissions = subprocess.run("chmod 666 " + measurements_.serialentry.get(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        self.output = [self.permissions.returncode, self.permissions.stdout, self.permissions.stderr]
        if (self.output[0] == 1):
            messagebox.showerror("An error occured.", output[2])
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
