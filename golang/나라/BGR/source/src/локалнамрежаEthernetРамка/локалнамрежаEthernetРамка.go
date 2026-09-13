package локалнамрежаEthernetРамка

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var локалнамрежаEthernetconsole TConsole = TConsole{}

type TЛокалнамрежаEthernetРамкаheaderbuffer struct {
	назначениеmacbe			[6]byte
	източникmacbe			[6]byte
	локалнамрежаEthernetТипbe	[2]byte
}

var рамкаheaderРазмер int = 14

type TЛокалнамрежаEthernetРамкаheader struct {
	назначениеmacbe			uint64
	източникmacbe			uint64
	локалнамрежаEthernetТипbe	uint16
}

func (себеси *TЛокалнамрежаEthernetРамкаheader) Init(buffer_2 TЛокалнамрежаEthernetРамкаheaderbuffer) {
	себеси.назначениеmacbe = (Масивtounsignedinteger48(buffer_2.назначениеmacbe))
	себеси.източникmacbe = (Масивtounsignedinteger48(buffer_2.източникmacbe))
	себеси.локалнамрежаEthernetТипbe = (Масивtounsignedinteger16(buffer_2.локалнамрежаEthernetТипbe))

}
func (себеси *TЛокалнамрежаEthernetРамкаheader) Задайbuffer(buffer_2 *TЛокалнамрежаEthernetРамкаheaderbuffer) {
	buffer_2.назначениеmacbe = Unsignedinteger48toМасив(Unsignedinteger48r(себеси.назначениеmacbe))
	buffer_2.източникmacbe = Unsignedinteger48toМасив(Unsignedinteger48r(себеси.източникmacbe))
	buffer_2.локалнамрежаEthernetТипbe = Unsignedinteger16toМасив(Unsignedinteger16r(себеси.локалнамрежаEthernetТипbe))
}

type IЛокалнамрежаEthernetРамкаhandler interface {
	Init(backend TЛокалнамрежаEthernetРамкаprovider)
	Задайhandler(handler IЛокалнамрежаEthernetРамкаhandler, локалнамрежаEthernetТип uint16)
	ЛокалнамрежаEthernetРамкаreceivewhen(dataПоказалци uintptr, размер int) bool
	Изпращане(назначениеmacbe uint64, dataПоказалци uintptr, размер uint32)
	РамкаИзпращане(назначениеmacbe uint64, локалнамрежаEthernetТипbe uint16, dataПоказалци uintptr, размер uint32)
	Providerget() TЛокалнамрежаEthernetРамкаprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TЛокалнамрежаEthernetРамкаhandler struct {
}

var рамка TЛокалнамрежаEthernetРамкаheader
var Backend TЛокалнамрежаEthernetРамкаprovider
var handler_2 [65535]IЛокалнамрежаEthernetРамкаhandler
var efhandler *TЛокалнамрежаEthernetРамкаhandler = nil

func (себеси *TЛокалнамрежаEthernetРамкаhandler) Init(backend TЛокалнамрежаEthernetРамкаprovider) {
	Backend = backend
}

func (себеси *TЛокалнамрежаEthernetРамкаhandler) Задайhandler(handler IЛокалнамрежаEthernetРамкаhandler, pЛокалнамрежаEthernetТип uint16) {
	handler_2[pЛокалнамрежаEthernetТип] = handler
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) Задайbackend(backend TЛокалнамрежаEthernetРамкаprovider) {
	Backend = backend
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) Getbackend() TЛокалнамрежаEthernetРамкаprovider {
	return Backend
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) ЛокалнамрежаEthernetРамкаreceivewhen(dataПоказалци uintptr, размер int) bool {
	локалнамрежаEthernetconsole.MПечат(([]byte)("OnEtherFrameReceived"))
	return false
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) Изпращане(назначениеmacbe uint64, dataПоказалци uintptr, размер uint32) {
	Backend.РамкаИзпращане(назначениеmacbe, рамка.локалнамрежаEthernetТипbe, dataПоказалци, размер)
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) РамкаИзпращане(назначениеmacbe uint64, локалнамрежаEthernetТипbe uint16, dataПоказалци uintptr, размер uint32) {
	Backend.РамкаИзпращане(назначениеmacbe, локалнамрежаEthernetТипbe, dataПоказалци, размер)
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (себеси *TЛокалнамрежаEthernetРамкаhandler) Providerget() TЛокалнамрежаEthernetРамкаprovider {
	return Backend
}

type TЛокалнамрежаEthernetРамкаrawdatahandler struct {
	TRawdatahandler
}

var provider TЛокалнамрежаEthernetРамкаprovider

func (себеси *TЛокалнамрежаEthernetРамкаrawdatahandler) Init(pprovider TЛокалнамрежаEthernetРамкаprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (себеси *TЛокалнамрежаEthernetРамкаrawdatahandler) Вклrawdatareceive(dataПоказалци uintptr, размер int) bool {
	return provider.Вклrawdatareceive(dataПоказалци, размер)
}
func (себеси *TЛокалнамрежаEthernetРамкаrawdatahandler) Изпращане(dataПоказалци uintptr, размер uint32) {
	provider.Изпращане(dataПоказалци, размер)
}
func (себеси *TЛокалнамрежаEthernetРамкаrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (себеси *TЛокалнамрежаEthernetРамкаrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (себеси *TЛокалнамрежаEthernetРамкаrawdatahandler) Providerget() TЛокалнамрежаEthernetРамкаprovider {
	return provider
}

type TЛокалнамрежаEthernetРамкаprovider struct {
	мрежаКарти	Tamdam79c973
	handler_2	[65565]IЛокалнамрежаEthernetРамкаhandler
}

func (себеси *TЛокалнамрежаEthernetРамкаprovider) Init(backend Tamdam79c973) {

	себеси.мрежаКарти = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		себеси.handler_2[i] = nil
	}
}

var count uint16 = 0

func (себеси *TЛокалнамрежаEthernetРамкаprovider) Вклrawdatareceive(dataПоказалци uintptr, размер int) bool {

	var buffer_2 *TЛокалнамрежаEthernetРамкаheaderbuffer = (*TЛокалнамрежаEthernetРамкаheaderbuffer)(Pointer(dataПоказалци))
	var рамка TЛокалнамрежаEthernetРамкаheader = TЛокалнамрежаEthernetРамкаheader{}
	рамка.Init(*buffer_2)
	var reply bool = false

	if рамка.назначениеmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(рамка.назначениеmacbe) == себеси.Getmacaddress() {
		if handler_2[рамка.локалнамрежаEthernetТипbe] != nil {
			локалнамрежаEthernetconsole.MПечат(([]byte)("provider\n"))

			var показалци uintptr = uintptr(Pointer(dataПоказалци)) + uintptr(рамкаheaderРазмер)
			reply = handler_2[рамка.локалнамрежаEthernetТипbe].ЛокалнамрежаEthernetРамкаreceivewhen(показалци, размер-рамкаheaderРазмер)

		}
	}

	if reply {
		рамка.назначениеmacbe = рамка.източникmacbe
		рамка.източникmacbe = Unsignedinteger48r(себеси.Getmacaddress())
		рамка.Задайbuffer(buffer_2)

	}

	локалнамрежаEthernetconsole.MПечатxy(([]byte)("spro["), 0, 1)
	локалнамрежаEthernetconsole.MUnsignedinteger64Печат(рамка.източникmacbe)
	локалнамрежаEthernetconsole.MПечат(([]byte)(":"))
	локалнамрежаEthernetconsole.MUnsignedinteger64Печат(рамка.назначениеmacbe)
	локалнамрежаEthernetconsole.MПечат(([]byte)(":]["))
	локалнамрежаEthernetconsole.MUnsignedinteger64Печат(себеси.Getmacaddress())
	локалнамрежаEthernetconsole.MПечат(([]byte)(":"))
	локалнамрежаEthernetconsole.MUnsignedinteger16Печат(рамка.локалнамрежаEthernetТипbe)
	локалнамрежаEthernetconsole.MПечат(([]byte)("]"))

	return reply

}
func (себеси *TЛокалнамрежаEthernetРамкаprovider) Изпращане(dataПоказалци uintptr, размер uint32) {
	себеси.мрежаКарти.Изпращане(dataПоказалци, размер)
}
func (себеси *TЛокалнамрежаEthernetРамкаprovider) РамкаИзпращане(назначениеmacbe uint64, локалнамрежаEthernetТипbe uint16, dataПоказалци uintptr, размер uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TЛокалнамрежаEthernetРамкаheaderbuffer = (*TЛокалнамрежаEthernetРамкаheaderbuffer)(Pointer(&buffer2_2))

	var рамка TЛокалнамрежаEthernetРамкаheader = TЛокалнамрежаEthernetРамкаheader{}
	рамка.Init(*buffer_2)

	рамка.назначениеmacbe = Unsignedinteger48r(назначениеmacbe)
	рамка.източникmacbe = Unsignedinteger48r(себеси.мрежаКарти.Getmacaddress())
	рамка.локалнамрежаEthernetТипbe = Unsignedinteger16r(локалнамрежаEthernetТипbe)

	рамка.Задайbuffer(buffer_2)
	var източник_2 [4096]byte = *(*([4096]byte))(Pointer(dataПоказалци))

	var i uint32 = 0
	for i = 0; i < размер; i++ {
		buffer2_2[uint32(рамкаheaderРазмер)+i] = източник_2[i]

	}

	var показалци uintptr = uintptr(Pointer(&buffer2_2))

	себеси.мрежаКарти.Изпращане(показалци, размер+uint32(рамкаheaderРазмер))

}
func (себеси *TЛокалнамрежаEthernetРамкаprovider) Getmacaddress() uint64 {
	return себеси.мрежаКарти.Getmacaddress()
}
func (себеси *TЛокалнамрежаEthernetРамкаprovider) Getipaddress() uint64 {
	return себеси.мрежаКарти.Getipaddress()
}
