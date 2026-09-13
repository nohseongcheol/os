package udp

import . "unsafe"
import . "console"
import . "util"
import . "memorymanager"
import . "ipv4"

var udpconsole = TConsole{}

type TBrúkaridatagramprotocolheaderbuffer struct {
	sourceportnumber	[2]byte
	destinationportnumber	[2]byte

	longd		[2]byte
	checksum	[2]byte
}

var udpheaderStødd uint32 = 8

type TBrúkaridatagramprotocolheader struct {
	sourceportnumber	uint16
	destinationportnumber	uint16

	longd		uint16
	checksum	uint16
}

func (self *TBrúkaridatagramprotocolheader) Init(buffer_2 *TBrúkaridatagramprotocolheaderbuffer) {
	self.sourceportnumber = Arraytounsignedinteger16(buffer_2.sourceportnumber)
	self.destinationportnumber = Arraytounsignedinteger16(buffer_2.destinationportnumber)

	self.longd = Arraytounsignedinteger16(buffer_2.longd)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *TBrúkaridatagramprotocolheader) Setbuffer(buffer_2 *TBrúkaridatagramprotocolheaderbuffer) {

	buffer_2.sourceportnumber = Unsignedinteger16toarray(self.sourceportnumber)
	buffer_2.destinationportnumber = Unsignedinteger16toarray(self.destinationportnumber)

	buffer_2.longd = Unsignedinteger16toarray(self.longd)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type IBrúkaridatagramprotocolhandler interface {
	HandleBrúkaridatagramprotocolboðan(socket *TBrúkaridatagramprotocolsocket, data uintptr, stødd uint16)
}

type TBrúkaridatagramprotocolhandler struct {
}

func (self *TBrúkaridatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *TBrúkaridatagramprotocolhandler) HandleBrúkaridatagramprotocolboðan(socket *TBrúkaridatagramprotocolsocket, data uintptr, stødd uint16) {
}

type IBrúkaridatagramprotocolsocket interface {
	HandleBrúkaridatagramprotocolboðan(data uintptr, stødd uint16)
}
type TBrúkaridatagramprotocolsocket struct {
	remoteportnumber	uint16
	remoteip		uint32
	localportnumber		uint16
	localip			uint32

	listening	bool
}

var udpprovider TBrúkaridatagramprotocolprovider
var udphandler IBrúkaridatagramprotocolhandler

func (self *TBrúkaridatagramprotocolsocket) Test() {
}
func (self *TBrúkaridatagramprotocolsocket) Init(pudpprovider TBrúkaridatagramprotocolprovider, pudphandler IBrúkaridatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TBrúkaridatagramprotocolsocket) HandleBrúkaridatagramprotocolboðan(data uintptr, stødd uint16) {
	if udphandler != nil {
		udphandler.HandleBrúkaridatagramprotocolboðan(self, data, stødd)
	}
}
func (self *TBrúkaridatagramprotocolsocket) Send(pdata []byte, stødd uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(stødd); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, stødd)
}
func (self *TBrúkaridatagramprotocolsocket) Disconnect() {
	udpprovider.Disconnect(self)
}

type TBrúkaridatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TBrúkaridatagramprotocolsocket
var numbersockets int
var freeport uint16

func (self *TBrúkaridatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	freeport = 1024
}
func (self *TBrúkaridatagramprotocolprovider) Internetprotocolreceivewhen(sourceipaddressNetbyteorder uint32, destinationipaddressNetbyteorder uint32, internetprotocolpayload uintptr, stødd uint32) bool {
	if stødd < udpheaderStødd {
		return false
	}

	var buffer_2 *TBrúkaridatagramprotocolheaderbuffer = (*TBrúkaridatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TBrúkaridatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TBrúkaridatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localportnumber == msg.destinationportnumber && sockets[i].localip == destinationipaddressNetbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteportnumber = msg.sourceportnumber
			socket.remoteip = sourceipaddressNetbyteorder
		} else if sockets[i].localportnumber == msg.destinationportnumber && sockets[i].localip == destinationipaddressNetbyteorder && sockets[i].remoteportnumber == msg.sourceportnumber && sockets[i].remoteip == sourceipaddressNetbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleBrúkaridatagramprotocolboðan(internetprotocolpayload+uintptr(udpheaderStødd), uint16(stødd-udpheaderStødd))
	}

	return false
}

func (self *TBrúkaridatagramprotocolprovider) Connect(ip uint32, port uint16) *TBrúkaridatagramprotocolsocket {
	var memorymanager = &TMemorymanager{}
	var socket = (*TBrúkaridatagramprotocolsocket)(memorymanager.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteportnumber = port
		socket.remoteip = ip
		socket.localportnumber = freeport
		freeport++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteportnumber = Unsignedinteger16r(socket.remoteportnumber)
		socket.localportnumber = Unsignedinteger16r(socket.localportnumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (self *TBrúkaridatagramprotocolprovider) Listen(port uint16) *TBrúkaridatagramprotocolsocket {
	var socket = &TBrúkaridatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.localportnumber = port
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localportnumber = Unsignedinteger16r(socket.localportnumber)
	}
	return socket
}
func (self *TBrúkaridatagramprotocolprovider) Disconnect(socket *TBrúkaridatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *TBrúkaridatagramprotocolprovider) Send(socket *TBrúkaridatagramprotocolsocket, pdata uintptr, stødd uint16) {
	var totalLongd = uint32(stødd) + udpheaderStødd

	var buffer_2 [4096]byte

	var msgbuffer = (*TBrúkaridatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TBrúkaridatagramprotocolheader{}

	msg.sourceportnumber = socket.localportnumber
	msg.destinationportnumber = socket.remoteportnumber
	msg.longd = Unsignedinteger16r(uint16(totalLongd))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var databýt [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(stødd); i++ {
		buffer_2[int(udpheaderStødd)+i] = databýt[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, totalLongd)

}
func (self *TBrúkaridatagramprotocolprovider) Bind(socket *TBrúkaridatagramprotocolsocket, handler *TBrúkaridatagramprotocolhandler) {
}
