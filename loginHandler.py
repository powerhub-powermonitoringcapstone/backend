##from xml.dom import minidom
import platform, numpy, datetime, xml.etree.ElementTree as ET, hashlib, uuid, settingsHandler as sh
cwd = '/home/capstone/codebase'
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
try:
    open(cwd + '/logins.xml', 'r')
except FileNotFoundError:
    with open (cwd+ '/logins.xml', 'w') as filew:
        filew.write('<login></login>')
def mntnLogin():
    with open(cwd + '/logins.xml', 'r') as file:
        file.seek(0)
        data = ET.parse(file)
        root = data.getroot()
        found = root.findall(".logind")[19:]
        for elem in found:
            root.remove(elem)
        with open (cwd + '/logins.xml', 'wb') as filew:
            data.write(filew)
def isLogin(fgt):
    mntnLogin()
    with open(cwd + '/logins.xml', 'r') as file:
        file.seek(0)
        data = ET.parse(file)
        root = data.getroot()
        found = root.find(".//logind/[@fgt={}]".format("\""+str(fgt)+"\""))
        if (found == None):
            return False
        else:
            return True
        
def clearLogins():
    with open (cwd + '/logins.xml', 'w') as filew:
        filew.write('<login></login>')
def newLogin(fgt):
    mntnLogin()
    with open(cwd + '/logins.xml', 'r') as file:
        file.seek(0)
        data = ET.parse(file)
        root = data.getroot()
        fgt = str(fgt)
##        now = datetime.datetime.utcnow()
##        nowString = (now + datetime.timedelta(minutes = 10)).strftime("%m/%d/%Y %H:%M")
        found = root.find(".//logind/[@fgt={}]".format("\""+fgt+"\""))
        if (found == None):
            root.append(ET.Element("logind", {'fgt': fgt}))#{'expires': nowString, 'fgt': fgt, 'interval':"10"}))
        else:
            found.set('fgt', fgt)
        with open (cwd + '/logins.xml', 'wb') as filew:
            data.write(filew)
        
def authenticate(passkey, fgt):
    with open(cwd + '/pvt.xml', 'r') as file:
        file.seek(0)
        data = ET.parse(file)
        root = data.getroot()
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
        with open(cwd + '/pvt.xml', 'r') as file:
            file.seek(0)
            data = ET.parse(file)
            root = data.getroot()
            found = root.find("./private")
            found.set('key', localkey)
            found.set('salt', localsalt)
            with open (cwd + '/pvt.xml', 'wb') as filew:
                data.write(filew)
        return ("True")
    clearLogins()
    
