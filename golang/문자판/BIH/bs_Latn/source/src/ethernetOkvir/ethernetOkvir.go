package ethernetOkvir

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetOkvirheaderbuffer struct {
	odredištemacbe	[6]byte
	izvormacbe	[6]byte
	ethernetTipbe	[2]byte
}

var okvirheaderVeličina int = 14

type TEthernetOkvirheader struct {
	odredištemacbe	uint64
	izvormacbe	uint64
	ethernetTipbe	uint16
}

func (self *TEthernetOkvirheader) Init(buffer_2 TEthernetOkvirheaderbuffer) {
	self.odredištemacbe = (Arraytounsignedinteger48(buffer_2.odredištemacbe))
	self.izvormacbe = (Arraytounsignedinteger48(buffer_2.izvormacbe))
	self.ethernetTipbe = (Arraytounsignedinteger16(buffer_2.ethernetTipbe))

}
func (self *TEthernetOkvirheader) Skupbuffer(buffer_2 *TEthernetOkvirheaderbuffer) {
	buffer_2.odredištemacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.odredištemacbe))
	buffer_2.izvormacbe = Unsignedinteger48toarray(Unsignedinteger48r(self.izvormacbe))
	buffer_2.ethernetTipbe = Unsignedinteger16toarray(Unsignedinteger16r(self.ethernetTipbe))
}

type IEthernetOkvirhandler interface {
	Init(backend TEthernetOkvirprovider)
	Skuphandler(handler IEthernetOkvirhandler, ethernetTip uint16)
	EthernetOkvirreceivewhen(datapointer uintptr, veličina int) bool
	Pošalji(odredištemacbe uint64, datapointer uintptr, veličina uint32)
	OkvirPošalji(odredištemacbe uint64, ethernetTipbe uint16, datapointer uintptr, veličina uint32)
	Providerget() TEthernetOkvirprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetOkvirhandler struct {
}

var okvir TEthernetOkvirheader
var Backend TEthernetOkvirprovider
var handler_2 [65535]IEthernetOkvirhandler
var efhandler *TEthernetOkvirhandler = nil

func (self *TEthernetOkvirhandler) Init(backend TEthernetOkvirprovider) {
	Backend = backend
}

func (self *TEthernetOkvirhandler) Skuphandler(handler IEthernetOkvirhandler, pethernetTip uint16) {
	handler_2[pethernetTip] = handler
}
func (self *TEthernetOkvirhandler) Skupbackend(backend TEthernetOkvirprovider) {
	Backend = backend
}
func (self *TEthernetOkvirhandler) Getbackend() TEthernetOkvirprovider {
	return Backend
}
func (self *TEthernetOkvirhandler) EthernetOkvirreceivewhen(datapointer uintptr, veličina int) bool {
	ethernetconsole.MŠtampaj(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetOkvirhandler) Pošalji(odredištemacbe uint64, datapointer uintptr, veličina uint32) {
	Backend.OkvirPošalji(odredištemacbe, okvir.ethernetTipbe, datapointer, veličina)
}
func (self *TEthernetOkvirhandler) OkvirPošalji(odredištemacbe uint64, ethernetTipbe uint16, datapointer uintptr, veličina uint32) {
	Backend.OkvirPošalji(odredištemacbe, ethernetTipbe, datapointer, veličina)
}
func (self *TEthernetOkvirhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetOkvirhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetOkvirhandler) Providerget() TEthernetOkvirprovider {
	return Backend
}

type TEthernetOkvirrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetOkvirprovider

func (self *TEthernetOkvirrawdatahandler) Init(pprovider TEthernetOkvirprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetOkvirrawdatahandler) Uključenrawdatareceive(datapointer uintptr, veličina int) bool {
	return provider.Uključenrawdatareceive(datapointer, veličina)
}
func (self *TEthernetOkvirrawdatahandler) Pošalji(datapointer uintptr, veličina uint32) {
	provider.Pošalji(datapointer, veličina)
}
func (self *TEthernetOkvirrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetOkvirrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetOkvirrawdatahandler) Providerget() TEthernetOkvirprovider {
	return provider
}

type TEthernetOkvirprovider struct {
	mrežaKartaške	Tamdam79c973
	handler_2	[65565]IEthernetOkvirhandler
}

func (self *TEthernetOkvirprovider) Init(backend Tamdam79c973) {

	self.mrežaKartaške = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetOkvirprovider) Uključenrawdatareceive(datapointer uintptr, veličina int) bool {

	var buffer_2 *TEthernetOkvirheaderbuffer = (*TEthernetOkvirheaderbuffer)(Pointer(datapointer))
	var okvir TEthernetOkvirheader = TEthernetOkvirheader{}
	okvir.Init(*buffer_2)
	var reply bool = false

	if okvir.odredištemacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(okvir.odredištemacbe) == self.Getmacaddress() {
		if handler_2[okvir.ethernetTipbe] != nil {
			ethernetconsole.MŠtampaj(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(okvirheaderVeličina)
			reply = handler_2[okvir.ethernetTipbe].EthernetOkvirreceivewhen(pointer, veličina-okvirheaderVeličina)

		}
	}

	if reply {
		okvir.odredištemacbe = okvir.izvormacbe
		okvir.izvormacbe = Unsignedinteger48r(self.Getmacaddress())
		okvir.Skupbuffer(buffer_2)

	}

	ethernetconsole.MŠtampajxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Štampaj(okvir.izvormacbe)
	ethernetconsole.MŠtampaj(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Štampaj(okvir.odredištemacbe)
	ethernetconsole.MŠtampaj(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Štampaj(self.Getmacaddress())
	ethernetconsole.MŠtampaj(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Štampaj(okvir.ethernetTipbe)
	ethernetconsole.MŠtampaj(([]byte)("]"))

	return reply

}
func (self *TEthernetOkvirprovider) Pošalji(datapointer uintptr, veličina uint32) {
	self.mrežaKartaške.Pošalji(datapointer, veličina)
}
func (self *TEthernetOkvirprovider) OkvirPošalji(odredištemacbe uint64, ethernetTipbe uint16, datapointer uintptr, veličina uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetOkvirheaderbuffer = (*TEthernetOkvirheaderbuffer)(Pointer(&buffer2_2))

	var okvir TEthernetOkvirheader = TEthernetOkvirheader{}
	okvir.Init(*buffer_2)

	okvir.odredištemacbe = Unsignedinteger48r(odredištemacbe)
	okvir.izvormacbe = Unsignedinteger48r(self.mrežaKartaške.Getmacaddress())
	okvir.ethernetTipbe = Unsignedinteger16r(ethernetTipbe)

	okvir.Skupbuffer(buffer_2)
	var izvor_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < veličina; i++ {
		buffer2_2[uint32(okvirheaderVeličina)+i] = izvor_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	self.mrežaKartaške.Pošalji(pointer, veličina+uint32(okvirheaderVeličina))

}
func (self *TEthernetOkvirprovider) Getmacaddress() uint64 {
	return self.mrežaKartaške.Getmacaddress()
}
func (self *TEthernetOkvirprovider) Getipaddress() uint64 {
	return self.mrežaKartaške.Getipaddress()
}
