package udp

import . "unsafe"
import . "console"
import . "util"
import . "xotiramanager"
import . "ipv4"

var udpconsole = TConsole{}

type TFoydalanuvchidatagramprotocolheaderbuffer struct {
	sourceportRAQAM		[2]byte
	destinationportRAQAM	[2]byte

	uzunlik		[2]byte
	checksum	[2]byte
}

var udpheaderHajmi uint32 = 8

type TFoydalanuvchidatagramprotocolheader struct {
	sourceportRAQAM		uint16
	destinationportRAQAM	uint16

	uzunlik		uint16
	checksum	uint16
}

func (self *TFoydalanuvchidatagramprotocolheader) Init(buffer_2 *TFoydalanuvchidatagramprotocolheaderbuffer) {
	self.sourceportRAQAM = Arraytounsignedinteger16(buffer_2.sourceportRAQAM)
	self.destinationportRAQAM = Arraytounsignedinteger16(buffer_2.destinationportRAQAM)

	self.uzunlik = Arraytounsignedinteger16(buffer_2.uzunlik)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *TFoydalanuvchidatagramprotocolheader) Setbuffer(buffer_2 *TFoydalanuvchidatagramprotocolheaderbuffer) {

	buffer_2.sourceportRAQAM = Unsignedinteger16toarray(self.sourceportRAQAM)
	buffer_2.destinationportRAQAM = Unsignedinteger16toarray(self.destinationportRAQAM)

	buffer_2.uzunlik = Unsignedinteger16toarray(self.uzunlik)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type IFoydalanuvchidatagramprotocolhandler interface {
	HandleFoydalanuvchidatagramprotocolXABAR(socket *TFoydalanuvchidatagramprotocolsocket, data uintptr, hajmi uint16)
}

type TFoydalanuvchidatagramprotocolhandler struct {
}

func (self *TFoydalanuvchidatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *TFoydalanuvchidatagramprotocolhandler) HandleFoydalanuvchidatagramprotocolXABAR(socket *TFoydalanuvchidatagramprotocolsocket, data uintptr, hajmi uint16) {
}

type IFoydalanuvchidatagramprotocolsocket interface {
	HandleFoydalanuvchidatagramprotocolXABAR(data uintptr, hajmi uint16)
}
type TFoydalanuvchidatagramprotocolsocket struct {
	remoteportRAQAM		uint16
	remoteip		uint32
	mahalliyportRAQAM	uint16
	mahalliyip		uint32

	listening	bool
}

var udpprovider TFoydalanuvchidatagramprotocolprovider
var udphandler IFoydalanuvchidatagramprotocolhandler

func (self *TFoydalanuvchidatagramprotocolsocket) Sinash() {
}
func (self *TFoydalanuvchidatagramprotocolsocket) Init(pudpprovider TFoydalanuvchidatagramprotocolprovider, pudphandler IFoydalanuvchidatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TFoydalanuvchidatagramprotocolsocket) HandleFoydalanuvchidatagramprotocolXABAR(data uintptr, hajmi uint16) {
	if udphandler != nil {
		udphandler.HandleFoydalanuvchidatagramprotocolXABAR(self, data, hajmi)
	}
}
func (self *TFoydalanuvchidatagramprotocolsocket) Joʻnatish(pdata []byte, hajmi uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(hajmi); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Joʻnatish(self, data, hajmi)
}
func (self *TFoydalanuvchidatagramprotocolsocket) Uzish() {
	udpprovider.Uzish(self)
}

type TFoydalanuvchidatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TFoydalanuvchidatagramprotocolsocket
var rAQAMsockets int
var boshport uint16

func (self *TFoydalanuvchidatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	rAQAMsockets = 0
	boshport = 1024
}
func (self *TFoydalanuvchidatagramprotocolprovider) Internetprotocolreceivewhen(sourceipaddressTarmoqbyteorder uint32, destinationipaddressTarmoqbyteorder uint32, internetprotocolpayload uintptr, hajmi uint32) bool {
	if hajmi < udpheaderHajmi {
		return false
	}

	var buffer_2 *TFoydalanuvchidatagramprotocolheaderbuffer = (*TFoydalanuvchidatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TFoydalanuvchidatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TFoydalanuvchidatagramprotocolsocket = nil

	for i := 0; i < rAQAMsockets && socket == nil; i++ {
		if sockets[i].mahalliyportRAQAM == msg.destinationportRAQAM && sockets[i].mahalliyip == destinationipaddressTarmoqbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteportRAQAM = msg.sourceportRAQAM
			socket.remoteip = sourceipaddressTarmoqbyteorder
		} else if sockets[i].mahalliyportRAQAM == msg.destinationportRAQAM && sockets[i].mahalliyip == destinationipaddressTarmoqbyteorder && sockets[i].remoteportRAQAM == msg.sourceportRAQAM && sockets[i].remoteip == sourceipaddressTarmoqbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleFoydalanuvchidatagramprotocolXABAR(internetprotocolpayload+uintptr(udpheaderHajmi), uint16(hajmi-udpheaderHajmi))
	}

	return false
}

func (self *TFoydalanuvchidatagramprotocolprovider) Ulanish(ip uint32, port uint16) *TFoydalanuvchidatagramprotocolsocket {
	var xotiramanager = &TXotiramanager{}
	var socket = (*TFoydalanuvchidatagramprotocolsocket)(xotiramanager.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteportRAQAM = port
		socket.remoteip = ip
		socket.mahalliyportRAQAM = boshport
		boshport++
		socket.mahalliyip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteportRAQAM = Unsignedinteger16r(socket.remoteportRAQAM)
		socket.mahalliyportRAQAM = Unsignedinteger16r(socket.mahalliyportRAQAM)

		sockets[rAQAMsockets] = *socket
		rAQAMsockets++

	}
	return socket

}
func (self *TFoydalanuvchidatagramprotocolprovider) Listen(port uint16) *TFoydalanuvchidatagramprotocolsocket {
	var socket = &TFoydalanuvchidatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.mahalliyportRAQAM = port
		socket.mahalliyip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.mahalliyportRAQAM = Unsignedinteger16r(socket.mahalliyportRAQAM)
	}
	return socket
}
func (self *TFoydalanuvchidatagramprotocolprovider) Uzish(socket *TFoydalanuvchidatagramprotocolsocket) {
	for i := 0; i < rAQAMsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			rAQAMsockets--
			sockets[i] = sockets[rAQAMsockets]
			break
		}
	}
}
func (self *TFoydalanuvchidatagramprotocolprovider) Joʻnatish(socket *TFoydalanuvchidatagramprotocolsocket, pdata uintptr, hajmi uint16) {
	var jamiUzunlik = uint32(hajmi) + udpheaderHajmi

	var buffer_2 [4096]byte

	var msgbuffer = (*TFoydalanuvchidatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TFoydalanuvchidatagramprotocolheader{}

	msg.sourceportRAQAM = socket.mahalliyportRAQAM
	msg.destinationportRAQAM = socket.remoteportRAQAM
	msg.uzunlik = Unsignedinteger16r(uint16(jamiUzunlik))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataBaytlar [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(hajmi); i++ {
		buffer_2[int(udpheaderHajmi)+i] = dataBaytlar[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Joʻnatish(socket.remoteip, 0x11, data, jamiUzunlik)

}
func (self *TFoydalanuvchidatagramprotocolprovider) Bind(socket *TFoydalanuvchidatagramprotocolsocket, handler *TFoydalanuvchidatagramprotocolhandler,) {
}
