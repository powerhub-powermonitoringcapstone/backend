## DATA LOGGING AND GRAPHING HANDLER SUBPROGRAM
## ALL CODE (C)2019
import os, platform, csv, numpy, datetime
cwd = os.path.dirname(os.path.realpath(__file__))
if (platform.system()[:7] == 'Windows'): 
    csvfile = open(cwd + '\\csv.csv', 'r+')
else:
    csvfile = open(cwd + '/csv.csv', 'r+')
csvwriter = csv.writer(csvfile, dialect='excel',)
csvArray = numpy.empty((2), dtype=object)
def getData(n): ## All -> all values, ProgStart -> every time program has started, any timestamp -> everything from that timestamp on
    csvfile.seek(0)
    csvSeek=rowsParsed=0
    data = csvfile.readlines()
    csvArray = instances = numpy.empty((2), dtype=object)
    if (n == "All"):
        index = int([i for i, s in enumerate(data) if 'program started' in s][-1])+2
        csvparser = csv.reader(data[index:], dialect='excel',)
        for row in csvparser:
            try:
                csvArray = numpy.vstack((csvArray, numpy.array(row)))
            except ValueError:
                csvArray = numpy.array(row)
        return csvArray
    else:
        if (n == "ProgStart"):
            for line in data:
                if ('program started' in line):
                    try:
                        instances = numpy.vstack((instances, numpy.array(line)))
                    except ValueError:
                        instances = numpy.array(line)
            return instances
        else:
            index = int([i for i, s in enumerate(data) if n in s][-1])+2
            csvparser = csv.reader(data[index:], dialect='excel',)
            csvArray = numpy.empty((2), dtype=object)                           ## NEEDS
            for row in csvparser:                                                         ## WORK ##
                if ('program started' in row):
                    pass
                else:
                    try:
                        csvArray = numpy.vstack((csvArray, numpy.array(row)))
                    except ValueError:
                        csvArray = numpy.array(row)                    
            return csvArray
def wrtData(n,c,v,w,mu,cv,d,ntf):
    csvwriter.writerow([n, c, v, w, mu, cv, d, ntf])
    csvfile.flush()
    ## dito lahat ng data write
def intData(n,c,v,w,mu,cv,d,ntf):
    csvwriter.writerow(['program started', str(datetime.datetime.now())])
    csvwriter.writerow(['n', 'c', 'v', 'w', 'mean', 'cv', 'timestamp', 'notified?'])
    csvwriter.writerow([n, c, v, w, mu, cv, d, ntf])
    csvfile.flush()
    ## data write and initialize
