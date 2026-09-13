package ramka_sieci_o_wspólnym_medium

import . "konsola"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonsola TKonsola = TKonsola{}

type TEthernetRamkaheaderbuffer struct {
	celmacbe	[6]byte
	źródłomacbe	[6]byte
	ethernetTypbe	[2]byte
}

var ramkaheaderRozmiar int = 14

type TNagłówek_ramki_sieci_o_wspólnym_medium struct {
	celmacbe	uint64
	źródłomacbe	uint64
	ethernetTypbe	uint16
}

func (bieżący *TNagłówek_ramki_sieci_o_wspólnym_medium) Init(buffer_2 TEthernetRamkaheaderbuffer) {
	bieżący.celmacbe = (Tablicatounsignedinteger48(buffer_2.celmacbe))
	bieżący.źródłomacbe = (Tablicatounsignedinteger48(buffer_2.źródłomacbe))
	bieżący.ethernetTypbe = (Tablicatounsignedinteger16(buffer_2.ethernetTypbe))

}
func (bieżący *TNagłówek_ramki_sieci_o_wspólnym_medium) Zbiórbuffer(buffer_2 *TEthernetRamkaheaderbuffer) {
	buffer_2.celmacbe = Unsignedinteger48toTablica(Unsignedinteger48r(bieżący.celmacbe))
	buffer_2.źródłomacbe = Unsignedinteger48toTablica(Unsignedinteger48r(bieżący.źródłomacbe))
	buffer_2.ethernetTypbe = Unsignedinteger16toTablica(Unsignedinteger16r(bieżący.ethernetTypbe))
}

type IEthernetRamkahandler interface {
	Init(backend TDostawca_ramek_sieci_o_wspólnym_medium)
	Zbiórhandler(handler IEthernetRamkahandler, ethernetTyp uint16)
	EthernetRamkareceivewhen(dataKursor uintptr, rozmiar int) bool
	Wyślij(celmacbe uint64, dataKursor uintptr, rozmiar uint32)
	RamkaWyślij(celmacbe uint64, ethernetTypbe uint16, dataKursor uintptr, rozmiar uint32)
	Providerget() TDostawca_ramek_sieci_o_wspólnym_medium
	GetmacAdres() uint64
	GetipAdres() uint64
}

type TEthernetRamkahandler struct {
}

var ramka TNagłówek_ramki_sieci_o_wspólnym_medium
var Backend TDostawca_ramek_sieci_o_wspólnym_medium
var handler_2 [65535]IEthernetRamkahandler
var efhandler *TEthernetRamkahandler = nil

func (bieżący *TEthernetRamkahandler) Init(backend TDostawca_ramek_sieci_o_wspólnym_medium) {
	Backend = backend
}

func (bieżący *TEthernetRamkahandler) Zbiórhandler(handler IEthernetRamkahandler, pethernetTyp uint16) {
	handler_2[pethernetTyp] = handler
}
func (bieżący *TEthernetRamkahandler) Zbiórbackend(backend TDostawca_ramek_sieci_o_wspólnym_medium) {
	Backend = backend
}
func (bieżący *TEthernetRamkahandler) Getbackend() TDostawca_ramek_sieci_o_wspólnym_medium {
	return Backend
}
func (bieżący *TEthernetRamkahandler) EthernetRamkareceivewhen(dataKursor uintptr, rozmiar int) bool {
	ethernetKonsola.MWydrukuj(([]byte)("OnEtherFrameReceived"))
	return false
}
func (bieżący *TEthernetRamkahandler) Wyślij(celmacbe uint64, dataKursor uintptr, rozmiar uint32) {
	Backend.RamkaWyślij(celmacbe, ramka.ethernetTypbe, dataKursor, rozmiar)
}
func (bieżący *TEthernetRamkahandler) RamkaWyślij(celmacbe uint64, ethernetTypbe uint16, dataKursor uintptr, rozmiar uint32) {
	Backend.RamkaWyślij(celmacbe, ethernetTypbe, dataKursor, rozmiar)
}
func (bieżący *TEthernetRamkahandler) GetmacAdres() uint64 {
	return Backend.GetmacAdres()
}
func (bieżący *TEthernetRamkahandler) GetipAdres() uint64 {
	return Backend.GetipAdres()
}
func (bieżący *TEthernetRamkahandler) Providerget() TDostawca_ramek_sieci_o_wspólnym_medium {
	return Backend
}

type TEthernetRamkarawdatahandler struct {
	TRawdatahandler
}

var provider TDostawca_ramek_sieci_o_wspólnym_medium

func (bieżący *TEthernetRamkarawdatahandler) Init(pprovider TDostawca_ramek_sieci_o_wspólnym_medium, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (bieżący *TEthernetRamkarawdatahandler) Włączrawdatareceive(dataKursor uintptr, rozmiar int) bool {
	return provider.Włączrawdatareceive(dataKursor, rozmiar)
}
func (bieżący *TEthernetRamkarawdatahandler) Wyślij(dataKursor uintptr, rozmiar uint32) {
	provider.Wyślij(dataKursor, rozmiar)
}
func (bieżący *TEthernetRamkarawdatahandler) GetmacAdres() uint64 {
	return provider.GetmacAdres()
}
func (bieżący *TEthernetRamkarawdatahandler) GetipAdres() uint64 {
	return provider.GetipAdres()
}
func (bieżący *TEthernetRamkarawdatahandler) Providerget() TDostawca_ramek_sieci_o_wspólnym_medium {
	return provider
}

type TDostawca_ramek_sieci_o_wspólnym_medium struct {
	siećKarciane	Tamdam79c973
	handler_2	[65565]IEthernetRamkahandler
}

func (bieżący *TDostawca_ramek_sieci_o_wspólnym_medium) Init(backend Tamdam79c973) {

	bieżący.siećKarciane = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		bieżący.handler_2[i] = nil
	}
}

var liczba uint16 = 0

func (bieżący *TDostawca_ramek_sieci_o_wspólnym_medium) Włączrawdatareceive(dataKursor uintptr, rozmiar int) bool {

	var buffer_2 *TEthernetRamkaheaderbuffer = (*TEthernetRamkaheaderbuffer)(Pointer(dataKursor))
	var ramka TNagłówek_ramki_sieci_o_wspólnym_medium = TNagłówek_ramki_sieci_o_wspólnym_medium{}
	ramka.Init(*buffer_2)
	var reply bool = false

	if ramka.celmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ramka.celmacbe) == bieżący.GetmacAdres() {
		if handler_2[ramka.ethernetTypbe] != nil {
			ethernetKonsola.MWydrukuj(([]byte)("provider\n"))

			var odwołanie_do_adresu uintptr = uintptr(Pointer(dataKursor)) + uintptr(ramkaheaderRozmiar)
			reply = handler_2[ramka.ethernetTypbe].EthernetRamkareceivewhen(odwołanie_do_adresu, rozmiar-ramkaheaderRozmiar)

		}
	}

	if reply {
		ramka.celmacbe = ramka.źródłomacbe
		ramka.źródłomacbe = Unsignedinteger48r(bieżący.GetmacAdres())
		ramka.Zbiórbuffer(buffer_2)

	}

	ethernetKonsola.MWydrukujxy(([]byte)("spro["), 0, 1)
	ethernetKonsola.MUnsignedinteger64Wydrukuj(ramka.źródłomacbe)
	ethernetKonsola.MWydrukuj(([]byte)(":"))
	ethernetKonsola.MUnsignedinteger64Wydrukuj(ramka.celmacbe)
	ethernetKonsola.MWydrukuj(([]byte)(":]["))
	ethernetKonsola.MUnsignedinteger64Wydrukuj(bieżący.GetmacAdres())
	ethernetKonsola.MWydrukuj(([]byte)(":"))
	ethernetKonsola.MUnsignedinteger16Wydrukuj(ramka.ethernetTypbe)
	ethernetKonsola.MWydrukuj(([]byte)("]"))

	return reply

}
func (bieżący *TDostawca_ramek_sieci_o_wspólnym_medium) Wyślij(dataKursor uintptr, rozmiar uint32) {
	bieżący.siećKarciane.Wyślij(dataKursor, rozmiar)
}
func (bieżący *TDostawca_ramek_sieci_o_wspólnym_medium) RamkaWyślij(celmacbe uint64, ethernetTypbe uint16, dataKursor uintptr, rozmiar uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRamkaheaderbuffer = (*TEthernetRamkaheaderbuffer)(Pointer(&buffer2_2))

	var ramka TNagłówek_ramki_sieci_o_wspólnym_medium = TNagłówek_ramki_sieci_o_wspólnym_medium{}
	ramka.Init(*buffer_2)

	ramka.celmacbe = Unsignedinteger48r(celmacbe)
	ramka.źródłomacbe = Unsignedinteger48r(bieżący.siećKarciane.GetmacAdres())
	ramka.ethernetTypbe = Unsignedinteger16r(ethernetTypbe)

	ramka.Zbiórbuffer(buffer_2)
	var źródło_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursor))

	var i uint32 = 0
	for i = 0; i < rozmiar; i++ {
		buffer2_2[uint32(ramkaheaderRozmiar)+i] = źródło_2[i]

	}

	var odwołanie_do_adresu uintptr = uintptr(Pointer(&buffer2_2))

	bieżący.siećKarciane.Wyślij(odwołanie_do_adresu, rozmiar+uint32(ramkaheaderRozmiar))

}
func (bieżący *TDostawca_ramek_sieci_o_wspólnym_medium) GetmacAdres() uint64 {
	return bieżący.siećKarciane.GetmacAdres()
}
func (bieżący *TDostawca_ramek_sieci_o_wspólnym_medium) GetipAdres() uint64 {
	return bieżący.siećKarciane.GetipAdres()
}
