/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "консол"
import . "util"
import . "санахойЗохицуулагч"
import . "ipv4"

var udpКонсол = TКонсол{}

type TХэрэглэгчdatagramprotocolheaderbuffer struct {
	эхПортnumber		[2]byte
	destinationПортnumber	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheaderХэмжээ uint32 = 8

type TХэрэглэгчdatagramprotocolheader struct {
	эхПортnumber		uint16
	destinationПортnumber	uint16

	length		uint16
	checksum	uint16
}

func (self *TХэрэглэгчdatagramprotocolheader) Init(buffer_2 *TХэрэглэгчdatagramprotocolheaderbuffer) {
	self.эхПортnumber = Arraytounsignedinteger16(buffer_2.эхПортnumber)
	self.destinationПортnumber = Arraytounsignedinteger16(buffer_2.destinationПортnumber)

	self.length = Arraytounsignedinteger16(buffer_2.length)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *TХэрэглэгчdatagramprotocolheader) Setbuffer(buffer_2 *TХэрэглэгчdatagramprotocolheaderbuffer) {

	buffer_2.эхПортnumber = Unsignedinteger16toarray(self.эхПортnumber)
	buffer_2.destinationПортnumber = Unsignedinteger16toarray(self.destinationПортnumber)

	buffer_2.length = Unsignedinteger16toarray(self.length)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type IХэрэглэгчdatagramprotocolhandler interface {
	HandleХэрэглэгчdatagramprotocolМэдээ(socket *TХэрэглэгчdatagramprotocolsocket, data uintptr, хэмжээ uint16)
}

type TХэрэглэгчdatagramprotocolhandler struct {
}

func (self *TХэрэглэгчdatagramprotocolhandler) Init(backend TИнтернетprotocolprovider) {
}
func (self *TХэрэглэгчdatagramprotocolhandler) HandleХэрэглэгчdatagramprotocolМэдээ(socket *TХэрэглэгчdatagramprotocolsocket, data uintptr, хэмжээ uint16) {
}

type IХэрэглэгчdatagramprotocolsocket interface {
	HandleХэрэглэгчdatagramprotocolМэдээ(data uintptr, хэмжээ uint16)
}
type TХэрэглэгчdatagramprotocolsocket struct {
	remoteПортnumber	uint16
	remoteip		uint32
	localПортnumber		uint16
	localip			uint32

	listening	bool
}

var udpprovider TХэрэглэгчdatagramprotocolprovider
var udphandler IХэрэглэгчdatagramprotocolhandler

func (self *TХэрэглэгчdatagramprotocolsocket) Test() {
}
func (self *TХэрэглэгчdatagramprotocolsocket) Init(pudpprovider TХэрэглэгчdatagramprotocolprovider, pudphandler IХэрэглэгчdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TХэрэглэгчdatagramprotocolsocket) HandleХэрэглэгчdatagramprotocolМэдээ(data uintptr, хэмжээ uint16) {
	if udphandler != nil {
		udphandler.HandleХэрэглэгчdatagramprotocolМэдээ(self, data, хэмжээ)
	}
}
func (self *TХэрэглэгчdatagramprotocolsocket) Send(pdata []byte, хэмжээ uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(хэмжээ); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, хэмжээ)
}
func (self *TХэрэглэгчdatagramprotocolsocket) Disconnect() {
	udpprovider.Disconnect(self)
}

type TХэрэглэгчdatagramprotocolprovider struct {
}

var iphandler IИнтернетprotocolhandler
var sockets [65535]TХэрэглэгчdatagramprotocolsocket
var numbersockets int
var чөлөөтПорт uint16

func (self *TХэрэглэгчdatagramprotocolprovider) Init(pipprovider TИнтернетprotocolprovider, piphandler IИнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	чөлөөтПорт = 1024
}
func (self *TХэрэглэгчdatagramprotocolprovider) Интернетprotocolreceivewhen(эхipaddressСүлжээbyteorder uint32, destinationipaddressСүлжээbyteorder uint32, интернетprotocolpayload uintptr, хэмжээ uint32) bool {
	if хэмжээ < udpheaderХэмжээ {
		return false
	}

	var buffer_2 *TХэрэглэгчdatagramprotocolheaderbuffer = (*TХэрэглэгчdatagramprotocolheaderbuffer)(Pointer(интернетprotocolpayload))
	var msg TХэрэглэгчdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TХэрэглэгчdatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localПортnumber == msg.destinationПортnumber && sockets[i].localip == destinationipaddressСүлжээbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteПортnumber = msg.эхПортnumber
			socket.remoteip = эхipaddressСүлжээbyteorder
		} else if sockets[i].localПортnumber == msg.destinationПортnumber && sockets[i].localip == destinationipaddressСүлжээbyteorder && sockets[i].remoteПортnumber == msg.эхПортnumber && sockets[i].remoteip == эхipaddressСүлжээbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleХэрэглэгчdatagramprotocolМэдээ(интернетprotocolpayload+uintptr(udpheaderХэмжээ), uint16(хэмжээ-udpheaderХэмжээ))
	}

	return false
}

func (self *TХэрэглэгчdatagramprotocolprovider) Холбох(ip uint32, порт uint16) *TХэрэглэгчdatagramprotocolsocket {
	var санахойЗохицуулагч = &TСанахойЗохицуулагч{}
	var socket = (*TХэрэглэгчdatagramprotocolsocket)(санахойЗохицуулагч.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteПортnumber = порт
		socket.remoteip = ip
		socket.localПортnumber = чөлөөтПорт
		чөлөөтПорт++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteПортnumber = Unsignedinteger16r(socket.remoteПортnumber)
		socket.localПортnumber = Unsignedinteger16r(socket.localПортnumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (self *TХэрэглэгчdatagramprotocolprovider) Listen(порт uint16) *TХэрэглэгчdatagramprotocolsocket {
	var socket = &TХэрэглэгчdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.localПортnumber = порт
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localПортnumber = Unsignedinteger16r(socket.localПортnumber)
	}
	return socket
}
func (self *TХэрэглэгчdatagramprotocolprovider) Disconnect(socket *TХэрэглэгчdatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *TХэрэглэгчdatagramprotocolprovider) Send(socket *TХэрэглэгчdatagramprotocolsocket, pdata uintptr, хэмжээ uint16) {
	var нийтlength = uint32(хэмжээ) + udpheaderХэмжээ

	var buffer_2 [4096]byte

	var msgbuffer = (*TХэрэглэгчdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TХэрэглэгчdatagramprotocolheader{}

	msg.эхПортnumber = socket.localПортnumber
	msg.destinationПортnumber = socket.remoteПортnumber
	msg.length = Unsignedinteger16r(uint16(нийтlength))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataБайт [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(хэмжээ); i++ {
		buffer_2[int(udpheaderХэмжээ)+i] = dataБайт[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, нийтlength)

}
func (self *TХэрэглэгчdatagramprotocolprovider) Bind(socket *TХэрэглэгчdatagramprotocolsocket, handler *TХэрэглэгчdatagramprotocolhandler,) {
}
