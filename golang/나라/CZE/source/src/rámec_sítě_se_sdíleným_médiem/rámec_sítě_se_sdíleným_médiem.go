package rámec_sítě_se_sdíleným_médiem

import . "konzole"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonzole TKonzole = TKonzole{}

type TEthernetRámheaderbuffer struct {
	cílmacbe	[6]byte
	zdrojmacbe	[6]byte
	ethernetTypbe	[2]byte
}

var rámheaderVelikost int = 14

type THlavička_rámce_sítě_se_sdíleným_médiem struct {
	cílmacbe	uint64
	zdrojmacbe	uint64
	ethernetTypbe	uint16
}

func (self *THlavička_rámce_sítě_se_sdíleným_médiem) Init(buffer_2 TEthernetRámheaderbuffer) {
	self.cílmacbe = (Poledounsignedinteger48(buffer_2.cílmacbe))
	self.zdrojmacbe = (Poledounsignedinteger48(buffer_2.zdrojmacbe))
	self.ethernetTypbe = (Poledounsignedinteger16(buffer_2.ethernetTypbe))

}
func (self *THlavička_rámce_sítě_se_sdíleným_médiem) Nastavitbuffer(buffer_2 *TEthernetRámheaderbuffer) {
	buffer_2.cílmacbe = Unsignedinteger48doPole(Unsignedinteger48r(self.cílmacbe))
	buffer_2.zdrojmacbe = Unsignedinteger48doPole(Unsignedinteger48r(self.zdrojmacbe))
	buffer_2.ethernetTypbe = Unsignedinteger16doPole(Unsignedinteger16r(self.ethernetTypbe))
}

type IEthernetRámhandler interface {
	Init(backend TPoskytovatel_rámců_sítě_se_sdíleným_médiem)
	Nastavithandler(handler IEthernetRámhandler, ethernetTyp uint16)
	EthernetRámreceivewhen(dataKurzor uintptr, velikost int) bool
	Poslat(cílmacbe uint64, dataKurzor uintptr, velikost uint32)
	RámPoslat(cílmacbe uint64, ethernetTypbe uint16, dataKurzor uintptr, velikost uint32)
	Providerget() TPoskytovatel_rámců_sítě_se_sdíleným_médiem
	GetmacAdresa() uint64
	GetipAdresa() uint64
}

type TEthernetRámhandler struct {
}

var rám THlavička_rámce_sítě_se_sdíleným_médiem
var Backend TPoskytovatel_rámců_sítě_se_sdíleným_médiem
var handler_2 [65535]IEthernetRámhandler
var efhandler *TEthernetRámhandler = nil

func (self *TEthernetRámhandler) Init(backend TPoskytovatel_rámců_sítě_se_sdíleným_médiem) {
	Backend = backend
}

func (self *TEthernetRámhandler) Nastavithandler(handler IEthernetRámhandler, pethernetTyp uint16) {
	handler_2[pethernetTyp] = handler
}
func (self *TEthernetRámhandler) Nastavitbackend(backend TPoskytovatel_rámců_sítě_se_sdíleným_médiem) {
	Backend = backend
}
func (self *TEthernetRámhandler) Getbackend() TPoskytovatel_rámců_sítě_se_sdíleným_médiem {
	return Backend
}
func (self *TEthernetRámhandler) EthernetRámreceivewhen(dataKurzor uintptr, velikost int) bool {
	ethernetKonzole.MTisknout(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetRámhandler) Poslat(cílmacbe uint64, dataKurzor uintptr, velikost uint32) {
	Backend.RámPoslat(cílmacbe, rám.ethernetTypbe, dataKurzor, velikost)
}
func (self *TEthernetRámhandler) RámPoslat(cílmacbe uint64, ethernetTypbe uint16, dataKurzor uintptr, velikost uint32) {
	Backend.RámPoslat(cílmacbe, ethernetTypbe, dataKurzor, velikost)
}
func (self *TEthernetRámhandler) GetmacAdresa() uint64 {
	return Backend.GetmacAdresa()
}
func (self *TEthernetRámhandler) GetipAdresa() uint64 {
	return Backend.GetipAdresa()
}
func (self *TEthernetRámhandler) Providerget() TPoskytovatel_rámců_sítě_se_sdíleným_médiem {
	return Backend
}

type TEthernetRámrawdatahandler struct {
	TRawdatahandler
}

var provider TPoskytovatel_rámců_sítě_se_sdíleným_médiem

func (self *TEthernetRámrawdatahandler) Init(pprovider TPoskytovatel_rámců_sítě_se_sdíleným_médiem, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetRámrawdatahandler) Zapnutorawdatareceive(dataKurzor uintptr, velikost int) bool {
	return provider.Zapnutorawdatareceive(dataKurzor, velikost)
}
func (self *TEthernetRámrawdatahandler) Poslat(dataKurzor uintptr, velikost uint32) {
	provider.Poslat(dataKurzor, velikost)
}
func (self *TEthernetRámrawdatahandler) GetmacAdresa() uint64 {
	return provider.GetmacAdresa()
}
func (self *TEthernetRámrawdatahandler) GetipAdresa() uint64 {
	return provider.GetipAdresa()
}
func (self *TEthernetRámrawdatahandler) Providerget() TPoskytovatel_rámců_sítě_se_sdíleným_médiem {
	return provider
}

type TPoskytovatel_rámců_sítě_se_sdíleným_médiem struct {
	síťKaretní	Tamdam79c973
	handler_2	[65565]IEthernetRámhandler
}

func (self *TPoskytovatel_rámců_sítě_se_sdíleným_médiem) Init(backend Tamdam79c973) {

	self.síťKaretní = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var počet uint16 = 0

func (self *TPoskytovatel_rámců_sítě_se_sdíleným_médiem) Zapnutorawdatareceive(dataKurzor uintptr, velikost int) bool {

	var buffer_2 *TEthernetRámheaderbuffer = (*TEthernetRámheaderbuffer)(Pointer(dataKurzor))
	var rám THlavička_rámce_sítě_se_sdíleným_médiem = THlavička_rámce_sítě_se_sdíleným_médiem{}
	rám.Init(*buffer_2)
	var reply bool = false

	if rám.cílmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(rám.cílmacbe) == self.GetmacAdresa() {
		if handler_2[rám.ethernetTypbe] != nil {
			ethernetKonzole.MTisknout(([]byte)("provider\n"))

			var odkaz_na_adresu uintptr = uintptr(Pointer(dataKurzor)) + uintptr(rámheaderVelikost)
			reply = handler_2[rám.ethernetTypbe].EthernetRámreceivewhen(odkaz_na_adresu, velikost-rámheaderVelikost)

		}
	}

	if reply {
		rám.cílmacbe = rám.zdrojmacbe
		rám.zdrojmacbe = Unsignedinteger48r(self.GetmacAdresa())
		rám.Nastavitbuffer(buffer_2)

	}

	ethernetKonzole.MTisknoutxy(([]byte)("spro["), 0, 1)
	ethernetKonzole.MUnsignedinteger64Tisknout(rám.zdrojmacbe)
	ethernetKonzole.MTisknout(([]byte)(":"))
	ethernetKonzole.MUnsignedinteger64Tisknout(rám.cílmacbe)
	ethernetKonzole.MTisknout(([]byte)(":]["))
	ethernetKonzole.MUnsignedinteger64Tisknout(self.GetmacAdresa())
	ethernetKonzole.MTisknout(([]byte)(":"))
	ethernetKonzole.MUnsignedinteger16Tisknout(rám.ethernetTypbe)
	ethernetKonzole.MTisknout(([]byte)("]"))

	return reply

}
func (self *TPoskytovatel_rámců_sítě_se_sdíleným_médiem) Poslat(dataKurzor uintptr, velikost uint32) {
	self.síťKaretní.Poslat(dataKurzor, velikost)
}
func (self *TPoskytovatel_rámců_sítě_se_sdíleným_médiem) RámPoslat(cílmacbe uint64, ethernetTypbe uint16, dataKurzor uintptr, velikost uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRámheaderbuffer = (*TEthernetRámheaderbuffer)(Pointer(&buffer2_2))

	var rám THlavička_rámce_sítě_se_sdíleným_médiem = THlavička_rámce_sítě_se_sdíleným_médiem{}
	rám.Init(*buffer_2)

	rám.cílmacbe = Unsignedinteger48r(cílmacbe)
	rám.zdrojmacbe = Unsignedinteger48r(self.síťKaretní.GetmacAdresa())
	rám.ethernetTypbe = Unsignedinteger16r(ethernetTypbe)

	rám.Nastavitbuffer(buffer_2)
	var zdroj_2 [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))

	var i uint32 = 0
	for i = 0; i < velikost; i++ {
		buffer2_2[uint32(rámheaderVelikost)+i] = zdroj_2[i]

	}

	var odkaz_na_adresu uintptr = uintptr(Pointer(&buffer2_2))

	self.síťKaretní.Poslat(odkaz_na_adresu, velikost+uint32(rámheaderVelikost))

}
func (self *TPoskytovatel_rámců_sítě_se_sdíleným_médiem) GetmacAdresa() uint64 {
	return self.síťKaretní.GetmacAdresa()
}
func (self *TPoskytovatel_rámců_sítě_se_sdíleným_médiem) GetipAdresa() uint64 {
	return self.síťKaretní.GetipAdresa()
}
