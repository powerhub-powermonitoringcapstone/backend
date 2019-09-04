## TKINTERGRAPH
## DEPRECATED
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os, platform, matplotlib, matplotlib.pyplot, _thread, numpy
import graphingHandler as gh
csvArray = gh.getData("All")
length = csvArray.shape[0]
def adjustGraph(m):
    if (m=="Voltage"):
        if (voltage.cget("relief")=="sunken"):
            voltage.config(relief="raised")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
        else:
            voltage.config(relief="sunken")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
    if (m=="Wattage"):
        if (wattage.cget("relief")=="sunken"):
            wattage.config(relief="raised")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
        else:
            wattage.config(relief="sunken")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
    if (m=="Mean Wattage"):
        if (mwattage.cget("relief")=="sunken"):
            mwattage.config(relief="raised")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
        else:
            mwattage.config(relief="sunken")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
    if (m=="Notification Triggered"):
        if (trigger.cget("relief")=="sunken"):
            trigger.config(relief="raised")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
        else:
            trigger.config(relief="sunken")
            for c in ax1.get_lines():
                if(str(c)[7:-1] == m):
                    c.set_visible(not c.get_visible())
                    graph1.draw()
def shiftGraph():
    print(gh.getData("ProgStart"))
mainWindow = tk.Tk()
mainWindow.title("Grapher Subprogram")
matplotlib.pyplot.ion()
figure1 = plt.Figure(dpi=100,figsize=(4,3))
ax1 = figure1.add_subplot(111)
graph1 = FigureCanvasTkAgg(figure1, mainWindow)
ax1.set_title('Grapher', fontsize=16)
ax1.axis([1, length, float(csvArray[-1, 3])/2, float(csvArray[-1, 3])*2])
ax1.grid()
ax1.plot( [ float(x) for x in list(csvArray[:, 0]) ], [ float(x) for x in list(csvArray[:, 2]) ], label = "Voltage")
ax1.plot( [ float(x) for x in list(csvArray[:, 0]) ], [ float(x) for x in list(csvArray[:, 3]) ], label = "Wattage")
ax1.plot( [ float(x) for x in list(csvArray[:, 0]) ], [ float(x) for x in list(csvArray[:, 4]) ], label = "Mean Wattage")
ax1.plot( [ float(x) for x in list(csvArray[:, 0]) ], [ float(x) for x in list(csvArray[:, 7]) ], label = "Notification Triggered")
graph1.get_tk_widget().grid(sticky=tk.N,row=0,column=0)
buttons = tk.Frame()
voltage = tk.Button(buttons, text="Voltage", relief="sunken", command=lambda m="Voltage": adjustGraph(m))
wattage = tk.Button(buttons, text="Wattage", relief="sunken", command=lambda m="Wattage": adjustGraph(m))
mwattage = tk.Button(buttons, text="Mean Wattage", relief="sunken", command=lambda m="Mean Wattage": adjustGraph(m))
trigger = tk.Button(buttons, text="Trigger", relief="sunken", command=lambda m="Notification Triggered": adjustGraph(m))
left = tk.Button(buttons, text="<-", command=shiftGraph)
right = tk.Button(buttons, text="->", command=shiftGraph)
dateBox = tk.Listbox(buttons)
left.pack(in_=buttons, side=tk.LEFT)
right.pack(in_=buttons, side=tk.LEFT)
voltage.pack(in_=buttons, side=tk.LEFT)
wattage.pack(in_=buttons, side=tk.LEFT)
mwattage.pack(in_=buttons, side=tk.LEFT)
trigger.pack(in_=buttons, side=tk.LEFT)
buttons.grid(sticky=tk.NW,row=1,column=0)
#print (float(x) for x in list(csvArray[:,0]))
#plt.plot( [ float(x) for x in list(csvArray[:, 0]) ], [ float(x) for x  , label = "Voltage")


