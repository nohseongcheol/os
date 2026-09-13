package ethernetframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetframeheaderbuffer struct {
	destinationmacbe	[6]byte
	çeşmemacbe		[6]byte
	ethernetHilbe		[2]byte
}

var frameheaderUlulyk int = 14

type TEthernetframeheader struct {
	destinationmacbe	uint64
	çeşmemacbe		uint64
	ethernetHilbe		uint16
}

func (self *TEthernetframeheader) Init(buffer_2 TEthernetframeheaderbuffer) {
	self.destinationmacbe = (Arraytounsignedinteger48(buffer_2.destinationmacbe))
	self.çeşmemacbe = (Arraytounsignedinteger48(buffer_2.çeşmemacbe))
	self.ethernetHilbe = (Arraytounsignedinteger16(buffer_2.ethernetHilbe))

}
func (self *TEthernetframeheader) Setbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.çeşmemacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.çeşmemacbe))
	buffer_2.ethernetHilbe = Unsignedinteger16toarray(Unsignedinteger16r(self.ethernetHilbe))
}

type IEthernetframehandler interface {
	Init(backend TEthernetframeprovider)
	Sethandler(handler IEthernetframehandler, ethernetHil uint16)
	Ethernetframereceivewhen(datapointer uintptr, ululyk int) bool
	Send(destinationmacbe uint64, datapointer uintptr, ululyk uint32)
	Framesend(destinationmacbe uint64, ethernetHilbe uint16, datapointer uintptr, ululyk uint32)
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

func (self *TEthernetframehandler) Sethandler(handler IEthernetframehandler, pethernetHil uint16) {
	handler_2[pethernetHil] = handler
}
func (self *TEthernetframehandler) Setbackend(backend TEthernetframeprovider) {
	Backend = backend
}
func (self *TEthernetframehandler) Getbackend() TEthernetframeprovider {
	return Backend
}
func (self *TEthernetframehandler) Ethernetframereceivewhen(datapointer uintptr, ululyk int) bool {
	ethernetconsole.MÇap(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, ululyk uint32) {
	Backend.Framesend(destinationmacbe, frame.ethernetHilbe, datapointer, ululyk)
}
func (self *TEthernetframehandler) Framesend(destinationmacbe uint64, ethernetHilbe uint16, datapointer uintptr, ululyk uint32) {
	Backend.Framesend(destinationmacbe, ethernetHilbe, datapointer, ululyk)
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
func (self *TEthernetframerawdatahandler) Onrawdatareceive(datapointer uintptr, ululyk int) bool {
	return provider.Onrawdatareceive(datapointer, ululyk)
}
func (self *TEthernetframerawdatahandler) Send(datapointer uintptr, ululyk uint32) {
	provider.Send(datapointer, ululyk)
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
	şebekecard	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (self *TEthernetframeprovider) Init(backend Tamdam79c973) {

	self.şebekecard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetframeprovider) Onrawdatareceive(datapointer uintptr, ululyk int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(datapointer))
	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.ethernetHilbe] != nil {
			ethernetconsole.MÇap(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(frameheaderUlulyk)
			reply = handler_2[frame.ethernetHilbe].Ethernetframereceivewhen(pointer, ululyk-frameheaderUlulyk)

		}
	}

	if reply {
		frame.destinationmacbe = frame.çeşmemacbe
		frame.çeşmemacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Setbuffer(buffer_2)

	}

	ethernetconsole.MÇapxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Çap(frame.çeşmemacbe)
	ethernetconsole.MÇap(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Çap(frame.destinationmacbe)
	ethernetconsole.MÇap(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Çap(self.Getmacaddress())
	ethernetconsole.MÇap(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Çap(frame.ethernetHilbe)
	ethernetconsole.MÇap(([]byte)("]"))

	return reply

}
func (self *TEthernetframeprovider) Send(datapointer uintptr, ululyk uint32) {
	self.şebekecard.Send(datapointer, ululyk)
}
func (self *TEthernetframeprovider) Framesend(destinationmacbe uint64, ethernetHilbe uint16, datapointer uintptr, ululyk uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.çeşmemacbe = Unsignedinteger48r(self.şebekecard.Getmacaddress())
	frame.ethernetHilbe = Unsignedinteger16r(ethernetHilbe)

	frame.Setbuffer(buffer_2)
	var çeşme_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < ululyk; i++ {
		buffer2_2[uint32(frameheaderUlulyk)+i] = çeşme_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	self.şebekecard.Send(pointer, ululyk+uint32(frameheaderUlulyk))

}
func (self *TEthernetframeprovider) Getmacaddress() uint64 {
	return self.şebekecard.Getmacaddress()
}
func (self *TEthernetframeprovider) Getipaddress() uint64 {
	return self.şebekecard.Getipaddress()
}
