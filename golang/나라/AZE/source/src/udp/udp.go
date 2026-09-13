package udp

import . "unsafe"
import . "console"
import . "util"
import . "yaddaşmanager"
import . "ipv4"

var udpconsole = TConsole{}

type Tİstifadəçidatagramprotocolheaderbuffer struct {
	mənbəQapınumber		[2]byte
	destinationQapınumber	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheaderBöyüklük uint32 = 8

type Tİstifadəçidatagramprotocolheader struct {
	mənbəQapınumber		uint16
	destinationQapınumber	uint16

	length		uint16
	checksum	uint16
}

func (self *Tİstifadəçidatagramprotocolheader) Init(buffer_2 *Tİstifadəçidatagramprotocolheaderbuffer) {
	self.mənbəQapınumber = Arraytounsignedinteger16(buffer_2.mənbəQapınumber)
	self.destinationQapınumber = Arraytounsignedinteger16(buffer_2.destinationQapınumber)

	self.length = Arraytounsignedinteger16(buffer_2.length)
	self.checksum = Arraytounsignedinteger16(buffer_2.checksum)
}
func (self *Tİstifadəçidatagramprotocolheader) Setbuffer(buffer_2 *Tİstifadəçidatagramprotocolheaderbuffer) {

	buffer_2.mənbəQapınumber = Unsignedinteger16toarray(self.mənbəQapınumber)
	buffer_2.destinationQapınumber = Unsignedinteger16toarray(self.destinationQapınumber)

	buffer_2.length = Unsignedinteger16toarray(self.length)
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

}

type Iİstifadəçidatagramprotocolhandler interface {
	Handleİstifadəçidatagramprotocolİsmarıc(socket *Tİstifadəçidatagramprotocolsocket, data uintptr, böyüklük uint16)
}

type Tİstifadəçidatagramprotocolhandler struct {
}

func (self *Tİstifadəçidatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *Tİstifadəçidatagramprotocolhandler) Handleİstifadəçidatagramprotocolİsmarıc(socket *Tİstifadəçidatagramprotocolsocket, data uintptr, böyüklük uint16) {
}

type Iİstifadəçidatagramprotocolsocket interface {
	Handleİstifadəçidatagramprotocolİsmarıc(data uintptr, böyüklük uint16)
}
type Tİstifadəçidatagramprotocolsocket struct {
	remoteQapınumber	uint16
	remoteip		uint32
	localQapınumber		uint16
	localip			uint32

	listening	bool
}

var udpprovider Tİstifadəçidatagramprotocolprovider
var udphandler Iİstifadəçidatagramprotocolhandler

func (self *Tİstifadəçidatagramprotocolsocket) Test() {
}
func (self *Tİstifadəçidatagramprotocolsocket) Init(pudpprovider Tİstifadəçidatagramprotocolprovider, pudphandler Iİstifadəçidatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *Tİstifadəçidatagramprotocolsocket) Handleİstifadəçidatagramprotocolİsmarıc(data uintptr, böyüklük uint16) {
	if udphandler != nil {
		udphandler.Handleİstifadəçidatagramprotocolİsmarıc(self, data, böyüklük)
	}
}
func (self *Tİstifadəçidatagramprotocolsocket) Send(pdata []byte, böyüklük uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(böyüklük); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, böyüklük)
}
func (self *Tİstifadəçidatagramprotocolsocket) Ayır() {
	udpprovider.Ayır(self)
}

type Tİstifadəçidatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]Tİstifadəçidatagramprotocolsocket
var numbersockets int
var boşQapı uint16

func (self *Tİstifadəçidatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	boşQapı = 1024
}
func (self *Tİstifadəçidatagramprotocolprovider) Internetprotocolreceivewhen(mənbəipaddressŞəbəkəbyteorder uint32, destinationipaddressŞəbəkəbyteorder uint32, internetprotocolpayload uintptr, böyüklük uint32) bool {
	if böyüklük < udpheaderBöyüklük {
		return false
	}

	var buffer_2 *Tİstifadəçidatagramprotocolheaderbuffer = (*Tİstifadəçidatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg Tİstifadəçidatagramprotocolheader
	msg.Init(buffer_2)

	var socket *Tİstifadəçidatagramprotocolsocket = nil

	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i].localQapınumber == msg.destinationQapınumber && sockets[i].localip == destinationipaddressŞəbəkəbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteQapınumber = msg.mənbəQapınumber
			socket.remoteip = mənbəipaddressŞəbəkəbyteorder
		} else if sockets[i].localQapınumber == msg.destinationQapınumber && sockets[i].localip == destinationipaddressŞəbəkəbyteorder && sockets[i].remoteQapınumber == msg.mənbəQapınumber && sockets[i].remoteip == mənbəipaddressŞəbəkəbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.Handleİstifadəçidatagramprotocolİsmarıc(internetprotocolpayload+uintptr(udpheaderBöyüklük), uint16(böyüklük-udpheaderBöyüklük))
	}

	return false
}

func (self *Tİstifadəçidatagramprotocolprovider) Bağlan(ip uint32, qapı uint16) *Tİstifadəçidatagramprotocolsocket {
	var yaddaşmanager = &TYaddaşmanager{}
	var socket = (*Tİstifadəçidatagramprotocolsocket)(yaddaşmanager.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteQapınumber = qapı
		socket.remoteip = ip
		socket.localQapınumber = boşQapı
		boşQapı++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteQapınumber = Unsignedinteger16r(socket.remoteQapınumber)
		socket.localQapınumber = Unsignedinteger16r(socket.localQapınumber)

		sockets[numbersockets] = *socket
		numbersockets++

	}
	return socket

}
func (self *Tİstifadəçidatagramprotocolprovider) Listen(qapı uint16) *Tİstifadəçidatagramprotocolsocket {
	var socket = &Tİstifadəçidatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.localQapınumber = qapı
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localQapınumber = Unsignedinteger16r(socket.localQapınumber)
	}
	return socket
}
func (self *Tİstifadəçidatagramprotocolprovider) Ayır(socket *Tİstifadəçidatagramprotocolsocket) {
	for i := 0; i < numbersockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *Tİstifadəçidatagramprotocolprovider) Send(socket *Tİstifadəçidatagramprotocolsocket, pdata uintptr, böyüklük uint16) {
	var cəmilength = uint32(böyüklük) + udpheaderBöyüklük

	var buffer_2 [4096]byte

	var msgbuffer = (*Tİstifadəçidatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = Tİstifadəçidatagramprotocolheader{}

	msg.mənbəQapınumber = socket.localQapınumber
	msg.destinationQapınumber = socket.remoteQapınumber
	msg.length = Unsignedinteger16r(uint16(cəmilength))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataBayt [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(böyüklük); i++ {
		buffer_2[int(udpheaderBöyüklük)+i] = dataBayt[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(socket.remoteip, 0x11, data, cəmilength)

}
func (self *Tİstifadəçidatagramprotocolprovider) Bind(socket *Tİstifadəçidatagramprotocolsocket, handler *Tİstifadəçidatagramprotocolhandler,) {
}
