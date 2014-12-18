#!/usr/bin/python
import base64, os, time, sys, termcolor, smtplib, datetime
from pySysLib import *
from socket import *
myHost = ''
myPort = 50007
alertStack = []
activeChildren = []
registeredHosts = []
alertHeader = "pySys Alert Stack\n============================\n"
alertFooter = "\n===========================\nSent at "
def writeToLog(s):
	sysLogOutFile = 'log/sysLogOutFile'
	f = open(sysLogOutFile,'a')
	f.write(s)
	f.close()
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)
def now():
    return time.ctime(time.time())
def getCurrentDateTime():
    currentDateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return currentDateTime
def printAlert(s, level):
	if level == 5:
		print termcolor.colored(s, 'red')
def reapChildren():
    while activeChildren:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid: break
        activeChildren.remove(pid)
def handleClient(connection, address):
    #time.sleep(5) # simulate a blocking activity
    while True:
        data = decryptData(connection.recv(2048)) 
        if not data:
		break
	lineMsg = searchStrings(data)
	if str(address[0]) != "HOME IP ADDRESS":
		lineMsg = "[ALERT: UNKNOWN ORIGIN - DIRECT][" + str(now()) + "] " + str(address[0])+":"+str(address[1]) + " ==> " + str(lineMsg)
		writeToLog(lineMsg)
		printAlert(lineMsg, 5)
	if str(address[0]) == "184.172.7.234":
		lineMsg = "[" + str(now()) + "] " + str(address[0])+":"+str(address[1]) + " ==> " + str(lineMsg)
		writeToLog(lineMsg)
		print(lineMsg)
	            	if "COMPROMISE OVER HTTP(S)" in lineMsg:
                urls = findURL(data)
                for url in urls:
                    	curlOutFile = "dl/evil@" + getCurrentDateTime() + ".snaggled"
                    	downloadMsg = "Downloading file @ " + url + " and storing it under " + curlOutFile
                    	writeToLog(downloadMsg)
                    	print(downloadMsg)
                    	messageReturn = "curl -s " + url + " -o " + curlOutFile
                    	connection.send(encryptData(messageReturn))
                    	connection.send(encryptData(curlOutFile))
                    	downloadFile(connection, curlOutFile) 
            	messageReturn = "Done with line"
            	connection.send(encryptData(messageReturn))
	if "ALERT" in lineMsg:
		global alertStack
		alertStack += [lineMsg]
		if len(alertStack) >= 5:
			print 'Sending Alert Email!'
			emailer(alertHeader + '\n'.join(alertStack) + alertFooter + now())
    connection.close()
    os._exit(0)
def downloadFile(connection, curlOutFile): # receives the file using binary through sockets
    f = open(curlOutFile, 'wb')
    l = connection.recv(1024)
    while (l):
        f.write(l)
        l = connection.recv(1024)
        if 'finish' in l:
            break
    f.close()
def emailer(messageContent):
	fromAddress = 'pySysLog'
	toAddress  = 'yourtoemail@whatever.com'
	username = 'yourfromemail@gmail.com'
	password = base64.b64decode('XXXXXXXXXXXXXXXXXXXXXXXXX')
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromAddress,toAddress,messageContent)
	server.quit()
	fromAddress, toAddress, username, password = '','','',''
def dispatcher():
    while True:
        connection, address = sockobj.accept()
        print 'Server connected to by ', address,
        print 'at', now()
        reapChildren()
        childPid = os.fork()
        if childPid == 0:
            handleClient(connection, address)
        else:
            activeChildren.append(childPid)
try:
	dispatcher()
except (KeyboardInterrupt, SystemExit):
	print "\nClosing Connection..."
	sockobj.close()
	time.sleep(3)
	print "Goodbye!"
	exit
