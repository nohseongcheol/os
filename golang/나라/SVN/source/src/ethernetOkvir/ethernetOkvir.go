package ethernetOkvir

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetOkvirheaderbuffer struct {
	ciljmacbe	[6]byte
	virmacbe	[6]byte
	ethernetVrstabe	[2]byte
}

var okvirheaderVelikost int = 14

type TEthernetOkvirheader struct {
	ciljmacbe	uint64
	virmacbe	uint64
	ethernetVrstabe	uint16
}

func (sam *TEthernetOkvirheader) Init(buffer_2 TEthernetOkvirheaderbuffer) {
	sam.ciljmacbe = (Poljetounsignedinteger48(buffer_2.ciljmacbe))
	sam.virmacbe = (Poljetounsignedinteger48(buffer_2.virmacbe))
	sam.ethernetVrstabe = (Poljetounsignedinteger16(buffer_2.ethernetVrstabe))

}
func (sam *TEthernetOkvirheader) Množicabuffer(buffer_2 *TEthernetOkvirheaderbuffer) {
	buffer_2.ciljmacbe = Unsignedinteger48toPolje(Unsignedinteger48r(sam.ciljmacbe))
	buffer_2.virmacbe = Unsignedinteger48toPolje(Unsignedinteger48r(sam.virmacbe))
	buffer_2.ethernetVrstabe = Unsignedinteger16toPolje(Unsignedinteger16r(sam.ethernetVrstabe))
}

type IEthernetOkvirhandler interface {
	Init(backend TEthernetOkvirprovider)
	Množicahandler(handler IEthernetOkvirhandler, ethernetVrsta uint16)
	EthernetOkvirreceivewhen(dataKazalnik uintptr, velikost int) bool
	Pošlji(ciljmacbe uint64, dataKazalnik uintptr, velikost uint32)
	OkvirPošlji(ciljmacbe uint64, ethernetVrstabe uint16, dataKazalnik uintptr, velikost uint32)
	Providerget() TEthernetOkvirprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetOkvirhandler struct {
}

var okvir TEthernetOkvirheader
var Backend TEthernetOkvirprovider
var handler_2 [65535]IEthernetOkvirhandler
var efhandler *TEthernetOkvirhandler = nil

func (sam *TEthernetOkvirhandler) Init(backend TEthernetOkvirprovider) {
	Backend = backend
}

func (sam *TEthernetOkvirhandler) Množicahandler(handler IEthernetOkvirhandler, pethernetVrsta uint16) {
	handler_2[pethernetVrsta] = handler
}
func (sam *TEthernetOkvirhandler) Množicabackend(backend TEthernetOkvirprovider) {
	Backend = backend
}
func (sam *TEthernetOkvirhandler) Getbackend() TEthernetOkvirprovider {
	return Backend
}
func (sam *TEthernetOkvirhandler) EthernetOkvirreceivewhen(dataKazalnik uintptr, velikost int) bool {
	ethernetconsole.MNatisni(([]byte)("OnEtherFrameReceived"))
	return false
}
func (sam *TEthernetOkvirhandler) Pošlji(ciljmacbe uint64, dataKazalnik uintptr, velikost uint32) {
	Backend.OkvirPošlji(ciljmacbe, okvir.ethernetVrstabe, dataKazalnik, velikost)
}
func (sam *TEthernetOkvirhandler) OkvirPošlji(ciljmacbe uint64, ethernetVrstabe uint16, dataKazalnik uintptr, velikost uint32) {
	Backend.OkvirPošlji(ciljmacbe, ethernetVrstabe, dataKazalnik, velikost)
}
func (sam *TEthernetOkvirhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (sam *TEthernetOkvirhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (sam *TEthernetOkvirhandler) Providerget() TEthernetOkvirprovider {
	return Backend
}

type TEthernetOkvirrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetOkvirprovider

func (sam *TEthernetOkvirrawdatahandler) Init(pprovider TEthernetOkvirprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (sam *TEthernetOkvirrawdatahandler) Vključenorawdatareceive(dataKazalnik uintptr, velikost int) bool {
	return provider.Vključenorawdatareceive(dataKazalnik, velikost)
}
func (sam *TEthernetOkvirrawdatahandler) Pošlji(dataKazalnik uintptr, velikost uint32) {
	provider.Pošlji(dataKazalnik, velikost)
}
func (sam *TEthernetOkvirrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (sam *TEthernetOkvirrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (sam *TEthernetOkvirrawdatahandler) Providerget() TEthernetOkvirprovider {
	return provider
}

type TEthernetOkvirprovider struct {
	omrežjecard	Tamdam79c973
	handler_2	[65565]IEthernetOkvirhandler
}

func (sam *TEthernetOkvirprovider) Init(backend Tamdam79c973) {

	sam.omrežjecard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		sam.handler_2[i] = nil
	}
}

var count uint16 = 0

func (sam *TEthernetOkvirprovider) Vključenorawdatareceive(dataKazalnik uintptr, velikost int) bool {

	var buffer_2 *TEthernetOkvirheaderbuffer = (*TEthernetOkvirheaderbuffer)(Pointer(dataKazalnik))
	var okvir TEthernetOkvirheader = TEthernetOkvirheader{}
	okvir.Init(*buffer_2)
	var reply bool = false

	if okvir.ciljmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(okvir.ciljmacbe) == sam.Getmacaddress() {
		if handler_2[okvir.ethernetVrstabe] != nil {
			ethernetconsole.MNatisni(([]byte)("provider\n"))

			var kazalnik uintptr = uintptr(Pointer(dataKazalnik)) + uintptr(okvirheaderVelikost)
			reply = handler_2[okvir.ethernetVrstabe].EthernetOkvirreceivewhen(kazalnik, velikost-okvirheaderVelikost)

		}
	}

	if reply {
		okvir.ciljmacbe = okvir.virmacbe
		okvir.virmacbe = Unsignedinteger48r(sam.Getmacaddress())
		okvir.Množicabuffer(buffer_2)

	}

	ethernetconsole.MNatisnixy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Natisni(okvir.virmacbe)
	ethernetconsole.MNatisni(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Natisni(okvir.ciljmacbe)
	ethernetconsole.MNatisni(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Natisni(sam.Getmacaddress())
	ethernetconsole.MNatisni(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Natisni(okvir.ethernetVrstabe)
	ethernetconsole.MNatisni(([]byte)("]"))

	return reply

}
func (sam *TEthernetOkvirprovider) Pošlji(dataKazalnik uintptr, velikost uint32) {
	sam.omrežjecard.Pošlji(dataKazalnik, velikost)
}
func (sam *TEthernetOkvirprovider) OkvirPošlji(ciljmacbe uint64, ethernetVrstabe uint16, dataKazalnik uintptr, velikost uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetOkvirheaderbuffer = (*TEthernetOkvirheaderbuffer)(Pointer(&buffer2_2))

	var okvir TEthernetOkvirheader = TEthernetOkvirheader{}
	okvir.Init(*buffer_2)

	okvir.ciljmacbe = Unsignedinteger48r(ciljmacbe)
	okvir.virmacbe = Unsignedinteger48r(sam.omrežjecard.Getmacaddress())
	okvir.ethernetVrstabe = Unsignedinteger16r(ethernetVrstabe)

	okvir.Množicabuffer(buffer_2)
	var vir_2 [4096]byte = *(*([4096]byte))(Pointer(dataKazalnik))

	var i uint32 = 0
	for i = 0; i < velikost; i++ {
		buffer2_2[uint32(okvirheaderVelikost)+i] = vir_2[i]

	}

	var kazalnik uintptr = uintptr(Pointer(&buffer2_2))

	sam.omrežjecard.Pošlji(kazalnik, velikost+uint32(okvirheaderVelikost))

}
func (sam *TEthernetOkvirprovider) Getmacaddress() uint64 {
	return sam.omrežjecard.Getmacaddress()
}
func (sam *TEthernetOkvirprovider) Getipaddress() uint64 {
	return sam.omrežjecard.Getipaddress()
}
