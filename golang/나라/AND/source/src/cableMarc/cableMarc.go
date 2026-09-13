package cableMarc

import . "consola"

import . "amdam79c973"
import . "unsafe"
import . "util"

var cableConsola TConsola = TConsola{}

type TCableMarcheaderbuffer struct {
	destinaciómacbe	[6]byte
	origenmacbe	[6]byte
	cableTipusbe	[2]byte
}

var marcheaderMida int = 14

type TCableMarcheader struct {
	destinaciómacbe	uint64
	origenmacbe	uint64
	cableTipusbe	uint16
}

func (unmateix *TCableMarcheader) Init(buffer_2 TCableMarcheaderbuffer) {
	unmateix.destinaciómacbe = (Matriutounsignedinteger48(buffer_2.destinaciómacbe))
	unmateix.origenmacbe = (Matriutounsignedinteger48(buffer_2.origenmacbe))
	unmateix.cableTipusbe = (Matriutounsignedinteger16(buffer_2.cableTipusbe))

}
func (unmateix *TCableMarcheader) Estableixbuffer(buffer_2 *TCableMarcheaderbuffer) {
	buffer_2.destinaciómacbe = Unsignedinteger48toMatriu(Unsignedinteger48r(unmateix.destinaciómacbe))
	buffer_2.origenmacbe = Unsignedinteger48toMatriu(Unsignedinteger48r(unmateix.origenmacbe))
	buffer_2.cableTipusbe = Unsignedinteger16toMatriu(Unsignedinteger16r(unmateix.cableTipusbe))
}

type ICableMarchandler interface {
	Init(backend TCableMarcprovider)
	Estableixhandler(handler ICableMarchandler, cableTipus uint16)
	CableMarcreceivewhen(dataPunter uintptr, mida int) bool
	Envia(destinaciómacbe uint64, dataPunter uintptr, mida uint32)
	MarcEnvia(destinaciómacbe uint64, cableTipusbe uint16, dataPunter uintptr, mida uint32)
	Providerget() TCableMarcprovider
	GetmacAdreça() uint64
	GetipAdreça() uint64
}

type TCableMarchandler struct {
}

var marc TCableMarcheader
var Backend TCableMarcprovider
var handler_2 [65535]ICableMarchandler
var efhandler *TCableMarchandler = nil

func (unmateix *TCableMarchandler) Init(backend TCableMarcprovider) {
	Backend = backend
}

func (unmateix *TCableMarchandler) Estableixhandler(handler ICableMarchandler, pCableTipus uint16) {
	handler_2[pCableTipus] = handler
}
func (unmateix *TCableMarchandler) Estableixbackend(backend TCableMarcprovider) {
	Backend = backend
}
func (unmateix *TCableMarchandler) Getbackend() TCableMarcprovider {
	return Backend
}
func (unmateix *TCableMarchandler) CableMarcreceivewhen(dataPunter uintptr, mida int) bool {
	cableConsola.MImprimeix(([]byte)("OnEtherFrameReceived"))
	return false
}
func (unmateix *TCableMarchandler) Envia(destinaciómacbe uint64, dataPunter uintptr, mida uint32) {
	Backend.MarcEnvia(destinaciómacbe, marc.cableTipusbe, dataPunter, mida)
}
func (unmateix *TCableMarchandler) MarcEnvia(destinaciómacbe uint64, cableTipusbe uint16, dataPunter uintptr, mida uint32) {
	Backend.MarcEnvia(destinaciómacbe, cableTipusbe, dataPunter, mida)
}
func (unmateix *TCableMarchandler) GetmacAdreça() uint64 {
	return Backend.GetmacAdreça()
}
func (unmateix *TCableMarchandler) GetipAdreça() uint64 {
	return Backend.GetipAdreça()
}
func (unmateix *TCableMarchandler) Providerget() TCableMarcprovider {
	return Backend
}

type TCableMarcrawdatahandler struct {
	TRawdatahandler
}

var provider TCableMarcprovider

func (unmateix *TCableMarcrawdatahandler) Init(pprovider TCableMarcprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (unmateix *TCableMarcrawdatahandler) Engegatrawdatareceive(dataPunter uintptr, mida int) bool {
	return provider.Engegatrawdatareceive(dataPunter, mida)
}
func (unmateix *TCableMarcrawdatahandler) Envia(dataPunter uintptr, mida uint32) {
	provider.Envia(dataPunter, mida)
}
func (unmateix *TCableMarcrawdatahandler) GetmacAdreça() uint64 {
	return provider.GetmacAdreça()
}
func (unmateix *TCableMarcrawdatahandler) GetipAdreça() uint64 {
	return provider.GetipAdreça()
}
func (unmateix *TCableMarcrawdatahandler) Providerget() TCableMarcprovider {
	return provider
}

type TCableMarcprovider struct {
	xarxaCartes	Tamdam79c973
	handler_2	[65565]ICableMarchandler
}

func (unmateix *TCableMarcprovider) Init(backend Tamdam79c973) {

	unmateix.xarxaCartes = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		unmateix.handler_2[i] = nil
	}
}

var recompte uint16 = 0

func (unmateix *TCableMarcprovider) Engegatrawdatareceive(dataPunter uintptr, mida int) bool {

	var buffer_2 *TCableMarcheaderbuffer = (*TCableMarcheaderbuffer)(Pointer(dataPunter))
	var marc TCableMarcheader = TCableMarcheader{}
	marc.Init(*buffer_2)
	var reply bool = false

	if marc.destinaciómacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(marc.destinaciómacbe) == unmateix.GetmacAdreça() {
		if handler_2[marc.cableTipusbe] != nil {
			cableConsola.MImprimeix(([]byte)("provider\n"))

			var punter uintptr = uintptr(Pointer(dataPunter)) + uintptr(marcheaderMida)
			reply = handler_2[marc.cableTipusbe].CableMarcreceivewhen(punter, mida-marcheaderMida)

		}
	}

	if reply {
		marc.destinaciómacbe = marc.origenmacbe
		marc.origenmacbe = Unsignedinteger48r(unmateix.GetmacAdreça())
		marc.Estableixbuffer(buffer_2)

	}

	cableConsola.MImprimeixxy(([]byte)("spro["), 0, 1)
	cableConsola.MUnsignedinteger64Imprimeix(marc.origenmacbe)
	cableConsola.MImprimeix(([]byte)(":"))
	cableConsola.MUnsignedinteger64Imprimeix(marc.destinaciómacbe)
	cableConsola.MImprimeix(([]byte)(":]["))
	cableConsola.MUnsignedinteger64Imprimeix(unmateix.GetmacAdreça())
	cableConsola.MImprimeix(([]byte)(":"))
	cableConsola.MUnsignedinteger16Imprimeix(marc.cableTipusbe)
	cableConsola.MImprimeix(([]byte)("]"))

	return reply

}
func (unmateix *TCableMarcprovider) Envia(dataPunter uintptr, mida uint32) {
	unmateix.xarxaCartes.Envia(dataPunter, mida)
}
func (unmateix *TCableMarcprovider) MarcEnvia(destinaciómacbe uint64, cableTipusbe uint16, dataPunter uintptr, mida uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TCableMarcheaderbuffer = (*TCableMarcheaderbuffer)(Pointer(&buffer2_2))

	var marc TCableMarcheader = TCableMarcheader{}
	marc.Init(*buffer_2)

	marc.destinaciómacbe = Unsignedinteger48r(destinaciómacbe)
	marc.origenmacbe = Unsignedinteger48r(unmateix.xarxaCartes.GetmacAdreça())
	marc.cableTipusbe = Unsignedinteger16r(cableTipusbe)

	marc.Estableixbuffer(buffer_2)
	var origen_2 [4096]byte = *(*([4096]byte))(Pointer(dataPunter))

	var i uint32 = 0
	for i = 0; i < mida; i++ {
		buffer2_2[uint32(marcheaderMida)+i] = origen_2[i]

	}

	var punter uintptr = uintptr(Pointer(&buffer2_2))

	unmateix.xarxaCartes.Envia(punter, mida+uint32(marcheaderMida))

}
func (unmateix *TCableMarcprovider) GetmacAdreça() uint64 {
	return unmateix.xarxaCartes.GetmacAdreça()
}
func (unmateix *TCableMarcprovider) GetipAdreça() uint64 {
	return unmateix.xarxaCartes.GetipAdreça()
}
