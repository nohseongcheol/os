package ethernetRaam

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetRaamheaderbuffer struct {
	sihtfailmacbe	[6]byte
	aLLIKASmacbe	[6]byte
	ethernetLiikbe	[2]byte
}

var raamheaderSuurus int = 14

type TEthernetRaamheader struct {
	sihtfailmacbe	uint64
	aLLIKASmacbe	uint64
	ethernetLiikbe	uint16
}

func (ise *TEthernetRaamheader) Init(buffer_2 TEthernetRaamheaderbuffer) {
	ise.sihtfailmacbe = (Massiivtounsignedinteger48(buffer_2.sihtfailmacbe))
	ise.aLLIKASmacbe = (Massiivtounsignedinteger48(buffer_2.aLLIKASmacbe))
	ise.ethernetLiikbe = (Massiivtounsignedinteger16(buffer_2.ethernetLiikbe))

}
func (ise *TEthernetRaamheader) Määrabuffer(buffer_2 *TEthernetRaamheaderbuffer) {
	buffer_2.sihtfailmacbe = Unsignedinteger48toMassiiv(Unsignedinteger48r(ise.sihtfailmacbe))
	buffer_2.aLLIKASmacbe = Unsignedinteger48toMassiiv(Unsignedinteger48r(ise.aLLIKASmacbe))
	buffer_2.ethernetLiikbe = Unsignedinteger16toMassiiv(Unsignedinteger16r(ise.ethernetLiikbe))
}

type IEthernetRaamhandler interface {
	Init(backend TEthernetRaamprovider)
	Määrahandler(handler IEthernetRaamhandler, ethernetLiik uint16)
	EthernetRaamreceivewhen(dataKursor uintptr, suurus int) bool
	Saada(sihtfailmacbe uint64, dataKursor uintptr, suurus uint32)
	RaamSaada(sihtfailmacbe uint64, ethernetLiikbe uint16, dataKursor uintptr, suurus uint32)
	Providerget() TEthernetRaamprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRaamhandler struct {
}

var raam TEthernetRaamheader
var Backend TEthernetRaamprovider
var handler_2 [65535]IEthernetRaamhandler
var efhandler *TEthernetRaamhandler = nil

func (ise *TEthernetRaamhandler) Init(backend TEthernetRaamprovider) {
	Backend = backend
}

func (ise *TEthernetRaamhandler) Määrahandler(handler IEthernetRaamhandler, pethernetLiik uint16) {
	handler_2[pethernetLiik] = handler
}
func (ise *TEthernetRaamhandler) Määrabackend(backend TEthernetRaamprovider) {
	Backend = backend
}
func (ise *TEthernetRaamhandler) Getbackend() TEthernetRaamprovider {
	return Backend
}
func (ise *TEthernetRaamhandler) EthernetRaamreceivewhen(dataKursor uintptr, suurus int) bool {
	ethernetconsole.MPrindi(([]byte)("OnEtherFrameReceived"))
	return false
}
func (ise *TEthernetRaamhandler) Saada(sihtfailmacbe uint64, dataKursor uintptr, suurus uint32) {
	Backend.RaamSaada(sihtfailmacbe, raam.ethernetLiikbe, dataKursor, suurus)
}
func (ise *TEthernetRaamhandler) RaamSaada(sihtfailmacbe uint64, ethernetLiikbe uint16, dataKursor uintptr, suurus uint32) {
	Backend.RaamSaada(sihtfailmacbe, ethernetLiikbe, dataKursor, suurus)
}
func (ise *TEthernetRaamhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (ise *TEthernetRaamhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (ise *TEthernetRaamhandler) Providerget() TEthernetRaamprovider {
	return Backend
}

type TEthernetRaamrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetRaamprovider

func (ise *TEthernetRaamrawdatahandler) Init(pprovider TEthernetRaamprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (ise *TEthernetRaamrawdatahandler) Seesrawdatareceive(dataKursor uintptr, suurus int) bool {
	return provider.Seesrawdatareceive(dataKursor, suurus)
}
func (ise *TEthernetRaamrawdatahandler) Saada(dataKursor uintptr, suurus uint32) {
	provider.Saada(dataKursor, suurus)
}
func (ise *TEthernetRaamrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (ise *TEthernetRaamrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (ise *TEthernetRaamrawdatahandler) Providerget() TEthernetRaamprovider {
	return provider
}

type TEthernetRaamprovider struct {
	võrkKaardimängud	Tamdam79c973
	handler_2		[65565]IEthernetRaamhandler
}

func (ise *TEthernetRaamprovider) Init(backend Tamdam79c973) {

	ise.võrkKaardimängud = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		ise.handler_2[i] = nil
	}
}

var count uint16 = 0

func (ise *TEthernetRaamprovider) Seesrawdatareceive(dataKursor uintptr, suurus int) bool {

	var buffer_2 *TEthernetRaamheaderbuffer = (*TEthernetRaamheaderbuffer)(Pointer(dataKursor))
	var raam TEthernetRaamheader = TEthernetRaamheader{}
	raam.Init(*buffer_2)
	var reply bool = false

	if raam.sihtfailmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(raam.sihtfailmacbe) == ise.Getmacaddress() {
		if handler_2[raam.ethernetLiikbe] != nil {
			ethernetconsole.MPrindi(([]byte)("provider\n"))

			var kursor uintptr = uintptr(Pointer(dataKursor)) + uintptr(raamheaderSuurus)
			reply = handler_2[raam.ethernetLiikbe].EthernetRaamreceivewhen(kursor, suurus-raamheaderSuurus)

		}
	}

	if reply {
		raam.sihtfailmacbe = raam.aLLIKASmacbe
		raam.aLLIKASmacbe = Unsignedinteger48r(ise.Getmacaddress())
		raam.Määrabuffer(buffer_2)

	}

	ethernetconsole.MPrindixy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Prindi(raam.aLLIKASmacbe)
	ethernetconsole.MPrindi(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Prindi(raam.sihtfailmacbe)
	ethernetconsole.MPrindi(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Prindi(ise.Getmacaddress())
	ethernetconsole.MPrindi(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Prindi(raam.ethernetLiikbe)
	ethernetconsole.MPrindi(([]byte)("]"))

	return reply

}
func (ise *TEthernetRaamprovider) Saada(dataKursor uintptr, suurus uint32) {
	ise.võrkKaardimängud.Saada(dataKursor, suurus)
}
func (ise *TEthernetRaamprovider) RaamSaada(sihtfailmacbe uint64, ethernetLiikbe uint16, dataKursor uintptr, suurus uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRaamheaderbuffer = (*TEthernetRaamheaderbuffer)(Pointer(&buffer2_2))

	var raam TEthernetRaamheader = TEthernetRaamheader{}
	raam.Init(*buffer_2)

	raam.sihtfailmacbe = Unsignedinteger48r(sihtfailmacbe)
	raam.aLLIKASmacbe = Unsignedinteger48r(ise.võrkKaardimängud.Getmacaddress())
	raam.ethernetLiikbe = Unsignedinteger16r(ethernetLiikbe)

	raam.Määrabuffer(buffer_2)
	var aLLIKAS_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursor))

	var i uint32 = 0
	for i = 0; i < suurus; i++ {
		buffer2_2[uint32(raamheaderSuurus)+i] = aLLIKAS_2[i]

	}

	var kursor uintptr = uintptr(Pointer(&buffer2_2))

	ise.võrkKaardimängud.Saada(kursor, suurus+uint32(raamheaderSuurus))

}
func (ise *TEthernetRaamprovider) Getmacaddress() uint64 {
	return ise.võrkKaardimängud.Getmacaddress()
}
func (ise *TEthernetRaamprovider) Getipaddress() uint64 {
	return ise.võrkKaardimängud.Getipaddress()
}
