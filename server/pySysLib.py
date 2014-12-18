#! /usr/bin/python

"""
Server side: module to go with pySys.py
This contains the alerts and strings we want to search for. 
Also finds urls and double checks that the list is unique.
"""

import gnupg, re

gpg = gnupg.GPG(gnupghome='/.gnupg') # select directory of where gpg keys are stored
gpg.encoding = 'utf-8'
recipient = "client@client.com"    # select key through name/email assoc. w/secret key  

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
