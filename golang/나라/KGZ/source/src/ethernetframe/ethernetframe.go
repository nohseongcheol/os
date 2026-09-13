package ethernetframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetframeheaderbuffer struct {
	destinationmacbe	[6]byte
	баштапкытекстmacbe	[6]byte
	ethernetТүрүbe		[2]byte
}

var frameheaderӨлчөм int = 14

type TEthernetframeheader struct {
	destinationmacbe	uint64
	баштапкытекстmacbe	uint64
	ethernetТүрүbe		uint16
}

func (self *TEthernetframeheader) Init(buffer_2 TEthernetframeheaderbuffer) {
	self.destinationmacbe = (Массивtounsignedinteger48(buffer_2.destinationmacbe))
	self.баштапкытекстmacbe = (Массивtounsignedinteger48(buffer_2.баштапкытекстmacbe))
	self.ethernetТүрүbe = (Массивtounsignedinteger16(buffer_2.ethernetТүрүbe))

}
func (self *TEthernetframeheader) Setbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toМассив(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.баштапкытекстmacbe = Unsignedinteger48toМассив(Unsignedinteger48r(self.баштапкытекстmacbe))
	buffer_2.ethernetТүрүbe = Unsignedinteger16toМассив(Unsignedinteger16r(self.ethernetТүрүbe))
}

type IEthernetframehandler interface {
	Init(backend TEthernetframeprovider)
	Sethandler(handler IEthernetframehandler, ethernetТүрү uint16)
	Ethernetframereceivewhen(dataКөрсөткүч uintptr, өлчөм int) bool
	Send(destinationmacbe uint64, dataКөрсөткүч uintptr, өлчөм uint32)
	Framesend(destinationmacbe uint64, ethernetТүрүbe uint16, dataКөрсөткүч uintptr, өлчөм uint32)
	Providerget() TEthernetframeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetframehandler struct {
}

var frame TEthernetframeheader
var Backend TEthernetframeprovider
var handler_2 [65535]IEthernetframehandler
var efhandler *TEthernetframehandler = nil

func (self *TEthernetframehandler) Init(backend TEthernetframeprovider) {
	Backend = backend
}

func (self *TEthernetframehandler) Sethandler(handler IEthernetframehandler, pethernetТүрү uint16) {
	handler_2[pethernetТүрү] = handler
}
func (self *TEthernetframehandler) Setbackend(backend TEthernetframeprovider) {
	Backend = backend
}
func (self *TEthernetframehandler) Getbackend() TEthernetframeprovider {
	return Backend
}
func (self *TEthernetframehandler) Ethernetframereceivewhen(dataКөрсөткүч uintptr, өлчөм int) bool {
	ethernetconsole.MБасма(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetframehandler) Send(destinationmacbe uint64, dataКөрсөткүч uintptr, өлчөм uint32) {
	Backend.Framesend(destinationmacbe, frame.ethernetТүрүbe, dataКөрсөткүч, өлчөм)
}
func (self *TEthernetframehandler) Framesend(destinationmacbe uint64, ethernetТүрүbe uint16, dataКөрсөткүч uintptr, өлчөм uint32) {
	Backend.Framesend(destinationmacbe, ethernetТүрүbe, dataКөрсөткүч, өлчөм)
}
func (self *TEthernetframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetframehandler) Providerget() TEthernetframeprovider {
	return Backend
}

type TEthernetframerawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetframeprovider

func (self *TEthernetframerawdatahandler) Init(pprovider TEthernetframeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetframerawdatahandler) Onrawdatareceive(dataКөрсөткүч uintptr, өлчөм int) bool {
	return provider.Onrawdatareceive(dataКөрсөткүч, өлчөм)
}
func (self *TEthernetframerawdatahandler) Send(dataКөрсөткүч uintptr, өлчөм uint32) {
	provider.Send(dataКөрсөткүч, өлчөм)
}
func (self *TEthernetframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetframerawdatahandler) Providerget() TEthernetframeprovider {
	return provider
}

type TEthernetframeprovider struct {
	тармакcard	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (self *TEthernetframeprovider) Init(backend Tamdam79c973) {

	self.тармакcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetframeprovider) Onrawdatareceive(dataКөрсөткүч uintptr, өлчөм int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(dataКөрсөткүч))
	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.ethernetТүрүbe] != nil {
			ethernetconsole.MБасма(([]byte)("provider\n"))

			var көрсөткүч uintptr = uintptr(Pointer(dataКөрсөткүч)) + uintptr(frameheaderӨлчөм)
			reply = handler_2[frame.ethernetТүрүbe].Ethernetframereceivewhen(көрсөткүч, өлчөм-frameheaderӨлчөм)

		}
	}

	if reply {
		frame.destinationmacbe = frame.баштапкытекстmacbe
		frame.баштапкытекстmacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Setbuffer(buffer_2)

	}

	ethernetconsole.MБасмаxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Басма(frame.баштапкытекстmacbe)
	ethernetconsole.MБасма(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Басма(frame.destinationmacbe)
	ethernetconsole.MБасма(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Басма(self.Getmacaddress())
	ethernetconsole.MБасма(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Басма(frame.ethernetТүрүbe)
	ethernetconsole.MБасма(([]byte)("]"))

	return reply

}
func (self *TEthernetframeprovider) Send(dataКөрсөткүч uintptr, өлчөм uint32) {
	self.тармакcard.Send(dataКөрсөткүч, өлчөм)
}
func (self *TEthernetframeprovider) Framesend(destinationmacbe uint64, ethernetТүрүbe uint16, dataКөрсөткүч uintptr, өлчөм uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.баштапкытекстmacbe = Unsignedinteger48r(self.тармакcard.Getmacaddress())
	frame.ethernetТүрүbe = Unsignedinteger16r(ethernetТүрүbe)

	frame.Setbuffer(buffer_2)
	var баштапкытекст_2 [4096]byte = *(*([4096]byte))(Pointer(dataКөрсөткүч))

	var i uint32 = 0
	for i = 0; i < өлчөм; i++ {
		buffer2_2[uint32(frameheaderӨлчөм)+i] = баштапкытекст_2[i]

	}

	var көрсөткүч uintptr = uintptr(Pointer(&buffer2_2))

	self.тармакcard.Send(көрсөткүч, өлчөм+uint32(frameheaderӨлчөм))

}
func (self *TEthernetframeprovider) Getmacaddress() uint64 {
	return self.тармакcard.Getmacaddress()
}
func (self *TEthernetframeprovider) Getipaddress() uint64 {
	return self.тармакcard.Getipaddress()
}
