package ایتھرنیٹframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ایتھرنیٹconsole TConsole = TConsole{}

type Tایتھرنیٹframeheaderbuffer struct {
	destinationmacbe	[6]byte
	مصدرmacbe		[6]byte
	ایتھرنیٹنوعیتbe		[2]byte
}

var frameheaderحجم int = 14

type Tایتھرنیٹframeheader struct {
	destinationmacbe	uint64
	مصدرmacbe		uint64
	ایتھرنیٹنوعیتbe		uint16
}

func (self *Tایتھرنیٹframeheader) Init(buffer_2 Tایتھرنیٹframeheaderbuffer) {
	self.destinationmacbe = (Aلڑیtounsignedinteger48(buffer_2.destinationmacbe))
	self.مصدرmacbe = (Aلڑیtounsignedinteger48(buffer_2.مصدرmacbe))
	self.ایتھرنیٹنوعیتbe = (Aلڑیtounsignedinteger16(buffer_2.ایتھرنیٹنوعیتbe))

}
func (self *Tایتھرنیٹframeheader) Sسیٹbuffer(buffer_2 *Tایتھرنیٹframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toلڑی(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.مصدرmacbe = Unsignedinteger48toلڑی(Unsignedinteger48r(self.مصدرmacbe))
	buffer_2.ایتھرنیٹنوعیتbe = Unsignedinteger16toلڑی(Unsignedinteger16r(self.ایتھرنیٹنوعیتbe))
}

type Iایتھرنیٹframehandler interface {
	Init(backend Tایتھرنیٹframeprovider)
	Sسیٹhandler(handler Iایتھرنیٹframehandler, ایتھرنیٹنوعیت uint16)
	Oایتھرنیٹframereceivewhen(dataپؤائنٹر uintptr, حجم int) bool
	Send(destinationmacbe uint64, dataپؤائنٹر uintptr, حجم uint32)
	Framesend(destinationmacbe uint64, ایتھرنیٹنوعیتbe uint16, dataپؤائنٹر uintptr, حجم uint32)
	Providerget() Tایتھرنیٹframeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type Tایتھرنیٹframehandler struct {
}

var frame Tایتھرنیٹframeheader
var Backend Tایتھرنیٹframeprovider
var handler_2 [65535]Iایتھرنیٹframehandler
var efhandler *Tایتھرنیٹframehandler = nil

func (self *Tایتھرنیٹframehandler) Init(backend Tایتھرنیٹframeprovider) {
	Backend = backend
}

func (self *Tایتھرنیٹframehandler) Sسیٹhandler(handler Iایتھرنیٹframehandler, pایتھرنیٹنوعیت uint16) {
	handler_2[pایتھرنیٹنوعیت] = handler
}
func (self *Tایتھرنیٹframehandler) Sسیٹbackend(backend Tایتھرنیٹframeprovider) {
	Backend = backend
}
func (self *Tایتھرنیٹframehandler) Getbackend() Tایتھرنیٹframeprovider {
	return Backend
}
func (self *Tایتھرنیٹframehandler) Oایتھرنیٹframereceivewhen(dataپؤائنٹر uintptr, حجم int) bool {
	ایتھرنیٹconsole.Mچھاپیں(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *Tایتھرنیٹframehandler) Send(destinationmacbe uint64, dataپؤائنٹر uintptr, حجم uint32) {
	Backend.Framesend(destinationmacbe, frame.ایتھرنیٹنوعیتbe, dataپؤائنٹر, حجم)
}
func (self *Tایتھرنیٹframehandler) Framesend(destinationmacbe uint64, ایتھرنیٹنوعیتbe uint16, dataپؤائنٹر uintptr, حجم uint32) {
	Backend.Framesend(destinationmacbe, ایتھرنیٹنوعیتbe, dataپؤائنٹر, حجم)
}
func (self *Tایتھرنیٹframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *Tایتھرنیٹframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *Tایتھرنیٹframehandler) Providerget() Tایتھرنیٹframeprovider {
	return Backend
}

type Tایتھرنیٹframerawdatahandler struct {
	TRawdatahandler
}

var provider Tایتھرنیٹframeprovider

func (self *Tایتھرنیٹframerawdatahandler) Init(pprovider Tایتھرنیٹframeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *Tایتھرنیٹframerawdatahandler) Oچالوrawdatareceive(dataپؤائنٹر uintptr, حجم int) bool {
	return provider.Oچالوrawdatareceive(dataپؤائنٹر, حجم)
}
func (self *Tایتھرنیٹframerawdatahandler) Send(dataپؤائنٹر uintptr, حجم uint32) {
	provider.Send(dataپؤائنٹر, حجم)
}
func (self *Tایتھرنیٹframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *Tایتھرنیٹframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *Tایتھرنیٹframerawdatahandler) Providerget() Tایتھرنیٹframeprovider {
	return provider
}

type Tایتھرنیٹframeprovider struct {
	نیٹورکcard	Tamdam79c973
	handler_2	[65565]Iایتھرنیٹframehandler
}

func (self *Tایتھرنیٹframeprovider) Init(backend Tamdam79c973) {

	self.نیٹورکcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *Tایتھرنیٹframeprovider) Oچالوrawdatareceive(dataپؤائنٹر uintptr, حجم int) bool {

	var buffer_2 *Tایتھرنیٹframeheaderbuffer = (*Tایتھرنیٹframeheaderbuffer)(Pointer(dataپؤائنٹر))
	var frame Tایتھرنیٹframeheader = Tایتھرنیٹframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[frame.ایتھرنیٹنوعیتbe] != nil {
			ایتھرنیٹconsole.Mچھاپیں(([]byte)("provider\n"))

			var پؤائنٹر uintptr = uintptr(Pointer(dataپؤائنٹر)) + uintptr(frameheaderحجم)
			reply = handler_2[frame.ایتھرنیٹنوعیتbe].Oایتھرنیٹframereceivewhen(پؤائنٹر, حجم-frameheaderحجم)

		}
	}

	if reply {
		frame.destinationmacbe = frame.مصدرmacbe
		frame.مصدرmacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Sسیٹbuffer(buffer_2)

	}

	ایتھرنیٹconsole.Mچھاپیںxy(([]byte)("spro["), 0, 1)
	ایتھرنیٹconsole.MUnsignedinteger64چھاپیں(frame.مصدرmacbe)
	ایتھرنیٹconsole.Mچھاپیں(([]byte)(":"))
	ایتھرنیٹconsole.MUnsignedinteger64چھاپیں(frame.destinationmacbe)
	ایتھرنیٹconsole.Mچھاپیں(([]byte)(":]["))
	ایتھرنیٹconsole.MUnsignedinteger64چھاپیں(self.Getmacaddress())
	ایتھرنیٹconsole.Mچھاپیں(([]byte)(":"))
	ایتھرنیٹconsole.MUnsignedinteger16چھاپیں(frame.ایتھرنیٹنوعیتbe)
	ایتھرنیٹconsole.Mچھاپیں(([]byte)("]"))

	return reply

}
func (self *Tایتھرنیٹframeprovider) Send(dataپؤائنٹر uintptr, حجم uint32) {
	self.نیٹورکcard.Send(dataپؤائنٹر, حجم)
}
func (self *Tایتھرنیٹframeprovider) Framesend(destinationmacbe uint64, ایتھرنیٹنوعیتbe uint16, dataپؤائنٹر uintptr, حجم uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *Tایتھرنیٹframeheaderbuffer = (*Tایتھرنیٹframeheaderbuffer)(Pointer(&buffer2_2))

	var frame Tایتھرنیٹframeheader = Tایتھرنیٹframeheader{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.مصدرmacbe = Unsignedinteger48r(self.نیٹورکcard.Getmacaddress())
	frame.ایتھرنیٹنوعیتbe = Unsignedinteger16r(ایتھرنیٹنوعیتbe)

	frame.Sسیٹbuffer(buffer_2)
	var مصدر_2 [4096]byte = *(*([4096]byte))(Pointer(dataپؤائنٹر))

	var i uint32 = 0
	for i = 0; i < حجم; i++ {
		buffer2_2[uint32(frameheaderحجم)+i] = مصدر_2[i]

	}

	var پؤائنٹر uintptr = uintptr(Pointer(&buffer2_2))

	self.نیٹورکcard.Send(پؤائنٹر, حجم+uint32(frameheaderحجم))

}
func (self *Tایتھرنیٹframeprovider) Getmacaddress() uint64 {
	return self.نیٹورکcard.Getmacaddress()
}
func (self *Tایتھرنیٹframeprovider) Getipaddress() uint64 {
	return self.نیٹورکcard.Getipaddress()
}
