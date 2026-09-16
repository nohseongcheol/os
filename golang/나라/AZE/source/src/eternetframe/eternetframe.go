/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package eternetframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var eternetconsole TConsole = TConsole{}

type TEternetframeheaderbuffer struct {
	destinationmacbe	[6]byte
	mənbəmacbe		[6]byte
	eternetNövbe		[2]byte
}

var frameheaderBöyüklük int = 14

type TEternetframeheader struct {
	destinationmacbe	uint64
	mənbəmacbe		uint64
	eternetNövbe		uint16
}

func (self *TEternetframeheader) Init(buffer_2 TEternetframeheaderbuffer) {
	self.destinationmacbe = (Arraytounsignedinteger48(buffer_2.destinationmacbe))
	self.mənbəmacbe = (Arraytounsignedinteger48(buffer_2.mənbəmacbe))
	self.eternetNövbe = (Arraytounsignedinteger16(buffer_2.eternetNövbe))

}
func (self *TEternetframeheader) Setbuffer(buffer_2 *TEternetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.mənbəmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.mənbəmacbe))
	buffer_2.eternetNövbe = Unsignedinteger16toarray(Unsignedinteger16r(self.eternetNövbe))
}

type IEternetframehandler interface {
	Init(backend TEternetframeprovider)
	Sethandler(handler IEternetframehandler, eternetNöv uint16)
	Eternetframereceivewhen(datapointer uintptr, böyüklük int) bool
	Send(destinationmacbe uint64, datapointer uintptr, böyüklük uint32)
	Framesend(destinationmacbe uint64, eternetNövbe uint16, datapointer uintptr, böyüklük uint32)
	Providerget() TEternetframeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEternetframehandler struct {
}

var frame TEternetframeheader
var Backend TEternetframeprovider
var handler_2 [65535]IEternetframehandler
var efhandler *TEternetframehandler = nil

func (self *TEternetframehandler) Init(backend TEternetframeprovider) {
	Backend = backend
}

func (self *TEternetframehandler) Sethandler(handler IEternetframehandler, pEternetNöv uint16) {
	handler_2[pEternetNöv] = handler
}
func (self *TEternetframehandler) Setbackend(backend TEternetframeprovider) {
	Backend = backend
}
func (self *TEternetframehandler) Getbackend() TEternetframeprovider {
	return Backend
}
func (self *TEternetframehandler) Eternetframereceivewhen(datapointer uintptr, böyüklük int) bool {
	eternetconsole.MÇapEt(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEternetframehandler) Send(destinationmacbe uint64, datapointer uintptr, böyüklük uint32) {
	Backend.Framesend(destinationmacbe, frame.eternetNövbe, datapointer, böyüklük)
}
func (self *TEternetframehandler) Framesend(destinationmacbe uint64, eternetNövbe uint16, datapointer uintptr, böyüklük uint32) {
	Backend.Framesend(destinationmacbe, eternetNövbe, datapointer, böyüklük)
}
func (self *TEternetframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEternetframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEternetframehandler) Providerget() TEternetframeprovider {
	return Backend
}

type TEternetframerawdatahandler struct {
	TRawdatahandler
}

var provider TEternetframeprovider

func (self *TEternetframerawdatahandler) Init(pprovider TEternetframeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEternetframerawdatahandler) Onrawdatareceive(datapointer uintptr, böyüklük int) bool {
	return provider.Onrawdatareceive(datapointer, böyüklük)
}
func (self *TEternetframerawdatahandler) Send(datapointer uintptr, böyüklük uint32) {
	provider.Send(datapointer, böyüklük)
}
func (self *TEternetframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEternetframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEternetframerawdatahandler) Providerget() TEternetframeprovider {
	return provider
}

type TEternetframeprovider struct {
	şəbəkəcard	Tamdam79c973
	handler_2	[65565]IEternetframehandler
}

func (self *TEternetframeprovider) Init(backend Tamdam79c973) {

	self.şəbəkəcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEternetframeprovider) Onrawdatareceive(datapointer uintptr, böyüklük int) bool {

	var buffer_2 *TEternetframeheaderbuffer = (*TEternetframeheaderbuffer)(Pointer(datapointer))
	var frame TEternetframeheader = TEternetframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.eternetNövbe] != nil {
			eternetconsole.MÇapEt(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(frameheaderBöyüklük)
			reply = handler_2[frame.eternetNövbe].Eternetframereceivewhen(pointer, böyüklük-frameheaderBöyüklük)

		}
	}

	if reply {
		frame.destinationmacbe = frame.mənbəmacbe
		frame.mənbəmacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Setbuffer(buffer_2)

	}

	eternetconsole.MÇapEtxy(([]byte)("spro["), 0, 1)
	eternetconsole.MUnsignedinteger64ÇapEt(frame.mənbəmacbe)
	eternetconsole.MÇapEt(([]byte)(":"))
	eternetconsole.MUnsignedinteger64ÇapEt(frame.destinationmacbe)
	eternetconsole.MÇapEt(([]byte)(":]["))
	eternetconsole.MUnsignedinteger64ÇapEt(self.Getmacaddress())
	eternetconsole.MÇapEt(([]byte)(":"))
	eternetconsole.MUnsignedinteger16ÇapEt(frame.eternetNövbe)
	eternetconsole.MÇapEt(([]byte)("]"))

	return reply

}
func (self *TEternetframeprovider) Send(datapointer uintptr, böyüklük uint32) {
	self.şəbəkəcard.Send(datapointer, böyüklük)
}
func (self *TEternetframeprovider) Framesend(destinationmacbe uint64, eternetNövbe uint16, datapointer uintptr, böyüklük uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEternetframeheaderbuffer = (*TEternetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TEternetframeheader = TEternetframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.mənbəmacbe = Unsignedinteger48r(self.şəbəkəcard.Getmacaddress())
	frame.eternetNövbe = Unsignedinteger16r(eternetNövbe)

	frame.Setbuffer(buffer_2)
	var mənbə_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < böyüklük; i++ {
		buffer2_2[uint32(frameheaderBöyüklük)+i] = mənbə_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	self.şəbəkəcard.Send(pointer, böyüklük+uint32(frameheaderBöyüklük))

}
func (self *TEternetframeprovider) Getmacaddress() uint64 {
	return self.şəbəkəcard.Getmacaddress()
}
func (self *TEternetframeprovider) Getipaddress() uint64 {
	return self.şəbəkəcard.Getipaddress()
}
