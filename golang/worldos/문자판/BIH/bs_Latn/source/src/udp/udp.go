/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "memorijamanager"
import . "ipv4"

var udpconsole = TConsole{}

type TKorisnikdatagramprotocolheaderbuffer struct {
	izvorportBroj		[2]byte
	odredišteportBroj	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheaderVeličina uint32 = 8

type TKorisnikdatagramprotocolheader struct {
	izvorportBroj		uint16
	odredišteportBroj	uint16

	length		uint16
	checksum	uint16
}

func (self *TKorisnikdatagramprotocolheader) Init(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {
	self.izvorportBroj = Arraytounsignedinteger16(buffer_2.izvorportBroj)
	self.odredišteportBroj = Arraytounsignedinteger16(buffer_2.odredišteportBroj)

	self.length = Arraytounsignedinteger16(buffer_2.length)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *TKorisnikdatagramprotocolheader) Skupbuffer(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {

	buffer_2.izvorportBroj = Unsignedinteger16toarray(self.izvorportBroj)
	buffer_2.odredišteportBroj = Unsignedinteger16toarray(self.odredišteportBroj)

	buffer_2.length = Unsignedinteger16toarray(self.length)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type IKorisnikdatagramprotocolhandler interface {
	HandleKorisnikdatagramprotocolPoruka(socket *TKorisnikdatagramprotocolsocket, data uintptr, veličina uint16)
}

type TKorisnikdatagramprotocolhandler struct {
}

func (self *TKorisnikdatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *TKorisnikdatagramprotocolhandler) HandleKorisnikdatagramprotocolPoruka(socket *TKorisnikdatagramprotocolsocket, data uintptr, veličina uint16) {
}

type IKorisnikdatagramprotocolsocket interface {
	HandleKorisnikdatagramprotocolPoruka(data uintptr, veličina uint16)
}
type TKorisnikdatagramprotocolsocket struct {
	remoteportBroj	uint16
	remoteip	uint32
	lokalnaportBroj	uint16
	lokalnaip	uint32

	listening	bool
}

var udpprovider TKorisnikdatagramprotocolprovider
var udphandler IKorisnikdatagramprotocolhandler

func (self *TKorisnikdatagramprotocolsocket) Test() {
}
func (self *TKorisnikdatagramprotocolsocket) Init(pudpprovider TKorisnikdatagramprotocolprovider, pudphandler IKorisnikdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TKorisnikdatagramprotocolsocket) HandleKorisnikdatagramprotocolPoruka(data uintptr, veličina uint16) {
	if udphandler != nil {
		udphandler.HandleKorisnikdatagramprotocolPoruka(self, data, veličina)
	}
}
func (self *TKorisnikdatagramprotocolsocket) Pošalji(pdata []byte, veličina uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(veličina); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Pošalji(self, data, veličina)
}
func (self *TKorisnikdatagramprotocolsocket) Prekinivezu() {
	udpprovider.Prekinivezu(self)
}

type TKorisnikdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TKorisnikdatagramprotocolsocket
var brojsockets int
var slobodnoport uint16

func (self *TKorisnikdatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	brojsockets = 0
	slobodnoport = 1024
}
func (self *TKorisnikdatagramprotocolprovider) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, internetprotocolpayload uintptr, veličina uint32) bool {
	if veličina < udpheaderVeličina {
		return false
	}

	var buffer_2 *TKorisnikdatagramprotocolheaderbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TKorisnikdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TKorisnikdatagramprotocolsocket = nil

	for i := 0; i < brojsockets && socket == nil; i++ {
		if sockets[i].lokalnaportBroj == msg.odredišteportBroj && sockets[i].lokalnaip == odredišteipaddressMrežabyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteportBroj = msg.izvorportBroj
			socket.remoteip = izvoripaddressMrežabyteorder
		} else if sockets[i].lokalnaportBroj == msg.odredišteportBroj && sockets[i].lokalnaip == odredišteipaddressMrežabyteorder && sockets[i].remoteportBroj == msg.izvorportBroj && sockets[i].remoteip == izvoripaddressMrežabyteorder {
			socket = &sockets[i]

		}
	}

	msg.Skupbuffer(buffer_2)
	if socket != nil {
		socket.HandleKorisnikdatagramprotocolPoruka(internetprotocolpayload+uintptr(udpheaderVeličina), uint16(veličina-udpheaderVeličina))
	}

	return false
}

func (self *TKorisnikdatagramprotocolprovider) Spojise(ip uint32, port uint16) *TKorisnikdatagramprotocolsocket {
	var memorijamanager = &TMemorijamanager{}
	var socket = (*TKorisnikdatagramprotocolsocket)(memorijamanager.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteportBroj = port
		socket.remoteip = ip
		socket.lokalnaportBroj = slobodnoport
		slobodnoport++
		socket.lokalnaip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteportBroj = Unsignedinteger16r(socket.remoteportBroj)
		socket.lokalnaportBroj = Unsignedinteger16r(socket.lokalnaportBroj)

		sockets[brojsockets] = *socket
		brojsockets++

	}
	return socket

}
func (self *TKorisnikdatagramprotocolprovider) Listen(port uint16) *TKorisnikdatagramprotocolsocket {
	var socket = &TKorisnikdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.lokalnaportBroj = port
		socket.lokalnaip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.lokalnaportBroj = Unsignedinteger16r(socket.lokalnaportBroj)
	}
	return socket
}
func (self *TKorisnikdatagramprotocolprovider) Prekinivezu(socket *TKorisnikdatagramprotocolsocket) {
	for i := 0; i < brojsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			brojsockets--
			sockets[i] = sockets[brojsockets]
			break
		}
	}
}
func (self *TKorisnikdatagramprotocolprovider) Pošalji(socket *TKorisnikdatagramprotocolsocket, pdata uintptr, veličina uint16) {
	var ukupnolength = uint32(veličina) + udpheaderVeličina

	var buffer_2 [4096]byte

	var msgbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKorisnikdatagramprotocolheader{}

	msg.izvorportBroj = socket.lokalnaportBroj
	msg.odredišteportBroj = socket.remoteportBroj
	msg.length = Unsignedinteger16r(uint16(ukupnolength))

	msg.checksum = 0x0
	msg.Skupbuffer(msgbuffer)

	var dataBajtova [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(veličina); i++ {
		buffer_2[int(udpheaderVeličina)+i] = dataBajtova[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Pošalji(socket.remoteip, 0x11, data, ukupnolength)

}
func (self *TKorisnikdatagramprotocolprovider) Bind(socket *TKorisnikdatagramprotocolsocket, handler *TKorisnikdatagramprotocolhandler) {
}
