/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package етернетРамка

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var етернетconsole TConsole = TConsole{}

type TЕтернетРамкаheaderbuffer struct {
	одредиштеmacbe	[6]byte
	изворmacbe	[6]byte
	етернетТипbe	[2]byte
}

var рамкаheaderГолемина int = 14

type TЕтернетРамкаheader struct {
	одредиштеmacbe	uint64
	изворmacbe	uint64
	етернетТипbe	uint16
}

func (само *TЕтернетРамкаheader) Init(buffer_2 TЕтернетРамкаheaderbuffer) {
	само.одредиштеmacbe = (Построиtounsignedinteger48(buffer_2.одредиштеmacbe))
	само.изворmacbe = (Построиtounsignedinteger48(buffer_2.изворmacbe))
	само.етернетТипbe = (Построиtounsignedinteger16(buffer_2.етернетТипbe))

}
func (само *TЕтернетРамкаheader) Поставиbuffer(buffer_2 *TЕтернетРамкаheaderbuffer) {
	buffer_2.одредиштеmacbe = Unsignedinteger48toПострои(Unsignedinteger48r(само.одредиштеmacbe))
	buffer_2.изворmacbe = Unsignedinteger48toПострои(Unsignedinteger48r(само.изворmacbe))
	buffer_2.етернетТипbe = Unsignedinteger16toПострои(Unsignedinteger16r(само.етернетТипbe))
}

type IЕтернетРамкаhandler interface {
	Init(backend TЕтернетРамкаprovider)
	Поставиhandler(handler IЕтернетРамкаhandler, етернетТип uint16)
	ЕтернетРамкаreceivewhen(dataСтрелка uintptr, големина int) bool
	Испрати(одредиштеmacbe uint64, dataСтрелка uintptr, големина uint32)
	РамкаИспрати(одредиштеmacbe uint64, етернетТипbe uint16, dataСтрелка uintptr, големина uint32)
	Providerget() TЕтернетРамкаprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TЕтернетРамкаhandler struct {
}

var рамка TЕтернетРамкаheader
var Backend TЕтернетРамкаprovider
var handler_2 [65535]IЕтернетРамкаhandler
var efhandler *TЕтернетРамкаhandler = nil

func (само *TЕтернетРамкаhandler) Init(backend TЕтернетРамкаprovider) {
	Backend = backend
}

func (само *TЕтернетРамкаhandler) Поставиhandler(handler IЕтернетРамкаhandler, pЕтернетТип uint16) {
	handler_2[pЕтернетТип] = handler
}
func (само *TЕтернетРамкаhandler) Поставиbackend(backend TЕтернетРамкаprovider) {
	Backend = backend
}
func (само *TЕтернетРамкаhandler) Getbackend() TЕтернетРамкаprovider {
	return Backend
}
func (само *TЕтернетРамкаhandler) ЕтернетРамкаreceivewhen(dataСтрелка uintptr, големина int) bool {
	етернетconsole.MПечати(([]byte)("OnEtherFrameReceived"))
	return false
}
func (само *TЕтернетРамкаhandler) Испрати(одредиштеmacbe uint64, dataСтрелка uintptr, големина uint32) {
	Backend.РамкаИспрати(одредиштеmacbe, рамка.етернетТипbe, dataСтрелка, големина)
}
func (само *TЕтернетРамкаhandler) РамкаИспрати(одредиштеmacbe uint64, етернетТипbe uint16, dataСтрелка uintptr, големина uint32) {
	Backend.РамкаИспрати(одредиштеmacbe, етернетТипbe, dataСтрелка, големина)
}
func (само *TЕтернетРамкаhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (само *TЕтернетРамкаhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (само *TЕтернетРамкаhandler) Providerget() TЕтернетРамкаprovider {
	return Backend
}

type TЕтернетРамкаrawdatahandler struct {
	TRawdatahandler
}

var provider TЕтернетРамкаprovider

func (само *TЕтернетРамкаrawdatahandler) Init(pprovider TЕтернетРамкаprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (само *TЕтернетРамкаrawdatahandler) Вклученоrawdatareceive(dataСтрелка uintptr, големина int) bool {
	return provider.Вклученоrawdatareceive(dataСтрелка, големина)
}
func (само *TЕтернетРамкаrawdatahandler) Испрати(dataСтрелка uintptr, големина uint32) {
	provider.Испрати(dataСтрелка, големина)
}
func (само *TЕтернетРамкаrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (само *TЕтернетРамкаrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (само *TЕтернетРамкаrawdatahandler) Providerget() TЕтернетРамкаprovider {
	return provider
}

type TЕтернетРамкаprovider struct {
	мрежаКарти	Tamdam79c973
	handler_2	[65565]IЕтернетРамкаhandler
}

func (само *TЕтернетРамкаprovider) Init(backend Tamdam79c973) {

	само.мрежаКарти = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		само.handler_2[i] = nil
	}
}

var count uint16 = 0

func (само *TЕтернетРамкаprovider) Вклученоrawdatareceive(dataСтрелка uintptr, големина int) bool {

	var buffer_2 *TЕтернетРамкаheaderbuffer = (*TЕтернетРамкаheaderbuffer)(Pointer(dataСтрелка))
	var рамка TЕтернетРамкаheader = TЕтернетРамкаheader{}
	рамка.Init(*buffer_2)
	var reply bool = false

	if рамка.одредиштеmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(рамка.одредиштеmacbe) == само.Getmacaddress() {
		if handler_2[рамка.етернетТипbe] != nil {
			етернетconsole.MПечати(([]byte)("provider\n"))

			var стрелка uintptr = uintptr(Pointer(dataСтрелка)) + uintptr(рамкаheaderГолемина)
			reply = handler_2[рамка.етернетТипbe].ЕтернетРамкаreceivewhen(стрелка, големина-рамкаheaderГолемина)

		}
	}

	if reply {
		рамка.одредиштеmacbe = рамка.изворmacbe
		рамка.изворmacbe = Unsignedinteger48r(само.Getmacaddress())
		рамка.Поставиbuffer(buffer_2)

	}

	етернетconsole.MПечатиxy(([]byte)("spro["), 0, 1)
	етернетconsole.MUnsignedinteger64Печати(рамка.изворmacbe)
	етернетconsole.MПечати(([]byte)(":"))
	етернетconsole.MUnsignedinteger64Печати(рамка.одредиштеmacbe)
	етернетconsole.MПечати(([]byte)(":]["))
	етернетconsole.MUnsignedinteger64Печати(само.Getmacaddress())
	етернетconsole.MПечати(([]byte)(":"))
	етернетconsole.MUnsignedinteger16Печати(рамка.етернетТипbe)
	етернетconsole.MПечати(([]byte)("]"))

	return reply

}
func (само *TЕтернетРамкаprovider) Испрати(dataСтрелка uintptr, големина uint32) {
	само.мрежаКарти.Испрати(dataСтрелка, големина)
}
func (само *TЕтернетРамкаprovider) РамкаИспрати(одредиштеmacbe uint64, етернетТипbe uint16, dataСтрелка uintptr, големина uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TЕтернетРамкаheaderbuffer = (*TЕтернетРамкаheaderbuffer)(Pointer(&buffer2_2))

	var рамка TЕтернетРамкаheader = TЕтернетРамкаheader{}
	рамка.Init(*buffer_2)

	рамка.одредиштеmacbe = Unsignedinteger48r(одредиштеmacbe)
	рамка.изворmacbe = Unsignedinteger48r(само.мрежаКарти.Getmacaddress())
	рамка.етернетТипbe = Unsignedinteger16r(етернетТипbe)

	рамка.Поставиbuffer(buffer_2)
	var извор_2 [4096]byte = *(*([4096]byte))(Pointer(dataСтрелка))

	var i uint32 = 0
	for i = 0; i < големина; i++ {
		buffer2_2[uint32(рамкаheaderГолемина)+i] = извор_2[i]

	}

	var стрелка uintptr = uintptr(Pointer(&buffer2_2))

	само.мрежаКарти.Испрати(стрелка, големина+uint32(рамкаheaderГолемина))

}
func (само *TЕтернетРамкаprovider) Getmacaddress() uint64 {
	return само.мрежаКарти.Getmacaddress()
}
func (само *TЕтернетРамкаprovider) Getipaddress() uint64 {
	return само.мрежаКарти.Getipaddress()
}
