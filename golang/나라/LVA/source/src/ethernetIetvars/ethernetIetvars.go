package ethernetIetvars

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetIetvarsheaderbuffer struct {
	mērķismacbe	[6]byte
	avotsmacbe	[6]byte
	ethernetTipsbe	[2]byte
}

var ietvarsheaderIzmērs int = 14

type TEthernetIetvarsheader struct {
	mērķismacbe	uint64
	avotsmacbe	uint64
	ethernetTipsbe	uint16
}

func (pats *TEthernetIetvarsheader) Init(buffer_2 TEthernetIetvarsheaderbuffer) {
	pats.mērķismacbe = (Masīvstounsignedinteger48(buffer_2.mērķismacbe))
	pats.avotsmacbe = (Masīvstounsignedinteger48(buffer_2.avotsmacbe))
	pats.ethernetTipsbe = (Masīvstounsignedinteger16(buffer_2.ethernetTipsbe))

}
func (pats *TEthernetIetvarsheader) Kopabuffer(buffer_2 *TEthernetIetvarsheaderbuffer) {
	buffer_2.mērķismacbe = Unsignedinteger48toMasīvs(Unsignedinteger48r(pats.mērķismacbe))
	buffer_2.avotsmacbe = Unsignedinteger48toMasīvs(Unsignedinteger48r(pats.avotsmacbe))
	buffer_2.ethernetTipsbe = Unsignedinteger16toMasīvs(Unsignedinteger16r(pats.ethernetTipsbe))
}

type IEthernetIetvarshandler interface {
	Init(backend TEthernetIetvarsprovider)
	Kopahandler(handler IEthernetIetvarshandler, ethernetTips uint16)
	EthernetIetvarsreceivewhen(dataKursors uintptr, izmērs int) bool
	Sūtīt(mērķismacbe uint64, dataKursors uintptr, izmērs uint32)
	IetvarsSūtīt(mērķismacbe uint64, ethernetTipsbe uint16, dataKursors uintptr, izmērs uint32)
	Providerget() TEthernetIetvarsprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetIetvarshandler struct {
}

var ietvars TEthernetIetvarsheader
var Backend TEthernetIetvarsprovider
var handler_2 [65535]IEthernetIetvarshandler
var efhandler *TEthernetIetvarshandler = nil

func (pats *TEthernetIetvarshandler) Init(backend TEthernetIetvarsprovider) {
	Backend = backend
}

func (pats *TEthernetIetvarshandler) Kopahandler(handler IEthernetIetvarshandler, pethernetTips uint16) {
	handler_2[pethernetTips] = handler
}
func (pats *TEthernetIetvarshandler) Kopabackend(backend TEthernetIetvarsprovider) {
	Backend = backend
}
func (pats *TEthernetIetvarshandler) Getbackend() TEthernetIetvarsprovider {
	return Backend
}
func (pats *TEthernetIetvarshandler) EthernetIetvarsreceivewhen(dataKursors uintptr, izmērs int) bool {
	ethernetconsole.MDrukāt(([]byte)("OnEtherFrameReceived"))
	return false
}
func (pats *TEthernetIetvarshandler) Sūtīt(mērķismacbe uint64, dataKursors uintptr, izmērs uint32) {
	Backend.IetvarsSūtīt(mērķismacbe, ietvars.ethernetTipsbe, dataKursors, izmērs)
}
func (pats *TEthernetIetvarshandler) IetvarsSūtīt(mērķismacbe uint64, ethernetTipsbe uint16, dataKursors uintptr, izmērs uint32) {
	Backend.IetvarsSūtīt(mērķismacbe, ethernetTipsbe, dataKursors, izmērs)
}
func (pats *TEthernetIetvarshandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (pats *TEthernetIetvarshandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (pats *TEthernetIetvarshandler) Providerget() TEthernetIetvarsprovider {
	return Backend
}

type TEthernetIetvarsrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetIetvarsprovider

func (pats *TEthernetIetvarsrawdatahandler) Init(pprovider TEthernetIetvarsprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (pats *TEthernetIetvarsrawdatahandler) Ieslēgtsrawdatareceive(dataKursors uintptr, izmērs int) bool {
	return provider.Ieslēgtsrawdatareceive(dataKursors, izmērs)
}
func (pats *TEthernetIetvarsrawdatahandler) Sūtīt(dataKursors uintptr, izmērs uint32) {
	provider.Sūtīt(dataKursors, izmērs)
}
func (pats *TEthernetIetvarsrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (pats *TEthernetIetvarsrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (pats *TEthernetIetvarsrawdatahandler) Providerget() TEthernetIetvarsprovider {
	return provider
}

type TEthernetIetvarsprovider struct {
	tīklscard	Tamdam79c973
	handler_2	[65565]IEthernetIetvarshandler
}

func (pats *TEthernetIetvarsprovider) Init(backend Tamdam79c973) {

	pats.tīklscard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		pats.handler_2[i] = nil
	}
}

var count uint16 = 0

func (pats *TEthernetIetvarsprovider) Ieslēgtsrawdatareceive(dataKursors uintptr, izmērs int) bool {

	var buffer_2 *TEthernetIetvarsheaderbuffer = (*TEthernetIetvarsheaderbuffer)(Pointer(dataKursors))
	var ietvars TEthernetIetvarsheader = TEthernetIetvarsheader{}
	ietvars.Init(*buffer_2)
	var reply bool = false

	if ietvars.mērķismacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ietvars.mērķismacbe) == pats.Getmacaddress() {
		if handler_2[ietvars.ethernetTipsbe] != nil {
			ethernetconsole.MDrukāt(([]byte)("provider\n"))

			var kursors uintptr = uintptr(Pointer(dataKursors)) + uintptr(ietvarsheaderIzmērs)
			reply = handler_2[ietvars.ethernetTipsbe].EthernetIetvarsreceivewhen(kursors, izmērs-ietvarsheaderIzmērs)

		}
	}

	if reply {
		ietvars.mērķismacbe = ietvars.avotsmacbe
		ietvars.avotsmacbe = Unsignedinteger48r(pats.Getmacaddress())
		ietvars.Kopabuffer(buffer_2)

	}

	ethernetconsole.MDrukātxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Drukāt(ietvars.avotsmacbe)
	ethernetconsole.MDrukāt(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Drukāt(ietvars.mērķismacbe)
	ethernetconsole.MDrukāt(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Drukāt(pats.Getmacaddress())
	ethernetconsole.MDrukāt(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Drukāt(ietvars.ethernetTipsbe)
	ethernetconsole.MDrukāt(([]byte)("]"))

	return reply

}
func (pats *TEthernetIetvarsprovider) Sūtīt(dataKursors uintptr, izmērs uint32) {
	pats.tīklscard.Sūtīt(dataKursors, izmērs)
}
func (pats *TEthernetIetvarsprovider) IetvarsSūtīt(mērķismacbe uint64, ethernetTipsbe uint16, dataKursors uintptr, izmērs uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetIetvarsheaderbuffer = (*TEthernetIetvarsheaderbuffer)(Pointer(&buffer2_2))

	var ietvars TEthernetIetvarsheader = TEthernetIetvarsheader{}
	ietvars.Init(*buffer_2)

	ietvars.mērķismacbe = Unsignedinteger48r(mērķismacbe)
	ietvars.avotsmacbe = Unsignedinteger48r(pats.tīklscard.Getmacaddress())
	ietvars.ethernetTipsbe = Unsignedinteger16r(ethernetTipsbe)

	ietvars.Kopabuffer(buffer_2)
	var avots_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursors))

	var i uint32 = 0
	for i = 0; i < izmērs; i++ {
		buffer2_2[uint32(ietvarsheaderIzmērs)+i] = avots_2[i]

	}

	var kursors uintptr = uintptr(Pointer(&buffer2_2))

	pats.tīklscard.Sūtīt(kursors, izmērs+uint32(ietvarsheaderIzmērs))

}
func (pats *TEthernetIetvarsprovider) Getmacaddress() uint64 {
	return pats.tīklscard.Getmacaddress()
}
func (pats *TEthernetIetvarsprovider) Getipaddress() uint64 {
	return pats.tīklscard.Getipaddress()
}
