/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "მეხსიერებაmanager"
import . "ipv4"

var udpconsole = TConsole{}

type Tმომხმარებელიdatagramprotocolheaderbuffer struct {
	წყაროპორტირიცხვი	[2]byte
	destinationპორტირიცხვი	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpheaderზომა uint32 = 8

type Tმომხმარებელიdatagramprotocolheader struct {
	წყაროპორტირიცხვი	uint16
	destinationპორტირიცხვი	uint16

	length		uint16
	checksum	uint16
}

func (self *Tმომხმარებელიdatagramprotocolheader) Init(buffer_2 *Tმომხმარებელიdatagramprotocolheaderbuffer) {
	self.წყაროპორტირიცხვი = Aმასივიtounsignedinteger16(buffer_2.წყაროპორტირიცხვი)
	self.destinationპორტირიცხვი = Aმასივიtounsignedinteger16(buffer_2.destinationპორტირიცხვი)

	self.length = Aმასივიtounsignedinteger16(buffer_2.length)
	self.checksum = Aმასივიtounsignedinteger16(buffer_2.checksum)
}
func (self *Tმომხმარებელიdatagramprotocolheader) Setbuffer(buffer_2 *Tმომხმარებელიdatagramprotocolheaderbuffer) {

	buffer_2.წყაროპორტირიცხვი = Unsignedinteger16toმასივი(self.წყაროპორტირიცხვი)
	buffer_2.destinationპორტირიცხვი = Unsignedinteger16toმასივი(self.destinationპორტირიცხვი)

	buffer_2.length = Unsignedinteger16toმასივი(self.length)
	buffer_2.checksum = Unsignedinteger16toმასივი(self.checksum)

}

type Iმომხმარებელიdatagramprotocolhandler interface {
	Handleმომხმარებელიdatagramprotocolშეტყობინება(socket *Tმომხმარებელიdatagramprotocolsocket, data uintptr, ზომა uint16)
}

type Tმომხმარებელიdatagramprotocolhandler struct {
}

func (self *Tმომხმარებელიdatagramprotocolhandler) Init(backend Tინტერნეტიprotocolprovider) {
}
func (self *Tმომხმარებელიdatagramprotocolhandler) Handleმომხმარებელიdatagramprotocolშეტყობინება(socket *Tმომხმარებელიdatagramprotocolsocket, data uintptr, ზომა uint16) {
}

type Iმომხმარებელიdatagramprotocolsocket interface {
	Handleმომხმარებელიdatagramprotocolშეტყობინება(data uintptr, ზომა uint16)
}
type Tმომხმარებელიdatagramprotocolsocket struct {
	remoteპორტირიცხვი	uint16
	remoteip		uint32
	localპორტირიცხვი	uint16
	localip			uint32

	listening	bool
}

var udpprovider Tმომხმარებელიdatagramprotocolprovider
var udphandler Iმომხმარებელიdatagramprotocolhandler

func (self *Tმომხმარებელიdatagramprotocolsocket) Test() {
}
func (self *Tმომხმარებელიdatagramprotocolsocket) Init(pudpprovider Tმომხმარებელიdatagramprotocolprovider, pudphandler Iმომხმარებელიdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *Tმომხმარებელიdatagramprotocolsocket) Handleმომხმარებელიdatagramprotocolშეტყობინება(data uintptr, ზომა uint16) {
	if udphandler != nil {
		udphandler.Handleმომხმარებელიdatagramprotocolშეტყობინება(self, data, ზომა)
	}
}
func (self *Tმომხმარებელიdatagramprotocolsocket) Sგაგზავნა(pdata []byte, ზომა uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(ზომა); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Sგაგზავნა(self, data, ზომა)
}
func (self *Tმომხმარებელიdatagramprotocolsocket) Dგათიშვა() {
	udpprovider.Dგათიშვა(self)
}

type Tმომხმარებელიdatagramprotocolprovider struct {
}

var iphandler Iინტერნეტიprotocolhandler
var sockets [65535]Tმომხმარებელიdatagramprotocolsocket
var რიცხვიsockets int
var თავისუფალიპორტი uint16

func (self *Tმომხმარებელიdatagramprotocolprovider) Init(pipprovider Tინტერნეტიprotocolprovider, piphandler Iინტერნეტიprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	რიცხვიsockets = 0
	თავისუფალიპორტი = 1024
}
func (self *Tმომხმარებელიdatagramprotocolprovider) Oინტერნეტიprotocolreceivewhen(წყაროipaddressქსელიbyteorder uint32, destinationipaddressქსელიbyteorder uint32, ინტერნეტიprotocolpayload uintptr, ზომა uint32) bool {
	if ზომა < udpheaderზომა {
		return false
	}

	var buffer_2 *Tმომხმარებელიdatagramprotocolheaderbuffer = (*Tმომხმარებელიdatagramprotocolheaderbuffer)(Pointer(ინტერნეტიprotocolpayload))
	var msg Tმომხმარებელიdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *Tმომხმარებელიdatagramprotocolsocket = nil

	for i := 0; i < რიცხვიsockets && socket == nil; i++ {
		if sockets[i].localპორტირიცხვი == msg.destinationპორტირიცხვი && sockets[i].localip == destinationipaddressქსელიbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remoteპორტირიცხვი = msg.წყაროპორტირიცხვი
			socket.remoteip = წყაროipaddressქსელიbyteorder
		} else if sockets[i].localპორტირიცხვი == msg.destinationპორტირიცხვი && sockets[i].localip == destinationipaddressქსელიbyteorder && sockets[i].remoteპორტირიცხვი == msg.წყაროპორტირიცხვი && sockets[i].remoteip == წყაროipaddressქსელიbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if socket != nil {
		socket.Handleმომხმარებელიdatagramprotocolშეტყობინება(ინტერნეტიprotocolpayload+uintptr(udpheaderზომა), uint16(ზომა-udpheaderზომა))
	}

	return false
}

func (self *Tმომხმარებელიdatagramprotocolprovider) Cდაკავშირება(ip uint32, პორტი uint16) *Tმომხმარებელიdatagramprotocolsocket {
	var მეხსიერებაmanager = &Tმეხსიერებაmanager{}
	var socket = (*Tმომხმარებელიdatagramprotocolsocket)(მეხსიერებაmanager.Malloc(50))

	if socket != nil {

		socket.Init(*self, nil)
		socket.remoteპორტირიცხვი = პორტი
		socket.remoteip = ip
		socket.localპორტირიცხვი = თავისუფალიპორტი
		თავისუფალიპორტი++
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remoteპორტირიცხვი = Unsignedinteger16r(socket.remoteპორტირიცხვი)
		socket.localპორტირიცხვი = Unsignedinteger16r(socket.localპორტირიცხვი)

		sockets[რიცხვიsockets] = *socket
		რიცხვიsockets++

	}
	return socket

}
func (self *Tმომხმარებელიdatagramprotocolprovider) Listen(პორტი uint16) *Tმომხმარებელიdatagramprotocolsocket {
	var socket = &Tმომხმარებელიdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*self, nil)
		socket.listening = true
		socket.localპორტირიცხვი = პორტი
		socket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localპორტირიცხვი = Unsignedinteger16r(socket.localპორტირიცხვი)
	}
	return socket
}
func (self *Tმომხმარებელიdatagramprotocolprovider) Dგათიშვა(socket *Tმომხმარებელიdatagramprotocolsocket) {
	for i := 0; i < რიცხვიsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			რიცხვიsockets--
			sockets[i] = sockets[რიცხვიsockets]
			break
		}
	}
}
func (self *Tმომხმარებელიdatagramprotocolprovider) Sგაგზავნა(socket *Tმომხმარებელიdatagramprotocolsocket, pdata uintptr, ზომა uint16) {
	var სულlength = uint32(ზომა) + udpheaderზომა

	var buffer_2 [4096]byte

	var msgbuffer = (*Tმომხმარებელიdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = Tმომხმარებელიdatagramprotocolheader{}

	msg.წყაროპორტირიცხვი = socket.localპორტირიცხვი
	msg.destinationპორტირიცხვი = socket.remoteპორტირიცხვი
	msg.length = Unsignedinteger16r(uint16(სულlength))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataბაიტი [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(ზომა); i++ {
		buffer_2[int(udpheaderზომა)+i] = dataბაიტი[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Sგაგზავნა(socket.remoteip, 0x11, data, სულlength)

}
func (self *Tმომხმარებელიdatagramprotocolprovider) Bind(socket *Tმომხმარებელიdatagramprotocolsocket, handler *Tმომხმარებელიdatagramprotocolhandler,) {
}
