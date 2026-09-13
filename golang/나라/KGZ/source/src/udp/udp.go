package udp

import . "unsafe"
import . "console"
import . "util"
import . "эсиmanager"
import . "ipv4"

var udpconsole = TConsole{}

type TКолдонуучуdatagramprotocolheaderbuffer struct {
	баштапкытекстПортНОМЕР	[2]byte
	destinationПортНОМЕР	[2]byte

	узундук		[2]byte
	checksum	[2]byte
}

var udpheaderӨлчөм uint32 = 8

type TКолдонуучуdatagramprotocolheader struct {
	баштапкытекстПортНОМЕР	uint16
	destinationПортНОМЕР	uint16

	узундук		uint16
	checksum	uint16
}

func (self *TКолдонуучуdatagramprotocolheader) Init(buffer_2 *TКолдонуучуdatagramprotocolheaderbuffer) {
	self.баштапкытекстПортНОМЕР = Массивtounsignedinteger16(buffer_2.баштапкытекстПортНОМЕР)
	self.destinationПортНОМЕР = Массивtounsignedinteger16(buffer_2.destinationПортНОМЕР)

	self.узундук = Массивtounsignedinteger16(buffer_2.узундук)
	self.checksum = Массивtounsignedinteger16(buffer_2.checksum)
}
func (self *TКолдонуучуdatagramprotocolheader) Setbuffer(buffer_2 *TКолдонуучуdatagramprotocolheaderbuffer) {

	buffer_2.баштапкытекстПортНОМЕР = Unsignedinteger16toМассив(self.баштапкытекстПортНОМЕР)
	buffer_2.destinationПортНОМЕР = Unsignedinteger16toМассив(self.destinationПортНОМЕР)

	buffer_2.узундук = Unsignedinteger16toМассив(self.узундук)
	buffer_2.checksum = Unsignedinteger16toМассив(self.checksum)

}

type IКолдонуучуdatagramprotocolhandler interface {
	HandleКолдонуучуdatagramprotocolmessage(socket *TКолдонуучуdatagramprotocolsocket, data uintptr, өлчөм uint16)
}

type TКолдонуучуdatagramprotocolhandler struct {
}

func (self *TКолдонуучуdatagramprotocolhandler) Init(backend TИнтернетprotocolprovider) {
}
func (self *TКолдонуучуdatagramprotocolhandler) HandleКолдонуучуdatagramprotocolmessage(socket *TКолдонуучуdatagramprotocolsocket, data uintptr, өлчөм uint16) {
}

type IКолдонуучуdatagramprotocolsocket interface {
	HandleКолдонуучуdatagramprotocolmessage(data uintptr, өлчөм uint16)
}
type TКолдонуучуdatagramprotocolsocket struct {
	remoteПортНОМЕР	uint16
	remoteip	uint32
	localПортНОМЕР	uint16
	localip		uint32

	listening	bool
}

var udpprovider TКолдонуучуdatagramprotocolprovider
var udphandler IКолдонуучуdatagramprotocolhandler

func (self *TКолдонуучуdatagramprotocolsocket) Текшерүү() {
}
func (self *TКолдонуучуdatagramprotocolsocket) Init(pudpprovider TКолдонуучуdatagramprotocolprovider, pudphandler IКолдонуучуdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TКолдонуучуdatagramprotocolsocket) HandleКолдонуучуdatagramprotocolmessage(data uintptr, өлчөм uint16) {
	if udphandler != nil {
		udphandler.HandleКолдонуучуdatagramprotocolmessage(self, data, өлчөм)
	}
}
func (self *TКолдонуучуdatagramprotocolsocket) Send(pdata []byte, өлчөм uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(өлчөм); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, өлчөм)
}
func (self *TКолдонуучуdatagramprotocolsocket) Өчүрүлүү() {
	udpprovider.Өчүрүлүү(self)
}

type TКолдонуучуdatagramprotocolprovider struct {
}

var iphandler IИнтернетprotocolhandler
var sockets [65535]TКолдонуучуdatagramprotocolsocket
var нОМЕРsockets int
var бошПорт uint16

func (self *TКолдонуучуdatagramprotocolprovider) Init(pipprovider TИнтернетprotocolprovider, piphandler IИнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	нОМЕРsockets = 0
	бошПорт = 1024
}
func (self *TКолдонуучуdatagramprotocolprovider) Интернетprotocolreceivewhen(баштапкытекстipaddressТармакbyteorder uint32, destinationipaddressТармакbyteorder uint32, интернетprotocolpayload uintptr, өлчөм uint32) bool {
	if өлчөм < udpheaderӨлчөм {
		return false
	}

	var buffer_2 *TКолдонуучуdatagramprotocolheaderbuffer = (*TКолдонуучуdatagramprotocolheaderbuffer)(Pointer(интернетprotocolpayload))
	var msg TКолдонуучуdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TКолдонуучуdatagramprotocolsocket = nil

	for i := 0; i < нОМЕРsockets && socket == nil; i++ {
		if sockets[i].localПортНОМЕР == msg.destinationПортНОМЕР && sockets[i].localip == destinationipaddressТармакbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteПортНОМЕР = msg.баштапкытекстПортНОМЕР
			socket.remoteip = баштапкытекстipaddressТармакbyteorder
		} else if sockets[i].localПортНОМЕР == msg.destinationПортНОМЕР && sockets[i].localip == destinationipaddressТармакbyteorder && sockets[i].remoteПортНОМЕР == msg.баштапкытекстПортНОМЕР && sockets[i].remoteip == баштапкытекстipaddressТармакbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleКолдонуучуdatagramprotocolmessage(интернетprotocolpayload+uintptr(udpheaderӨлчөм), uint16(өлчөм-udpheaderӨлчөм))
	}

	return false
}

func (self *TКолдонуучуdatagramprotocolprovider) Туташуу(ip uint32, порт uint16) *TКолдонуучуdatagramprotocolsocket {
	var эсиmanager = &TЭсиmanager{}
	var socket = (*TКолдонуучуdatagramprotocolsocket)(эсиmanager.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteПортНОМЕР = порт
		socket.remoteip = ip
		socket.localПортНОМЕР = бошПорт
		бошПорт++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteПортНОМЕР = Unsignedinteger16r(socket.remoteПортНОМЕР)
		socket.localПортНОМЕР = Unsignedinteger16r(socket.localПортНОМЕР)

		sockets[нОМЕРsockets] = *socket
		нОМЕРsockets++

	}
	return socket

}
func (self *TКолдонуучуdatagramprotocolprovider) Listen(порт uint16) *TКолдонуучуdatagramprotocolsocket {
	var socket = &TКолдонуучуdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.localПортНОМЕР = порт
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localПортНОМЕР = Unsignedinteger16r(socket.localПортНОМЕР)
	}
	return socket
}
func (self *TКолдонуучуdatagramprotocolprovider) Өчүрүлүү(socket *TКолдонуучуdatagramprotocolsocket) {
	for i := 0; i < нОМЕРsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			нОМЕРsockets--
			sockets[i] = sockets[нОМЕРsockets]
			break
		}
	}
}
func (self *TКолдонуучуdatagramprotocolprovider) Send(socket *TКолдонуучуdatagramprotocolsocket, pdata uintptr, өлчөм uint16) {
	var бардыгыУзундук = uint32(өлчөм) + udpheaderӨлчөм

	var buffer_2 [4096]byte

	var msgbuffer = (*TКолдонуучуdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TКолдонуучуdatagramprotocolheader{}

	msg.баштапкытекстПортНОМЕР = socket.localПортНОМЕР
	msg.destinationПортНОМЕР = socket.remoteПортНОМЕР
	msg.узундук = Unsignedinteger16r(uint16(бардыгыУзундук))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataБайт [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(өлчөм); i++ {
		buffer_2[int(udpheaderӨлчөм)+i] = dataБайт[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, бардыгыУзундук)

}
func (self *TКолдонуучуdatagramprotocolprovider) Bind(socket *TКолдонуучуdatagramprotocolsocket, handler *TКолдонуучуdatagramprotocolhandler,) {
}
