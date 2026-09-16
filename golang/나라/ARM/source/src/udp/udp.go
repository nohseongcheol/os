/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "հիշողությունmanager"
import . "ipv4"

var udpconsole = TConsole{}

type TՕգտագործողdatagramprotocolheaderbuffer struct {
	աղբյուրՊորտՀԱՄԱՐ	[2]byte
	destinationՊորտՀԱՄԱՐ	[2]byte

	երկարություն	[2]byte
	checksum	[2]byte
}

var udpheaderՉափս uint32 = 8

type TՕգտագործողdatagramprotocolheader struct {
	աղբյուրՊորտՀԱՄԱՐ	uint16
	destinationՊորտՀԱՄԱՐ	uint16

	երկարություն	uint16
	checksum	uint16
}

func (ինքնուրույն *TՕգտագործողdatagramprotocolheader) Init(buffer_2 *TՕգտագործողdatagramprotocolheaderbuffer) {
	ինքնուրույն.աղբյուրՊորտՀԱՄԱՐ = Զանգվածtounsignedinteger16(buffer_2.աղբյուրՊորտՀԱՄԱՐ)
	ինքնուրույն.destinationՊորտՀԱՄԱՐ = Զանգվածtounsignedinteger16(buffer_2.destinationՊորտՀԱՄԱՐ)

	ինքնուրույն.երկարություն = Զանգվածtounsignedinteger16(buffer_2.երկարություն)
	ինքնուրույն.checksum = Զանգվածtounsignedinteger16(buffer_2.checksum)
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolheader) Setbuffer(buffer_2 *TՕգտագործողdatagramprotocolheaderbuffer) {

	buffer_2.աղբյուրՊորտՀԱՄԱՐ = Unsignedinteger16toԶանգված(ինքնուրույն.աղբյուրՊորտՀԱՄԱՐ)
	buffer_2.destinationՊորտՀԱՄԱՐ = Unsignedinteger16toԶանգված(ինքնուրույն.destinationՊորտՀԱՄԱՐ)

	buffer_2.երկարություն = Unsignedinteger16toԶանգված(ինքնուրույն.երկարություն)
	buffer_2.checksum = Unsignedinteger16toԶանգված(ինքնուրույն.checksum)

}

type IՕգտագործողdatagramprotocolhandler interface {
	HandleՕգտագործողdatagramprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ(socket *TՕգտագործողdatagramprotocolsocket, data uintptr, չափս uint16)
}

type TՕգտագործողdatagramprotocolhandler struct {
}

func (ինքնուրույն *TՕգտագործողdatagramprotocolhandler) Init(backend TՀամացանցprotocolprovider) {
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolhandler) HandleՕգտագործողdatagramprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ(socket *TՕգտագործողdatagramprotocolsocket, data uintptr, չափս uint16) {
}

type IՕգտագործողdatagramprotocolsocket interface {
	HandleՕգտագործողdatagramprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ(data uintptr, չափս uint16)
}
type TՕգտագործողdatagramprotocolsocket struct {
	remoteՊորտՀԱՄԱՐ		uint16
	remoteip		uint32
	տեղայինՊորտՀԱՄԱՐ	uint16
	տեղայինip		uint32

	listening	bool
}

var udpprovider TՕգտագործողdatagramprotocolprovider
var udphandler IՕգտագործողdatagramprotocolhandler

func (ինքնուրույն *TՕգտագործողdatagramprotocolsocket) Թեստ() {
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolsocket) Init(pudpprovider TՕգտագործողdatagramprotocolprovider, pudphandler IՕգտագործողdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	ինքնուրույն.listening = false
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolsocket) HandleՕգտագործողdatagramprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ(data uintptr, չափս uint16) {
	if udphandler != nil {
		udphandler.HandleՕգտագործողdatagramprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ(ինքնուրույն, data, չափս)
	}
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolsocket) ՈՒղարկել(pdata []byte, չափս uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(չափս); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.ՈՒղարկել(ինքնուրույն, data, չափս)
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolsocket) Անջատել() {
	udpprovider.Անջատել(ինքնուրույն)
}

type TՕգտագործողdatagramprotocolprovider struct {
}

var iphandler IՀամացանցprotocolhandler
var sockets [65535]TՕգտագործողdatagramprotocolsocket
var հԱՄԱՐsockets int
var ազատՊորտ uint16

func (ինքնուրույն *TՕգտագործողdatagramprotocolprovider) Init(pipprovider TՀամացանցprotocolprovider, piphandler IՀամացանցprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	հԱՄԱՐsockets = 0
	ազատՊորտ = 1024
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolprovider) Համացանցprotocolreceivewhen(աղբյուրipaddressՑանցbyteorder uint32, destinationipaddressՑանցbyteorder uint32, համացանցprotocolpayload uintptr, չափս uint32) bool {
	if չափս < udpheaderՉափս {
		return false
	}

	var buffer_2 *TՕգտագործողdatagramprotocolheaderbuffer = (*TՕգտագործողdatagramprotocolheaderbuffer)(Pointer(համացանցprotocolpayload))
	var msg TՕգտագործողdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TՕգտագործողdatagramprotocolsocket = nil

	for i := 0; i < հԱՄԱՐsockets && socket == nil; i++ {
		if sockets[i].տեղայինՊորտՀԱՄԱՐ == msg.destinationՊորտՀԱՄԱՐ && sockets[i].տեղայինip == destinationipaddressՑանցbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteՊորտՀԱՄԱՐ = msg.աղբյուրՊորտՀԱՄԱՐ
			socket.remoteip = աղբյուրipaddressՑանցbyteorder
		} else if sockets[i].տեղայինՊորտՀԱՄԱՐ == msg.destinationՊորտՀԱՄԱՐ && sockets[i].տեղայինip == destinationipaddressՑանցbyteorder && sockets[i].remoteՊորտՀԱՄԱՐ == msg.աղբյուրՊորտՀԱՄԱՐ && sockets[i].remoteip == աղբյուրipaddressՑանցbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.HandleՕգտագործողdatagramprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ(համացանցprotocolpayload+uintptr(udpheaderՉափս), uint16(չափս-udpheaderՉափս))
	}

	return false
}

func (ինքնուրույն *TՕգտագործողdatagramprotocolprovider) Միացնել(ip uint32, պորտ uint16) *TՕգտագործողdatagramprotocolsocket {
	var հիշողությունmanager = &TՀիշողությունmanager{}
	var socket = (*TՕգտագործողdatagramprotocolsocket)(հիշողությունmanager.Malloc(50))

	if socket != nil {

		socket.Init(*ինքնուրույն, nil)
		socket.remoteՊորտՀԱՄԱՐ = պորտ
		socket.remoteip = ip
		socket.տեղայինՊորտՀԱՄԱՐ = ազատՊորտ
		ազատՊորտ++
		socket.տեղայինip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteՊորտՀԱՄԱՐ = Unsignedinteger16r(socket.remoteՊորտՀԱՄԱՐ)
		socket.տեղայինՊորտՀԱՄԱՐ = Unsignedinteger16r(socket.տեղայինՊորտՀԱՄԱՐ)

		sockets[հԱՄԱՐsockets] = *socket
		հԱՄԱՐsockets++

	}
	return socket

}
func (ինքնուրույն *TՕգտագործողdatagramprotocolprovider) Listen(պորտ uint16) *TՕգտագործողdatagramprotocolsocket {
	var socket = &TՕգտագործողdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*ինքնուրույն, nil)
		socket.listening = true
		socket.տեղայինՊորտՀԱՄԱՐ = պորտ
		socket.տեղայինip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.տեղայինՊորտՀԱՄԱՐ = Unsignedinteger16r(socket.տեղայինՊորտՀԱՄԱՐ)
	}
	return socket
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolprovider) Անջատել(socket *TՕգտագործողdatagramprotocolsocket) {
	for i := 0; i < հԱՄԱՐsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			հԱՄԱՐsockets--
			sockets[i] = sockets[հԱՄԱՐsockets]
			break
		}
	}
}
func (ինքնուրույն *TՕգտագործողdatagramprotocolprovider) ՈՒղարկել(socket *TՕգտագործողdatagramprotocolsocket, pdata uintptr, չափս uint16) {
	var ընդհանուրԵրկարություն = uint32(չափս) + udpheaderՉափս

	var buffer_2 [4096]byte

	var msgbuffer = (*TՕգտագործողdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TՕգտագործողdatagramprotocolheader{}

	msg.աղբյուրՊորտՀԱՄԱՐ = socket.տեղայինՊորտՀԱՄԱՐ
	msg.destinationՊորտՀԱՄԱՐ = socket.remoteՊորտՀԱՄԱՐ
	msg.երկարություն = Unsignedinteger16r(uint16(ընդհանուրԵրկարություն))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataԲայթեր [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(չափս); i++ {
		buffer_2[int(udpheaderՉափս)+i] = dataԲայթեր[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.ՈՒղարկել(socket.remoteip, 0x11, data, ընդհանուրԵրկարություն)

}
func (ինքնուրույն *TՕգտագործողdatagramprotocolprovider) Bind(socket *TՕգտագործողdatagramprotocolsocket, handler *TՕգտագործողdatagramprotocolhandler,) {
}
