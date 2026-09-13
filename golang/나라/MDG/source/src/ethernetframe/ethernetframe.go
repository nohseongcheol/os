package ethernetframe

import . "konsoly"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonsoly TKonsoly = TKonsoly{}

type TEthernetframeheaderbuffer struct {
	destinationmacbe	[6]byte
	loharanomacbe		[6]byte
	ethernetKarazanabe	[2]byte
}

var frameheaderHabe int = 14

type TEthernetframeheader struct {
	destinationmacbe	uint64
	loharanomacbe		uint64
	ethernetKarazanabe	uint16
}

func (nytena *TEthernetframeheader) Init(buffer_2 TEthernetframeheaderbuffer) {
	nytena.destinationmacbe = (Arraytounsignedinteger48(buffer_2.destinationmacbe))
	nytena.loharanomacbe = (Arraytounsignedinteger48(buffer_2.loharanomacbe))
	nytena.ethernetKarazanabe = (Arraytounsignedinteger16(buffer_2.ethernetKarazanabe))

}
func (nytena *TEthernetframeheader) Setbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toarray(Unsignedinteger48r(nytena.destinationmacbe))
	buffer_2.loharanomacbe = Unsignedinteger48toarray(Unsignedinteger48r(nytena.loharanomacbe))
	buffer_2.ethernetKarazanabe = Unsignedinteger16toarray(Unsignedinteger16r(nytena.ethernetKarazanabe))
}

type IEthernetframehandler interface {
	Init(backend TEthernetframeprovider)
	Sethandler(handler IEthernetframehandler, ethernetKarazana uint16)
	Ethernetframereceivewhen(datapointer uintptr, habe int) bool
	Send(destinationmacbe uint64, datapointer uintptr, habe uint32)
	Framesend(destinationmacbe uint64, ethernetKarazanabe uint16, datapointer uintptr, habe uint32)
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

func (nytena *TEthernetframehandler) Init(backend TEthernetframeprovider) {
	Backend = backend
}

func (nytena *TEthernetframehandler) Sethandler(handler IEthernetframehandler, pethernetKarazana uint16) {
	handler_2[pethernetKarazana] = handler
}
func (nytena *TEthernetframehandler) Setbackend(backend TEthernetframeprovider) {
	Backend = backend
}
func (nytena *TEthernetframehandler) Getbackend() TEthernetframeprovider {
	return Backend
}
func (nytena *TEthernetframehandler) Ethernetframereceivewhen(datapointer uintptr, habe int) bool {
	ethernetKonsoly.MAtontay(([]byte)("OnEtherFrameReceived"))
	return false
}
func (nytena *TEthernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, habe uint32) {
	Backend.Framesend(destinationmacbe, frame.ethernetKarazanabe, datapointer, habe)
}
func (nytena *TEthernetframehandler) Framesend(destinationmacbe uint64, ethernetKarazanabe uint16, datapointer uintptr, habe uint32) {
	Backend.Framesend(destinationmacbe, ethernetKarazanabe, datapointer, habe)
}
func (nytena *TEthernetframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (nytena *TEthernetframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (nytena *TEthernetframehandler) Providerget() TEthernetframeprovider {
	return Backend
}

type TEthernetframerawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetframeprovider

func (nytena *TEthernetframerawdatahandler) Init(pprovider TEthernetframeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (nytena *TEthernetframerawdatahandler) Onrawdatareceive(datapointer uintptr, habe int) bool {
	return provider.Onrawdatareceive(datapointer, habe)
}
func (nytena *TEthernetframerawdatahandler) Send(datapointer uintptr, habe uint32) {
	provider.Send(datapointer, habe)
}
func (nytena *TEthernetframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (nytena *TEthernetframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (nytena *TEthernetframerawdatahandler) Providerget() TEthernetframeprovider {
	return provider
}

type TEthernetframeprovider struct {
	rezocard	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (nytena *TEthernetframeprovider) Init(backend Tamdam79c973) {

	nytena.rezocard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		nytena.handler_2[i] = nil
	}
}

var count uint16 = 0

func (nytena *TEthernetframeprovider) Onrawdatareceive(datapointer uintptr, habe int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(datapointer))
	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == nytena.Getmacaddress() {
		if handler_2[frame.ethernetKarazanabe] != nil {
			ethernetKonsoly.MAtontay(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(frameheaderHabe)
			reply = handler_2[frame.ethernetKarazanabe].Ethernetframereceivewhen(pointer, habe-frameheaderHabe)

		}
	}

	if reply {
		frame.destinationmacbe = frame.loharanomacbe
		frame.loharanomacbe = Unsignedinteger48r(nytena.Getmacaddress())
		frame.Setbuffer(buffer_2)

	}

	ethernetKonsoly.MAtontayxy(([]byte)("spro["), 0, 1)
	ethernetKonsoly.MUnsignedinteger64Atontay(frame.loharanomacbe)
	ethernetKonsoly.MAtontay(([]byte)(":"))
	ethernetKonsoly.MUnsignedinteger64Atontay(frame.destinationmacbe)
	ethernetKonsoly.MAtontay(([]byte)(":]["))
	ethernetKonsoly.MUnsignedinteger64Atontay(nytena.Getmacaddress())
	ethernetKonsoly.MAtontay(([]byte)(":"))
	ethernetKonsoly.MUnsignedinteger16Atontay(frame.ethernetKarazanabe)
	ethernetKonsoly.MAtontay(([]byte)("]"))

	return reply

}
func (nytena *TEthernetframeprovider) Send(datapointer uintptr, habe uint32) {
	nytena.rezocard.Send(datapointer, habe)
}
func (nytena *TEthernetframeprovider) Framesend(destinationmacbe uint64, ethernetKarazanabe uint16, datapointer uintptr, habe uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.loharanomacbe = Unsignedinteger48r(nytena.rezocard.Getmacaddress())
	frame.ethernetKarazanabe = Unsignedinteger16r(ethernetKarazanabe)

	frame.Setbuffer(buffer_2)
	var loharano_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < habe; i++ {
		buffer2_2[uint32(frameheaderHabe)+i] = loharano_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	nytena.rezocard.Send(pointer, habe+uint32(frameheaderHabe))

}
func (nytena *TEthernetframeprovider) Getmacaddress() uint64 {
	return nytena.rezocard.Getmacaddress()
}
func (nytena *TEthernetframeprovider) Getipaddress() uint64 {
	return nytena.rezocard.Getipaddress()
}
