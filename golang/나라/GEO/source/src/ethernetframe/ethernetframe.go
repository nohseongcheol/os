package ethernetframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetframeheaderbuffer struct {
	destinationmacbe	[6]byte
	წყაროmacbe		[6]byte
	ethernetტიპიbe		[2]byte
}

var frameheaderზომა int = 14

type TEthernetframeheader struct {
	destinationmacbe	uint64
	წყაროmacbe		uint64
	ethernetტიპიbe		uint16
}

func (self *TEthernetframeheader) Init(buffer_2 TEthernetframeheaderbuffer) {
	self.destinationmacbe = (Aმასივიtounsignedinteger48(buffer_2.destinationmacbe))
	self.წყაროmacbe = (Aმასივიtounsignedinteger48(buffer_2.წყაროmacbe))
	self.ethernetტიპიbe = (Aმასივიtounsignedinteger16(buffer_2.ethernetტიპიbe))

}
func (self *TEthernetframeheader) Setbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toმასივი(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.წყაროmacbe = Unsignedinteger48toმასივი(Unsignedinteger48r(self.წყაროmacbe))
	buffer_2.ethernetტიპიbe = Unsignedinteger16toმასივი(Unsignedinteger16r(self.ethernetტიპიbe))
}

type IEthernetframehandler interface {
	Init(backend TEthernetframeprovider)
	Sethandler(handler IEthernetframehandler, ethernetტიპი uint16)
	Ethernetframereceivewhen(dataკურსორი uintptr, ზომა int) bool
	Sგაგზავნა(destinationmacbe uint64, dataკურსორი uintptr, ზომა uint32)
	Frameგაგზავნა(destinationmacbe uint64, ethernetტიპიbe uint16, dataკურსორი uintptr, ზომა uint32)
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

func (self *TEthernetframehandler) Sethandler(handler IEthernetframehandler, pethernetტიპი uint16) {
	handler_2[pethernetტიპი] = handler
}
func (self *TEthernetframehandler) Setbackend(backend TEthernetframeprovider) {
	Backend = backend
}
func (self *TEthernetframehandler) Getbackend() TEthernetframeprovider {
	return Backend
}
func (self *TEthernetframehandler) Ethernetframereceivewhen(dataკურსორი uintptr, ზომა int) bool {
	ethernetconsole.Mბეჭდვა(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetframehandler) Sგაგზავნა(destinationmacbe uint64, dataკურსორი uintptr, ზომა uint32) {
	Backend.Frameგაგზავნა(destinationmacbe, frame.ethernetტიპიbe, dataკურსორი, ზომა)
}
func (self *TEthernetframehandler) Frameგაგზავნა(destinationmacbe uint64, ethernetტიპიbe uint16, dataკურსორი uintptr, ზომა uint32) {
	Backend.Frameგაგზავნა(destinationmacbe, ethernetტიპიbe, dataკურსორი, ზომა)
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
func (self *TEthernetframerawdatahandler) Onrawdatareceive(dataკურსორი uintptr, ზომა int) bool {
	return provider.Onrawdatareceive(dataკურსორი, ზომა)
}
func (self *TEthernetframerawdatahandler) Sგაგზავნა(dataკურსორი uintptr, ზომა uint32) {
	provider.Sგაგზავნა(dataკურსორი, ზომა)
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
	ქსელიბანქო	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (self *TEthernetframeprovider) Init(backend Tamdam79c973) {

	self.ქსელიბანქო = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetframeprovider) Onrawdatareceive(dataკურსორი uintptr, ზომა int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(dataკურსორი))
	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.ethernetტიპიbe] != nil {
			ethernetconsole.Mბეჭდვა(([]byte)("provider\n"))

			var კურსორი uintptr = uintptr(Pointer(dataკურსორი)) + uintptr(frameheaderზომა)
			reply = handler_2[frame.ethernetტიპიbe].Ethernetframereceivewhen(კურსორი, ზომა-frameheaderზომა)

		}
	}

	if reply {
		frame.destinationmacbe = frame.წყაროmacbe
		frame.წყაროmacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Setbuffer(buffer_2)

	}

	ethernetconsole.Mბეჭდვაxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64ბეჭდვა(frame.წყაროmacbe)
	ethernetconsole.Mბეჭდვა(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64ბეჭდვა(frame.destinationmacbe)
	ethernetconsole.Mბეჭდვა(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64ბეჭდვა(self.Getmacaddress())
	ethernetconsole.Mბეჭდვა(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16ბეჭდვა(frame.ethernetტიპიbe)
	ethernetconsole.Mბეჭდვა(([]byte)("]"))

	return reply

}
func (self *TEthernetframeprovider) Sგაგზავნა(dataკურსორი uintptr, ზომა uint32) {
	self.ქსელიბანქო.Sგაგზავნა(dataკურსორი, ზომა)
}
func (self *TEthernetframeprovider) Frameგაგზავნა(destinationmacbe uint64, ethernetტიპიbe uint16, dataკურსორი uintptr, ზომა uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.წყაროmacbe = Unsignedinteger48r(self.ქსელიბანქო.Getmacaddress())
	frame.ethernetტიპიbe = Unsignedinteger16r(ethernetტიპიbe)

	frame.Setbuffer(buffer_2)
	var წყარო_2 [4096]byte = *(*([4096]byte))(Pointer(dataკურსორი))

	var i uint32 = 0
	for i = 0; i < ზომა; i++ {
		buffer2_2[uint32(frameheaderზომა)+i] = წყარო_2[i]

	}

	var კურსორი uintptr = uintptr(Pointer(&buffer2_2))

	self.ქსელიბანქო.Sგაგზავნა(კურსორი, ზომა+uint32(frameheaderზომა))

}
func (self *TEthernetframeprovider) Getmacaddress() uint64 {
	return self.ქსელიბანქო.Getmacaddress()
}
func (self *TEthernetframeprovider) Getipaddress() uint64 {
	return self.ქსელიბანქო.Getipaddress()
}
