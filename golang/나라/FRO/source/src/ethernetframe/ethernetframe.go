package ethernetframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetframeheaderbuffer struct {
	destinationmacbe	[6]byte
	sourcemacbe		[6]byte
	ethernettypebe		[2]byte
}

var frameheaderStødd int = 14

type TEthernetframeheader struct {
	destinationmacbe	uint64
	sourcemacbe		uint64
	ethernettypebe		uint16
}

func (self *TEthernetframeheader) Init(buffer_2 TEthernetframeheaderbuffer) {
	self.destinationmacbe = (Arraytounsignedinteger48(buffer_2.destinationmacbe))
	self.sourcemacbe = (Arraytounsignedinteger48(buffer_2.sourcemacbe))
	self.ethernettypebe = (Arraytounsignedinteger16(buffer_2.ethernettypebe))

}
func (self *TEthernetframeheader) Setbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.sourcemacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.sourcemacbe))
	buffer_2.ethernettypebe = Unsignedinteger16toarray(Unsignedinteger16r(self.ethernettypebe))
}

type IEthernetframehandler interface {
	Init(backend TEthernetframeprovider)
	Sethandler(handler IEthernetframehandler, ethernettype uint16)
	Ethernetframereceivewhen(datapointer uintptr, stødd int) bool
	Send(destinationmacbe uint64, datapointer uintptr, stødd uint32)
	Framesend(destinationmacbe uint64, ethernettypebe uint16, datapointer uintptr, stødd uint32)
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

func (self *TEthernetframehandler) Sethandler(handler IEthernetframehandler, pethernettype uint16) {
	handler_2[pethernettype] = handler
}
func (self *TEthernetframehandler) Setbackend(backend TEthernetframeprovider) {
	Backend = backend
}
func (self *TEthernetframehandler) Getbackend() TEthernetframeprovider {
	return Backend
}
func (self *TEthernetframehandler) Ethernetframereceivewhen(datapointer uintptr, stødd int) bool {
	ethernetconsole.MPrint(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, stødd uint32) {
	Backend.Framesend(destinationmacbe, frame.ethernettypebe, datapointer, stødd)
}
func (self *TEthernetframehandler) Framesend(destinationmacbe uint64, ethernettypebe uint16, datapointer uintptr, stødd uint32) {
	Backend.Framesend(destinationmacbe, ethernettypebe, datapointer, stødd)
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
func (self *TEthernetframerawdatahandler) Onrawdatareceive(datapointer uintptr, stødd int) bool {
	return provider.Onrawdatareceive(datapointer, stødd)
}
func (self *TEthernetframerawdatahandler) Send(datapointer uintptr, stødd uint32) {
	provider.Send(datapointer, stødd)
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
	netcard		Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (self *TEthernetframeprovider) Init(backend Tamdam79c973) {

	self.netcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetframeprovider) Onrawdatareceive(datapointer uintptr, stødd int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(datapointer))
	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.ethernettypebe] != nil {
			ethernetconsole.MPrint(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(frameheaderStødd)
			reply = handler_2[frame.ethernettypebe].Ethernetframereceivewhen(pointer, stødd-frameheaderStødd)

		}
	}

	if reply {
		frame.destinationmacbe = frame.sourcemacbe
		frame.sourcemacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Setbuffer(buffer_2)

	}

	ethernetconsole.MPrintxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64print(frame.sourcemacbe)
	ethernetconsole.MPrint(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64print(frame.destinationmacbe)
	ethernetconsole.MPrint(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64print(self.Getmacaddress())
	ethernetconsole.MPrint(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16print(frame.ethernettypebe)
	ethernetconsole.MPrint(([]byte)("]"))

	return reply

}
func (self *TEthernetframeprovider) Send(datapointer uintptr, stødd uint32) {
	self.netcard.Send(datapointer, stødd)
}
func (self *TEthernetframeprovider) Framesend(destinationmacbe uint64, ethernettypebe uint16, datapointer uintptr, stødd uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.sourcemacbe = Unsignedinteger48r(self.netcard.Getmacaddress())
	frame.ethernettypebe = Unsignedinteger16r(ethernettypebe)

	frame.Setbuffer(buffer_2)
	var source_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < stødd; i++ {
		buffer2_2[uint32(frameheaderStødd)+i] = source_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	self.netcard.Send(pointer, stødd+uint32(frameheaderStødd))

}
func (self *TEthernetframeprovider) Getmacaddress() uint64 {
	return self.netcard.Getmacaddress()
}
func (self *TEthernetframeprovider) Getipaddress() uint64 {
	return self.netcard.Getipaddress()
}
