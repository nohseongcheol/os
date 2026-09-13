package ethernetCadru

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetCadruheaderbuffer struct {
	destinațiemacbe	[6]byte
	sursămacbe	[6]byte
	ethernetTipbe	[2]byte
}

var cadruheaderMărime int = 14

type TEthernetCadruheader struct {
	destinațiemacbe	uint64
	sursămacbe	uint64
	ethernetTipbe	uint16
}

func (sine *TEthernetCadruheader) Init(buffer_2 TEthernetCadruheaderbuffer) {
	sine.destinațiemacbe = (Vectortounsignedinteger48(buffer_2.destinațiemacbe))
	sine.sursămacbe = (Vectortounsignedinteger48(buffer_2.sursămacbe))
	sine.ethernetTipbe = (Vectortounsignedinteger16(buffer_2.ethernetTipbe))

}
func (sine *TEthernetCadruheader) Definitbuffer(buffer_2 *TEthernetCadruheaderbuffer) {
	buffer_2.destinațiemacbe = Unsignedinteger48toVector(Unsignedinteger48r(sine.destinațiemacbe))
	buffer_2.sursămacbe = Unsignedinteger48toVector(Unsignedinteger48r(sine.sursămacbe))
	buffer_2.ethernetTipbe = Unsignedinteger16toVector(Unsignedinteger16r(sine.ethernetTipbe))
}

type IEthernetCadruhandler interface {
	Init(backend TEthernetCadruprovider)
	Definithandler(handler IEthernetCadruhandler, ethernetTip uint16)
	EthernetCadrureceivewhen(dataIndicator uintptr, mărime int) bool
	Trimite(destinațiemacbe uint64, dataIndicator uintptr, mărime uint32)
	CadruTrimite(destinațiemacbe uint64, ethernetTipbe uint16, dataIndicator uintptr, mărime uint32)
	Providerget() TEthernetCadruprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetCadruhandler struct {
}

var cadru TEthernetCadruheader
var Backend TEthernetCadruprovider
var handler_2 [65535]IEthernetCadruhandler
var efhandler *TEthernetCadruhandler = nil

func (sine *TEthernetCadruhandler) Init(backend TEthernetCadruprovider) {
	Backend = backend
}

func (sine *TEthernetCadruhandler) Definithandler(handler IEthernetCadruhandler, pethernetTip uint16) {
	handler_2[pethernetTip] = handler
}
func (sine *TEthernetCadruhandler) Definitbackend(backend TEthernetCadruprovider) {
	Backend = backend
}
func (sine *TEthernetCadruhandler) Getbackend() TEthernetCadruprovider {
	return Backend
}
func (sine *TEthernetCadruhandler) EthernetCadrureceivewhen(dataIndicator uintptr, mărime int) bool {
	ethernetconsole.MTipărește(([]byte)("OnEtherFrameReceived"))
	return false
}
func (sine *TEthernetCadruhandler) Trimite(destinațiemacbe uint64, dataIndicator uintptr, mărime uint32) {
	Backend.CadruTrimite(destinațiemacbe, cadru.ethernetTipbe, dataIndicator, mărime)
}
func (sine *TEthernetCadruhandler) CadruTrimite(destinațiemacbe uint64, ethernetTipbe uint16, dataIndicator uintptr, mărime uint32) {
	Backend.CadruTrimite(destinațiemacbe, ethernetTipbe, dataIndicator, mărime)
}
func (sine *TEthernetCadruhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (sine *TEthernetCadruhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (sine *TEthernetCadruhandler) Providerget() TEthernetCadruprovider {
	return Backend
}

type TEthernetCadrurawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetCadruprovider

func (sine *TEthernetCadrurawdatahandler) Init(pprovider TEthernetCadruprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (sine *TEthernetCadrurawdatahandler) Pornitrawdatareceive(dataIndicator uintptr, mărime int) bool {
	return provider.Pornitrawdatareceive(dataIndicator, mărime)
}
func (sine *TEthernetCadrurawdatahandler) Trimite(dataIndicator uintptr, mărime uint32) {
	provider.Trimite(dataIndicator, mărime)
}
func (sine *TEthernetCadrurawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (sine *TEthernetCadrurawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (sine *TEthernetCadrurawdatahandler) Providerget() TEthernetCadruprovider {
	return provider
}

type TEthernetCadruprovider struct {
	rețeaCărți	Tamdam79c973
	handler_2	[65565]IEthernetCadruhandler
}

func (sine *TEthernetCadruprovider) Init(backend Tamdam79c973) {

	sine.rețeaCărți = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		sine.handler_2[i] = nil
	}
}

var count uint16 = 0

func (sine *TEthernetCadruprovider) Pornitrawdatareceive(dataIndicator uintptr, mărime int) bool {

	var buffer_2 *TEthernetCadruheaderbuffer = (*TEthernetCadruheaderbuffer)(Pointer(dataIndicator))
	var cadru TEthernetCadruheader = TEthernetCadruheader{}
	cadru.Init(*buffer_2)
	var reply bool = false

	if cadru.destinațiemacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(cadru.destinațiemacbe) == sine.Getmacaddress() {
		if handler_2[cadru.ethernetTipbe] != nil {
			ethernetconsole.MTipărește(([]byte)("provider\n"))

			var indicator uintptr = uintptr(Pointer(dataIndicator)) + uintptr(cadruheaderMărime)
			reply = handler_2[cadru.ethernetTipbe].EthernetCadrureceivewhen(indicator, mărime-cadruheaderMărime)

		}
	}

	if reply {
		cadru.destinațiemacbe = cadru.sursămacbe
		cadru.sursămacbe = Unsignedinteger48r(sine.Getmacaddress())
		cadru.Definitbuffer(buffer_2)

	}

	ethernetconsole.MTipăreștexy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Tipărește(cadru.sursămacbe)
	ethernetconsole.MTipărește(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Tipărește(cadru.destinațiemacbe)
	ethernetconsole.MTipărește(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Tipărește(sine.Getmacaddress())
	ethernetconsole.MTipărește(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Tipărește(cadru.ethernetTipbe)
	ethernetconsole.MTipărește(([]byte)("]"))

	return reply

}
func (sine *TEthernetCadruprovider) Trimite(dataIndicator uintptr, mărime uint32) {
	sine.rețeaCărți.Trimite(dataIndicator, mărime)
}
func (sine *TEthernetCadruprovider) CadruTrimite(destinațiemacbe uint64, ethernetTipbe uint16, dataIndicator uintptr, mărime uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetCadruheaderbuffer = (*TEthernetCadruheaderbuffer)(Pointer(&buffer2_2))

	var cadru TEthernetCadruheader = TEthernetCadruheader{}
	cadru.Init(*buffer_2)

	cadru.destinațiemacbe = Unsignedinteger48r(destinațiemacbe)
	cadru.sursămacbe = Unsignedinteger48r(sine.rețeaCărți.Getmacaddress())
	cadru.ethernetTipbe = Unsignedinteger16r(ethernetTipbe)

	cadru.Definitbuffer(buffer_2)
	var sursă_2 [4096]byte = *(*([4096]byte))(Pointer(dataIndicator))

	var i uint32 = 0
	for i = 0; i < mărime; i++ {
		buffer2_2[uint32(cadruheaderMărime)+i] = sursă_2[i]

	}

	var indicator uintptr = uintptr(Pointer(&buffer2_2))

	sine.rețeaCărți.Trimite(indicator, mărime+uint32(cadruheaderMărime))

}
func (sine *TEthernetCadruprovider) Getmacaddress() uint64 {
	return sine.rețeaCărți.Getmacaddress()
}
func (sine *TEthernetCadruprovider) Getipaddress() uint64 {
	return sine.rețeaCărți.Getipaddress()
}
