/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "меморијаmanager"
import . "ipv4"

var udpconsole = TConsole{}

type TКорисникdatagramprotocolheaderbuffer struct {
	изворПортаnumber	[2]byte
	одредиштеПортаnumber	[2]byte

	должина		[2]byte
	checksum	[2]byte
}

var udpheaderГолемина uint32 = 8

type TКорисникdatagramprotocolheader struct {
	изворПортаnumber	uint16
	одредиштеПортаnumber	uint16

	должина		uint16
	checksum	uint16
}

func (само *TКорисникdatagramprotocolheader) Init(buffer_2 *TКорисникdatagramprotocolheaderbuffer) {
	само.изворПортаnumber = Построиtounsignedinteger16(buffer_2.изворПортаnumber)
	само.одредиштеПортаnumber = Построиtounsignedinteger16(buffer_2.одредиштеПортаnumber)

	само.должина = Построиtounsignedinteger16(buffer_2.должина)
	само.checksum = Построиtounsignedinteger16(buffer_2.checksum)
}
func (само *TКорисникdatagramprotocolheader) Поставиbuffer(buffer_2 *TКорисникdatagramprotocolheaderbuffer) {

	buffer_2.изворПортаnumber = Unsignedinteger16toПострои(само.изворПортаnumber)
	buffer_2.одредиштеПортаnumber = Unsignedinteger16toПострои(само.одредиштеПортаnumber)

	buffer_2.должина = Unsignedinteger16toПострои(само.должина)
	buffer_2.checksum = Unsignedinteger16toПострои(само.checksum)

}

type IКорисникdatagramprotocolhandler interface {
	HandleКорисникdatagramprotocolПорака(socket *TКорисникdatagramprotocolsocket, data uintptr, големина uint16)
}

type TКорисникdatagramprotocolhandler struct {
}

func (само *TКорисникdatagramprotocolhandler) Init(backend TИнтернетprotocolprovider) {
}
func (само *TКорисникdatagramprotocolhandler) HandleКорисникdatagramprotocolПорака(socket *TКорисникdatagramprotocolsocket, data uintptr, големина uint16) {
}

type IКорисникdatagramprotocolsocket interface {
	HandleКорисникdatagramprotocolПорака(data uintptr, големина uint16)
}
type TКорисникdatagramprotocolsocket struct {
	remoteПортаnumber	uint16
	remoteip		uint32
	localПортаnumber	uint16
	localip			uint32

	listening	bool
}

var udpprovider TКорисникdatagramprotocolprovider
var udphandler IКорисникdatagramprotocolhandler

func (само *TКорисникdatagramprotocolsocket) Test() {
}
func (само *TКорисникdatagramprotocolsocket) Init(pudpprovider TКорисникdatagramprotocolprovider, pudphandler IКорисникdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	само.listening = false
}
func (само *TКорисникdatagramprotocolsocket) HandleКорисникdatagramprotocolПорака(data uintptr, големина uint16) {
	if udphandler != nil {
		udphandler.HandleКорисникdatagramprotocolПорака(само, data, големина)
	}
}
func (само *TКорисникdatagramprotocolsocket) Испрати(pdata []byte, големина uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(големина); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Испрати(само, data, големина)
}
func (само *TКорисникdatagramprotocolsocket) Одврзисе() {
	udpprovider.Одврзисе(само)
}

type TКорисникdatagramprotocolprovider struct {
}

var iphandler IИнтернетprotocolhandler
var sockets [65535]TКорисникdatagramprotocolsocket
var numbersockets int
var слободниПорта uint16

func (само *TКорисникdatagramprotocolprovider) Init(pipprovider TИнтернетprotocolprovider, piphandler IИнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	слободниПорта = 1024
}
func (само *TКорисникdatagramprotocolprovider) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, интернетprotocolpayload uintptr, големина uint32) bool {
	if големина < udpheaderГолемина {
		return false
	}

	var buffer_2 *TКорисникdatagramprotocolheaderbuffer = (*TКорисникdatagramprotocolheaderbuffer)(Pointer(интернетprotocolpayload))
	var msg TКорисникdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TКорисникdatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localПортаnumber == msg.одредиштеПортаnumber && sockets[i].localip == одредиштеipaddressМрежаbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteПортаnumber = msg.изворПортаnumber
			socket.remoteip = изворipaddressМрежаbyteorder
		} else if sockets[i].localПортаnumber == msg.одредиштеПортаnumber && sockets[i].localip == одредиштеipaddressМрежаbyteorder && sockets[i].remoteПортаnumber == msg.изворПортаnumber && sockets[i].remoteip == изворipaddressМрежаbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Поставиbuffer(buffer_2)
	if socket != nil {
		socket.HandleКорисникdatagramprotocolПорака(интернетprotocolpayload+uintptr(udpheaderГолемина), uint16(големина-udpheaderГолемина))
	}

	return false
}

func (само *TКорисникdatagramprotocolprovider) Врзисе(ip uint32, порта uint16) *TКорисникdatagramprotocolsocket {
	var меморијаmanager = &TМеморијаmanager{}
	var socket = (*TКорисникdatagramprotocolsocket)(меморијаmanager.Malloc(50))

	if socket != nil {

		socket.Init(*само, nil)
		socket.remoteПортаnumber = порта
		socket.remoteip = ip
		socket.localПортаnumber = слободниПорта
		слободниПорта++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteПортаnumber = Unsignedinteger16r(socket.remoteПортаnumber)
		socket.localПортаnumber = Unsignedinteger16r(socket.localПортаnumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (само *TКорисникdatagramprotocolprovider) Listen(порта uint16) *TКорисникdatagramprotocolsocket {
	var socket = &TКорисникdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*само, nil)
		socket.listening = true
		socket.localПортаnumber = порта
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localПортаnumber = Unsignedinteger16r(socket.localПортаnumber)
	}
	return socket
}
func (само *TКорисникdatagramprotocolprovider) Одврзисе(socket *TКорисникdatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (само *TКорисникdatagramprotocolprovider) Испрати(socket *TКорисникdatagramprotocolsocket, pdata uintptr, големина uint16) {
	var вкупноДолжина = uint32(големина) + udpheaderГолемина

	var buffer_2 [4096]byte

	var msgbuffer = (*TКорисникdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TКорисникdatagramprotocolheader{}

	msg.изворПортаnumber = socket.localПортаnumber
	msg.одредиштеПортаnumber = socket.remoteПортаnumber
	msg.должина = Unsignedinteger16r(uint16(вкупноДолжина))

	msg.checksum = 0x0
	msg.Поставиbuffer(msgbuffer)

	var dataбајти [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(големина); i++ {
		buffer_2[int(udpheaderГолемина)+i] = dataбајти[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Испрати(socket.remoteip, 0x11, data, вкупноДолжина)

}
func (само *TКорисникdatagramprotocolprovider) Bind(socket *TКорисникdatagramprotocolsocket, handler *TКорисникdatagramprotocolhandler,) {
}
