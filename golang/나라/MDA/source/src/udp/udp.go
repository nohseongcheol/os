package udp

import . "unsafe"
import . "console"
import . "util"
import . "memoriemanager"
import . "ipv4"

var udpconsole = TConsole{}

type TUtilizatordatagramprotocolheaderbuffer struct {
	sursăportNumăr		[2]byte
	destinațieportNumăr	[2]byte

	durată		[2]byte
	checksum	[2]byte
}

var udpheaderMărime uint32 = 8

type TUtilizatordatagramprotocolheader struct {
	sursăportNumăr		uint16
	destinațieportNumăr	uint16

	durată		uint16
	checksum	uint16
}

func (sine *TUtilizatordatagramprotocolheader) Init(buffer_2 *TUtilizatordatagramprotocolheaderbuffer) {
	sine.sursăportNumăr = Vectortounsignedinteger16(buffer_2.sursăportNumăr)
	sine.destinațieportNumăr = Vectortounsignedinteger16(buffer_2.destinațieportNumăr)

	sine.durată = Vectortounsignedinteger16(buffer_2.durată)
	sine.checksum = Vectortounsignedinteger16(buffer_2.checksum)
}
func (sine *TUtilizatordatagramprotocolheader) Definitbuffer(buffer_2 *TUtilizatordatagramprotocolheaderbuffer) {

	buffer_2.sursăportNumăr = Unsignedinteger16toVector(sine.sursăportNumăr)
	buffer_2.destinațieportNumăr = Unsignedinteger16toVector(sine.destinațieportNumăr)

	buffer_2.durată = Unsignedinteger16toVector(sine.durată)
	buffer_2.checksum = Unsignedinteger16toVector(sine.checksum)

}

type IUtilizatordatagramprotocolhandler interface {
	MânerUtilizatordatagramprotocolMesaj(socket *TUtilizatordatagramprotocolsocket, data uintptr, mărime uint16)
}

type TUtilizatordatagramprotocolhandler struct {
}

func (sine *TUtilizatordatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (sine *TUtilizatordatagramprotocolhandler) MânerUtilizatordatagramprotocolMesaj(socket *TUtilizatordatagramprotocolsocket, data uintptr, mărime uint16) {
}

type IUtilizatordatagramprotocolsocket interface {
	MânerUtilizatordatagramprotocolMesaj(data uintptr, mărime uint16)
}
type TUtilizatordatagramprotocolsocket struct {
	ladistanțăportNumăr	uint16
	ladistanțăip		uint32
	localportNumăr		uint16
	localip			uint32

	listening	bool
}

var udpprovider TUtilizatordatagramprotocolprovider
var udphandler IUtilizatordatagramprotocolhandler

func (sine *TUtilizatordatagramprotocolsocket) Testează() {
}
func (sine *TUtilizatordatagramprotocolsocket) Init(pudpprovider TUtilizatordatagramprotocolprovider, pudphandler IUtilizatordatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	sine.listening = false
}
func (sine *TUtilizatordatagramprotocolsocket) MânerUtilizatordatagramprotocolMesaj(data uintptr, mărime uint16) {
	if udphandler != nil {
		udphandler.MânerUtilizatordatagramprotocolMesaj(sine, data, mărime)
	}
}
func (sine *TUtilizatordatagramprotocolsocket) Trimite(pdata []byte, mărime uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(mărime); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Trimite(sine, data, mărime)
}
func (sine *TUtilizatordatagramprotocolsocket) Deconectează() {
	udpprovider.Deconectează(sine)
}

type TUtilizatordatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TUtilizatordatagramprotocolsocket
var numărsockets int
var liberport uint16

func (sine *TUtilizatordatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numărsockets = 0
	liberport = 1024
}
func (sine *TUtilizatordatagramprotocolprovider) Internetprotocolreceivewhen(sursăipaddressRețeabyteorder uint32, destinațieipaddressRețeabyteorder uint32, internetprotocolpayload uintptr, mărime uint32) bool {
	if mărime < udpheaderMărime {
		return false
	}

	var buffer_2 *TUtilizatordatagramprotocolheaderbuffer = (*TUtilizatordatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TUtilizatordatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TUtilizatordatagramprotocolsocket = nil

	for i := 0; i < numărsockets && socket == nil; i++ {
		if sockets[i].localportNumăr == msg.destinațieportNumăr && sockets[i].localip == destinațieipaddressRețeabyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.ladistanțăportNumăr = msg.sursăportNumăr
			socket.ladistanțăip = sursăipaddressRețeabyteorder
		} else if sockets[i].localportNumăr == msg.destinațieportNumăr && sockets[i].localip == destinațieipaddressRețeabyteorder && sockets[i].ladistanțăportNumăr == msg.sursăportNumăr && sockets[i].ladistanțăip == sursăipaddressRețeabyteorder {
			socket = &sockets[i]

		}
	}

	msg.Definitbuffer(buffer_2)
	if socket != nil {
		socket.MânerUtilizatordatagramprotocolMesaj(internetprotocolpayload+uintptr(udpheaderMărime), uint16(mărime-udpheaderMărime))
	}

	return false
}

func (sine *TUtilizatordatagramprotocolprovider) Conectează(ip uint32, port uint16) *TUtilizatordatagramprotocolsocket {
	var memoriemanager = &TMemoriemanager{}
	var socket = (*TUtilizatordatagramprotocolsocket)(memoriemanager.Malloc(50))

	if socket != nil {

		socket.Init(*sine, nil)
		socket.ladistanțăportNumăr = port
		socket.ladistanțăip = ip
		socket.localportNumăr = liberport
		liberport++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.ladistanțăportNumăr = Unsignedinteger16r(socket.ladistanțăportNumăr)
		socket.localportNumăr = Unsignedinteger16r(socket.localportNumăr)

		sockets[numărsockets] = *socket
		numărsockets++

	}
	return socket

}
func (sine *TUtilizatordatagramprotocolprovider) Listen(port uint16) *TUtilizatordatagramprotocolsocket {
	var socket = &TUtilizatordatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*sine, nil)
		socket.listening = true
		socket.localportNumăr = port
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localportNumăr = Unsignedinteger16r(socket.localportNumăr)
	}
	return socket
}
func (sine *TUtilizatordatagramprotocolprovider) Deconectează(socket *TUtilizatordatagramprotocolsocket) {
	for i := 0; i < numărsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numărsockets--
			sockets[i] = sockets[numărsockets]
			break
		}
	}
}
func (sine *TUtilizatordatagramprotocolprovider) Trimite(socket *TUtilizatordatagramprotocolsocket, pdata uintptr, mărime uint16) {
	var totalDurată = uint32(mărime) + udpheaderMărime

	var buffer_2 [4096]byte

	var msgbuffer = (*TUtilizatordatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TUtilizatordatagramprotocolheader{}

	msg.sursăportNumăr = socket.localportNumăr
	msg.destinațieportNumăr = socket.ladistanțăportNumăr
	msg.durată = Unsignedinteger16r(uint16(totalDurată))

	msg.checksum = 0x0
	msg.Definitbuffer(msgbuffer)

	var dataOcteți [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(mărime); i++ {
		buffer_2[int(udpheaderMărime)+i] = dataOcteți[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Trimite(socket.ladistanțăip, 0x11, data, totalDurată)

}
func (sine *TUtilizatordatagramprotocolprovider) Bind(socket *TUtilizatordatagramprotocolsocket, handler *TUtilizatordatagramprotocolhandler) {
}
