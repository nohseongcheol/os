/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package jaetun_siirtotien_verkkokehys

import . "konsoli"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonsoli TKonsoli = TKonsoli{}

type TEthernetKehysheaderbuffer struct {
	kohdemacbe		[6]byte
	lähdemacbe		[6]byte
	ethernetTyyppibe	[2]byte
}

var kehysheaderKoko int = 14

type TJaetun_siirtotien_verkkokehyksen_otsake struct {
	kohdemacbe		uint64
	lähdemacbe		uint64
	ethernetTyyppibe	uint16
}

func (itse *TJaetun_siirtotien_verkkokehyksen_otsake) Init(buffer_2 TEthernetKehysheaderbuffer) {
	itse.kohdemacbe = (Taulukkotounsignedinteger48(buffer_2.kohdemacbe))
	itse.lähdemacbe = (Taulukkotounsignedinteger48(buffer_2.lähdemacbe))
	itse.ethernetTyyppibe = (Taulukkotounsignedinteger16(buffer_2.ethernetTyyppibe))

}
func (itse *TJaetun_siirtotien_verkkokehyksen_otsake) Asetabuffer(buffer_2 *TEthernetKehysheaderbuffer) {
	buffer_2.kohdemacbe = Unsignedinteger48toTaulukko(Unsignedinteger48r(itse.kohdemacbe))
	buffer_2.lähdemacbe = Unsignedinteger48toTaulukko(Unsignedinteger48r(itse.lähdemacbe))
	buffer_2.ethernetTyyppibe = Unsignedinteger16toTaulukko(Unsignedinteger16r(itse.ethernetTyyppibe))
}

type IEthernetKehyshandler interface {
	Init(backend TJaetun_siirtotien_verkkokehysten_tarjoaja)
	Asetahandler(handler IEthernetKehyshandler, ethernetTyyppi uint16)
	EthernetKehysreceivewhen(dataOsoitin uintptr, koko int) bool
	Lähetä(kohdemacbe uint64, dataOsoitin uintptr, koko uint32)
	KehysLähetä(kohdemacbe uint64, ethernetTyyppibe uint16, dataOsoitin uintptr, koko uint32)
	Providerget() TJaetun_siirtotien_verkkokehysten_tarjoaja
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetKehyshandler struct {
}

var kehys TJaetun_siirtotien_verkkokehyksen_otsake
var Backend TJaetun_siirtotien_verkkokehysten_tarjoaja
var handler_2 [65535]IEthernetKehyshandler
var efhandler *TEthernetKehyshandler = nil

func (itse *TEthernetKehyshandler) Init(backend TJaetun_siirtotien_verkkokehysten_tarjoaja) {
	Backend = backend
}

func (itse *TEthernetKehyshandler) Asetahandler(handler IEthernetKehyshandler, pethernetTyyppi uint16) {
	handler_2[pethernetTyyppi] = handler
}
func (itse *TEthernetKehyshandler) Asetabackend(backend TJaetun_siirtotien_verkkokehysten_tarjoaja) {
	Backend = backend
}
func (itse *TEthernetKehyshandler) Getbackend() TJaetun_siirtotien_verkkokehysten_tarjoaja {
	return Backend
}
func (itse *TEthernetKehyshandler) EthernetKehysreceivewhen(dataOsoitin uintptr, koko int) bool {
	ethernetKonsoli.MTulosta(([]byte)("OnEtherFrameReceived"))
	return false
}
func (itse *TEthernetKehyshandler) Lähetä(kohdemacbe uint64, dataOsoitin uintptr, koko uint32) {
	Backend.KehysLähetä(kohdemacbe, kehys.ethernetTyyppibe, dataOsoitin, koko)
}
func (itse *TEthernetKehyshandler) KehysLähetä(kohdemacbe uint64, ethernetTyyppibe uint16, dataOsoitin uintptr, koko uint32) {
	Backend.KehysLähetä(kohdemacbe, ethernetTyyppibe, dataOsoitin, koko)
}
func (itse *TEthernetKehyshandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (itse *TEthernetKehyshandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (itse *TEthernetKehyshandler) Providerget() TJaetun_siirtotien_verkkokehysten_tarjoaja {
	return Backend
}

type TEthernetKehysrawdatahandler struct {
	TRawdatahandler
}

var provider TJaetun_siirtotien_verkkokehysten_tarjoaja

func (itse *TEthernetKehysrawdatahandler) Init(pprovider TJaetun_siirtotien_verkkokehysten_tarjoaja, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (itse *TEthernetKehysrawdatahandler) Päällärawdatareceive(dataOsoitin uintptr, koko int) bool {
	return provider.Päällärawdatareceive(dataOsoitin, koko)
}
func (itse *TEthernetKehysrawdatahandler) Lähetä(dataOsoitin uintptr, koko uint32) {
	provider.Lähetä(dataOsoitin, koko)
}
func (itse *TEthernetKehysrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (itse *TEthernetKehysrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (itse *TEthernetKehysrawdatahandler) Providerget() TJaetun_siirtotien_verkkokehysten_tarjoaja {
	return provider
}

type TJaetun_siirtotien_verkkokehysten_tarjoaja struct {
	verkkoKortti	Tamdam79c973
	handler_2	[65565]IEthernetKehyshandler
}

func (itse *TJaetun_siirtotien_verkkokehysten_tarjoaja) Init(backend Tamdam79c973) {

	itse.verkkoKortti = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		itse.handler_2[i] = nil
	}
}

var count uint16 = 0

func (itse *TJaetun_siirtotien_verkkokehysten_tarjoaja) Päällärawdatareceive(dataOsoitin uintptr, koko int) bool {

	var buffer_2 *TEthernetKehysheaderbuffer = (*TEthernetKehysheaderbuffer)(Pointer(dataOsoitin))
	var kehys TJaetun_siirtotien_verkkokehyksen_otsake = TJaetun_siirtotien_verkkokehyksen_otsake{}
	kehys.Init(*buffer_2)
	var reply bool = false

	if kehys.kohdemacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(kehys.kohdemacbe) == itse.Getmacaddress() {
		if handler_2[kehys.ethernetTyyppibe] != nil {
			ethernetKonsoli.MTulosta(([]byte)("provider\n"))

			var osoiteviite uintptr = uintptr(Pointer(dataOsoitin)) + uintptr(kehysheaderKoko)
			reply = handler_2[kehys.ethernetTyyppibe].EthernetKehysreceivewhen(osoiteviite, koko-kehysheaderKoko)

		}
	}

	if reply {
		kehys.kohdemacbe = kehys.lähdemacbe
		kehys.lähdemacbe = Unsignedinteger48r(itse.Getmacaddress())
		kehys.Asetabuffer(buffer_2)

	}

	ethernetKonsoli.MTulostaxy(([]byte)("spro["), 0, 1)
	ethernetKonsoli.MUnsignedinteger64Tulosta(kehys.lähdemacbe)
	ethernetKonsoli.MTulosta(([]byte)(":"))
	ethernetKonsoli.MUnsignedinteger64Tulosta(kehys.kohdemacbe)
	ethernetKonsoli.MTulosta(([]byte)(":]["))
	ethernetKonsoli.MUnsignedinteger64Tulosta(itse.Getmacaddress())
	ethernetKonsoli.MTulosta(([]byte)(":"))
	ethernetKonsoli.MUnsignedinteger16Tulosta(kehys.ethernetTyyppibe)
	ethernetKonsoli.MTulosta(([]byte)("]"))

	return reply

}
func (itse *TJaetun_siirtotien_verkkokehysten_tarjoaja) Lähetä(dataOsoitin uintptr, koko uint32) {
	itse.verkkoKortti.Lähetä(dataOsoitin, koko)
}
func (itse *TJaetun_siirtotien_verkkokehysten_tarjoaja) KehysLähetä(kohdemacbe uint64, ethernetTyyppibe uint16, dataOsoitin uintptr, koko uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetKehysheaderbuffer = (*TEthernetKehysheaderbuffer)(Pointer(&buffer2_2))

	var kehys TJaetun_siirtotien_verkkokehyksen_otsake = TJaetun_siirtotien_verkkokehyksen_otsake{}
	kehys.Init(*buffer_2)

	kehys.kohdemacbe = Unsignedinteger48r(kohdemacbe)
	kehys.lähdemacbe = Unsignedinteger48r(itse.verkkoKortti.Getmacaddress())
	kehys.ethernetTyyppibe = Unsignedinteger16r(ethernetTyyppibe)

	kehys.Asetabuffer(buffer_2)
	var lähde_2 [4096]byte = *(*([4096]byte))(Pointer(dataOsoitin))

	var i uint32 = 0
	for i = 0; i < koko; i++ {
		buffer2_2[uint32(kehysheaderKoko)+i] = lähde_2[i]

	}

	var osoiteviite uintptr = uintptr(Pointer(&buffer2_2))

	itse.verkkoKortti.Lähetä(osoiteviite, koko+uint32(kehysheaderKoko))

}
func (itse *TJaetun_siirtotien_verkkokehysten_tarjoaja) Getmacaddress() uint64 {
	return itse.verkkoKortti.Getmacaddress()
}
func (itse *TJaetun_siirtotien_verkkokehysten_tarjoaja) Getipaddress() uint64 {
	return itse.verkkoKortti.Getipaddress()
}
