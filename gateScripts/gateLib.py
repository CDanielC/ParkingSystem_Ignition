from java.util import Date
from java.util import Calendar

def handleTCPGateRequest() :
	tag = system.tag.read("Gate");
	json_str = tag.value
	
	json = system.util.jsonDecode(json_str)
	
	if "gateEntryRequest" in json_str : 
		project.GateLib.handleGateEntryRequest(json)
		
	elif "gateExitRequest" in json_str :
		project.GateLib.handleGateExitRequest(json)
		
	elif "paymentCompletedMessage" in json_str:
		project.GateLib.handlePaymentCompletedMessage(json)
		
	elif "openGateRequest" in json_str:
		project.GateLib.handleOpenGateRequest(json)


def gateReply(message) :
	baseTagName = "SystemTag/Proxy"
	address = project.TagUtil.readComplexTag(baseTagName, "address")
	port = project.TagUtil.readComplexTag(baseTagName, "port")
	project.Packet.sendTCP(address, port, message) 

def handleGateEntryRequest(json):
	json = json["gateEntryRequest"]
	parkingStationId = json["ParkingStationId"];

	#insert the new ticket in the db
	system.db.runPrepUpdate("INSERT INTO ticket(ArrivalTime, ParkingStationId, State) VALUES (CURRENT_TIMESTAMP, ?, \"Entered\")", [parkingStationId], "ParkingSystem")
	
	#prepare parkingStationReply
	data = project.GateLib.extractGateEntryReplyData(parkingStationId)
	json_reply = project.GateLib.createJSONGateEntryReply(parkingStationId, data["ticketId"], data["name"], data["freeParkingPlaces"], data["timestamp"], data["fee_hr"], data["freeParkingPlaceId"])
	
	print json_reply
	gateReply(json_reply)

def handleGateExitRequest(json):
	json = json["gateExitRequest"]
	print json
	parkingStationId = json["ParkingStationId"];
	parkingTicketId =  json["ParkingTicketID"];
	
	baseTagName = "ParkingStationTags/ParkingStation_"+ str(parkingStationId) 
	name = project.TagUtil.readComplexTag(baseTagName, "name")
	fee = project.Fee.computeTicketFee(parkingStationId, parkingTicketId)
	
	json_reply = project.GateLib.createJSONGateExitReply(parkingStationId, parkingTicketId, name, fee)
	
	print fee
	print json_reply
	gateReply(json_reply)

def handlePaymentCompletedMessage(json):
	json = json["paymentCompletedMessage"]
	print json
	parkingStationId = json["ParkingStationId"];
	parkingTicketId =  json["ParkingTicketID"];
	
	#update status in the db
	system.db.runPrepUpdate(" UPDATE Ticket SET PaymentTime = CURRENT_TIMESTAMP , State = \"Payed\" WHERE parkingstationID = ? AND TicketID = ? ;", [parkingStationId, parkingTicketId], "ParkingSystem")
	
	timestamp = system.db.runScalarPrepQuery("SELECT PaymentTime FROM Ticket WHERE parkingstationID = ? AND TicketID = ? ;", [parkingStationId, parkingTicketId], "ParkingSystem")
	exit_min = system.db.runScalarPrepQuery("SELECT ExitMinutes FROM ParkingStation WHERE ID = ? ;", [parkingStationId], "ParkingSystem")
	json_reply = project.GateLib.createJSONPaymentAcceptedMsg(parkingStationId, parkingTicketId, timestamp, exit_min)
	
	print json_reply
	gateReply(json_reply)

def handleOpenGateRequest(json):
	print "ajashsahs"
	json = json["openGateRequest"]
	
	parkingStationId = json["ParkingStationId"];
	parkingTicketId =  json["ParkingTicketID"];
	result = system.db.runPrepQuery("SELECT State, PaymentTime FROM Ticket WHERE parkingStationId = ? AND TicketId = ? ;", [parkingStationId, parkingTicketId], "ParkingSystem")
	result = system.dataset.toDataSet(result)
	print result
	elapsed_min = project.GateLib.minDiff(result.getValueAt(0, "PaymentTime"))
	print result.getValueAt(0, "PaymentTime")
	exit_min = system.db.runScalarPrepQuery("SELECT ExitMinutes FROM ParkingStation WHERE ID = ? ;", [parkingStationId], "ParkingSystem")
	if result.getValueAt(0, "State") == "Payed" and elapsed_min < exit_min:
		status = "Ok"
		system.db.runPrepUpdate(" UPDATE Ticket SET ExitTime = CURRENT_TIMESTAMP , State = \"Exited\" WHERE parkingstationID = ? AND TicketID = ? ;", [parkingStationId, parkingTicketId], "ParkingSystem")
	else :
		status = "Error"
	json_reply = project.GateLib.createJSONOpenGateReply(parkingStationId, parkingTicketId, status)
	print json_reply
	gateReply(json_reply)
	
	
def createJSONGateExitReply(parkingStationId, ticketId, name, fee):	
	json_reply = project.Packet.JSONMessageStart("gateExitReply")
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingStationId", parkingStationId, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingTicketID", ticketId, 0)
	json_reply = project.Packet.addStrField2JSON(json_reply, "ParkingStationName", name, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "Fee", fee, 1)
	json_reply = project.Packet.JSONMessageEnd(json_reply)
	return json_reply

def createJSONGateEntryReply(parkingStationId, ticketId, name, freeParkingPlaces, timestamp, fee_hr, freeParkingPlaceId):
	json_reply = project.Packet.JSONMessageStart("gateEntryReply")
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingStationId", parkingStationId, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingTicketID", ticketId, 0)
	json_reply = project.Packet.addStrField2JSON(json_reply, "ParkingStationName", name, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "NumFreePlaces", freeParkingPlaces, 0)
	json_reply = project.Packet.addStrField2JSON(json_reply, "Timestamp", timestamp, 0)
	json_reply = project.Packet.addStrField2JSON(json_reply, "FeeDescription", fee_hr, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "FreeParkingPlaceId", freeParkingPlaceId, 1)
	json_reply = project.Packet.JSONMessageEnd(json_reply)
	return json_reply

def createJSONPaymentAcceptedMsg(parkingStationId, ticketId, timestamp, exit_min):
	json_reply = project.Packet.JSONMessageStart("paymentAcceptedMessage")
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingStationId", parkingStationId, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingTicketId", ticketId, 0)
	json_reply = project.Packet.addStrField2JSON(json_reply, "Timestamp", timestamp, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "ExitMinutes", exit_min, 1)
	json_reply = project.Packet.JSONMessageEnd(json_reply)
	return json_reply
 
def createJSONOpenGateReply(parkingStationId, ticketId, status):
	json_reply = project.Packet.JSONMessageStart("openGateReply")
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingStationId", parkingStationId, 0)
	json_reply = project.Packet.addField2JSON(json_reply, "ParkingTicketId", ticketId, 0)
	json_reply = project.Packet.addStrField2JSON(json_reply, "Status", status, 1)
	json_reply = project.Packet.JSONMessageEnd(json_reply)
	return json_reply
 
def minDiff(date):
	now = Date()
		
	cal = Calendar.getInstance()
	now = cal.getTime()
	
	dbDataTime = date.getTime() 	#in ms
	nowTime = now.getTime()			#in ms
	diff = nowTime - dbDataTime
	min = ((diff / (1000 * 60)) % 60)
	hr = ((diff / (1000 * 60 * 60)) % 24)
	days = (diff / (1000 * 60 * 60 * 24))
	
	tot_min = (days * 24) * 60 + hr * 60 + min
	
	return min
	
def extractGateEntryReplyData(parkingStationId) :
	ticketId = system.db.runScalarPrepQuery("SELECT MAX(TicketID) FROM Ticket Where ParkingStationId = ?", [parkingStationId], "ParkingSystem")
	timestamp = system.db.runScalarPrepQuery("SELECT ArrivalTime FROM Ticket Where ParkingStationId = ? AND TicketId = ?", [parkingStationId, ticketId], "ParkingSystem")
	freeParkingPlaceId = system.db.runScalarPrepQuery("SELECT ID FROM ParkingPlace Where ParkingStationId = ? AND busy = 0", [parkingStationId], "ParkingSystem")
	
	baseTagName = "ParkingStationTags/ParkingStation_"+ str(parkingStationId) 
 
	maxParkingPlaces = project.TagUtil.readComplexTag(baseTagName, "maxParkingPlaces")
	busyParkingPlaces = project.TagUtil.readComplexTag(baseTagName, "busyParkingPlaces")
	
	freeParkingPlaces = maxParkingPlaces - busyParkingPlaces
	name = project.TagUtil.readComplexTag(baseTagName, "name")
	fee_hr = project.TagUtil.readComplexTag(baseTagName, "fee_hr")
	
	return { "ticketId" : ticketId, "timestamp" : timestamp, "freeParkingPlaceId" : freeParkingPlaceId, "freeParkingPlaces" : freeParkingPlaces, "name" : name, "fee_hr" : fee_hr}
