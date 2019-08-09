import time, math, os, threading, queue, numpy
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
measurements = queue.Queue(120)
def peakVoltage():
        measarray = []
        if (measurements.full()):
            while (not measurements.empty()):
##                print(measurements.qsize())
                measarray.append(measurements.get())
                measurements.task_done()
            return(max(measarray)/math.sqrt(2))
def measure():
    x = 0
    ##file = open(cwd + '/etits.txt', 'r+')
    while True:
        time.sleep(0.0166666666667)
        x += 0.0166666666667
        y = math.sin(x)
        v = 325.2691193 * y
        measurements.put(v)
        if (x%1 == 0):
            measurements.join()
        if (measurements.full()):
            return(peakVoltage())
            break
##    file = open(cwd + '/etits.txt', 'a')
##    file.write(str(v)+'\n')
##    file.close()
##measThread = thread()
##measThread.start()


        
        
