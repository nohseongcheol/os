package udp

import . "unsafe"
import . "console"
import . "util"
import . "ububikomanager"
import . "ipv4"

var udpconsole = TConsole{}

type TUkoreshadatagramprotocolheaderbuffer struct {
	inkomokoUmuyoboronumber		[2]byte
	destinationUmuyoboronumber	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheaderIngano uint32 = 8

type TUkoreshadatagramprotocolheader struct {
	inkomokoUmuyoboronumber		uint16
	destinationUmuyoboronumber	uint16

	length		uint16
	checksum	uint16
}

func (self *TUkoreshadatagramprotocolheader) Init(buffer_2 *TUkoreshadatagramprotocolheaderbuffer) {
	self.inkomokoUmuyoboronumber = Imbonerahamwetounsignedinteger16(buffer_2.inkomokoUmuyoboronumber)
	self.destinationUmuyoboronumber = Imbonerahamwetounsignedinteger16(buffer_2.destinationUmuyoboronumber)

	self.length = Imbonerahamwetounsignedinteger16(buffer_2.length)
	self.checksum = Imbonerahamwetounsignedinteger16(buffer_2.checksum)
}
func (self *TUkoreshadatagramprotocolheader) Setbuffer(buffer_2 *TUkoreshadatagramprotocolheaderbuffer) {

	buffer_2.inkomokoUmuyoboronumber = Unsignedinteger16toImbonerahamwe(self.inkomokoUmuyoboronumber)
	buffer_2.destinationUmuyoboronumber = Unsignedinteger16toImbonerahamwe(self.destinationUmuyoboronumber)

	buffer_2.length = Unsignedinteger16toImbonerahamwe(self.length)
	buffer_2.checksum = Unsignedinteger16toImbonerahamwe(self.checksum)

}

type IUkoreshadatagramprotocolhandler interface {
	HandleUkoreshadatagramprotocolUbutumwa(socket *TUkoreshadatagramprotocolsocket, data uintptr, ingano uint16)
}

type TUkoreshadatagramprotocolhandler struct {
}

func (self *TUkoreshadatagramprotocolhandler) Init(backend TInterinetiprotocolprovider) {
}
func (self *TUkoreshadatagramprotocolhandler) HandleUkoreshadatagramprotocolUbutumwa(socket *TUkoreshadatagramprotocolsocket, data uintptr, ingano uint16) {
}

type IUkoreshadatagramprotocolsocket interface {
	HandleUkoreshadatagramprotocolUbutumwa(data uintptr, ingano uint16)
}
type TUkoreshadatagramprotocolsocket struct {
	remoteUmuyoboronumber	uint16
	remoteip		uint32
	localUmuyoboronumber	uint16
	localip			uint32

	listening	bool
}

var udpprovider TUkoreshadatagramprotocolprovider
var udphandler IUkoreshadatagramprotocolhandler

func (self *TUkoreshadatagramprotocolsocket) Test() {
}
func (self *TUkoreshadatagramprotocolsocket) Init(pudpprovider TUkoreshadatagramprotocolprovider, pudphandler IUkoreshadatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TUkoreshadatagramprotocolsocket) HandleUkoreshadatagramprotocolUbutumwa(data uintptr, ingano uint16) {
	if udphandler != nil {
		udphandler.HandleUkoreshadatagramprotocolUbutumwa(self, data, ingano)
	}
}
func (self *TUkoreshadatagramprotocolsocket) Send(pdata []byte, ingano uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(ingano); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, ingano)
}
func (self *TUkoreshadatagramprotocolsocket) Disconnect() {
	udpprovider.Disconnect(self)
}

type TUkoreshadatagramprotocolprovider struct {
}

var iphandler IInterinetiprotocolhandler
var sockets [65535]TUkoreshadatagramprotocolsocket
var numbersockets int
var kigengaUmuyoboro uint16

func (self *TUkoreshadatagramprotocolprovider) Init(pipprovider TInterinetiprotocolprovider, piphandler IInterinetiprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	kigengaUmuyoboro = 1024
}
func (self *TUkoreshadatagramprotocolprovider) Interinetiprotocolreceivewhen(inkomokoipaddressurusobebyteorder uint32, destinationipaddressurusobebyteorder uint32, interinetiprotocolpayload uintptr, ingano uint32) bool {
	if ingano < udpheaderIngano {
		return false
	}

	var buffer_2 *TUkoreshadatagramprotocolheaderbuffer = (*TUkoreshadatagramprotocolheaderbuffer)(Pointer(interinetiprotocolpayload))
	var msg TUkoreshadatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TUkoreshadatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localUmuyoboronumber == msg.destinationUmuyoboronumber && sockets[i].localip == destinationipaddressurusobebyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteUmuyoboronumber = msg.inkomokoUmuyoboronumber
			socket.remoteip = inkomokoipaddressurusobebyteorder
		} else if sockets[i].localUmuyoboronumber == msg.destinationUmuyoboronumber && sockets[i].localip == destinationipaddressurusobebyteorder && sockets[i].remoteUmuyoboronumber == msg.inkomokoUmuyoboronumber && sockets[i].remoteip == inkomokoipaddressurusobebyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleUkoreshadatagramprotocolUbutumwa(interinetiprotocolpayload+uintptr(udpheaderIngano), uint16(ingano-udpheaderIngano))
	}

	return false
}

func (self *TUkoreshadatagramprotocolprovider) Connect(ip uint32, umuyoboro uint16) *TUkoreshadatagramprotocolsocket {
	var ububikomanager = &TUbubikomanager{}
	var socket = (*TUkoreshadatagramprotocolsocket)(ububikomanager.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteUmuyoboronumber = umuyoboro
		socket.remoteip = ip
		socket.localUmuyoboronumber = kigengaUmuyoboro
		kigengaUmuyoboro++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteUmuyoboronumber = Unsignedinteger16r(socket.remoteUmuyoboronumber)
		socket.localUmuyoboronumber = Unsignedinteger16r(socket.localUmuyoboronumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (self *TUkoreshadatagramprotocolprovider) Listen(umuyoboro uint16) *TUkoreshadatagramprotocolsocket {
	var socket = &TUkoreshadatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.localUmuyoboronumber = umuyoboro
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localUmuyoboronumber = Unsignedinteger16r(socket.localUmuyoboronumber)
	}
	return socket
}
func (self *TUkoreshadatagramprotocolprovider) Disconnect(socket *TUkoreshadatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *TUkoreshadatagramprotocolprovider) Send(socket *TUkoreshadatagramprotocolsocket, pdata uintptr, ingano uint16) {
	var igiteranyolength = uint32(ingano) + udpheaderIngano

	var buffer_2 [4096]byte

	var msgbuffer = (*TUkoreshadatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TUkoreshadatagramprotocolheader{}

	msg.inkomokoUmuyoboronumber = socket.localUmuyoboronumber
	msg.destinationUmuyoboronumber = socket.remoteUmuyoboronumber
	msg.length = Unsignedinteger16r(uint16(igiteranyolength))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataBayite [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(ingano); i++ {
		buffer_2[int(udpheaderIngano)+i] = dataBayite[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, igiteranyolength)

}
func (self *TUkoreshadatagramprotocolprovider) Bind(socket *TUkoreshadatagramprotocolsocket, handler *TUkoreshadatagramprotocolhandler) {
}
