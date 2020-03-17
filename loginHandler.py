##from xml.dom import minidom
import platform, numpy, datetime, xml.etree.ElementTree as ET, hashlib, uuid, settingsHandler as sh, time, portalocker
cwd = '/home/capstone/codebase'
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
try:
    open(cwd + '/logins.xml', 'r')
except FileNotFoundError:
    with open (cwd+ '/logins.xml', 'w') as filew:
        filew.write('<login></login>')
##def mntnLogin():
##    root = ET.parse(cwd + '/logins.xml').getroot()
##    found = root.findall(".logind")[19:]
##    for elem in found:
##        root.remove(elem)
##    data.write(cwd + '/logins.xml')
def isLogin(fgt):
    lock = False
    while lock == False:
        try:
            with portalocker.Lock(cwd + '/logins.xml', 'r+') as loginfile:
                data = ET.parse(loginfile)
                root = data.getroot()
                found = root.findall(".logind")[20:]
                for elem in found:
                    root.remove(elem)
                data.write(cwd + '/logins.xml')
                found = root.find(".//logind/[@fgt={}]".format("\""+str(fgt)+"\""))
            lock = True
        except portalocker.exceptions.LockException:
            pass
    if (found == None):
        return False
    else:
        return True   
def clearLogins():
    lock = False
    while lock == False:
        try:
            with portalocker.Lock(cwd + '/logins.xml', 'r+') as loginfile:
                data = ET.parse(loginfile)
                root = data.getroot()
                found = root.findall(".logind")
                for elem in found:
                    root.remove(elem)
                with open (cwd + '/logins.xml', 'wb') as filew:
                    data.write(cwd + '/logins.xml')
            lock = True
        except portalocker.exceptions.LockException:
            pass 
def newLogin(fgt):
    lock = False
    while lock == False:
        try:
            with portalocker.Lock(cwd + '/logins.xml', 'r+') as loginfile:
                data = ET.parse(loginfile)
                root = data.getroot()
                found = root.findall(".logind")[20:]
                for elem in found:
                    root.remove(elem)
                fgt = str(fgt)
                found = root.find(".//logind/[@fgt={}]".format("\""+fgt+"\""))
                if (found == None):
                    root.append(ET.Element("logind", {'fgt': fgt}))
                else:
                    found.set('fgt', fgt)
                data.write(cwd + '/logins.xml')
            lock = True
        except portalocker.exceptions.LockException:
            pass 

        
def authenticate(passkey, fgt):
    root = ET.parse(cwd + '/pvt.xml').getroot()
    localkey = str(root.find(".private").attrib['key'])
    localsalt = str(root.find(".private").attrib['salt'])
    auth = passkey + localsalt
    auth = str(hashlib.sha256(auth.encode('utf-8')).hexdigest())
    if (auth == localkey):
        newLogin(fgt)
        return ("True")
    else:
        return ("False")
def changeKey(passkey, fgt):
    localsalt = str(uuid.uuid4())
    localkey = str(hashlib.sha256((str(passkey) + localsalt).encode('utf-8')).hexdigest())
    if (isLogin(fgt) or sh.readSettings()[0] == "False"):
        try:
            with portalocker.Lock(cwd + '/pvt.xml', 'r') as authfile:
                data = ET.parse(authfile)
                root = data.getroot()
                found = root.find("./private")
                found.set('key', localkey)
                found.set('salt', localsalt)
                data.write(cwd + '/pvt.xml')
                clearLogins()                
            lock = True
        except portalocker.exceptions.LockException:
            pass         
        return ("True")
    else:
        return ("False")
    
