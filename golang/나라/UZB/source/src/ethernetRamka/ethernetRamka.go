package ethernetRamka

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetRamkaheaderbuffer struct {
	destinationmacbe	[6]byte
	sourcemacbe		[6]byte
	ethernetTuribe		[2]byte
}

var ramkaheaderHajmi int = 14

type TEthernetRamkaheader struct {
	destinationmacbe	uint64
	sourcemacbe		uint64
	ethernetTuribe		uint16
}

func (self *TEthernetRamkaheader) Init(buffer_2 TEthernetRamkaheaderbuffer) {
	self.destinationmacbe = (Arraytounsignedinteger48(buffer_2.destinationmacbe))
	self.sourcemacbe = (Arraytounsignedinteger48(buffer_2.sourcemacbe))
	self.ethernetTuribe = (Arraytounsignedinteger16(buffer_2.ethernetTuribe))

}
func (self *TEthernetRamkaheader) Setbuffer(buffer_2 *TEthernetRamkaheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.sourcemacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.sourcemacbe))
	buffer_2.ethernetTuribe = Unsignedinteger16toarray(Unsignedinteger16r(self.ethernetTuribe))
}

type IEthernetRamkahandler interface {
	Init(backend TEthernetRamkaprovider)
	Sethandler(handler IEthernetRamkahandler, ethernetTuri uint16)
	EthernetRamkareceivewhen(dataKorsatgich uintptr, hajmi int) bool
	Joʻnatish(destinationmacbe uint64, dataKorsatgich uintptr, hajmi uint32)
	RamkaJoʻnatish(destinationmacbe uint64, ethernetTuribe uint16, dataKorsatgich uintptr, hajmi uint32)
	Providerget() TEthernetRamkaprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRamkahandler struct {
}

var ramka TEthernetRamkaheader
var Backend TEthernetRamkaprovider
var handler_2 [65535]IEthernetRamkahandler
var efhandler *TEthernetRamkahandler = nil

func (self *TEthernetRamkahandler) Init(backend TEthernetRamkaprovider) {
	Backend = backend
}

func (self *TEthernetRamkahandler) Sethandler(handler IEthernetRamkahandler, pethernetTuri uint16) {
	handler_2[pethernetTuri] = handler
}
func (self *TEthernetRamkahandler) Setbackend(backend TEthernetRamkaprovider) {
	Backend = backend
}
func (self *TEthernetRamkahandler) Getbackend() TEthernetRamkaprovider {
	return Backend
}
func (self *TEthernetRamkahandler) EthernetRamkareceivewhen(dataKorsatgich uintptr, hajmi int) bool {
	ethernetconsole.MChopetish(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetRamkahandler) Joʻnatish(destinationmacbe uint64, dataKorsatgich uintptr, hajmi uint32) {
	Backend.RamkaJoʻnatish(destinationmacbe, ramka.ethernetTuribe, dataKorsatgich, hajmi)
}
func (self *TEthernetRamkahandler) RamkaJoʻnatish(destinationmacbe uint64, ethernetTuribe uint16, dataKorsatgich uintptr, hajmi uint32) {
	Backend.RamkaJoʻnatish(destinationmacbe, ethernetTuribe, dataKorsatgich, hajmi)
}
func (self *TEthernetRamkahandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetRamkahandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetRamkahandler) Providerget() TEthernetRamkaprovider {
	return Backend
}

type TEthernetRamkarawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetRamkaprovider

func (self *TEthernetRamkarawdatahandler) Init(pprovider TEthernetRamkaprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetRamkarawdatahandler) Yoqishrawdatareceive(dataKorsatgich uintptr, hajmi int) bool {
	return provider.Yoqishrawdatareceive(dataKorsatgich, hajmi)
}
func (self *TEthernetRamkarawdatahandler) Joʻnatish(dataKorsatgich uintptr, hajmi uint32) {
	provider.Joʻnatish(dataKorsatgich, hajmi)
}
func (self *TEthernetRamkarawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetRamkarawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetRamkarawdatahandler) Providerget() TEthernetRamkaprovider {
	return provider
}

type TEthernetRamkaprovider struct {
	tarmoqcard	Tamdam79c973
	handler_2	[65565]IEthernetRamkahandler
}

func (self *TEthernetRamkaprovider) Init(backend Tamdam79c973) {

	self.tarmoqcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetRamkaprovider) Yoqishrawdatareceive(dataKorsatgich uintptr, hajmi int) bool {

	var buffer_2 *TEthernetRamkaheaderbuffer = (*TEthernetRamkaheaderbuffer)(Pointer(dataKorsatgich))
	var ramka TEthernetRamkaheader = TEthernetRamkaheader{}
	ramka.Init(*buffer_2)
	var reply bool = false

	if ramka.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ramka.destinationmacbe) == self.Getmacaddress() {
		if handler_2[ramka.ethernetTuribe] != nil {
			ethernetconsole.MChopetish(([]byte)("provider\n"))

			var korsatgich uintptr = uintptr(Pointer(dataKorsatgich)) + uintptr(ramkaheaderHajmi)
			reply = handler_2[ramka.ethernetTuribe].EthernetRamkareceivewhen(korsatgich, hajmi-ramkaheaderHajmi)

		}
	}

	if reply {
		ramka.destinationmacbe = ramka.sourcemacbe
		ramka.sourcemacbe = Unsignedinteger48r(self.Getmacaddress())
		ramka.Setbuffer(buffer_2)

	}

	ethernetconsole.MChopetishxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Chopetish(ramka.sourcemacbe)
	ethernetconsole.MChopetish(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Chopetish(ramka.destinationmacbe)
	ethernetconsole.MChopetish(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Chopetish(self.Getmacaddress())
	ethernetconsole.MChopetish(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Chopetish(ramka.ethernetTuribe)
	ethernetconsole.MChopetish(([]byte)("]"))

	return reply

}
func (self *TEthernetRamkaprovider) Joʻnatish(dataKorsatgich uintptr, hajmi uint32) {
	self.tarmoqcard.Joʻnatish(dataKorsatgich, hajmi)
}
func (self *TEthernetRamkaprovider) RamkaJoʻnatish(destinationmacbe uint64, ethernetTuribe uint16, dataKorsatgich uintptr, hajmi uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRamkaheaderbuffer = (*TEthernetRamkaheaderbuffer)(Pointer(&buffer2_2))

	var ramka TEthernetRamkaheader = TEthernetRamkaheader{}
	ramka.Init(*buffer_2)

	ramka.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	ramka.sourcemacbe = Unsignedinteger48r(self.tarmoqcard.Getmacaddress())
	ramka.ethernetTuribe = Unsignedinteger16r(ethernetTuribe)

	ramka.Setbuffer(buffer_2)
	var source_2 [4096]byte = *(*([4096]byte))(Pointer(dataKorsatgich))

	var i uint32 = 0
	for i = 0; i < hajmi; i++ {
		buffer2_2[uint32(ramkaheaderHajmi)+i] = source_2[i]

	}

	var korsatgich uintptr = uintptr(Pointer(&buffer2_2))

	self.tarmoqcard.Joʻnatish(korsatgich, hajmi+uint32(ramkaheaderHajmi))

}
func (self *TEthernetRamkaprovider) Getmacaddress() uint64 {
	return self.tarmoqcard.Getmacaddress()
}
func (self *TEthernetRamkaprovider) Getipaddress() uint64 {
	return self.tarmoqcard.Getipaddress()
}
