package итернэтframe

import . "консол"

import . "amdam79c973"
import . "unsafe"
import . "util"

var итернэтКонсол TКонсол = TКонсол{}

type TИтернэтframeheaderbuffer struct {
	destinationmacbe	[6]byte
	эхmacbe			[6]byte
	итернэтТөрөлbe		[2]byte
}

var frameheaderХэмжээ int = 14

type TИтернэтframeheader struct {
	destinationmacbe	uint64
	эхmacbe			uint64
	итернэтТөрөлbe		uint16
}

func (self *TИтернэтframeheader) Init(buffer_2 TИтернэтframeheaderbuffer) {
	self.destinationmacbe = (Arraytounsignedinteger48(buffer_2.destinationmacbe))
	self.эхmacbe = (Arraytounsignedinteger48(buffer_2.эхmacbe))
	self.итернэтТөрөлbe = (Arraytounsignedinteger16(buffer_2.итернэтТөрөлbe))

}
func (self *TИтернэтframeheader) Setbuffer(buffer_2 *TИтернэтframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.эхmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.эхmacbe))
	buffer_2.итернэтТөрөлbe = Unsignedinteger16toarray(Unsignedinteger16r(self.итернэтТөрөлbe))
}

type IИтернэтframehandler interface {
	Init(backend TИтернэтframeprovider)
	Sethandler(handler IИтернэтframehandler, итернэтТөрөл uint16)
	Итернэтframereceivewhen(datapointer uintptr, хэмжээ int) bool
	Send(destinationmacbe uint64, datapointer uintptr, хэмжээ uint32)
	Framesend(destinationmacbe uint64, итернэтТөрөлbe uint16, datapointer uintptr, хэмжээ uint32)
	Providerget() TИтернэтframeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TИтернэтframehandler struct {
}

var frame TИтернэтframeheader
var Backend TИтернэтframeprovider
var handler_2 [65535]IИтернэтframehandler
var efhandler *TИтернэтframehandler = nil

func (self *TИтернэтframehandler) Init(backend TИтернэтframeprovider) {
	Backend = backend
}

func (self *TИтернэтframehandler) Sethandler(handler IИтернэтframehandler, pИтернэтТөрөл uint16) {
	handler_2[pИтернэтТөрөл] = handler
}
func (self *TИтернэтframehandler) Setbackend(backend TИтернэтframeprovider) {
	Backend = backend
}
func (self *TИтернэтframehandler) Getbackend() TИтернэтframeprovider {
	return Backend
}
func (self *TИтернэтframehandler) Итернэтframereceivewhen(datapointer uintptr, хэмжээ int) bool {
	итернэтКонсол.MХэвлэх(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TИтернэтframehandler) Send(destinationmacbe uint64, datapointer uintptr, хэмжээ uint32) {
	Backend.Framesend(destinationmacbe, frame.итернэтТөрөлbe, datapointer, хэмжээ)
}
func (self *TИтернэтframehandler) Framesend(destinationmacbe uint64, итернэтТөрөлbe uint16, datapointer uintptr, хэмжээ uint32) {
	Backend.Framesend(destinationmacbe, итернэтТөрөлbe, datapointer, хэмжээ)
}
func (self *TИтернэтframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TИтернэтframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TИтернэтframehandler) Providerget() TИтернэтframeprovider {
	return Backend
}

type TИтернэтframerawdatahandler struct {
	TRawdatahandler
}

var provider TИтернэтframeprovider

func (self *TИтернэтframerawdatahandler) Init(pprovider TИтернэтframeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TИтернэтframerawdatahandler) Onrawdatareceive(datapointer uintptr, хэмжээ int) bool {
	return provider.Onrawdatareceive(datapointer, хэмжээ)
}
func (self *TИтернэтframerawdatahandler) Send(datapointer uintptr, хэмжээ uint32) {
	provider.Send(datapointer, хэмжээ)
}
func (self *TИтернэтframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TИтернэтframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TИтернэтframerawdatahandler) Providerget() TИтернэтframeprovider {
	return provider
}

type TИтернэтframeprovider struct {
	сүлжээcard	Tamdam79c973
	handler_2	[65565]IИтернэтframehandler
}

func (self *TИтернэтframeprovider) Init(backend Tamdam79c973) {

	self.сүлжээcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TИтернэтframeprovider) Onrawdatareceive(datapointer uintptr, хэмжээ int) bool {

	var buffer_2 *TИтернэтframeheaderbuffer = (*TИтернэтframeheaderbuffer)(Pointer(datapointer))
	var frame TИтернэтframeheader = TИтернэтframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.итернэтТөрөлbe] != nil {
			итернэтКонсол.MХэвлэх(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(frameheaderХэмжээ)
			reply = handler_2[frame.итернэтТөрөлbe].Итернэтframereceivewhen(pointer, хэмжээ-frameheaderХэмжээ)

		}
	}

	if reply {
		frame.destinationmacbe = frame.эхmacbe
		frame.эхmacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Setbuffer(buffer_2)

	}

	итернэтКонсол.MХэвлэхxy(([]byte)("spro["), 0, 1)
	итернэтКонсол.MUnsignedinteger64Хэвлэх(frame.эхmacbe)
	итернэтКонсол.MХэвлэх(([]byte)(":"))
	итернэтКонсол.MUnsignedinteger64Хэвлэх(frame.destinationmacbe)
	итернэтКонсол.MХэвлэх(([]byte)(":]["))
	итернэтКонсол.MUnsignedinteger64Хэвлэх(self.Getmacaddress())
	итернэтКонсол.MХэвлэх(([]byte)(":"))
	итернэтКонсол.MUnsignedinteger16Хэвлэх(frame.итернэтТөрөлbe)
	итернэтКонсол.MХэвлэх(([]byte)("]"))

	return reply

}
func (self *TИтернэтframeprovider) Send(datapointer uintptr, хэмжээ uint32) {
	self.сүлжээcard.Send(datapointer, хэмжээ)
}
func (self *TИтернэтframeprovider) Framesend(destinationmacbe uint64, итернэтТөрөлbe uint16, datapointer uintptr, хэмжээ uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TИтернэтframeheaderbuffer = (*TИтернэтframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TИтернэтframeheader = TИтернэтframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.эхmacbe = Unsignedinteger48r(self.сүлжээcard.Getmacaddress())
	frame.итернэтТөрөлbe = Unsignedinteger16r(итернэтТөрөлbe)

	frame.Setbuffer(buffer_2)
	var эх_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < хэмжээ; i++ {
		buffer2_2[uint32(frameheaderХэмжээ)+i] = эх_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	self.сүлжээcard.Send(pointer, хэмжээ+uint32(frameheaderХэмжээ))

}
func (self *TИтернэтframeprovider) Getmacaddress() uint64 {
	return self.сүлжээcard.Getmacaddress()
}
func (self *TИтернэтframeprovider) Getipaddress() uint64 {
	return self.сүлжээcard.Getipaddress()
}
