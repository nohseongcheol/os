/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ram_i_nät_med_delat_medium

import . "konsol"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonsol TKonsol = TKonsol{}

type TEthernetRamheaderbuffer struct {
	målmacbe	[6]byte
	källamacbe	[6]byte
	ethernetTypbe	[2]byte
}

var ramheaderStorlek int = 14

type TRamhuvud_för_nät_med_delat_medium struct {
	målmacbe	uint64
	källamacbe	uint64
	ethernetTypbe	uint16
}

func (själv *TRamhuvud_för_nät_med_delat_medium) Init(buffer_2 TEthernetRamheaderbuffer) {
	själv.målmacbe = (Vektortounsignedinteger48(buffer_2.målmacbe))
	själv.källamacbe = (Vektortounsignedinteger48(buffer_2.källamacbe))
	själv.ethernetTypbe = (Vektortounsignedinteger16(buffer_2.ethernetTypbe))

}
func (själv *TRamhuvud_för_nät_med_delat_medium) Mängdbuffer(buffer_2 *TEthernetRamheaderbuffer) {
	buffer_2.målmacbe = Unsignedinteger48toVektor(Unsignedinteger48r(själv.målmacbe))
	buffer_2.källamacbe = Unsignedinteger48toVektor(Unsignedinteger48r(själv.källamacbe))
	buffer_2.ethernetTypbe = Unsignedinteger16toVektor(Unsignedinteger16r(själv.ethernetTypbe))
}

type IEthernetRamhandler interface {
	Init(backend TRamleverantör_för_nät_med_delat_medium)
	Mängdhandler(handler IEthernetRamhandler, ethernetTyp uint16)
	EthernetRamreceivewhen(dataMuspekare uintptr, storlek int) bool
	Skicka(målmacbe uint64, dataMuspekare uintptr, storlek uint32)
	RamSkicka(målmacbe uint64, ethernetTypbe uint16, dataMuspekare uintptr, storlek uint32)
	Providerget() TRamleverantör_för_nät_med_delat_medium
	GetmacAdress() uint64
	GetipAdress() uint64
}

type TEthernetRamhandler struct {
}

var ram TRamhuvud_för_nät_med_delat_medium
var Backend TRamleverantör_för_nät_med_delat_medium
var handler_2 [65535]IEthernetRamhandler
var efhandler *TEthernetRamhandler = nil

func (själv *TEthernetRamhandler) Init(backend TRamleverantör_för_nät_med_delat_medium) {
	Backend = backend
}

func (själv *TEthernetRamhandler) Mängdhandler(handler IEthernetRamhandler, pethernetTyp uint16) {
	handler_2[pethernetTyp] = handler
}
func (själv *TEthernetRamhandler) Mängdbackend(backend TRamleverantör_för_nät_med_delat_medium) {
	Backend = backend
}
func (själv *TEthernetRamhandler) Getbackend() TRamleverantör_för_nät_med_delat_medium {
	return Backend
}
func (själv *TEthernetRamhandler) EthernetRamreceivewhen(dataMuspekare uintptr, storlek int) bool {
	ethernetKonsol.MSkrivut(([]byte)("OnEtherFrameReceived"))
	return false
}
func (själv *TEthernetRamhandler) Skicka(målmacbe uint64, dataMuspekare uintptr, storlek uint32) {
	Backend.RamSkicka(målmacbe, ram.ethernetTypbe, dataMuspekare, storlek)
}
func (själv *TEthernetRamhandler) RamSkicka(målmacbe uint64, ethernetTypbe uint16, dataMuspekare uintptr, storlek uint32) {
	Backend.RamSkicka(målmacbe, ethernetTypbe, dataMuspekare, storlek)
}
func (själv *TEthernetRamhandler) GetmacAdress() uint64 {
	return Backend.GetmacAdress()
}
func (själv *TEthernetRamhandler) GetipAdress() uint64 {
	return Backend.GetipAdress()
}
func (själv *TEthernetRamhandler) Providerget() TRamleverantör_för_nät_med_delat_medium {
	return Backend
}

type TEthernetRamrawdatahandler struct {
	TRawdatahandler
}

var provider TRamleverantör_för_nät_med_delat_medium

func (själv *TEthernetRamrawdatahandler) Init(pprovider TRamleverantör_för_nät_med_delat_medium, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (själv *TEthernetRamrawdatahandler) Pårawdatareceive(dataMuspekare uintptr, storlek int) bool {
	return provider.Pårawdatareceive(dataMuspekare, storlek)
}
func (själv *TEthernetRamrawdatahandler) Skicka(dataMuspekare uintptr, storlek uint32) {
	provider.Skicka(dataMuspekare, storlek)
}
func (själv *TEthernetRamrawdatahandler) GetmacAdress() uint64 {
	return provider.GetmacAdress()
}
func (själv *TEthernetRamrawdatahandler) GetipAdress() uint64 {
	return provider.GetipAdress()
}
func (själv *TEthernetRamrawdatahandler) Providerget() TRamleverantör_för_nät_med_delat_medium {
	return provider
}

type TRamleverantör_för_nät_med_delat_medium struct {
	nätverkKortspel	Tamdam79c973
	handler_2	[65565]IEthernetRamhandler
}

func (själv *TRamleverantör_för_nät_med_delat_medium) Init(backend Tamdam79c973) {

	själv.nätverkKortspel = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		själv.handler_2[i] = nil
	}
}

var antal uint16 = 0

func (själv *TRamleverantör_för_nät_med_delat_medium) Pårawdatareceive(dataMuspekare uintptr, storlek int) bool {

	var buffer_2 *TEthernetRamheaderbuffer = (*TEthernetRamheaderbuffer)(Pointer(dataMuspekare))
	var ram TRamhuvud_för_nät_med_delat_medium = TRamhuvud_för_nät_med_delat_medium{}
	ram.Init(*buffer_2)
	var reply bool = false

	if ram.målmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ram.målmacbe) == själv.GetmacAdress() {
		if handler_2[ram.ethernetTypbe] != nil {
			ethernetKonsol.MSkrivut(([]byte)("provider\n"))

			var adressreferens uintptr = uintptr(Pointer(dataMuspekare)) + uintptr(ramheaderStorlek)
			reply = handler_2[ram.ethernetTypbe].EthernetRamreceivewhen(adressreferens, storlek-ramheaderStorlek)

		}
	}

	if reply {
		ram.målmacbe = ram.källamacbe
		ram.källamacbe = Unsignedinteger48r(själv.GetmacAdress())
		ram.Mängdbuffer(buffer_2)

	}

	ethernetKonsol.MSkrivutxy(([]byte)("spro["), 0, 1)
	ethernetKonsol.MUnsignedinteger64Skrivut(ram.källamacbe)
	ethernetKonsol.MSkrivut(([]byte)(":"))
	ethernetKonsol.MUnsignedinteger64Skrivut(ram.målmacbe)
	ethernetKonsol.MSkrivut(([]byte)(":]["))
	ethernetKonsol.MUnsignedinteger64Skrivut(själv.GetmacAdress())
	ethernetKonsol.MSkrivut(([]byte)(":"))
	ethernetKonsol.MUnsignedinteger16Skrivut(ram.ethernetTypbe)
	ethernetKonsol.MSkrivut(([]byte)("]"))

	return reply

}
func (själv *TRamleverantör_för_nät_med_delat_medium) Skicka(dataMuspekare uintptr, storlek uint32) {
	själv.nätverkKortspel.Skicka(dataMuspekare, storlek)
}
func (själv *TRamleverantör_för_nät_med_delat_medium) RamSkicka(målmacbe uint64, ethernetTypbe uint16, dataMuspekare uintptr, storlek uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRamheaderbuffer = (*TEthernetRamheaderbuffer)(Pointer(&buffer2_2))

	var ram TRamhuvud_för_nät_med_delat_medium = TRamhuvud_för_nät_med_delat_medium{}
	ram.Init(*buffer_2)

	ram.målmacbe = Unsignedinteger48r(målmacbe)
	ram.källamacbe = Unsignedinteger48r(själv.nätverkKortspel.GetmacAdress())
	ram.ethernetTypbe = Unsignedinteger16r(ethernetTypbe)

	ram.Mängdbuffer(buffer_2)
	var källa_2 [4096]byte = *(*([4096]byte))(Pointer(dataMuspekare))

	var i uint32 = 0
	for i = 0; i < storlek; i++ {
		buffer2_2[uint32(ramheaderStorlek)+i] = källa_2[i]

	}

	var adressreferens uintptr = uintptr(Pointer(&buffer2_2))

	själv.nätverkKortspel.Skicka(adressreferens, storlek+uint32(ramheaderStorlek))

}
func (själv *TRamleverantör_för_nät_med_delat_medium) GetmacAdress() uint64 {
	return själv.nätverkKortspel.GetmacAdress()
}
func (själv *TRamleverantör_för_nät_med_delat_medium) GetipAdress() uint64 {
	return själv.nätverkKortspel.GetipAdress()
}
