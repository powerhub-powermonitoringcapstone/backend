## POWERHUB MAIN PROGRAM CODE (C) 2019
import tkinter as tk
def showMain():
    mainf = tk.Frame(subf,height=508, width=800)
    demo = tk.Label(mainf, text="Fuck you all!")
    demo.grid(row=0, column=0)
    if ({1:True, 0:False}[demo.winfo_exists()]):
        pass
    
    mainf.pack()
    
main = tk.Tk()
main.title("PowerHub Consumer Interface")
main.geometry("800x540")
subf = tk.Frame(main, height=508, width=800)
##subf.geometry("800x518")
textbox = tk.Label(subf, text="Hello World!")
textbox.pack()
selector = tk.Frame(main,height=32, width=800)
b0 = tk.Button(selector, text="Main", command=showMain)
b1 = tk.Button(selector, text="Settings")
b2 = tk.Button(selector, text="Security")
b3 = tk.Button(selector, text="About")
for r in range (4):
    exec("b"+str(r)+".grid(row=0,column="+str(r)+")")
subf.grid(row=0,column=0)
selector.grid(row=1,column=0)
tk.mainloop()

