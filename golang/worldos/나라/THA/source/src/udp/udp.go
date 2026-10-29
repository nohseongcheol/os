/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "memorymanager"
import . "ipv4"

var udpconsole = TConsole{}

type TUserdatagramprotocolheaderbuffer struct {
	sourceportnumber	[2]byte
	ปลายทางportnumber	[2]byte

	ความยาว		[2]byte
	checksum	[2]byte
}

var udpheaderขนาด uint32 = 8

type TUserdatagramprotocolheader struct {
	sourceportnumber	uint16
	ปลายทางportnumber	uint16

	ความยาว		uint16
	checksum	uint16
}

func (self *TUserdatagramprotocolheader) Init(buffer_2 *TUserdatagramprotocolheaderbuffer) {
	self.sourceportnumber = Arraytounsignedinteger16(buffer_2.sourceportnumber)
	self.ปลายทางportnumber = Arraytounsignedinteger16(buffer_2.ปลายทางportnumber)

	self.ความยาว = Arraytounsignedinteger16(buffer_2.ความยาว)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *TUserdatagramprotocolheader) Sกำหนดbuffer(buffer_2 *TUserdatagramprotocolheaderbuffer) {

	buffer_2.sourceportnumber = Unsignedinteger16toarray(self.sourceportnumber)
	buffer_2.ปลายทางportnumber = Unsignedinteger16toarray(self.ปลายทางportnumber)

	buffer_2.ความยาว = Unsignedinteger16toarray(self.ความยาว)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type IUserdatagramprotocolhandler interface {
	Handleuserdatagramprotocolmessage(socket *TUserdatagramprotocolsocket, data uintptr, ขนาด uint16)
}

type TUserdatagramprotocolhandler struct {
}

func (self *TUserdatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *TUserdatagramprotocolhandler) Handleuserdatagramprotocolmessage(socket *TUserdatagramprotocolsocket, data uintptr, ขนาด uint16) {
}

type IUserdatagramprotocolsocket interface {
	Handleuserdatagramprotocolmessage(data uintptr, ขนาด uint16)
}
type TUserdatagramprotocolsocket struct {
	remoteportnumber	uint16
	remoteip		uint32
	localportnumber		uint16
	localip			uint32

	listening	bool
}

var udpprovider TUserdatagramprotocolprovider
var udphandler IUserdatagramprotocolhandler

func (self *TUserdatagramprotocolsocket) Tทดสอบ() {
}
func (self *TUserdatagramprotocolsocket) Init(pudpprovider TUserdatagramprotocolprovider, pudphandler IUserdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TUserdatagramprotocolsocket) Handleuserdatagramprotocolmessage(data uintptr, ขนาด uint16) {
	if udphandler != nil {
		udphandler.Handleuserdatagramprotocolmessage(self, data, ขนาด)
	}
}
func (self *TUserdatagramprotocolsocket) Send(pdata []byte, ขนาด uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(ขนาด); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, ขนาด)
}
func (self *TUserdatagramprotocolsocket) Disconnect() {
	udpprovider.Disconnect(self)
}

type TUserdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TUserdatagramprotocolsocket
var numbersockets int
var freeport uint16

func (self *TUserdatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	freeport = 1024
}
func (self *TUserdatagramprotocolprovider) Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, ปลายทางipaddressnetworkbyteorder uint32, internetprotocolpayload uintptr, ขนาด uint32) bool {
	if ขนาด < udpheaderขนาด {
		return false
	}

	var buffer_2 *TUserdatagramprotocolheaderbuffer = (*TUserdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TUserdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TUserdatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localportnumber == msg.ปลายทางportnumber && sockets[i].localip == ปลายทางipaddressnetworkbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteportnumber = msg.sourceportnumber
			socket.remoteip = sourceipaddressnetworkbyteorder
		} else if sockets[i].localportnumber == msg.ปลายทางportnumber && sockets[i].localip == ปลายทางipaddressnetworkbyteorder && sockets[i].remoteportnumber == msg.sourceportnumber && sockets[i].remoteip == sourceipaddressnetworkbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Sกำหนดbuffer(buffer_2)
	if socket != nil {
		socket.Handleuserdatagramprotocolmessage(internetprotocolpayload+uintptr(udpheaderขนาด), uint16(ขนาด-udpheaderขนาด))
	}

	return false
}

func (self *TUserdatagramprotocolprovider) Connect(ip uint32, port uint16) *TUserdatagramprotocolsocket {
	var memorymanager = &TMemorymanager{}
	var socket = (*TUserdatagramprotocolsocket)(memorymanager.Malloc(50))

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
func (self *TUserdatagramprotocolprovider) Listen(port uint16) *TUserdatagramprotocolsocket {
	var socket = &TUserdatagramprotocolsocket{}
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
func (self *TUserdatagramprotocolprovider) Disconnect(socket *TUserdatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *TUserdatagramprotocolprovider) Send(socket *TUserdatagramprotocolsocket, pdata uintptr, ขนาด uint16) {
	var รวมความยาว = uint32(ขนาด) + udpheaderขนาด

	var buffer_2 [4096]byte

	var msgbuffer = (*TUserdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TUserdatagramprotocolheader{}

	msg.sourceportnumber = socket.localportnumber
	msg.ปลายทางportnumber = socket.remoteportnumber
	msg.ความยาว = Unsignedinteger16r(uint16(รวมความยาว))

	msg.checksum = 0x0
	msg.Sกำหนดbuffer(msgbuffer)

	var databytes [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(ขนาด); i++ {
		buffer_2[int(udpheaderขนาด)+i] = databytes[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, รวมความยาว)

}
func (self *TUserdatagramprotocolprovider) Bind(socket *TUserdatagramprotocolsocket, handler *TUserdatagramprotocolhandler) {
}
