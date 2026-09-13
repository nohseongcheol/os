package žičanavezaOkvir

import . "конзола"

import . "amdam79c973"
import . "unsafe"
import . "util"

var žičanavezaКонзола TКонзола = TКонзола{}

type TŽičanavezaOkvirheaderbuffer struct {
	odredištemacbe		[6]byte
	izvormacbe		[6]byte
	žičanavezaВрстаbe	[2]byte
}

var okvirheaderВеличина int = 14

type TŽičanavezaOkvirheader struct {
	odredištemacbe		uint64
	izvormacbe		uint64
	žičanavezaВрстаbe	uint16
}

func (isti *TŽičanavezaOkvirheader) Init(buffer_2 TŽičanavezaOkvirheaderbuffer) {
	isti.odredištemacbe = (Низtounsignedinteger48(buffer_2.odredištemacbe))
	isti.izvormacbe = (Низtounsignedinteger48(buffer_2.izvormacbe))
	isti.žičanavezaВрстаbe = (Низtounsignedinteger16(buffer_2.žičanavezaВрстаbe))

}
func (isti *TŽičanavezaOkvirheader) Скупbuffer(buffer_2 *TŽičanavezaOkvirheaderbuffer) {
	buffer_2.odredištemacbe = Unsignedinteger48toНиз(Unsignedinteger48r(isti.odredištemacbe))
	buffer_2.izvormacbe = Unsignedinteger48toНиз(Unsignedinteger48r(isti.izvormacbe))
	buffer_2.žičanavezaВрстаbe = Unsignedinteger16toНиз(Unsignedinteger16r(isti.žičanavezaВрстаbe))
}

type IŽičanavezaOkvirhandler interface {
	Init(backend TŽičanavezaOkvirprovider)
	Скупhandler(handler IŽičanavezaOkvirhandler, žičanavezaВрста uint16)
	ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, величина int) bool
	Пошаљи(odredištemacbe uint64, dataPokazivač uintptr, величина uint32)
	OkvirПошаљи(odredištemacbe uint64, žičanavezaВрстаbe uint16, dataPokazivač uintptr, величина uint32)
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

func (isti *TŽičanavezaOkvirhandler) Скупhandler(handler IŽičanavezaOkvirhandler, pŽičanavezaВрста uint16) {
	handler_2[pŽičanavezaВрста] = handler
}
func (isti *TŽičanavezaOkvirhandler) Скупbackend(backend TŽičanavezaOkvirprovider) {
	Backend = backend
}
func (isti *TŽičanavezaOkvirhandler) Getbackend() TŽičanavezaOkvirprovider {
	return Backend
}
func (isti *TŽičanavezaOkvirhandler) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, величина int) bool {
	žičanavezaКонзола.MŠtampaj(([]byte)("OnEtherFrameReceived"))
	return false
}
func (isti *TŽičanavezaOkvirhandler) Пошаљи(odredištemacbe uint64, dataPokazivač uintptr, величина uint32) {
	Backend.OkvirПошаљи(odredištemacbe, okvir.žičanavezaВрстаbe, dataPokazivač, величина)
}
func (isti *TŽičanavezaOkvirhandler) OkvirПошаљи(odredištemacbe uint64, žičanavezaВрстаbe uint16, dataPokazivač uintptr, величина uint32) {
	Backend.OkvirПошаљи(odredištemacbe, žičanavezaВрстаbe, dataPokazivač, величина)
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
func (isti *TŽičanavezaOkvirrawdatahandler) Narawdatareceive(dataPokazivač uintptr, величина int) bool {
	return provider.Narawdatareceive(dataPokazivač, величина)
}
func (isti *TŽičanavezaOkvirrawdatahandler) Пошаљи(dataPokazivač uintptr, величина uint32) {
	provider.Пошаљи(dataPokazivač, величина)
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
	мрежаcard	Tamdam79c973
	handler_2	[65565]IŽičanavezaOkvirhandler
}

func (isti *TŽičanavezaOkvirprovider) Init(backend Tamdam79c973) {

	isti.мрежаcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		isti.handler_2[i] = nil
	}
}

var count uint16 = 0

func (isti *TŽičanavezaOkvirprovider) Narawdatareceive(dataPokazivač uintptr, величина int) bool {

	var buffer_2 *TŽičanavezaOkvirheaderbuffer = (*TŽičanavezaOkvirheaderbuffer)(Pointer(dataPokazivač))
	var okvir TŽičanavezaOkvirheader = TŽičanavezaOkvirheader{}
	okvir.Init(*buffer_2)
	var reply bool = false

	if okvir.odredištemacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(okvir.odredištemacbe) == isti.Getmacaddress() {
		if handler_2[okvir.žičanavezaВрстаbe] != nil {
			žičanavezaКонзола.MŠtampaj(([]byte)("provider\n"))

			var pokazivač uintptr = uintptr(Pointer(dataPokazivač)) + uintptr(okvirheaderВеличина)
			reply = handler_2[okvir.žičanavezaВрстаbe].ŽičanavezaOkvirreceivewhen(pokazivač, величина-okvirheaderВеличина)

		}
	}

	if reply {
		okvir.odredištemacbe = okvir.izvormacbe
		okvir.izvormacbe = Unsignedinteger48r(isti.Getmacaddress())
		okvir.Скупbuffer(buffer_2)

	}

	žičanavezaКонзола.MŠtampajxy(([]byte)("spro["), 0, 1)
	žičanavezaКонзола.MUnsignedinteger64Štampaj(okvir.izvormacbe)
	žičanavezaКонзола.MŠtampaj(([]byte)(":"))
	žičanavezaКонзола.MUnsignedinteger64Štampaj(okvir.odredištemacbe)
	žičanavezaКонзола.MŠtampaj(([]byte)(":]["))
	žičanavezaКонзола.MUnsignedinteger64Štampaj(isti.Getmacaddress())
	žičanavezaКонзола.MŠtampaj(([]byte)(":"))
	žičanavezaКонзола.MUnsignedinteger16Štampaj(okvir.žičanavezaВрстаbe)
	žičanavezaКонзола.MŠtampaj(([]byte)("]"))

	return reply

}
func (isti *TŽičanavezaOkvirprovider) Пошаљи(dataPokazivač uintptr, величина uint32) {
	isti.мрежаcard.Пошаљи(dataPokazivač, величина)
}
func (isti *TŽičanavezaOkvirprovider) OkvirПошаљи(odredištemacbe uint64, žičanavezaВрстаbe uint16, dataPokazivač uintptr, величина uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TŽičanavezaOkvirheaderbuffer = (*TŽičanavezaOkvirheaderbuffer)(Pointer(&buffer2_2))

	var okvir TŽičanavezaOkvirheader = TŽičanavezaOkvirheader{}
	okvir.Init(*buffer_2)

	okvir.odredištemacbe = Unsignedinteger48r(odredištemacbe)
	okvir.izvormacbe = Unsignedinteger48r(isti.мрежаcard.Getmacaddress())
	okvir.žičanavezaВрстаbe = Unsignedinteger16r(žičanavezaВрстаbe)

	okvir.Скупbuffer(buffer_2)
	var izvor_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))

	var i uint32 = 0
	for i = 0; i < величина; i++ {
		buffer2_2[uint32(okvirheaderВеличина)+i] = izvor_2[i]

	}

	var pokazivač uintptr = uintptr(Pointer(&buffer2_2))

	isti.мрежаcard.Пошаљи(pokazivač, величина+uint32(okvirheaderВеличина))

}
func (isti *TŽičanavezaOkvirprovider) Getmacaddress() uint64 {
	return isti.мрежаcard.Getmacaddress()
}
func (isti *TŽičanavezaOkvirprovider) Getipaddress() uint64 {
	return isti.мрежаcard.Getipaddress()
}
