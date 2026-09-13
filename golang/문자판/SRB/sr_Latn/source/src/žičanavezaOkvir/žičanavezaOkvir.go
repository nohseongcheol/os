package žičanavezaOkvir

import . "konzola"

import . "amdam79c973"
import . "unsafe"
import . "util"

var žičanavezaKonzola TKonzola = TKonzola{}

type TŽičanavezaOkvirheaderbuffer struct {
	odredištemacbe		[6]byte
	izvormacbe		[6]byte
	žičanavezaVrstabe	[2]byte
}

var okvirheaderVeličina int = 14

type TŽičanavezaOkvirheader struct {
	odredištemacbe		uint64
	izvormacbe		uint64
	žičanavezaVrstabe	uint16
}

func (isti *TŽičanavezaOkvirheader) Init(buffer_2 TŽičanavezaOkvirheaderbuffer) {
	isti.odredištemacbe = (Niztounsignedinteger48(buffer_2.odredištemacbe))
	isti.izvormacbe = (Niztounsignedinteger48(buffer_2.izvormacbe))
	isti.žičanavezaVrstabe = (Niztounsignedinteger16(buffer_2.žičanavezaVrstabe))

}
func (isti *TŽičanavezaOkvirheader) Skupbuffer(buffer_2 *TŽičanavezaOkvirheaderbuffer) {
	buffer_2.odredištemacbe = Unsignedinteger48toNiz(Unsignedinteger48r(isti.odredištemacbe))
	buffer_2.izvormacbe = Unsignedinteger48toNiz(Unsignedinteger48r(isti.izvormacbe))
	buffer_2.žičanavezaVrstabe = Unsignedinteger16toNiz(Unsignedinteger16r(isti.žičanavezaVrstabe))
}

type IŽičanavezaOkvirhandler interface {
	Init(backend TŽičanavezaOkvirprovider)
	Skuphandler(handler IŽičanavezaOkvirhandler, žičanavezaVrsta uint16)
	ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, veličina int) bool
	Pošalji(odredištemacbe uint64, dataPokazivač uintptr, veličina uint32)
	OkvirPošalji(odredištemacbe uint64, žičanavezaVrstabe uint16, dataPokazivač uintptr, veličina uint32)
	Providerget() TŽičanavezaOkvirprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TŽičanavezaOkvirhandler struct {
}

var okvir TŽičanavezaOkvirheader
var Backend TŽičanavezaOkvirprovider
var handler_2 [65535]IŽičanavezaOkvirhandler
var efhandler *TŽičanavezaOkvirhandler = nil

func (isti *TŽičanavezaOkvirhandler) Init(backend TŽičanavezaOkvirprovider) {
	Backend = backend
}

func (isti *TŽičanavezaOkvirhandler) Skuphandler(handler IŽičanavezaOkvirhandler, pŽičanavezaVrsta uint16) {
	handler_2[pŽičanavezaVrsta] = handler
}
func (isti *TŽičanavezaOkvirhandler) Skupbackend(backend TŽičanavezaOkvirprovider) {
	Backend = backend
}
func (isti *TŽičanavezaOkvirhandler) Getbackend() TŽičanavezaOkvirprovider {
	return Backend
}
func (isti *TŽičanavezaOkvirhandler) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, veličina int) bool {
	žičanavezaKonzola.MŠtampaj(([]byte)("OnEtherFrameReceived"))
	return false
}
func (isti *TŽičanavezaOkvirhandler) Pošalji(odredištemacbe uint64, dataPokazivač uintptr, veličina uint32) {
	Backend.OkvirPošalji(odredištemacbe, okvir.žičanavezaVrstabe, dataPokazivač, veličina)
}
func (isti *TŽičanavezaOkvirhandler) OkvirPošalji(odredištemacbe uint64, žičanavezaVrstabe uint16, dataPokazivač uintptr, veličina uint32) {
	Backend.OkvirPošalji(odredištemacbe, žičanavezaVrstabe, dataPokazivač, veličina)
}
func (isti *TŽičanavezaOkvirhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (isti *TŽičanavezaOkvirhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (isti *TŽičanavezaOkvirhandler) Providerget() TŽičanavezaOkvirprovider {
	return Backend
}

type TŽičanavezaOkvirrawdatahandler struct {
	TRawdatahandler
}

var provider TŽičanavezaOkvirprovider

func (isti *TŽičanavezaOkvirrawdatahandler) Init(pprovider TŽičanavezaOkvirprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (isti *TŽičanavezaOkvirrawdatahandler) Narawdatareceive(dataPokazivač uintptr, veličina int) bool {
	return provider.Narawdatareceive(dataPokazivač, veličina)
}
func (isti *TŽičanavezaOkvirrawdatahandler) Pošalji(dataPokazivač uintptr, veličina uint32) {
	provider.Pošalji(dataPokazivač, veličina)
}
func (isti *TŽičanavezaOkvirrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (isti *TŽičanavezaOkvirrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (isti *TŽičanavezaOkvirrawdatahandler) Providerget() TŽičanavezaOkvirprovider {
	return provider
}

type TŽičanavezaOkvirprovider struct {
	mrežacard	Tamdam79c973
	handler_2	[65565]IŽičanavezaOkvirhandler
}

func (isti *TŽičanavezaOkvirprovider) Init(backend Tamdam79c973) {

	isti.mrežacard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		isti.handler_2[i] = nil
	}
}

var count uint16 = 0

func (isti *TŽičanavezaOkvirprovider) Narawdatareceive(dataPokazivač uintptr, veličina int) bool {

	var buffer_2 *TŽičanavezaOkvirheaderbuffer = (*TŽičanavezaOkvirheaderbuffer)(Pointer(dataPokazivač))
	var okvir TŽičanavezaOkvirheader = TŽičanavezaOkvirheader{}
	okvir.Init(*buffer_2)
	var reply bool = false

	if okvir.odredištemacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(okvir.odredištemacbe) == isti.Getmacaddress() {
		if handler_2[okvir.žičanavezaVrstabe] != nil {
			žičanavezaKonzola.MŠtampaj(([]byte)("provider\n"))

			var pokazivač uintptr = uintptr(Pointer(dataPokazivač)) + uintptr(okvirheaderVeličina)
			reply = handler_2[okvir.žičanavezaVrstabe].ŽičanavezaOkvirreceivewhen(pokazivač, veličina-okvirheaderVeličina)

		}
	}

	if reply {
		okvir.odredištemacbe = okvir.izvormacbe
		okvir.izvormacbe = Unsignedinteger48r(isti.Getmacaddress())
		okvir.Skupbuffer(buffer_2)

	}

	žičanavezaKonzola.MŠtampajxy(([]byte)("spro["), 0, 1)
	žičanavezaKonzola.MUnsignedinteger64Štampaj(okvir.izvormacbe)
	žičanavezaKonzola.MŠtampaj(([]byte)(":"))
	žičanavezaKonzola.MUnsignedinteger64Štampaj(okvir.odredištemacbe)
	žičanavezaKonzola.MŠtampaj(([]byte)(":]["))
	žičanavezaKonzola.MUnsignedinteger64Štampaj(isti.Getmacaddress())
	žičanavezaKonzola.MŠtampaj(([]byte)(":"))
	žičanavezaKonzola.MUnsignedinteger16Štampaj(okvir.žičanavezaVrstabe)
	žičanavezaKonzola.MŠtampaj(([]byte)("]"))

	return reply

}
func (isti *TŽičanavezaOkvirprovider) Pošalji(dataPokazivač uintptr, veličina uint32) {
	isti.mrežacard.Pošalji(dataPokazivač, veličina)
}
func (isti *TŽičanavezaOkvirprovider) OkvirPošalji(odredištemacbe uint64, žičanavezaVrstabe uint16, dataPokazivač uintptr, veličina uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TŽičanavezaOkvirheaderbuffer = (*TŽičanavezaOkvirheaderbuffer)(Pointer(&buffer2_2))

	var okvir TŽičanavezaOkvirheader = TŽičanavezaOkvirheader{}
	okvir.Init(*buffer_2)

	okvir.odredištemacbe = Unsignedinteger48r(odredištemacbe)
	okvir.izvormacbe = Unsignedinteger48r(isti.mrežacard.Getmacaddress())
	okvir.žičanavezaVrstabe = Unsignedinteger16r(žičanavezaVrstabe)

	okvir.Skupbuffer(buffer_2)
	var izvor_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))

	var i uint32 = 0
	for i = 0; i < veličina; i++ {
		buffer2_2[uint32(okvirheaderVeličina)+i] = izvor_2[i]

	}

	var pokazivač uintptr = uintptr(Pointer(&buffer2_2))

	isti.mrežacard.Pošalji(pokazivač, veličina+uint32(okvirheaderVeličina))

}
func (isti *TŽičanavezaOkvirprovider) Getmacaddress() uint64 {
	return isti.mrežacard.Getmacaddress()
}
func (isti *TŽičanavezaOkvirprovider) Getipaddress() uint64 {
	return isti.mrežacard.Getipaddress()
}
