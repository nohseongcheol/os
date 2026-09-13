package udp

import . "unsafe"
import . "console"
import . "util"
import . "memorymanager"
import . "ipv4"

var udpconsole = TConsole{}

type TИстифодакунандаdatagramprotocolheaderbuffer struct {
	sourceportnumber	[2]byte
	destinationportnumber	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheadersize uint32 = 8

type TИстифодакунандаdatagramprotocolheader struct {
	sourceportnumber	uint16
	destinationportnumber	uint16

	length		uint16
	checksum	uint16
}

func (self *TИстифодакунандаdatagramprotocolheader) Init(buffer_2 *TИстифодакунандаdatagramprotocolheaderbuffer) {
	self.sourceportnumber = Arraytounsignedinteger16(buffer_2.sourceportnumber)
	self.destinationportnumber = Arraytounsignedinteger16(buffer_2.destinationportnumber)

	self.length = Arraytounsignedinteger16(buffer_2.length)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *TИстифодакунандаdatagramprotocolheader) Setbuffer(buffer_2 *TИстифодакунандаdatagramprotocolheaderbuffer) {

	buffer_2.sourceportnumber = Unsignedinteger16toarray(self.sourceportnumber)
	buffer_2.destinationportnumber = Unsignedinteger16toarray(self.destinationportnumber)

	buffer_2.length = Unsignedinteger16toarray(self.length)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type IИстифодакунандаdatagramprotocolhandler interface {
	HandleИстифодакунандаdatagramprotocolmessage(socket *TИстифодакунандаdatagramprotocolsocket, data uintptr, size uint16)
}

type TИстифодакунандаdatagramprotocolhandler struct {
}

func (self *TИстифодакунандаdatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *TИстифодакунандаdatagramprotocolhandler) HandleИстифодакунандаdatagramprotocolmessage(socket *TИстифодакунандаdatagramprotocolsocket, data uintptr, size uint16) {
}

type IИстифодакунандаdatagramprotocolsocket interface {
	HandleИстифодакунандаdatagramprotocolmessage(data uintptr, size uint16)
}
type TИстифодакунандаdatagramprotocolsocket struct {
	remoteportnumber	uint16
	remoteip		uint32
	localportnumber		uint16
	localip			uint32

	listening	bool
}

var udpprovider TИстифодакунандаdatagramprotocolprovider
var udphandler IИстифодакунандаdatagramprotocolhandler

func (self *TИстифодакунандаdatagramprotocolsocket) Test() {
}
func (self *TИстифодакунандаdatagramprotocolsocket) Init(pudpprovider TИстифодакунандаdatagramprotocolprovider, pudphandler IИстифодакунандаdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TИстифодакунандаdatagramprotocolsocket) HandleИстифодакунандаdatagramprotocolmessage(data uintptr, size uint16) {
	if udphandler != nil {
		udphandler.HandleИстифодакунандаdatagramprotocolmessage(self, data, size)
	}
}
func (self *TИстифодакунандаdatagramprotocolsocket) Ирсолкунед(pdata []byte, size uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(size); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Ирсолкунед(self, data, size)
}
func (self *TИстифодакунандаdatagramprotocolsocket) Disconnect() {
	udpprovider.Disconnect(self)
}

type TИстифодакунандаdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TИстифодакунандаdatagramprotocolsocket
var numbersockets int
var freeport uint16

func (self *TИстифодакунандаdatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	freeport = 1024
}
func (self *TИстифодакунандаdatagramprotocolprovider) Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, destinationipaddressnetworkbyteorder uint32, internetprotocolpayload uintptr, size uint32) bool {
	if size < udpheadersize {
		return false
	}

	var buffer_2 *TИстифодакунандаdatagramprotocolheaderbuffer = (*TИстифодакунандаdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TИстифодакунандаdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TИстифодакунандаdatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localportnumber == msg.destinationportnumber && sockets[i].localip == destinationipaddressnetworkbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteportnumber = msg.sourceportnumber
			socket.remoteip = sourceipaddressnetworkbyteorder
		} else if sockets[i].localportnumber == msg.destinationportnumber && sockets[i].localip == destinationipaddressnetworkbyteorder && sockets[i].remoteportnumber == msg.sourceportnumber && sockets[i].remoteip == sourceipaddressnetworkbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleИстифодакунандаdatagramprotocolmessage(internetprotocolpayload+uintptr(udpheadersize), uint16(size-udpheadersize))
	}

	return false
}

func (self *TИстифодакунандаdatagramprotocolprovider) Connect(ip uint32, port uint16) *TИстифодакунандаdatagramprotocolsocket {
	var memorymanager = &TMemorymanager{}
	var socket = (*TИстифодакунандаdatagramprotocolsocket)(memorymanager.Malloc(50))

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
func (self *TИстифодакунандаdatagramprotocolprovider) Listen(port uint16) *TИстифодакунандаdatagramprotocolsocket {
	var socket = &TИстифодакунандаdatagramprotocolsocket{}
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
func (self *TИстифодакунандаdatagramprotocolprovider) Disconnect(socket *TИстифодакунандаdatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *TИстифодакунандаdatagramprotocolprovider) Ирсолкунед(socket *TИстифодакунандаdatagramprotocolsocket, pdata uintptr, size uint16) {
	var totallength = uint32(size) + udpheadersize

	var buffer_2 [4096]byte

	var msgbuffer = (*TИстифодакунандаdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TИстифодакунандаdatagramprotocolheader{}

	msg.sourceportnumber = socket.localportnumber
	msg.destinationportnumber = socket.remoteportnumber
	msg.length = Unsignedinteger16r(uint16(totallength))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var databytes [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(size); i++ {
		buffer_2[int(udpheadersize)+i] = databytes[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Ирсолкунед(socket.remoteip, 0x11, data, totallength)

}
func (self *TИстифодакунандаdatagramprotocolprovider) Bind(socket *TИстифодакунандаdatagramprotocolsocket, handler *TИстифодакунандаdatagramprotocolhandler,) {
}
