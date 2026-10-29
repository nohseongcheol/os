/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "حافظهmanager"
import . "ipv4"

var udpconsole = TConsole{}

type Tکاربرdatagramprotocolheaderbuffer struct {
	مبدأدرگاهnumber	[2]byte
	مقصددرگاهnumber	[2]byte

	طول		[2]byte
	checksum	[2]byte
}

var udpheaderاندازه uint32 = 8

type Tکاربرdatagramprotocolheader struct {
	مبدأدرگاهnumber	uint16
	مقصددرگاهnumber	uint16

	طول		uint16
	checksum	uint16
}

func (خود *Tکاربرdatagramprotocolheader) Init(buffer_2 *Tکاربرdatagramprotocolheaderbuffer) {
	خود.مبدأدرگاهnumber = Aآرایهtounsignedinteger16(buffer_2.مبدأدرگاهnumber)
	خود.مقصددرگاهnumber = Aآرایهtounsignedinteger16(buffer_2.مقصددرگاهnumber)

	خود.طول = Aآرایهtounsignedinteger16(buffer_2.طول)
	خود.checksum = Aآرایهtounsignedinteger16(buffer_2.checksum)
}
func (خود *Tکاربرdatagramprotocolheader) Setbuffer(buffer_2 *Tکاربرdatagramprotocolheaderbuffer) {

	buffer_2.مبدأدرگاهnumber = Unsignedinteger16toآرایه(خود.مبدأدرگاهnumber)
	buffer_2.مقصددرگاهnumber = Unsignedinteger16toآرایه(خود.مقصددرگاهnumber)

	buffer_2.طول = Unsignedinteger16toآرایه(خود.طول)
	buffer_2.checksum = Unsignedinteger16toآرایه(خود.checksum)

}

type Iکاربرdatagramprotocolhandler interface {
	Handleکاربرdatagramprotocolپیغام(socket *Tکاربرdatagramprotocolsocket, data uintptr, اندازه uint16)
}

type Tکاربرdatagramprotocolhandler struct {
}

func (خود *Tکاربرdatagramprotocolhandler) Init(backend Tاینترنتprotocolprovider) {
}
func (خود *Tکاربرdatagramprotocolhandler) Handleکاربرdatagramprotocolپیغام(socket *Tکاربرdatagramprotocolsocket, data uintptr, اندازه uint16) {
}

type Iکاربرdatagramprotocolsocket interface {
	Handleکاربرdatagramprotocolپیغام(data uintptr, اندازه uint16)
}
type Tکاربرdatagramprotocolsocket struct {
	راهدوردرگاهnumber	uint16
	راهدورip		uint32
	محلیدرگاهnumber		uint16
	محلیip			uint32

	listening	bool
}

var udpprovider Tکاربرdatagramprotocolprovider
var udphandler Iکاربرdatagramprotocolhandler

func (خود *Tکاربرdatagramprotocolsocket) Test() {
}
func (خود *Tکاربرdatagramprotocolsocket) Init(pudpprovider Tکاربرdatagramprotocolprovider, pudphandler Iکاربرdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	خود.listening = false
}
func (خود *Tکاربرdatagramprotocolsocket) Handleکاربرdatagramprotocolپیغام(data uintptr, اندازه uint16) {
	if udphandler != nil {
		udphandler.Handleکاربرdatagramprotocolپیغام(خود, data, اندازه)
	}
}
func (خود *Tکاربرdatagramprotocolsocket) Send(pdata []byte, اندازه uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(اندازه); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(خود, data, اندازه)
}
func (خود *Tکاربرdatagramprotocolsocket) Dقطع() {
	udpprovider.Dقطع(خود)
}

type Tکاربرdatagramprotocolprovider struct {
}

var iphandler Iاینترنتprotocolhandler
var sockets [65535]Tکاربرdatagramprotocolsocket
var numbersockets int
var آزاددرگاه uint16

func (خود *Tکاربرdatagramprotocolprovider) Init(pipprovider Tاینترنتprotocolprovider, piphandler Iاینترنتprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	آزاددرگاه = 1024
}
func (خود *Tکاربرdatagramprotocolprovider) Oاینترنتprotocolreceivewhen(مبدأipaddressشبکهbyteorder uint32, مقصدipaddressشبکهbyteorder uint32, اینترنتprotocolpayload uintptr, اندازه uint32) bool {
	if اندازه < udpheaderاندازه {
		return false
	}

	var buffer_2 *Tکاربرdatagramprotocolheaderbuffer = (*Tکاربرdatagramprotocolheaderbuffer)(Pointer(اینترنتprotocolpayload))
	var msg Tکاربرdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *Tکاربرdatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].محلیدرگاهnumber == msg.مقصددرگاهnumber && sockets[i].محلیip == مقصدipaddressشبکهbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.راهدوردرگاهnumber = msg.مبدأدرگاهnumber
			socket.راهدورip = مبدأipaddressشبکهbyteorder
		} else if sockets[i].محلیدرگاهnumber == msg.مقصددرگاهnumber && sockets[i].محلیip == مقصدipaddressشبکهbyteorder && sockets[i].راهدوردرگاهnumber == msg.مبدأدرگاهnumber && sockets[i].راهدورip == مبدأipaddressشبکهbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.Handleکاربرdatagramprotocolپیغام(اینترنتprotocolpayload+uintptr(udpheaderاندازه), uint16(اندازه-udpheaderاندازه))
	}

	return false
}

func (خود *Tکاربرdatagramprotocolprovider) Cاتصال(ip uint32, درگاه uint16) *Tکاربرdatagramprotocolsocket {
	var حافظهmanager = &Tحافظهmanager{}
	var socket = (*Tکاربرdatagramprotocolsocket)(حافظهmanager.Malloc(50))

	if socket != nil {

		socket.Init(*خود, nil)
		socket.راهدوردرگاهnumber = درگاه
		socket.راهدورip = ip
		socket.محلیدرگاهnumber = آزاددرگاه
		آزاددرگاه++
		socket.محلیip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.راهدوردرگاهnumber = Unsignedinteger16r(socket.راهدوردرگاهnumber)
		socket.محلیدرگاهnumber = Unsignedinteger16r(socket.محلیدرگاهnumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (خود *Tکاربرdatagramprotocolprovider) Listen(درگاه uint16) *Tکاربرdatagramprotocolsocket {
	var socket = &Tکاربرdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*خود, nil)
		socket.listening = true
		socket.محلیدرگاهnumber = درگاه
		socket.محلیip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.محلیدرگاهnumber = Unsignedinteger16r(socket.محلیدرگاهnumber)
	}
	return socket
}
func (خود *Tکاربرdatagramprotocolprovider) Dقطع(socket *Tکاربرdatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (خود *Tکاربرdatagramprotocolprovider) Send(socket *Tکاربرdatagramprotocolsocket, pdata uintptr, اندازه uint16) {
	var totalطول = uint32(اندازه) + udpheaderاندازه

	var buffer_2 [4096]byte

	var msgbuffer = (*Tکاربرdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = Tکاربرdatagramprotocolheader{}

	msg.مبدأدرگاهnumber = socket.محلیدرگاهnumber
	msg.مقصددرگاهnumber = socket.راهدوردرگاهnumber
	msg.طول = Unsignedinteger16r(uint16(totalطول))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataبایت [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(اندازه); i++ {
		buffer_2[int(udpheaderاندازه)+i] = dataبایت[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.راهدورip, 0x11, data, totalطول)

}
func (خود *Tکاربرdatagramprotocolprovider) Bind(socket *Tکاربرdatagramprotocolsocket, handler *Tکاربرdatagramprotocolhandler) {
}
