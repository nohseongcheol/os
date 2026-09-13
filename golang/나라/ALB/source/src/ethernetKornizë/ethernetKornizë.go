package ethernetKornizë

import . "konsolë"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonsolë TKonsolë = TKonsolë{}

type TEthernetKornizëheaderbuffer struct {
	destinacionimacbe	[6]byte
	burimimacbe		[6]byte
	ethernetLlojibe		[2]byte
}

var kornizëheaderMadhësia int = 14

type TEthernetKornizëheader struct {
	destinacionimacbe	uint64
	burimimacbe		uint64
	ethernetLlojibe		uint16
}

func (vetvetja *TEthernetKornizëheader) Init(buffer_2 TEthernetKornizëheaderbuffer) {
	vetvetja.destinacionimacbe = (Rreshtimitounsignedinteger48(buffer_2.destinacionimacbe))
	vetvetja.burimimacbe = (Rreshtimitounsignedinteger48(buffer_2.burimimacbe))
	vetvetja.ethernetLlojibe = (Rreshtimitounsignedinteger16(buffer_2.ethernetLlojibe))

}
func (vetvetja *TEthernetKornizëheader) Caktonibuffer(buffer_2 *TEthernetKornizëheaderbuffer) {
	buffer_2.destinacionimacbe = Unsignedinteger48toRreshtimi(Unsignedinteger48r(vetvetja.destinacionimacbe))
	buffer_2.burimimacbe = Unsignedinteger48toRreshtimi(Unsignedinteger48r(vetvetja.burimimacbe))
	buffer_2.ethernetLlojibe = Unsignedinteger16toRreshtimi(Unsignedinteger16r(vetvetja.ethernetLlojibe))
}

type IEthernetKornizëhandler interface {
	Init(backend TEthernetKornizëprovider)
	Caktonihandler(handler IEthernetKornizëhandler, ethernetLloji uint16)
	EthernetKornizëreceivewhen(dataKursori uintptr, madhësia int) bool
	Dërgo(destinacionimacbe uint64, dataKursori uintptr, madhësia uint32)
	KornizëDërgo(destinacionimacbe uint64, ethernetLlojibe uint16, dataKursori uintptr, madhësia uint32)
	Providerget() TEthernetKornizëprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetKornizëhandler struct {
}

var kornizë TEthernetKornizëheader
var Backend TEthernetKornizëprovider
var handler_2 [65535]IEthernetKornizëhandler
var efhandler *TEthernetKornizëhandler = nil

func (vetvetja *TEthernetKornizëhandler) Init(backend TEthernetKornizëprovider) {
	Backend = backend
}

func (vetvetja *TEthernetKornizëhandler) Caktonihandler(handler IEthernetKornizëhandler, pethernetLloji uint16) {
	handler_2[pethernetLloji] = handler
}
func (vetvetja *TEthernetKornizëhandler) Caktonibackend(backend TEthernetKornizëprovider) {
	Backend = backend
}
func (vetvetja *TEthernetKornizëhandler) Getbackend() TEthernetKornizëprovider {
	return Backend
}
func (vetvetja *TEthernetKornizëhandler) EthernetKornizëreceivewhen(dataKursori uintptr, madhësia int) bool {
	ethernetKonsolë.MPrinto(([]byte)("OnEtherFrameReceived"))
	return false
}
func (vetvetja *TEthernetKornizëhandler) Dërgo(destinacionimacbe uint64, dataKursori uintptr, madhësia uint32) {
	Backend.KornizëDërgo(destinacionimacbe, kornizë.ethernetLlojibe, dataKursori, madhësia)
}
func (vetvetja *TEthernetKornizëhandler) KornizëDërgo(destinacionimacbe uint64, ethernetLlojibe uint16, dataKursori uintptr, madhësia uint32) {
	Backend.KornizëDërgo(destinacionimacbe, ethernetLlojibe, dataKursori, madhësia)
}
func (vetvetja *TEthernetKornizëhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (vetvetja *TEthernetKornizëhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (vetvetja *TEthernetKornizëhandler) Providerget() TEthernetKornizëprovider {
	return Backend
}

type TEthernetKornizërawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetKornizëprovider

func (vetvetja *TEthernetKornizërawdatahandler) Init(pprovider TEthernetKornizëprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (vetvetja *TEthernetKornizërawdatahandler) Onrawdatareceive(dataKursori uintptr, madhësia int) bool {
	return provider.Onrawdatareceive(dataKursori, madhësia)
}
func (vetvetja *TEthernetKornizërawdatahandler) Dërgo(dataKursori uintptr, madhësia uint32) {
	provider.Dërgo(dataKursori, madhësia)
}
func (vetvetja *TEthernetKornizërawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (vetvetja *TEthernetKornizërawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (vetvetja *TEthernetKornizërawdatahandler) Providerget() TEthernetKornizëprovider {
	return provider
}

type TEthernetKornizëprovider struct {
	rrjetiLetra	Tamdam79c973
	handler_2	[65565]IEthernetKornizëhandler
}

func (vetvetja *TEthernetKornizëprovider) Init(backend Tamdam79c973) {

	vetvetja.rrjetiLetra = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		vetvetja.handler_2[i] = nil
	}
}

var count uint16 = 0

func (vetvetja *TEthernetKornizëprovider) Onrawdatareceive(dataKursori uintptr, madhësia int) bool {

	var buffer_2 *TEthernetKornizëheaderbuffer = (*TEthernetKornizëheaderbuffer)(Pointer(dataKursori))
	var kornizë TEthernetKornizëheader = TEthernetKornizëheader{}
	kornizë.Init(*buffer_2)
	var reply bool = false

	if kornizë.destinacionimacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(kornizë.destinacionimacbe) == vetvetja.Getmacaddress() {
		if handler_2[kornizë.ethernetLlojibe] != nil {
			ethernetKonsolë.MPrinto(([]byte)("provider\n"))

			var kursori uintptr = uintptr(Pointer(dataKursori)) + uintptr(kornizëheaderMadhësia)
			reply = handler_2[kornizë.ethernetLlojibe].EthernetKornizëreceivewhen(kursori, madhësia-kornizëheaderMadhësia)

		}
	}

	if reply {
		kornizë.destinacionimacbe = kornizë.burimimacbe
		kornizë.burimimacbe = Unsignedinteger48r(vetvetja.Getmacaddress())
		kornizë.Caktonibuffer(buffer_2)

	}

	ethernetKonsolë.MPrintoxy(([]byte)("spro["), 0, 1)
	ethernetKonsolë.MUnsignedinteger64Printo(kornizë.burimimacbe)
	ethernetKonsolë.MPrinto(([]byte)(":"))
	ethernetKonsolë.MUnsignedinteger64Printo(kornizë.destinacionimacbe)
	ethernetKonsolë.MPrinto(([]byte)(":]["))
	ethernetKonsolë.MUnsignedinteger64Printo(vetvetja.Getmacaddress())
	ethernetKonsolë.MPrinto(([]byte)(":"))
	ethernetKonsolë.MUnsignedinteger16Printo(kornizë.ethernetLlojibe)
	ethernetKonsolë.MPrinto(([]byte)("]"))

	return reply

}
func (vetvetja *TEthernetKornizëprovider) Dërgo(dataKursori uintptr, madhësia uint32) {
	vetvetja.rrjetiLetra.Dërgo(dataKursori, madhësia)
}
func (vetvetja *TEthernetKornizëprovider) KornizëDërgo(destinacionimacbe uint64, ethernetLlojibe uint16, dataKursori uintptr, madhësia uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetKornizëheaderbuffer = (*TEthernetKornizëheaderbuffer)(Pointer(&buffer2_2))

	var kornizë TEthernetKornizëheader = TEthernetKornizëheader{}
	kornizë.Init(*buffer_2)

	kornizë.destinacionimacbe = Unsignedinteger48r(destinacionimacbe)
	kornizë.burimimacbe = Unsignedinteger48r(vetvetja.rrjetiLetra.Getmacaddress())
	kornizë.ethernetLlojibe = Unsignedinteger16r(ethernetLlojibe)

	kornizë.Caktonibuffer(buffer_2)
	var burimi_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursori))

	var i uint32 = 0
	for i = 0; i < madhësia; i++ {
		buffer2_2[uint32(kornizëheaderMadhësia)+i] = burimi_2[i]

	}

	var kursori uintptr = uintptr(Pointer(&buffer2_2))

	vetvetja.rrjetiLetra.Dërgo(kursori, madhësia+uint32(kornizëheaderMadhësia))

}
func (vetvetja *TEthernetKornizëprovider) Getmacaddress() uint64 {
	return vetvetja.rrjetiLetra.Getmacaddress()
}
func (vetvetja *TEthernetKornizëprovider) Getipaddress() uint64 {
	return vetvetja.rrjetiLetra.Getipaddress()
}
