import socket
import sys

def sendTCP(address, port, message) :

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Connect the socket to the port on the server given by the caller
	server_address = (address, port)
	print ('connecting to ' + server_address[0] + ' port ' + str(server_address[1]))
	sock.connect(server_address)
	try:

		sock.send(message.encode('utf-8'))
	finally:
		sock.close()


def JSONMessageStart(type) :
	return "{\""+ type + "\":{"
	
def JSONMessageEnd(partialJSON) :
	return partialJSON + "}}"
	
def addField2JSON(partialJSON, fieldName, fieldValue, last) :
	if(last == 0) :
		lineTerm = ","
	else :
		lineTerm = ""
	return partialJSON + "\"" + fieldName + "\"		:"  + str(fieldValue) + lineTerm
	
def addStrField2JSON(partialJSON, fieldName, fieldValue, last) :
	if(last == 0) :
		lineTerm = ","