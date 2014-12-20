#! /usr/bin/python

"""
Server side: module to go with pySys.py
This contains the alerts and strings we want to search for. 
Also finds urls and double checks that the list is unique.
"""

import gnupg, re, ConfigParser

Config = ConfigParser.ConfigParser()
Config.read('pySys.cfg')
pySysSetting = ConfigSectionMap('SectionOne')  # dict of pySys settings
clientSetting = ConfigSectionMap('SectionTwo') # dict of Client settings
alertInfo = ConfigSectionMap('SectionThree')   # dict of email alert info
gnupgInfo = ConfigSectionMap('SectionFour')    # dict of gnupg info

gpg = gnupg.GPG(gnupghome=gnupgInfo['gnupghome']) # select directory of where gpg keys are stored
gpg.encoding = gnupgInfo['encoding']
recipient = gnupgInfo['email']    # select key through name/email assoc. w/secret key  

shellShockStrings = ['wget', 'download', 'curl','{','}']
sshBadStrings = ['POSSIBLE BREAK-IN ATTEMPT!','Failed password for','Accepted password','session opened for user',
                 'Invalid user','Received disconnect from','segfault','Segmentation fault',
                 'refused connect from','invalid user support from','new user','password changed',
                 'delete user','Accepted publickey','Did not recieve identification string from',
                 'authentication failure','FAILED su','Permission denied']

def findURL(data):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    return uniqueURL(urls)

def uniqueURL(urls):  # make sure no duplicate urls in same line of log
    found = set([])
    keep = []
    for url in urls:
        if url not in found:
            found.add(url)
            keep.append(url)
    return keep

def searchStrings(data):
    if any(k in data for k in (shellShockStrings)):
        return "[ATTEMPTED COMPROMISE OVER HTTP(S)] " + str(data)
    elif any(k in data for k in (sshBadStrings)):
        return "[ATTEMPTED COMPROMISE OVER SSH] " + str(data)
    else:
        return data 

def decryptData(data):
    return str(gpg.decrypt(str(data)))

def encryptData(data):
    return str(gpg.encrypt(data, recipient, always_trust=True))

def ConfigSectionMap(section):
    optionsDict = {}
    options = Config.options(section)
    for option in options:
        try:
            optionsDict[option] = Config.get(section, option)
            if optionsDict == -1:
                DebutPrint("skip: %s" % option)
        except:
            print "exception on %s" % option
            optionsDict[option] = None
    return optionsDict
