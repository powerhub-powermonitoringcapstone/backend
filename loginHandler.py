##from xml.dom import minidom
import platform, numpy, datetime, xml.etree.ElementTree as ET, hashlib, uuid, settingsHandler as sh
cwd = '/home/capstone/codebase'
setArray = numpy.empty((30), dtype=object)
setWarray = numpy.empty((30), dtype=object)
try:
    open(cwd + '/logins.xml', 'r')
except FileNotFoundError:
    with open (cwd+ '/logins.xml', 'w') as settw:
        settw.write('<login></login>')
def mntnLogin():
    with open(cwd + '/logins.xml', 'r') as sett:
        sett.seek(0)
        settings = ET.parse(sett)
        root = settings.getroot()
        found = root.findall(".logind")[19:]
        for elem in found:
            root.remove(elem)
        with open (cwd + '/logins.xml', 'wb') as settw:
            settings.write(settw)
            settw.close()
        sett.close()
def isLogin(fgt):
    mntnLogin()
    with open(cwd + '/logins.xml', 'r') as sett:
        sett.seek(0)
        settings = ET.parse(sett)
        root = settings.getroot()
##        now = datetime.datetime.utcnow()
##        nowString = now.strftime("%m/%d/%Y %H:%M")
        found = root.find(".//logind/[@fgt={}]".format("\""+str(fgt)+"\""))
        if (found == None):
            return False
        else:
            return True
##            if (True):datetime.datetime.strptime(found.attrib['expires'], '%m/%d/%Y %H:%M') < now):
##                root.remove(found)
##                return(False)
##            else:
##                return(True)
##        with open (cwd + '/logins.xml', 'wb') as settw:
##            settings.write(settw)
        sett.close()
def clearLogins():
    with open (cwd + '/logins.xml', 'w') as sett:
        sett.seek(0)
        sett.write('<login></login>')
        sett.close()
def newLogin(fgt):
    mntnLogin()
    with open(cwd + '/logins.xml', 'r') as sett:
        sett.seek(0)
        settings = ET.parse(sett)
        root = settings.getroot()
        fgt = str(fgt)
##        now = datetime.datetime.utcnow()
##        nowString = (now + datetime.timedelta(minutes = 10)).strftime("%m/%d/%Y %H:%M")
        found = root.find(".//logind/[@fgt={}]".format("\""+fgt+"\""))
        if (found == None):
            root.append(ET.Element("logind", {'fgt': fgt}))#{'expires': nowString, 'fgt': fgt, 'interval':"10"}))
        else:
            found.set('fgt', fgt)
        with open (cwd + '/logins.xml', 'wb') as settw:
            settings.write(settw)
            settw.close()
        sett.close()
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
        file.close()
def changeKey(passkey, fgt):
    clearLogins()
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
                filew.close()
        return ("True")


    
    
                
