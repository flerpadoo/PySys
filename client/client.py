#!/usr/bin/python
import os, socket, sys, re, datetime
from pyWch import *
# examples of some parsing keywords
shellShockStrings = ['wget', 'download', 'curl','{','}']
sshBadStrings = ['POSSIBLE BREAK-IN ATTEMPT!','Failed password for','Accepted password','session opened for user']
localHostName = str(socket.gethostname())
remoteHostName = "hostname.com" #str(urllib.request.urlopen('http://blablabla/secretconninfo.txt').read()) <-- for obfuscation
remotePort = 50007
consoleOutputOn = True
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
		socksize = 2048
		conn.connect((remoteHostName, remotePort))
		conn.send(data)
		conn.close()
	except:
		pass
		showOutput("This shit isn't going anywhere...")
def findURL(data):
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
	return urls
def callback(filename, lines):
	for line in lines:
		if any(k in line for k in (shellShockStrings)):
			lineMsg = "[ATTEMPTED COMPROMISE OVER HTTP(S)] " + line
			showOutput(lineMsg)	
			sendDaterz(lineMsg)
			f = open(outFile, 'a')
			f.write(lineMsg)
			urls = findURL(line) 
			for url in urls:
				curlOutFile = "dl/evil@" + getCurrentDateTime() + ".snaggled"
				downloadMsg = "Downloading file @ " + url + " and storing it under " + curlOutFile
				showOutput(downloadMsg)
				sendDaterz(downloadMsg)
				f.write(downloadMsg)
				os.system("curl -s " + url + " -o " + curlOutFile) 
			f.close()
		if any (k in line for k in (sshBadStrings)):
			lineMsg = "[ATTEMPTED COMPROMISE OVER SSH] " + line
			showOutput(lineMsg)
			sendDaterz(lineMsg)
			f = open(outFile, 'a')
			f.write(lineMsg)
			urls = findURL(line)
		else:
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
