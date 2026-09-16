/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "konsoly"
import . "util"
import . "arikaMpandrindra"
import . "ipv4"

var udpKonsoly = TKonsoly{}

type TMpampiasadatagramprotocolheaderbuffer struct {
	loharanoIrikanumber	[2]byte
	destinationIrikanumber	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheaderHabe uint32 = 8

type TMpampiasadatagramprotocolheader struct {
	loharanoIrikanumber	uint16
	destinationIrikanumber	uint16

	length		uint16
	checksum	uint16
}

func (nytena *TMpampiasadatagramprotocolheader) Init(buffer_2 *TMpampiasadatagramprotocolheaderbuffer) {
	nytena.loharanoIrikanumber = Arraytounsignedinteger16(buffer_2.loharanoIrikanumber)
	nytena.destinationIrikanumber = Arraytounsignedinteger16(buffer_2.destinationIrikanumber)

	nytena.length = Arraytounsignedinteger16(buffer_2.length)
	nytena.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (nytena *TMpampiasadatagramprotocolheader) Setbuffer(buffer_2 *TMpampiasadatagramprotocolheaderbuffer) {

	buffer_2.loharanoIrikanumber = Unsignedinteger16toarray(nytena.loharanoIrikanumber)
	buffer_2.destinationIrikanumber = Unsignedinteger16toarray(nytena.destinationIrikanumber)

	buffer_2.length = Unsignedinteger16toarray(nytena.length)
	buffer_2.checksum = Unsignedinteger16toarray(nytena.checksum)

}

type IMpampiasadatagramprotocolhandler interface {
	HandleMpampiasadatagramprotocolHafatra(socket *TMpampiasadatagramprotocolsocket, data uintptr, habe uint16)
}

type TMpampiasadatagramprotocolhandler struct {
}

func (nytena *TMpampiasadatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (nytena *TMpampiasadatagramprotocolhandler) HandleMpampiasadatagramprotocolHafatra(socket *TMpampiasadatagramprotocolsocket, data uintptr, habe uint16) {
}

type IMpampiasadatagramprotocolsocket interface {
	HandleMpampiasadatagramprotocolHafatra(data uintptr, habe uint16)
}
type TMpampiasadatagramprotocolsocket struct {
	remoteIrikanumber	uint16
	remoteip		uint32
	localIrikanumber	uint16
	localip			uint32

	listening	bool
}

var udpprovider TMpampiasadatagramprotocolprovider
var udphandler IMpampiasadatagramprotocolhandler

func (nytena *TMpampiasadatagramprotocolsocket) Test() {
}
func (nytena *TMpampiasadatagramprotocolsocket) Init(pudpprovider TMpampiasadatagramprotocolprovider, pudphandler IMpampiasadatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	nytena.listening = false
}
func (nytena *TMpampiasadatagramprotocolsocket) HandleMpampiasadatagramprotocolHafatra(data uintptr, habe uint16) {
	if udphandler != nil {
		udphandler.HandleMpampiasadatagramprotocolHafatra(nytena, data, habe)
	}
}
func (nytena *TMpampiasadatagramprotocolsocket) Send(pdata []byte, habe uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(habe); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(nytena, data, habe)
}
func (nytena *TMpampiasadatagramprotocolsocket) Atsaharo_2() {
	udpprovider.Atsaharo_2(nytena)
}

type TMpampiasadatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TMpampiasadatagramprotocolsocket
var numbersockets int
var malalakaIrika uint16

func (nytena *TMpampiasadatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	malalakaIrika = 1024
}
func (nytena *TMpampiasadatagramprotocolprovider) Internetprotocolreceivewhen(loharanoipaddressRezobyteorder uint32, destinationipaddressRezobyteorder uint32, internetprotocolpayload uintptr, habe uint32) bool {
	if habe < udpheaderHabe {
		return false
	}

	var buffer_2 *TMpampiasadatagramprotocolheaderbuffer = (*TMpampiasadatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TMpampiasadatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TMpampiasadatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localIrikanumber == msg.destinationIrikanumber && sockets[i].localip == destinationipaddressRezobyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteIrikanumber = msg.loharanoIrikanumber
			socket.remoteip = loharanoipaddressRezobyteorder
		} else if sockets[i].localIrikanumber == msg.destinationIrikanumber && sockets[i].localip == destinationipaddressRezobyteorder && sockets[i].remoteIrikanumber == msg.loharanoIrikanumber && sockets[i].remoteip == loharanoipaddressRezobyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleMpampiasadatagramprotocolHafatra(internetprotocolpayload+uintptr(udpheaderHabe), uint16(habe-udpheaderHabe))
	}

	return false
}

func (nytena *TMpampiasadatagramprotocolprovider) Atomboy(ip uint32, irika uint16) *TMpampiasadatagramprotocolsocket {
	var arikaMpandrindra = &TArikaMpandrindra{}
	var socket = (*TMpampiasadatagramprotocolsocket)(arikaMpandrindra.Malloc(50))

	if socket != nil {

		socket.Init(*nytena, nil)
		socket.remoteIrikanumber = irika
		socket.remoteip = ip
		socket.localIrikanumber = malalakaIrika
		malalakaIrika++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteIrikanumber = Unsignedinteger16r(socket.remoteIrikanumber)
		socket.localIrikanumber = Unsignedinteger16r(socket.localIrikanumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (nytena *TMpampiasadatagramprotocolprovider) Listen(irika uint16) *TMpampiasadatagramprotocolsocket {
	var socket = &TMpampiasadatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*nytena, nil)
		socket.listening = true
		socket.localIrikanumber = irika
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localIrikanumber = Unsignedinteger16r(socket.localIrikanumber)
	}
	return socket
}
func (nytena *TMpampiasadatagramprotocolprovider) Atsaharo_2(socket *TMpampiasadatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (nytena *TMpampiasadatagramprotocolprovider) Send(socket *TMpampiasadatagramprotocolsocket, pdata uintptr, habe uint16) {
	var tontalinylength = uint32(habe) + udpheaderHabe

	var buffer_2 [4096]byte

	var msgbuffer = (*TMpampiasadatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TMpampiasadatagramprotocolheader{}

	msg.loharanoIrikanumber = socket.localIrikanumber
	msg.destinationIrikanumber = socket.remoteIrikanumber
	msg.length = Unsignedinteger16r(uint16(tontalinylength))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataOctet [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(habe); i++ {
		buffer_2[int(udpheaderHabe)+i] = dataOctet[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, tontalinylength)

}
func (nytena *TMpampiasadatagramprotocolprovider) Bind(socket *TMpampiasadatagramprotocolsocket, handler *TMpampiasadatagramprotocolhandler) {
}
