/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "konsolë"
import . "util"
import . "memoriaManazhuesi"
import . "ipv4"

var udpKonsolë = TKonsolë{}

type TPërdoruesidatagramprotocolheaderbuffer struct {
	burimiPortanumber	[2]byte
	destinacioniPortanumber	[2]byte

	gjatësi		[2]byte
	checksum	[2]byte
}

var udpheaderMadhësia uint32 = 8

type TPërdoruesidatagramprotocolheader struct {
	burimiPortanumber	uint16
	destinacioniPortanumber	uint16

	gjatësi		uint16
	checksum	uint16
}

func (vetvetja *TPërdoruesidatagramprotocolheader) Init(buffer_2 *TPërdoruesidatagramprotocolheaderbuffer) {
	vetvetja.burimiPortanumber = Rreshtimitounsignedinteger16(buffer_2.burimiPortanumber)
	vetvetja.destinacioniPortanumber = Rreshtimitounsignedinteger16(buffer_2.destinacioniPortanumber)

	vetvetja.gjatësi = Rreshtimitounsignedinteger16(buffer_2.gjatësi)
	vetvetja.checksum = Rreshtimitounsignedinteger16(buffer_2.checksum)
}
func (vetvetja *TPërdoruesidatagramprotocolheader) Caktonibuffer(buffer_2 *TPërdoruesidatagramprotocolheaderbuffer) {

	buffer_2.burimiPortanumber = Unsignedinteger16toRreshtimi(vetvetja.burimiPortanumber)
	buffer_2.destinacioniPortanumber = Unsignedinteger16toRreshtimi(vetvetja.destinacioniPortanumber)

	buffer_2.gjatësi = Unsignedinteger16toRreshtimi(vetvetja.gjatësi)
	buffer_2.checksum = Unsignedinteger16toRreshtimi(vetvetja.checksum)

}

type IPërdoruesidatagramprotocolhandler interface {
	HandlePërdoruesidatagramprotocolMesazhi(socket *TPërdoruesidatagramprotocolsocket, data uintptr, madhësia uint16)
}

type TPërdoruesidatagramprotocolhandler struct {
}

func (vetvetja *TPërdoruesidatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (vetvetja *TPërdoruesidatagramprotocolhandler) HandlePërdoruesidatagramprotocolMesazhi(socket *TPërdoruesidatagramprotocolsocket, data uintptr, madhësia uint16) {
}

type IPërdoruesidatagramprotocolsocket interface {
	HandlePërdoruesidatagramprotocolMesazhi(data uintptr, madhësia uint16)
}
type TPërdoruesidatagramprotocolsocket struct {
	remotePortanumber	uint16
	remoteip		uint32
	localPortanumber	uint16
	localip			uint32

	listening	bool
}

var udpprovider TPërdoruesidatagramprotocolprovider
var udphandler IPërdoruesidatagramprotocolhandler

func (vetvetja *TPërdoruesidatagramprotocolsocket) Provo() {
}
func (vetvetja *TPërdoruesidatagramprotocolsocket) Init(pudpprovider TPërdoruesidatagramprotocolprovider, pudphandler IPërdoruesidatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	vetvetja.listening = false
}
func (vetvetja *TPërdoruesidatagramprotocolsocket) HandlePërdoruesidatagramprotocolMesazhi(data uintptr, madhësia uint16) {
	if udphandler != nil {
		udphandler.HandlePërdoruesidatagramprotocolMesazhi(vetvetja, data, madhësia)
	}
}
func (vetvetja *TPërdoruesidatagramprotocolsocket) Dërgo(pdata []byte, madhësia uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(madhësia); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Dërgo(vetvetja, data, madhësia)
}
func (vetvetja *TPërdoruesidatagramprotocolsocket) Shkëputu() {
	udpprovider.Shkëputu(vetvetja)
}

type TPërdoruesidatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TPërdoruesidatagramprotocolsocket
var numbersockets int
var elirëPorta uint16

func (vetvetja *TPërdoruesidatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	elirëPorta = 1024
}
func (vetvetja *TPërdoruesidatagramprotocolprovider) Internetprotocolreceivewhen(burimiipaddressRrjetibyteorder uint32, destinacioniipaddressRrjetibyteorder uint32, internetprotocolpayload uintptr, madhësia uint32) bool {
	if madhësia < udpheaderMadhësia {
		return false
	}

	var buffer_2 *TPërdoruesidatagramprotocolheaderbuffer = (*TPërdoruesidatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TPërdoruesidatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TPërdoruesidatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localPortanumber == msg.destinacioniPortanumber && sockets[i].localip == destinacioniipaddressRrjetibyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remotePortanumber = msg.burimiPortanumber
			socket.remoteip = burimiipaddressRrjetibyteorder
		} else if sockets[i].localPortanumber == msg.destinacioniPortanumber && sockets[i].localip == destinacioniipaddressRrjetibyteorder && sockets[i].remotePortanumber == msg.burimiPortanumber && sockets[i].remoteip == burimiipaddressRrjetibyteorder {
			socket = &sockets[i]

		}
	}

	msg.Caktonibuffer(buffer_2)
	if socket != nil {
		socket.HandlePërdoruesidatagramprotocolMesazhi(internetprotocolpayload+uintptr(udpheaderMadhësia), uint16(madhësia-udpheaderMadhësia))
	}

	return false
}

func (vetvetja *TPërdoruesidatagramprotocolprovider) Lidhu(ip uint32, porta uint16) *TPërdoruesidatagramprotocolsocket {
	var memoriaManazhuesi = &TMemoriaManazhuesi{}
	var socket = (*TPërdoruesidatagramprotocolsocket)(memoriaManazhuesi.Malloc(50))

	if socket != nil {

		socket.Init(*vetvetja, nil)
		socket.remotePortanumber = porta
		socket.remoteip = ip
		socket.localPortanumber = elirëPorta
		elirëPorta++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remotePortanumber = Unsignedinteger16r(socket.remotePortanumber)
		socket.localPortanumber = Unsignedinteger16r(socket.localPortanumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (vetvetja *TPërdoruesidatagramprotocolprovider) Listen(porta uint16) *TPërdoruesidatagramprotocolsocket {
	var socket = &TPërdoruesidatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*vetvetja, nil)
		socket.listening = true
		socket.localPortanumber = porta
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localPortanumber = Unsignedinteger16r(socket.localPortanumber)
	}
	return socket
}
func (vetvetja *TPërdoruesidatagramprotocolprovider) Shkëputu(socket *TPërdoruesidatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (vetvetja *TPërdoruesidatagramprotocolprovider) Dërgo(socket *TPërdoruesidatagramprotocolsocket, pdata uintptr, madhësia uint16) {
	var gjithsejGjatësi = uint32(madhësia) + udpheaderMadhësia

	var buffer_2 [4096]byte

	var msgbuffer = (*TPërdoruesidatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TPërdoruesidatagramprotocolheader{}

	msg.burimiPortanumber = socket.localPortanumber
	msg.destinacioniPortanumber = socket.remotePortanumber
	msg.gjatësi = Unsignedinteger16r(uint16(gjithsejGjatësi))

	msg.checksum = 0x0
	msg.Caktonibuffer(msgbuffer)

	var databytes [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(madhësia); i++ {
		buffer_2[int(udpheaderMadhësia)+i] = databytes[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Dërgo(socket.remoteip, 0x11, data, gjithsejGjatësi)

}
func (vetvetja *TPërdoruesidatagramprotocolprovider) Bind(socket *TPërdoruesidatagramprotocolsocket, handler *TPërdoruesidatagramprotocolhandler,) {
}
