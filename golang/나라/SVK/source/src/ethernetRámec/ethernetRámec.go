package ethernetRámec

import . "konzola"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonzola TKonzola = TKonzola{}

type TEthernetRámecheaderbuffer struct {
	cieľmacbe	[6]byte
	zdrojmacbe	[6]byte
	ethernetTypbe	[2]byte
}

var rámecheaderVeľkosť int = 14

type TEthernetRámecheader struct {
	cieľmacbe	uint64
	zdrojmacbe	uint64
	ethernetTypbe	uint16
}

func (vlastný *TEthernetRámecheader) Init(buffer_2 TEthernetRámecheaderbuffer) {
	vlastný.cieľmacbe = (Poletounsignedinteger48(buffer_2.cieľmacbe))
	vlastný.zdrojmacbe = (Poletounsignedinteger48(buffer_2.zdrojmacbe))
	vlastný.ethernetTypbe = (Poletounsignedinteger16(buffer_2.ethernetTypbe))

}
func (vlastný *TEthernetRámecheader) Sadabuffer(buffer_2 *TEthernetRámecheaderbuffer) {
	buffer_2.cieľmacbe = Unsignedinteger48toPole(Unsignedinteger48r(vlastný.cieľmacbe))
	buffer_2.zdrojmacbe = Unsignedinteger48toPole(Unsignedinteger48r(vlastný.zdrojmacbe))
	buffer_2.ethernetTypbe = Unsignedinteger16toPole(Unsignedinteger16r(vlastný.ethernetTypbe))
}

type IEthernetRámechandler interface {
	Init(backend TEthernetRámecprovider)
	Sadahandler(handler IEthernetRámechandler, ethernetTyp uint16)
	EthernetRámecreceivewhen(dataKurzor uintptr, veľkosť int) bool
	Poslať(cieľmacbe uint64, dataKurzor uintptr, veľkosť uint32)
	RámecPoslať(cieľmacbe uint64, ethernetTypbe uint16, dataKurzor uintptr, veľkosť uint32)
	Providerget() TEthernetRámecprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRámechandler struct {
}

var rámec TEthernetRámecheader
var Backend TEthernetRámecprovider
var handler_2 [65535]IEthernetRámechandler
var efhandler *TEthernetRámechandler = nil

func (vlastný *TEthernetRámechandler) Init(backend TEthernetRámecprovider) {
	Backend = backend
}

func (vlastný *TEthernetRámechandler) Sadahandler(handler IEthernetRámechandler, pethernetTyp uint16) {
	handler_2[pethernetTyp] = handler
}
func (vlastný *TEthernetRámechandler) Sadabackend(backend TEthernetRámecprovider) {
	Backend = backend
}
func (vlastný *TEthernetRámechandler) Getbackend() TEthernetRámecprovider {
	return Backend
}
func (vlastný *TEthernetRámechandler) EthernetRámecreceivewhen(dataKurzor uintptr, veľkosť int) bool {
	ethernetKonzola.MTlačiť(([]byte)("OnEtherFrameReceived"))
	return false
}
func (vlastný *TEthernetRámechandler) Poslať(cieľmacbe uint64, dataKurzor uintptr, veľkosť uint32) {
	Backend.RámecPoslať(cieľmacbe, rámec.ethernetTypbe, dataKurzor, veľkosť)
}
func (vlastný *TEthernetRámechandler) RámecPoslať(cieľmacbe uint64, ethernetTypbe uint16, dataKurzor uintptr, veľkosť uint32) {
	Backend.RámecPoslať(cieľmacbe, ethernetTypbe, dataKurzor, veľkosť)
}
func (vlastný *TEthernetRámechandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (vlastný *TEthernetRámechandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (vlastný *TEthernetRámechandler) Providerget() TEthernetRámecprovider {
	return Backend
}

type TEthernetRámecrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetRámecprovider

func (vlastný *TEthernetRámecrawdatahandler) Init(pprovider TEthernetRámecprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (vlastný *TEthernetRámecrawdatahandler) Zapnutérawdatareceive(dataKurzor uintptr, veľkosť int) bool {
	return provider.Zapnutérawdatareceive(dataKurzor, veľkosť)
}
func (vlastný *TEthernetRámecrawdatahandler) Poslať(dataKurzor uintptr, veľkosť uint32) {
	provider.Poslať(dataKurzor, veľkosť)
}
func (vlastný *TEthernetRámecrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (vlastný *TEthernetRámecrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (vlastný *TEthernetRámecrawdatahandler) Providerget() TEthernetRámecprovider {
	return provider
}

type TEthernetRámecprovider struct {
	sieťKartové	Tamdam79c973
	handler_2	[65565]IEthernetRámechandler
}

func (vlastný *TEthernetRámecprovider) Init(backend Tamdam79c973) {

	vlastný.sieťKartové = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		vlastný.handler_2[i] = nil
	}
}

var count uint16 = 0

func (vlastný *TEthernetRámecprovider) Zapnutérawdatareceive(dataKurzor uintptr, veľkosť int) bool {

	var buffer_2 *TEthernetRámecheaderbuffer = (*TEthernetRámecheaderbuffer)(Pointer(dataKurzor))
	var rámec TEthernetRámecheader = TEthernetRámecheader{}
	rámec.Init(*buffer_2)
	var reply bool = false

	if rámec.cieľmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(rámec.cieľmacbe) == vlastný.Getmacaddress() {
		if handler_2[rámec.ethernetTypbe] != nil {
			ethernetKonzola.MTlačiť(([]byte)("provider\n"))

			var kurzor uintptr = uintptr(Pointer(dataKurzor)) + uintptr(rámecheaderVeľkosť)
			reply = handler_2[rámec.ethernetTypbe].EthernetRámecreceivewhen(kurzor, veľkosť-rámecheaderVeľkosť)

		}
	}

	if reply {
		rámec.cieľmacbe = rámec.zdrojmacbe
		rámec.zdrojmacbe = Unsignedinteger48r(vlastný.Getmacaddress())
		rámec.Sadabuffer(buffer_2)

	}

	ethernetKonzola.MTlačiťxy(([]byte)("spro["), 0, 1)
	ethernetKonzola.MUnsignedinteger64Tlačiť(rámec.zdrojmacbe)
	ethernetKonzola.MTlačiť(([]byte)(":"))
	ethernetKonzola.MUnsignedinteger64Tlačiť(rámec.cieľmacbe)
	ethernetKonzola.MTlačiť(([]byte)(":]["))
	ethernetKonzola.MUnsignedinteger64Tlačiť(vlastný.Getmacaddress())
	ethernetKonzola.MTlačiť(([]byte)(":"))
	ethernetKonzola.MUnsignedinteger16Tlačiť(rámec.ethernetTypbe)
	ethernetKonzola.MTlačiť(([]byte)("]"))

	return reply

}
func (vlastný *TEthernetRámecprovider) Poslať(dataKurzor uintptr, veľkosť uint32) {
	vlastný.sieťKartové.Poslať(dataKurzor, veľkosť)
}
func (vlastný *TEthernetRámecprovider) RámecPoslať(cieľmacbe uint64, ethernetTypbe uint16, dataKurzor uintptr, veľkosť uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRámecheaderbuffer = (*TEthernetRámecheaderbuffer)(Pointer(&buffer2_2))

	var rámec TEthernetRámecheader = TEthernetRámecheader{}
	rámec.Init(*buffer_2)

	rámec.cieľmacbe = Unsignedinteger48r(cieľmacbe)
	rámec.zdrojmacbe = Unsignedinteger48r(vlastný.sieťKartové.Getmacaddress())
	rámec.ethernetTypbe = Unsignedinteger16r(ethernetTypbe)

	rámec.Sadabuffer(buffer_2)
	var zdroj_2 [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))

	var i uint32 = 0
	for i = 0; i < veľkosť; i++ {
		buffer2_2[uint32(rámecheaderVeľkosť)+i] = zdroj_2[i]

	}

	var kurzor uintptr = uintptr(Pointer(&buffer2_2))

	vlastný.sieťKartové.Poslať(kurzor, veľkosť+uint32(rámecheaderVeľkosť))

}
func (vlastný *TEthernetRámecprovider) Getmacaddress() uint64 {
	return vlastný.sieťKartové.Getmacaddress()
}
func (vlastný *TEthernetRámecprovider) Getipaddress() uint64 {
	return vlastný.sieťKartové.Getipaddress()
}
