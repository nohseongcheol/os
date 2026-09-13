package ethernetRamme

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetRammeTopptekstbuffer struct {
	målmacbe		[6]byte
	kildemacbe		[6]byte
	ethernetFiltypebe	[2]byte
}

var rammeTopptekstStørrelse int = 14

type TEthernetRammeTopptekst struct {
	målmacbe		uint64
	kildemacbe		uint64
	ethernetFiltypebe	uint16
}

func (selv *TEthernetRammeTopptekst) Init(buffer_2 TEthernetRammeTopptekstbuffer) {
	selv.målmacbe = (Tabelltounsignedinteger48(buffer_2.målmacbe))
	selv.kildemacbe = (Tabelltounsignedinteger48(buffer_2.kildemacbe))
	selv.ethernetFiltypebe = (Tabelltounsignedinteger16(buffer_2.ethernetFiltypebe))

}
func (selv *TEthernetRammeTopptekst) Settbuffer(buffer_2 *TEthernetRammeTopptekstbuffer) {
	buffer_2.målmacbe = Unsignedinteger48toTabell(Unsignedinteger48r(selv.målmacbe))
	buffer_2.kildemacbe = Unsignedinteger48toTabell(Unsignedinteger48r(selv.kildemacbe))
	buffer_2.ethernetFiltypebe = Unsignedinteger16toTabell(Unsignedinteger16r(selv.ethernetFiltypebe))
}

type IEthernetRammehandler interface {
	Init(backend TEthernetRammeprovider)
	Setthandler(handler IEthernetRammehandler, ethernetFiltype uint16)
	EthernetRammereceivewhen(dataPeker uintptr, størrelse int) bool
	Send(målmacbe uint64, dataPeker uintptr, størrelse uint32)
	Rammesend(målmacbe uint64, ethernetFiltypebe uint16, dataPeker uintptr, størrelse uint32)
	Providerget() TEthernetRammeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRammehandler struct {
}

var ramme TEthernetRammeTopptekst
var Backend TEthernetRammeprovider
var handler_2 [65535]IEthernetRammehandler
var efhandler *TEthernetRammehandler = nil

func (selv *TEthernetRammehandler) Init(backend TEthernetRammeprovider) {
	Backend = backend
}

func (selv *TEthernetRammehandler) Setthandler(handler IEthernetRammehandler, pethernetFiltype uint16) {
	handler_2[pethernetFiltype] = handler
}
func (selv *TEthernetRammehandler) Settbackend(backend TEthernetRammeprovider) {
	Backend = backend
}
func (selv *TEthernetRammehandler) Getbackend() TEthernetRammeprovider {
	return Backend
}
func (selv *TEthernetRammehandler) EthernetRammereceivewhen(dataPeker uintptr, størrelse int) bool {
	ethernetconsole.MSkrivut(([]byte)("OnEtherFrameReceived"))
	return false
}
func (selv *TEthernetRammehandler) Send(målmacbe uint64, dataPeker uintptr, størrelse uint32) {
	Backend.Rammesend(målmacbe, ramme.ethernetFiltypebe, dataPeker, størrelse)
}
func (selv *TEthernetRammehandler) Rammesend(målmacbe uint64, ethernetFiltypebe uint16, dataPeker uintptr, størrelse uint32) {
	Backend.Rammesend(målmacbe, ethernetFiltypebe, dataPeker, størrelse)
}
func (selv *TEthernetRammehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (selv *TEthernetRammehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (selv *TEthernetRammehandler) Providerget() TEthernetRammeprovider {
	return Backend
}

type TEthernetRammerawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetRammeprovider

func (selv *TEthernetRammerawdatahandler) Init(pprovider TEthernetRammeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (selv *TEthernetRammerawdatahandler) Pårawdatareceive(dataPeker uintptr, størrelse int) bool {
	return provider.Pårawdatareceive(dataPeker, størrelse)
}
func (selv *TEthernetRammerawdatahandler) Send(dataPeker uintptr, størrelse uint32) {
	provider.Send(dataPeker, størrelse)
}
func (selv *TEthernetRammerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (selv *TEthernetRammerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (selv *TEthernetRammerawdatahandler) Providerget() TEthernetRammeprovider {
	return provider
}

type TEthernetRammeprovider struct {
	nettverkKort	Tamdam79c973
	handler_2	[65565]IEthernetRammehandler
}

func (selv *TEthernetRammeprovider) Init(backend Tamdam79c973) {

	selv.nettverkKort = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		selv.handler_2[i] = nil
	}
}

var antall uint16 = 0

func (selv *TEthernetRammeprovider) Pårawdatareceive(dataPeker uintptr, størrelse int) bool {

	var buffer_2 *TEthernetRammeTopptekstbuffer = (*TEthernetRammeTopptekstbuffer)(Pointer(dataPeker))
	var ramme TEthernetRammeTopptekst = TEthernetRammeTopptekst{}
	ramme.Init(*buffer_2)
	var reply bool = false

	if ramme.målmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ramme.målmacbe) == selv.Getmacaddress() {
		if handler_2[ramme.ethernetFiltypebe] != nil {
			ethernetconsole.MSkrivut(([]byte)("provider\n"))

			var peker uintptr = uintptr(Pointer(dataPeker)) + uintptr(rammeTopptekstStørrelse)
			reply = handler_2[ramme.ethernetFiltypebe].EthernetRammereceivewhen(peker, størrelse-rammeTopptekstStørrelse)

		}
	}

	if reply {
		ramme.målmacbe = ramme.kildemacbe
		ramme.kildemacbe = Unsignedinteger48r(selv.Getmacaddress())
		ramme.Settbuffer(buffer_2)

	}

	ethernetconsole.MSkrivutxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Skrivut(ramme.kildemacbe)
	ethernetconsole.MSkrivut(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Skrivut(ramme.målmacbe)
	ethernetconsole.MSkrivut(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Skrivut(selv.Getmacaddress())
	ethernetconsole.MSkrivut(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Skrivut(ramme.ethernetFiltypebe)
	ethernetconsole.MSkrivut(([]byte)("]"))

	return reply

}
func (selv *TEthernetRammeprovider) Send(dataPeker uintptr, størrelse uint32) {
	selv.nettverkKort.Send(dataPeker, størrelse)
}
func (selv *TEthernetRammeprovider) Rammesend(målmacbe uint64, ethernetFiltypebe uint16, dataPeker uintptr, størrelse uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRammeTopptekstbuffer = (*TEthernetRammeTopptekstbuffer)(Pointer(&buffer2_2))

	var ramme TEthernetRammeTopptekst = TEthernetRammeTopptekst{}
	ramme.Init(*buffer_2)

	ramme.målmacbe = Unsignedinteger48r(målmacbe)
	ramme.kildemacbe = Unsignedinteger48r(selv.nettverkKort.Getmacaddress())
	ramme.ethernetFiltypebe = Unsignedinteger16r(ethernetFiltypebe)

	ramme.Settbuffer(buffer_2)
	var kilde_2 [4096]byte = *(*([4096]byte))(Pointer(dataPeker))

	var i uint32 = 0
	for i = 0; i < størrelse; i++ {
		buffer2_2[uint32(rammeTopptekstStørrelse)+i] = kilde_2[i]

	}

	var peker uintptr = uintptr(Pointer(&buffer2_2))

	selv.nettverkKort.Send(peker, størrelse+uint32(rammeTopptekstStørrelse))

}
func (selv *TEthernetRammeprovider) Getmacaddress() uint64 {
	return selv.nettverkKort.Getmacaddress()
}
func (selv *TEthernetRammeprovider) Getipaddress() uint64 {
	return selv.nettverkKort.Getipaddress()
}
