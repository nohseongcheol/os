package ethernetRammi

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetRammiheaderbuffer struct {
	áfangastaðurmacbe	[6]byte
	upprunimacbe		[6]byte
	ethernetTegundbe	[2]byte
}

var rammiheaderStærð int = 14

type TEthernetRammiheader struct {
	áfangastaðurmacbe	uint64
	upprunimacbe		uint64
	ethernetTegundbe	uint16
}

func (sjálft *TEthernetRammiheader) Init(buffer_2 TEthernetRammiheaderbuffer) {
	sjálft.áfangastaðurmacbe = (Fylkitounsignedinteger48(buffer_2.áfangastaðurmacbe))
	sjálft.upprunimacbe = (Fylkitounsignedinteger48(buffer_2.upprunimacbe))
	sjálft.ethernetTegundbe = (Fylkitounsignedinteger16(buffer_2.ethernetTegundbe))

}
func (sjálft *TEthernetRammiheader) Setjabuffer(buffer_2 *TEthernetRammiheaderbuffer) {
	buffer_2.áfangastaðurmacbe = Unsignedinteger48toFylki(Unsignedinteger48r(sjálft.áfangastaðurmacbe))
	buffer_2.upprunimacbe = Unsignedinteger48toFylki(Unsignedinteger48r(sjálft.upprunimacbe))
	buffer_2.ethernetTegundbe = Unsignedinteger16toFylki(Unsignedinteger16r(sjálft.ethernetTegundbe))
}

type IEthernetRammihandler interface {
	Init(backend TEthernetRammiprovider)
	Setjahandler(handler IEthernetRammihandler, ethernetTegund uint16)
	EthernetRammireceivewhen(dataBendill uintptr, stærð int) bool
	Senda(áfangastaðurmacbe uint64, dataBendill uintptr, stærð uint32)
	RammiSenda(áfangastaðurmacbe uint64, ethernetTegundbe uint16, dataBendill uintptr, stærð uint32)
	Providerget() TEthernetRammiprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRammihandler struct {
}

var rammi TEthernetRammiheader
var Backend TEthernetRammiprovider
var handler_2 [65535]IEthernetRammihandler
var efhandler *TEthernetRammihandler = nil

func (sjálft *TEthernetRammihandler) Init(backend TEthernetRammiprovider) {
	Backend = backend
}

func (sjálft *TEthernetRammihandler) Setjahandler(handler IEthernetRammihandler, pethernetTegund uint16) {
	handler_2[pethernetTegund] = handler
}
func (sjálft *TEthernetRammihandler) Setjabackend(backend TEthernetRammiprovider) {
	Backend = backend
}
func (sjálft *TEthernetRammihandler) Getbackend() TEthernetRammiprovider {
	return Backend
}
func (sjálft *TEthernetRammihandler) EthernetRammireceivewhen(dataBendill uintptr, stærð int) bool {
	ethernetconsole.MPrenta(([]byte)("OnEtherFrameReceived"))
	return false
}
func (sjálft *TEthernetRammihandler) Senda(áfangastaðurmacbe uint64, dataBendill uintptr, stærð uint32) {
	Backend.RammiSenda(áfangastaðurmacbe, rammi.ethernetTegundbe, dataBendill, stærð)
}
func (sjálft *TEthernetRammihandler) RammiSenda(áfangastaðurmacbe uint64, ethernetTegundbe uint16, dataBendill uintptr, stærð uint32) {
	Backend.RammiSenda(áfangastaðurmacbe, ethernetTegundbe, dataBendill, stærð)
}
func (sjálft *TEthernetRammihandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (sjálft *TEthernetRammihandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (sjálft *TEthernetRammihandler) Providerget() TEthernetRammiprovider {
	return Backend
}

type TEthernetRammirawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetRammiprovider

func (sjálft *TEthernetRammirawdatahandler) Init(pprovider TEthernetRammiprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (sjálft *TEthernetRammirawdatahandler) Notarawdatareceive(dataBendill uintptr, stærð int) bool {
	return provider.Notarawdatareceive(dataBendill, stærð)
}
func (sjálft *TEthernetRammirawdatahandler) Senda(dataBendill uintptr, stærð uint32) {
	provider.Senda(dataBendill, stærð)
}
func (sjálft *TEthernetRammirawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (sjálft *TEthernetRammirawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (sjálft *TEthernetRammirawdatahandler) Providerget() TEthernetRammiprovider {
	return provider
}

type TEthernetRammiprovider struct {
	netkerficard	Tamdam79c973
	handler_2	[65565]IEthernetRammihandler
}

func (sjálft *TEthernetRammiprovider) Init(backend Tamdam79c973) {

	sjálft.netkerficard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		sjálft.handler_2[i] = nil
	}
}

var count uint16 = 0

func (sjálft *TEthernetRammiprovider) Notarawdatareceive(dataBendill uintptr, stærð int) bool {

	var buffer_2 *TEthernetRammiheaderbuffer = (*TEthernetRammiheaderbuffer)(Pointer(dataBendill))
	var rammi TEthernetRammiheader = TEthernetRammiheader{}
	rammi.Init(*buffer_2)
	var reply bool = false

	if rammi.áfangastaðurmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(rammi.áfangastaðurmacbe) == sjálft.Getmacaddress() {
		if handler_2[rammi.ethernetTegundbe] != nil {
			ethernetconsole.MPrenta(([]byte)("provider\n"))

			var bendill uintptr = uintptr(Pointer(dataBendill)) + uintptr(rammiheaderStærð)
			reply = handler_2[rammi.ethernetTegundbe].EthernetRammireceivewhen(bendill, stærð-rammiheaderStærð)

		}
	}

	if reply {
		rammi.áfangastaðurmacbe = rammi.upprunimacbe
		rammi.upprunimacbe = Unsignedinteger48r(sjálft.Getmacaddress())
		rammi.Setjabuffer(buffer_2)

	}

	ethernetconsole.MPrentaxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Prenta(rammi.upprunimacbe)
	ethernetconsole.MPrenta(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Prenta(rammi.áfangastaðurmacbe)
	ethernetconsole.MPrenta(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Prenta(sjálft.Getmacaddress())
	ethernetconsole.MPrenta(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Prenta(rammi.ethernetTegundbe)
	ethernetconsole.MPrenta(([]byte)("]"))

	return reply

}
func (sjálft *TEthernetRammiprovider) Senda(dataBendill uintptr, stærð uint32) {
	sjálft.netkerficard.Senda(dataBendill, stærð)
}
func (sjálft *TEthernetRammiprovider) RammiSenda(áfangastaðurmacbe uint64, ethernetTegundbe uint16, dataBendill uintptr, stærð uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRammiheaderbuffer = (*TEthernetRammiheaderbuffer)(Pointer(&buffer2_2))

	var rammi TEthernetRammiheader = TEthernetRammiheader{}
	rammi.Init(*buffer_2)

	rammi.áfangastaðurmacbe = Unsignedinteger48r(áfangastaðurmacbe)
	rammi.upprunimacbe = Unsignedinteger48r(sjálft.netkerficard.Getmacaddress())
	rammi.ethernetTegundbe = Unsignedinteger16r(ethernetTegundbe)

	rammi.Setjabuffer(buffer_2)
	var uppruni_2 [4096]byte = *(*([4096]byte))(Pointer(dataBendill))

	var i uint32 = 0
	for i = 0; i < stærð; i++ {
		buffer2_2[uint32(rammiheaderStærð)+i] = uppruni_2[i]

	}

	var bendill uintptr = uintptr(Pointer(&buffer2_2))

	sjálft.netkerficard.Senda(bendill, stærð+uint32(rammiheaderStærð))

}
func (sjálft *TEthernetRammiprovider) Getmacaddress() uint64 {
	return sjálft.netkerficard.Getmacaddress()
}
func (sjálft *TEthernetRammiprovider) Getipaddress() uint64 {
	return sjálft.netkerficard.Getipaddress()
}
