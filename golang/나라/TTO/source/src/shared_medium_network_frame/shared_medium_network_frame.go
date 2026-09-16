/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package shared_medium_network_frame

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

var frameheadersize int = 14

type TShared_medium_network_frame_header struct {
	destinationmacbe	uint64
	sourcemacbe		uint64
	ethernettypebe		uint16
}

func (self *TShared_medium_network_frame_header) Init(buffer_2 TEthernetframeheaderbuffer) {
	self.destinationmacbe = (Arraytounsignedinteger48(buffer_2.destinationmacbe))
	self.sourcemacbe = (Arraytounsignedinteger48(buffer_2.sourcemacbe))
	self.ethernettypebe = (Arraytounsignedinteger16(buffer_2.ethernettypebe))

}
func (self *TShared_medium_network_frame_header) Setbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.sourcemacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.sourcemacbe))
	buffer_2.ethernettypebe = Unsignedinteger16toarray(Unsignedinteger16r(self.ethernettypebe))
}

type IEthernetframehandler interface {
	Init(backend TShared_medium_network_frame_provider)
	Sethandler(handler IEthernetframehandler, ethernettype uint16)
	Ethernetframereceivewhen(datapointer uintptr, size int) bool
	Send(destinationmacbe uint64, datapointer uintptr, size uint32)
	Framesend(destinationmacbe uint64, ethernettypebe uint16, datapointer uintptr, size uint32)
	Providerget() TShared_medium_network_frame_provider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetframehandler struct {
}

var frame TShared_medium_network_frame_header
var Backend TShared_medium_network_frame_provider
var handler_2 [65535]IEthernetframehandler
var efhandler *TEthernetframehandler = nil

func (self *TEthernetframehandler) Init(backend TShared_medium_network_frame_provider) {
	Backend = backend
}

func (self *TEthernetframehandler) Sethandler(handler IEthernetframehandler, pethernettype uint16) {
	handler_2[pethernettype] = handler
}
func (self *TEthernetframehandler) Setbackend(backend TShared_medium_network_frame_provider) {
	Backend = backend
}
func (self *TEthernetframehandler) Getbackend() TShared_medium_network_frame_provider {
	return Backend
}
func (self *TEthernetframehandler) Ethernetframereceivewhen(datapointer uintptr, size int) bool {
	ethernetconsole.MPrint(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, size uint32) {
	Backend.Framesend(destinationmacbe, frame.ethernettypebe, datapointer, size)
}
func (self *TEthernetframehandler) Framesend(destinationmacbe uint64, ethernettypebe uint16, datapointer uintptr, size uint32) {
	Backend.Framesend(destinationmacbe, ethernettypebe, datapointer, size)
}
func (self *TEthernetframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetframehandler) Providerget() TShared_medium_network_frame_provider {
	return Backend
}

type TEthernetframerawdatahandler struct {
	TRawdatahandler
}

var provider TShared_medium_network_frame_provider

func (self *TEthernetframerawdatahandler) Init(pprovider TShared_medium_network_frame_provider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetframerawdatahandler) Onrawdatareceive(datapointer uintptr, size int) bool {
	return provider.Onrawdatareceive(datapointer, size)
}
func (self *TEthernetframerawdatahandler) Send(datapointer uintptr, size uint32) {
	provider.Send(datapointer, size)
}
func (self *TEthernetframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetframerawdatahandler) Providerget() TShared_medium_network_frame_provider {
	return provider
}

type TShared_medium_network_frame_provider struct {
	networkcard	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (self *TShared_medium_network_frame_provider) Init(backend Tamdam79c973) {

	self.networkcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TShared_medium_network_frame_provider) Onrawdatareceive(datapointer uintptr, size int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(datapointer))
	var frame TShared_medium_network_frame_header = TShared_medium_network_frame_header{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.ethernettypebe] != nil {
			ethernetconsole.MPrint(([]byte)("provider\n"))

			var address_reference uintptr = uintptr(Pointer(datapointer)) + uintptr(frameheadersize)
			reply = handler_2[frame.ethernettypebe].Ethernetframereceivewhen(address_reference, size-frameheadersize)

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
func (self *TShared_medium_network_frame_provider) Send(datapointer uintptr, size uint32) {
	self.networkcard.Send(datapointer, size)
}
func (self *TShared_medium_network_frame_provider) Framesend(destinationmacbe uint64, ethernettypebe uint16, datapointer uintptr, size uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TShared_medium_network_frame_header = TShared_medium_network_frame_header{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.sourcemacbe = Unsignedinteger48r(self.networkcard.Getmacaddress())
	frame.ethernettypebe = Unsignedinteger16r(ethernettypebe)

	frame.Setbuffer(buffer_2)
	var source_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < size; i++ {
		buffer2_2[uint32(frameheadersize)+i] = source_2[i]

	}

	var address_reference uintptr = uintptr(Pointer(&buffer2_2))

	self.networkcard.Send(address_reference, size+uint32(frameheadersize))

}
func (self *TShared_medium_network_frame_provider) Getmacaddress() uint64 {
	return self.networkcard.Getmacaddress()
}
func (self *TShared_medium_network_frame_provider) Getipaddress() uint64 {
	return self.networkcard.Getipaddress()
}
