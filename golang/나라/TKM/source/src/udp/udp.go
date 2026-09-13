package udp

import . "unsafe"
import . "console"
import . "util"
import . "memorymanager"
import . "ipv4"

var udpconsole = TConsole{}

type TUllançydatagramprotocolheaderbuffer struct {
	çeşmeportnumber		[2]byte
	destinationportnumber	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheaderUlulyk uint32 = 8

type TUllançydatagramprotocolheader struct {
	çeşmeportnumber		uint16
	destinationportnumber	uint16

	length		uint16
	checksum	uint16
}

func (self *TUllançydatagramprotocolheader) Init(buffer_2 *TUllançydatagramprotocolheaderbuffer) {
	self.çeşmeportnumber = Arraytounsignedinteger16(buffer_2.çeşmeportnumber)
	self.destinationportnumber = Arraytounsignedinteger16(buffer_2.destinationportnumber)

	self.length = Arraytounsignedinteger16(buffer_2.length)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *TUllançydatagramprotocolheader) Setbuffer(buffer_2 *TUllançydatagramprotocolheaderbuffer) {

	buffer_2.çeşmeportnumber = Unsignedinteger16toarray(self.çeşmeportnumber)
	buffer_2.destinationportnumber = Unsignedinteger16toarray(self.destinationportnumber)

	buffer_2.length = Unsignedinteger16toarray(self.length)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type IUllançydatagramprotocolhandler interface {
	HandleUllançydatagramprotocolSargyt(socket *TUllançydatagramprotocolsocket, data uintptr, ululyk uint16)
}

type TUllançydatagramprotocolhandler struct {
}

func (self *TUllançydatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *TUllançydatagramprotocolhandler) HandleUllançydatagramprotocolSargyt(socket *TUllançydatagramprotocolsocket, data uintptr, ululyk uint16) {
}

type IUllançydatagramprotocolsocket interface {
	HandleUllançydatagramprotocolSargyt(data uintptr, ululyk uint16)
}
type TUllançydatagramprotocolsocket struct {
	remoteportnumber	uint16
	remoteip		uint32
	localportnumber		uint16
	localip			uint32

	listening	bool
}

var udpprovider TUllançydatagramprotocolprovider
var udphandler IUllançydatagramprotocolhandler

func (self *TUllançydatagramprotocolsocket) Test() {
}
func (self *TUllançydatagramprotocolsocket) Init(pudpprovider TUllançydatagramprotocolprovider, pudphandler IUllançydatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TUllançydatagramprotocolsocket) HandleUllançydatagramprotocolSargyt(data uintptr, ululyk uint16) {
	if udphandler != nil {
		udphandler.HandleUllançydatagramprotocolSargyt(self, data, ululyk)
	}
}
func (self *TUllançydatagramprotocolsocket) Send(pdata []byte, ululyk uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(ululyk); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, ululyk)
}
func (self *TUllançydatagramprotocolsocket) Disconnect() {
	udpprovider.Disconnect(self)
}

type TUllançydatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TUllançydatagramprotocolsocket
var numbersockets int
var freeport uint16

func (self *TUllançydatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	freeport = 1024
}
func (self *TUllançydatagramprotocolprovider) Internetprotocolreceivewhen(çeşmeipaddressŞebekebyteorder uint32, destinationipaddressŞebekebyteorder uint32, internetprotocolpayload uintptr, ululyk uint32) bool {
	if ululyk < udpheaderUlulyk {
		return false
	}

	var buffer_2 *TUllançydatagramprotocolheaderbuffer = (*TUllançydatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TUllançydatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TUllançydatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localportnumber == msg.destinationportnumber && sockets[i].localip == destinationipaddressŞebekebyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteportnumber = msg.çeşmeportnumber
			socket.remoteip = çeşmeipaddressŞebekebyteorder
		} else if sockets[i].localportnumber == msg.destinationportnumber && sockets[i].localip == destinationipaddressŞebekebyteorder && sockets[i].remoteportnumber == msg.çeşmeportnumber && sockets[i].remoteip == çeşmeipaddressŞebekebyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleUllançydatagramprotocolSargyt(internetprotocolpayload+uintptr(udpheaderUlulyk), uint16(ululyk-udpheaderUlulyk))
	}

	return false
}

func (self *TUllançydatagramprotocolprovider) Connect(ip uint32, port uint16) *TUllançydatagramprotocolsocket {
	var memorymanager = &TMemorymanager{}
	var socket = (*TUllançydatagramprotocolsocket)(memorymanager.Malloc(50))

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
func (self *TUllançydatagramprotocolprovider) Listen(port uint16) *TUllançydatagramprotocolsocket {
	var socket = &TUllançydatagramprotocolsocket{}
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
func (self *TUllançydatagramprotocolprovider) Disconnect(socket *TUllançydatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *TUllançydatagramprotocolprovider) Send(socket *TUllançydatagramprotocolsocket, pdata uintptr, ululyk uint16) {
	var totallength = uint32(ululyk) + udpheaderUlulyk

	var buffer_2 [4096]byte

	var msgbuffer = (*TUllançydatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TUllançydatagramprotocolheader{}

	msg.çeşmeportnumber = socket.localportnumber
	msg.destinationportnumber = socket.remoteportnumber
	msg.length = Unsignedinteger16r(uint16(totallength))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataBaýtlar [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(ululyk); i++ {
		buffer_2[int(udpheaderUlulyk)+i] = dataBaýtlar[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, totallength)

}
func (self *TUllançydatagramprotocolprovider) Bind(socket *TUllançydatagramprotocolsocket, handler *TUllançydatagramprotocolhandler) {
}
