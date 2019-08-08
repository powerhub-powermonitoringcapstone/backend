import time, math, os
cwd = os.path.dirname(os.path.realpath(__file__))#take note this doesnt work when os.chdir() is called!
y = x = 0
##file = open(cwd + '/etits.txt', 'r+')
while True:
    time.sleep(0.0166666666667)
    x += 0.0166666666667
    y = math.sin(x)
    v = 325.2691193 * y
##    file = open(cwd + '/etits.txt', 'a')
##    file.write(str(v)+'\n')
##    file.close()
    print (v)
    return(v)
