package ethernetเฟรม

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetเฟรมheaderbuffer struct {
	ปลายทางmacbe		[6]byte
	sourcemacbe		[6]byte
	ethernetประเภทbe	[2]byte
}

var เฟรมheaderขนาด int = 14

type TEthernetเฟรมheader struct {
	ปลายทางmacbe		uint64
	sourcemacbe		uint64
	ethernetประเภทbe	uint16
}

func (self *TEthernetเฟรมheader) Init(buffer_2 TEthernetเฟรมheaderbuffer) {
	self.ปลายทางmacbe = (Arraytounsignedinteger48(buffer_2.ปลายทางmacbe))
	self.sourcemacbe = (Arraytounsignedinteger48(buffer_2.sourcemacbe))
	self.ethernetประเภทbe = (Arraytounsignedinteger16(buffer_2.ethernetประเภทbe))

}
func (self *TEthernetเฟรมheader) Sกำหนดbuffer(buffer_2 *TEthernetเฟรมheaderbuffer) {
	buffer_2.ปลายทางmacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.ปลายทางmacbe))
	buffer_2.sourcemacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.sourcemacbe))
	buffer_2.ethernetประเภทbe = Unsignedinteger16toarray(Unsignedinteger16r(self.ethernetประเภทbe))
}

type IEthernetเฟรมhandler interface {
	Init(backend TEthernetเฟรมprovider)
	Sกำหนดhandler(handler IEthernetเฟรมhandler, ethernetประเภท uint16)
	Ethernetเฟรมreceivewhen(datapointer uintptr, ขนาด int) bool
	Send(ปลายทางmacbe uint64, datapointer uintptr, ขนาด uint32)
	Sเฟรมsend(ปลายทางmacbe uint64, ethernetประเภทbe uint16, datapointer uintptr, ขนาด uint32)
	Providerget() TEthernetเฟรมprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetเฟรมhandler struct {
}

var เฟรม TEthernetเฟรมheader
var Backend TEthernetเฟรมprovider
var handler_2 [65535]IEthernetเฟรมhandler
var efhandler *TEthernetเฟรมhandler = nil

func (self *TEthernetเฟรมhandler) Init(backend TEthernetเฟรมprovider) {
	Backend = backend
}

func (self *TEthernetเฟรมhandler) Sกำหนดhandler(handler IEthernetเฟรมhandler, pethernetประเภท uint16) {
	handler_2[pethernetประเภท] = handler
}
func (self *TEthernetเฟรมhandler) Sกำหนดbackend(backend TEthernetเฟรมprovider) {
	Backend = backend
}
func (self *TEthernetเฟรมhandler) Getbackend() TEthernetเฟรมprovider {
	return Backend
}
func (self *TEthernetเฟรมhandler) Ethernetเฟรมreceivewhen(datapointer uintptr, ขนาด int) bool {
	ethernetconsole.MPrint(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetเฟรมhandler) Send(ปลายทางmacbe uint64, datapointer uintptr, ขนาด uint32) {
	Backend.Sเฟรมsend(ปลายทางmacbe, เฟรม.ethernetประเภทbe, datapointer, ขนาด)
}
func (self *TEthernetเฟรมhandler) Sเฟรมsend(ปลายทางmacbe uint64, ethernetประเภทbe uint16, datapointer uintptr, ขนาด uint32) {
	Backend.Sเฟรมsend(ปลายทางmacbe, ethernetประเภทbe, datapointer, ขนาด)
}
func (self *TEthernetเฟรมhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetเฟรมhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetเฟรมhandler) Providerget() TEthernetเฟรมprovider {
	return Backend
}

type TEthernetเฟรมrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetเฟรมprovider

func (self *TEthernetเฟรมrawdatahandler) Init(pprovider TEthernetเฟรมprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetเฟรมrawdatahandler) Onrawdatareceive(datapointer uintptr, ขนาด int) bool {
	return provider.Onrawdatareceive(datapointer, ขนาด)
}
func (self *TEthernetเฟรมrawdatahandler) Send(datapointer uintptr, ขนาด uint32) {
	provider.Send(datapointer, ขนาด)
}
func (self *TEthernetเฟรมrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetเฟรมrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetเฟรมrawdatahandler) Providerget() TEthernetเฟรมprovider {
	return provider
}

type TEthernetเฟรมprovider struct {
	networkcard	Tamdam79c973
	handler_2	[65565]IEthernetเฟรมhandler
}

func (self *TEthernetเฟรมprovider) Init(backend Tamdam79c973) {

	self.networkcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetเฟรมprovider) Onrawdatareceive(datapointer uintptr, ขนาด int) bool {

	var buffer_2 *TEthernetเฟรมheaderbuffer = (*TEthernetเฟรมheaderbuffer)(Pointer(datapointer))
	var เฟรม TEthernetเฟรมheader = TEthernetเฟรมheader{}
	เฟรม.Init(*buffer_2)
	var reply bool = false

	if เฟรม.ปลายทางmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(เฟรม.ปลายทางmacbe) == self.Getmacaddress() {
		if handler_2[เฟรม.ethernetประเภทbe] != nil {
			ethernetconsole.MPrint(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(เฟรมheaderขนาด)
			reply = handler_2[เฟรม.ethernetประเภทbe].Ethernetเฟรมreceivewhen(pointer, ขนาด-เฟรมheaderขนาด)

		}
	}

	if reply {
		เฟรม.ปลายทางmacbe = เฟรม.sourcemacbe
		เฟรม.sourcemacbe = Unsignedinteger48r(self.Getmacaddress())
		เฟรม.Sกำหนดbuffer(buffer_2)

	}

	ethernetconsole.MPrintxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64print(เฟรม.sourcemacbe)
	ethernetconsole.MPrint(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64print(เฟรม.ปลายทางmacbe)
	ethernetconsole.MPrint(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64print(self.Getmacaddress())
	ethernetconsole.MPrint(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16print(เฟรม.ethernetประเภทbe)
	ethernetconsole.MPrint(([]byte)("]"))

	return reply

}
func (self *TEthernetเฟรมprovider) Send(datapointer uintptr, ขนาด uint32) {
	self.networkcard.Send(datapointer, ขนาด)
}
func (self *TEthernetเฟรมprovider) Sเฟรมsend(ปลายทางmacbe uint64, ethernetประเภทbe uint16, datapointer uintptr, ขนาด uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetเฟรมheaderbuffer = (*TEthernetเฟรมheaderbuffer)(Pointer(&buffer2_2))

	var เฟรม TEthernetเฟรมheader = TEthernetเฟรมheader{}
	เฟรม.Init(*buffer_2)

	เฟรม.ปลายทางmacbe = Unsignedinteger48r(ปลายทางmacbe)
	เฟรม.sourcemacbe = Unsignedinteger48r(self.networkcard.Getmacaddress())
	เฟรม.ethernetประเภทbe = Unsignedinteger16r(ethernetประเภทbe)

	เฟรม.Sกำหนดbuffer(buffer_2)
	var source_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < ขนาด; i++ {
		buffer2_2[uint32(เฟรมheaderขนาด)+i] = source_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	self.networkcard.Send(pointer, ขนาด+uint32(เฟรมheaderขนาด))

}
func (self *TEthernetเฟรมprovider) Getmacaddress() uint64 {
	return self.networkcard.Getmacaddress()
}
func (self *TEthernetเฟรมprovider) Getipaddress() uint64 {
	return self.networkcard.Getipaddress()
}
