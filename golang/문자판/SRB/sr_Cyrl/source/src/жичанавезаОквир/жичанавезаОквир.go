package жичанавезаОквир

import . "конзола"

import . "amdam79c973"
import . "unsafe"
import . "util"

var жичанавезаКонзола TКонзола = TКонзола{}

type TЖичанавезаОквирheaderbuffer struct {
	одредиштеmacbe		[6]byte
	изворmacbe		[6]byte
	жичанавезаВрстаbe	[2]byte
}

var оквирheaderВеличина int = 14

type TЖичанавезаОквирheader struct {
	одредиштеmacbe		uint64
	изворmacbe		uint64
	жичанавезаВрстаbe	uint16
}

func (исти *TЖичанавезаОквирheader) Init(buffer_2 TЖичанавезаОквирheaderbuffer) {
	исти.одредиштеmacbe = (Низtounsignedinteger48(buffer_2.одредиштеmacbe))
	исти.изворmacbe = (Низtounsignedinteger48(buffer_2.изворmacbe))
	исти.жичанавезаВрстаbe = (Низtounsignedinteger16(buffer_2.жичанавезаВрстаbe))

}
func (исти *TЖичанавезаОквирheader) Скупbuffer(buffer_2 *TЖичанавезаОквирheaderbuffer) {
	buffer_2.одредиштеmacbe = Unsignedinteger48toНиз(Unsignedinteger48r(исти.одредиштеmacbe))
	buffer_2.изворmacbe = Unsignedinteger48toНиз(Unsignedinteger48r(исти.изворmacbe))
	buffer_2.жичанавезаВрстаbe = Unsignedinteger16toНиз(Unsignedinteger16r(исти.жичанавезаВрстаbe))
}

type IЖичанавезаОквирhandler interface {
	Init(backend TЖичанавезаОквирprovider)
	Скупhandler(handler IЖичанавезаОквирhandler, жичанавезаВрста uint16)
	ЖичанавезаОквирreceivewhen(dataПоказивач uintptr, величина int) bool
	Пошаљи(одредиштеmacbe uint64, dataПоказивач uintptr, величина uint32)
	ОквирПошаљи(одредиштеmacbe uint64, жичанавезаВрстаbe uint16, dataПоказивач uintptr, величина uint32)
	Providerget() TЖичанавезаОквирprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TЖичанавезаОквирhandler struct {
}

var оквир TЖичанавезаОквирheader
var Backend TЖичанавезаОквирprovider
var handler_2 [65535]IЖичанавезаОквирhandler
var efhandler *TЖичанавезаОквирhandler = nil

func (исти *TЖичанавезаОквирhandler) Init(backend TЖичанавезаОквирprovider) {
	Backend = backend
}

func (исти *TЖичанавезаОквирhandler) Скупhandler(handler IЖичанавезаОквирhandler, pЖичанавезаВрста uint16) {
	handler_2[pЖичанавезаВрста] = handler
}
func (исти *TЖичанавезаОквирhandler) Скупbackend(backend TЖичанавезаОквирprovider) {
	Backend = backend
}
func (исти *TЖичанавезаОквирhandler) Getbackend() TЖичанавезаОквирprovider {
	return Backend
}
func (исти *TЖичанавезаОквирhandler) ЖичанавезаОквирreceivewhen(dataПоказивач uintptr, величина int) bool {
	жичанавезаКонзола.MШтампај(([]byte)("OnEtherFrameReceived"))
	return false
}
func (исти *TЖичанавезаОквирhandler) Пошаљи(одредиштеmacbe uint64, dataПоказивач uintptr, величина uint32) {
	Backend.ОквирПошаљи(одредиштеmacbe, оквир.жичанавезаВрстаbe, dataПоказивач, величина)
}
func (исти *TЖичанавезаОквирhandler) ОквирПошаљи(одредиштеmacbe uint64, жичанавезаВрстаbe uint16, dataПоказивач uintptr, величина uint32) {
	Backend.ОквирПошаљи(одредиштеmacbe, жичанавезаВрстаbe, dataПоказивач, величина)
}
func (исти *TЖичанавезаОквирhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (исти *TЖичанавезаОквирhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (исти *TЖичанавезаОквирhandler) Providerget() TЖичанавезаОквирprovider {
	return Backend
}

type TЖичанавезаОквирrawdatahandler struct {
	TRawdatahandler
}

var provider TЖичанавезаОквирprovider

func (исти *TЖичанавезаОквирrawdatahandler) Init(pprovider TЖичанавезаОквирprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (исти *TЖичанавезаОквирrawdatahandler) Наrawdatareceive(dataПоказивач uintptr, величина int) bool {
	return provider.Наrawdatareceive(dataПоказивач, величина)
}
func (исти *TЖичанавезаОквирrawdatahandler) Пошаљи(dataПоказивач uintptr, величина uint32) {
	provider.Пошаљи(dataПоказивач, величина)
}
func (исти *TЖичанавезаОквирrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (исти *TЖичанавезаОквирrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (исти *TЖичанавезаОквирrawdatahandler) Providerget() TЖичанавезаОквирprovider {
	return provider
}

type TЖичанавезаОквирprovider struct {
	мрежаcard	Tamdam79c973
	handler_2	[65565]IЖичанавезаОквирhandler
}

func (исти *TЖичанавезаОквирprovider) Init(backend Tamdam79c973) {

	исти.мрежаcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		исти.handler_2[i] = nil
	}
}

var count uint16 = 0

func (исти *TЖичанавезаОквирprovider) Наrawdatareceive(dataПоказивач uintptr, величина int) bool {

	var buffer_2 *TЖичанавезаОквирheaderbuffer = (*TЖичанавезаОквирheaderbuffer)(Pointer(dataПоказивач))
	var оквир TЖичанавезаОквирheader = TЖичанавезаОквирheader{}
	оквир.Init(*buffer_2)
	var reply bool = false

	if оквир.одредиштеmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(оквир.одредиштеmacbe) == исти.Getmacaddress() {
		if handler_2[оквир.жичанавезаВрстаbe] != nil {
			жичанавезаКонзола.MШтампај(([]byte)("provider\n"))

			var показивач uintptr = uintptr(Pointer(dataПоказивач)) + uintptr(оквирheaderВеличина)
			reply = handler_2[оквир.жичанавезаВрстаbe].ЖичанавезаОквирreceivewhen(показивач, величина-оквирheaderВеличина)

		}
	}

	if reply {
		оквир.одредиштеmacbe = оквир.изворmacbe
		оквир.изворmacbe = Unsignedinteger48r(исти.Getmacaddress())
		оквир.Скупbuffer(buffer_2)

	}

	жичанавезаКонзола.MШтампајxy(([]byte)("spro["), 0, 1)
	жичанавезаКонзола.MUnsignedinteger64Штампај(оквир.изворmacbe)
	жичанавезаКонзола.MШтампај(([]byte)(":"))
	жичанавезаКонзола.MUnsignedinteger64Штампај(оквир.одредиштеmacbe)
	жичанавезаКонзола.MШтампај(([]byte)(":]["))
	жичанавезаКонзола.MUnsignedinteger64Штампај(исти.Getmacaddress())
	жичанавезаКонзола.MШтампај(([]byte)(":"))
	жичанавезаКонзола.MUnsignedinteger16Штампај(оквир.жичанавезаВрстаbe)
	жичанавезаКонзола.MШтампај(([]byte)("]"))

	return reply

}
func (исти *TЖичанавезаОквирprovider) Пошаљи(dataПоказивач uintptr, величина uint32) {
	исти.мрежаcard.Пошаљи(dataПоказивач, величина)
}
func (исти *TЖичанавезаОквирprovider) ОквирПошаљи(одредиштеmacbe uint64, жичанавезаВрстаbe uint16, dataПоказивач uintptr, величина uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TЖичанавезаОквирheaderbuffer = (*TЖичанавезаОквирheaderbuffer)(Pointer(&buffer2_2))

	var оквир TЖичанавезаОквирheader = TЖичанавезаОквирheader{}
	оквир.Init(*buffer_2)

	оквир.одредиштеmacbe = Unsignedinteger48r(одредиштеmacbe)
	оквир.изворmacbe = Unsignedinteger48r(исти.мрежаcard.Getmacaddress())
	оквир.жичанавезаВрстаbe = Unsignedinteger16r(жичанавезаВрстаbe)

	оквир.Скупbuffer(buffer_2)
	var извор_2 [4096]byte = *(*([4096]byte))(Pointer(dataПоказивач))

	var i uint32 = 0
	for i = 0; i < величина; i++ {
		buffer2_2[uint32(оквирheaderВеличина)+i] = извор_2[i]

	}

	var показивач uintptr = uintptr(Pointer(&buffer2_2))

	исти.мрежаcard.Пошаљи(показивач, величина+uint32(оквирheaderВеличина))

}
func (исти *TЖичанавезаОквирprovider) Getmacaddress() uint64 {
	return исти.мрежаcard.Getmacaddress()
}
func (исти *TЖичанавезаОквирprovider) Getipaddress() uint64 {
	return исти.мрежаcard.Getipaddress()
}
