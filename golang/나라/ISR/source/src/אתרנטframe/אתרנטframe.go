package אתרנטframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var אתרנטconsole TConsole = TConsole{}

type Tאתרנטframeheaderbuffer struct {
	יעדmacbe	[6]byte
	מקורmacbe	[6]byte
	אתרנטסוגbe	[2]byte
}

var frameheaderגודל int = 14

type Tאתרנטframeheader struct {
	יעדmacbe	uint64
	מקורmacbe	uint64
	אתרנטסוגbe	uint16
}

func (self *Tאתרנטframeheader) Init(buffer_2 Tאתרנטframeheaderbuffer) {
	self.יעדmacbe = (Aמערךtounsignedinteger48(buffer_2.יעדmacbe))
	self.מקורmacbe = (Aמערךtounsignedinteger48(buffer_2.מקורmacbe))
	self.אתרנטסוגbe = (Aמערךtounsignedinteger16(buffer_2.אתרנטסוגbe))

}
func (self *Tאתרנטframeheader) Sקבעbuffer(buffer_2 *Tאתרנטframeheaderbuffer) {
	buffer_2.יעדmacbe = Unsignedinteger48toמערך(Unsignedinteger48r(self.יעדmacbe))
	buffer_2.מקורmacbe = Unsignedinteger48toמערך(Unsignedinteger48r(self.מקורmacbe))
	buffer_2.אתרנטסוגbe = Unsignedinteger16toמערך(Unsignedinteger16r(self.אתרנטסוגbe))
}

type Iאתרנטframehandler interface {
	Init(backend Tאתרנטframeprovider)
	Sקבעhandler(handler Iאתרנטframehandler, אתרנטסוג uint16)
	Oאתרנטframereceivewhen(dataסמן uintptr, גודל int) bool
	Sשלח(יעדmacbe uint64, dataסמן uintptr, גודל uint32)
	Frameשלח(יעדmacbe uint64, אתרנטסוגbe uint16, dataסמן uintptr, גודל uint32)
	Providerget() Tאתרנטframeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type Tאתרנטframehandler struct {
}

var frame Tאתרנטframeheader
var Backend Tאתרנטframeprovider
var handler_2 [65535]Iאתרנטframehandler
var efhandler *Tאתרנטframehandler = nil

func (self *Tאתרנטframehandler) Init(backend Tאתרנטframeprovider) {
	Backend = backend
}

func (self *Tאתרנטframehandler) Sקבעhandler(handler Iאתרנטframehandler, pאתרנטסוג uint16) {
	handler_2[pאתרנטסוג] = handler
}
func (self *Tאתרנטframehandler) Sקבעbackend(backend Tאתרנטframeprovider) {
	Backend = backend
}
func (self *Tאתרנטframehandler) Getbackend() Tאתרנטframeprovider {
	return Backend
}
func (self *Tאתרנטframehandler) Oאתרנטframereceivewhen(dataסמן uintptr, גודל int) bool {
	אתרנטconsole.Mהדפסה(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *Tאתרנטframehandler) Sשלח(יעדmacbe uint64, dataסמן uintptr, גודל uint32) {
	Backend.Frameשלח(יעדmacbe, frame.אתרנטסוגbe, dataסמן, גודל)
}
func (self *Tאתרנטframehandler) Frameשלח(יעדmacbe uint64, אתרנטסוגbe uint16, dataסמן uintptr, גודל uint32) {
	Backend.Frameשלח(יעדmacbe, אתרנטסוגbe, dataסמן, גודל)
}
func (self *Tאתרנטframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *Tאתרנטframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *Tאתרנטframehandler) Providerget() Tאתרנטframeprovider {
	return Backend
}

type Tאתרנטframerawdatahandler struct {
	TRawdatahandler
}

var provider Tאתרנטframeprovider

func (self *Tאתרנטframerawdatahandler) Init(pprovider Tאתרנטframeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *Tאתרנטframerawdatahandler) Oפעילrawdatareceive(dataסמן uintptr, גודל int) bool {
	return provider.Oפעילrawdatareceive(dataסמן, גודל)
}
func (self *Tאתרנטframerawdatahandler) Sשלח(dataסמן uintptr, גודל uint32) {
	provider.Sשלח(dataסמן, גודל)
}
func (self *Tאתרנטframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *Tאתרנטframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *Tאתרנטframerawdatahandler) Providerget() Tאתרנטframeprovider {
	return provider
}

type Tאתרנטframeprovider struct {
	רשתקלפים	Tamdam79c973
	handler_2	[65565]Iאתרנטframehandler
}

func (self *Tאתרנטframeprovider) Init(backend Tamdam79c973) {

	self.רשתקלפים = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *Tאתרנטframeprovider) Oפעילrawdatareceive(dataסמן uintptr, גודל int) bool {

	var buffer_2 *Tאתרנטframeheaderbuffer = (*Tאתרנטframeheaderbuffer)(Pointer(dataסמן))
	var frame Tאתרנטframeheader = Tאתרנטframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.יעדmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.יעדmacbe) == self.Getmacaddress() {
		if handler_2[frame.אתרנטסוגbe] != nil {
			אתרנטconsole.Mהדפסה(([]byte)("provider\n"))

			var סמן uintptr = uintptr(Pointer(dataסמן)) + uintptr(frameheaderגודל)
			reply = handler_2[frame.אתרנטסוגbe].Oאתרנטframereceivewhen(סמן, גודל-frameheaderגודל)

		}
	}

	if reply {
		frame.יעדmacbe = frame.מקורmacbe
		frame.מקורmacbe = Unsignedinteger48r(self.Getmacaddress())
		frame.Sקבעbuffer(buffer_2)

	}

	אתרנטconsole.Mהדפסהxy(([]byte)("spro["), 0, 1)
	אתרנטconsole.MUnsignedinteger64הדפסה(frame.מקורmacbe)
	אתרנטconsole.Mהדפסה(([]byte)(":"))
	אתרנטconsole.MUnsignedinteger64הדפסה(frame.יעדmacbe)
	אתרנטconsole.Mהדפסה(([]byte)(":]["))
	אתרנטconsole.MUnsignedinteger64הדפסה(self.Getmacaddress())
	אתרנטconsole.Mהדפסה(([]byte)(":"))
	אתרנטconsole.MUnsignedinteger16הדפסה(frame.אתרנטסוגbe)
	אתרנטconsole.Mהדפסה(([]byte)("]"))

	return reply

}
func (self *Tאתרנטframeprovider) Sשלח(dataסמן uintptr, גודל uint32) {
	self.רשתקלפים.Sשלח(dataסמן, גודל)
}
func (self *Tאתרנטframeprovider) Frameשלח(יעדmacbe uint64, אתרנטסוגbe uint16, dataסמן uintptr, גודל uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *Tאתרנטframeheaderbuffer = (*Tאתרנטframeheaderbuffer)(Pointer(&buffer2_2))

	var frame Tאתרנטframeheader = Tאתרנטframeheader{}
	frame.Init(*buffer_2)

	frame.יעדmacbe = Unsignedinteger48r(יעדmacbe)
	frame.מקורmacbe = Unsignedinteger48r(self.רשתקלפים.Getmacaddress())
	frame.אתרנטסוגbe = Unsignedinteger16r(אתרנטסוגbe)

	frame.Sקבעbuffer(buffer_2)
	var מקור_2 [4096]byte = *(*([4096]byte))(Pointer(dataסמן))

	var i uint32 = 0
	for i = 0; i < גודל; i++ {
		buffer2_2[uint32(frameheaderגודל)+i] = מקור_2[i]

	}

	var סמן uintptr = uintptr(Pointer(&buffer2_2))

	self.רשתקלפים.Sשלח(סמן, גודל+uint32(frameheaderגודל))

}
func (self *Tאתרנטframeprovider) Getmacaddress() uint64 {
	return self.רשתקלפים.Getmacaddress()
}
func (self *Tאתרנטframeprovider) Getipaddress() uint64 {
	return self.רשתקלפים.Getipaddress()
}
