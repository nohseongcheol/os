package amdam79c973

import . "unsafe"
import . "přerušení"
import . "konzole"
import . "port"
import . "pci"

var síťKaretníKonzole TKonzole = TKonzole{}

type TInitializationBlokový struct {
	mÓD			uint16
	čísloPoslatbuffer	uint8
	číslorecvbuffer		uint8

	physicalAdresa	uint64

	logickáAdresa		uint64
	recvbufferPopisAdresa	uintptr
	poslatbufferPopisAdresa	uintptr
}
type TBufferdescriptor struct {
	adresa_2	uint32
	příznaky	uint32
	příznaky2	uint32
	kdispozici	uint32
}

type IRawdatahandler interface {
	Zapnutorawdatareceive(dataKurzor uintptr, velikost int) bool
	Poslat(dataKurzor uintptr, velikost uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Nastavitbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Zapnutorawdatareceive(dataKurzor uintptr, velikost int) bool {
	síťKaretníKonzole.MTisknoutxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Poslat(dataKurzor uintptr, velikost uint32) {
	síťKaretníKonzole.MTisknoutxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Poslat(dataKurzor, velikost)
}

var MacAdresa0port uint16
var MacAdresa2port uint16
var MacAdresa4port uint16
var registerdataport uint16
var registerAdresaport uint16
var inicializovatport uint16
var busOvládáníregisterdataport uint16

var initBlokový TInitializationBlokový

var poslatbufferPopis [8]TBufferdescriptor
var poslatbufferPopisPaměť [2048 + 15]byte
var poslatbuffer [2*1024 + 15][8]uint8
var současnýPoslatbuffer uint8

var recvbufferPopis [8]TBufferdescriptor
var recvbufferPopisPaměť [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var současnýrecvbuffer uint8
var funcHodnota func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TPřerušeníhandler
	zařízenídescriptor	TPeripheralcomponentinterconnectZařízenídescriptor
	přerušení		*TPřerušenímanager
	handler			*TRawdatahandler
}

var konzole_2 TKonzole = TKonzole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(přerušení *TPřerušenímanager, zařízenídescriptor TPeripheralcomponentinterconnectZařízenídescriptor, handler IRawdatahandler) {

	self.zařízenídescriptor = zařízenídescriptor

	funcHodnota = (*Tamdam79c973).ÚchytkaPřerušení
	var adresa uintptr
	adresa = uintptr(Pointer(&funcHodnota))

	self.Init(uint8(0x20+zařízenídescriptor.Přerušení), uintptr(Pointer(přerušení)), adresa)

	MacAdresa0port = uint16(zařízenídescriptor.Portbase)
	MacAdresa2port = uint16(zařízenídescriptor.Portbase) + 0x02
	MacAdresa4port = uint16(zařízenídescriptor.Portbase) + 0x04
	registerdataport = uint16(zařízenídescriptor.Portbase) + 0x10
	registerAdresaport = uint16(zařízenídescriptor.Portbase) + 0x12
	inicializovatport = uint16(zařízenídescriptor.Portbase) + 0x14
	busOvládáníregisterdataport = uint16(zařízenídescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	současnýPoslatbuffer = 0
	současnýrecvbuffer = 0

	var Mac0 uint64 = uint64(PortČteníslovo(MacAdresa0port) % 256)
	var Mac1 uint64 = uint64(PortČteníslovo(MacAdresa0port) / 256)
	var Mac2 uint64 = uint64(PortČteníslovo(MacAdresa2port) % 256)
	var Mac3 uint64 = uint64(PortČteníslovo(MacAdresa2port) / 256)
	var Mac4 uint64 = uint64(PortČteníslovo(MacAdresa4port) % 256)
	var Mac5 uint64 = uint64(PortČteníslovo(MacAdresa4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macAdresa uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konzole_2.MTisknoutxy(([]byte)("[interrupt num : "), 0, 13)
	konzole_2.MHexadecimalTisknout(uint8(zařízenídescriptor.Přerušení))
	konzole_2.MTisknout(([]byte)("]"))
	konzole_2.MTisknout(([]byte)("[mac address : "))
	konzole_2.MUnsignedinteger16Tisknout(uint16(macAdresa >> 32))
	konzole_2.MUnsignedinteger32Tisknout(uint32(macAdresa & 0x00000000FFFFFFFF))
	konzole_2.MTisknout(([]byte)("]"))

	PortZápisslovo(registerAdresaport, 20)
	PortZápisslovo(busOvládáníregisterdataport, 0x102)

	PortZápisslovo(registerAdresaport, 0)
	PortZápisslovo(registerdataport, 0x04)

	initBlokový.mÓD = 0x0000
	initBlokový.čísloPoslatbuffer = 3
	initBlokový.číslorecvbuffer = 3

	initBlokový.physicalAdresa = Mac

	initBlokový.logickáAdresa = 0

	poslatbufferPopis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&poslatbufferPopisPaměť)) + 15) & ^(uintptr)(0xF)))
	initBlokový.poslatbufferPopisAdresa = uintptr(Pointer(&poslatbufferPopis))
	recvbufferPopis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferPopisPaměť)) + 15) & ^(uintptr)(0xF)))
	initBlokový.recvbufferPopisAdresa = uintptr(Pointer(&recvbufferPopis))

	for i := 0; i < 8; i++ {
		poslatbufferPopis[i].adresa_2 = uint32((uintptr(Pointer(&poslatbuffer[i])) + 15) & ^(uintptr(0xF)))
		poslatbufferPopis[i].příznaky = 0x7FF | 0xF000
		poslatbufferPopis[i].příznaky2 = 0
		poslatbufferPopis[i].kdispozici = 0

		recvbufferPopis[i].adresa_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferPopis[i].příznaky = 0xF7FF | 0x80000000

	}

	PortZápisslovo(registerAdresaport, 1)
	PortZápisslovo(registerdataport, uint16(uintptr(Pointer(&initBlokový))&0xFFFF))

	PortZápisslovo(registerAdresaport, 2)
	PortZápisslovo(registerdataport, uint16((uintptr(Pointer(&initBlokový))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aktivovat() {
	PortZápisslovo(registerAdresaport, 0)
	PortZápisslovo(registerdataport, 0x41)

	PortZápisslovo(registerAdresaport, 4)
	temporary := PortČteníslovo(registerdataport)
	PortZápisslovo(registerAdresaport, 4)
	PortZápisslovo(registerdataport, temporary|0xC00)

	PortZápisslovo(registerAdresaport, 0)
	PortZápisslovo(registerdataport, 0x42)

}
func (self *Tamdam79c973) Inicializovat() int {
	PortČteníslovo(inicializovatport)
	PortZápisslovo(inicializovatport, 0)
	return 10
}

var počet uint16 = 0

func (self *Tamdam79c973) ÚchytkaPřerušení(esp uint32) uint32 {

	PortZápisslovo(registerAdresaport, 0)
	temporary := uint32(PortČteníslovo(registerdataport))
	konzole_2.MTisknout(([]byte)("interrupt("))
	konzole_2.MUnsignedinteger32Tisknout(esp)
	konzole_2.MTisknout(([]byte)(":"))
	konzole_2.MUnsignedinteger32Tisknout(temporary)
	konzole_2.MTisknout(([]byte)(":"))
	konzole_2.MUnsignedinteger16Tisknout(počet)
	počet++
	konzole_2.MTisknout(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konzole_2.MTisknout(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konzole_2.MTisknout(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konzole_2.MTisknout(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konzole_2.MTisknout(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konzole_2.MTisknout(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konzole_2.MTisknout(([]byte)("am79c973 data sent"))
	}

	PortZápisslovo(registerAdresaport, 0)
	PortZápisslovo(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konzole_2.MTisknout(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Poslat(dataKurzor uintptr, velikost uint32) {
	var poslatdescriptor uint16 = uint16(současnýPoslatbuffer)
	současnýPoslatbuffer = 0

	if velikost > 1518 {
		velikost = 1518
	}

	var zdroj_2 [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))
	var cíl_2 uint32 = poslatbufferPopis[poslatdescriptor].adresa_2 + velikost - 1

	for i := 0; i < int(velikost); i++ {

		*(*byte)(Pointer(uintptr(cíl_2))) = zdroj_2[int(velikost)-i-1]

		cíl_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))
	konzole_2.MTisknoutxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konzole_2.MHexadecimalTisknout(data[i])
		konzole_2.MTisknout(([]byte)(":"))
	}
	konzole_2.MTisknout(([]byte)("\n"))

	poslatbufferPopis[poslatdescriptor].kdispozici = 0
	poslatbufferPopis[poslatdescriptor].příznaky2 = 0
	poslatbufferPopis[poslatdescriptor].příznaky = 0x8300F000 | uint32((-velikost)&0xFFF)

	PortZápisslovo(registerAdresaport, 0)
	PortZápisslovo(registerdataport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	konzole_2.MTisknout(([]byte)(":"))
	konzole_2.MUnsignedinteger32Tisknout(uint32(uintptr(Pointer(&poslatbuffer))))
	konzole_2.MTisknout(([]byte)(":"))
	konzole_2.MHexadecimalTisknout(poslatbuffer[0][0])
	konzole_2.MHexadecimalTisknout(poslatbuffer[0][1])
	konzole_2.MTisknout(([]byte)(":"))
	současnýrecvbuffer = 0

	for ; (recvbufferPopis[současnýrecvbuffer].příznaky & 0x80000000) == 0; současnýrecvbuffer = (současnýrecvbuffer + 1) % 8 {

		if !(recvbufferPopis[současnýrecvbuffer].příznaky&0x40000000 != 0) && ((recvbufferPopis[současnýrecvbuffer].příznaky & 0x03000000) == 0x03000000) {
			var velikost uint32 = recvbufferPopis[současnýrecvbuffer].příznaky & 0xFFF
			if velikost > 64 {
				velikost -= 4
			}

			konzole_2.MTisknout([]byte(" size : ["))
			konzole_2.MUnsignedinteger32Tisknout(velikost)
			konzole_2.MTisknout([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferPopis[současnýrecvbuffer].adresa_2)))
			var odkaz_na_adresu uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Zapnutorawdatareceive(odkaz_na_adresu, int(velikost)) {

					konzole_2.MTisknoutxy(([]byte)("self.Send"), 0, 22)

					self.Poslat(odkaz_na_adresu, velikost)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konzole_2.MHexadecimalTisknout(buffer_2[i])
				konzole_2.MTisknout([]byte(":"))
			}

		}
		recvbufferPopis[současnýrecvbuffer].příznaky2 = 0
		recvbufferPopis[současnýrecvbuffer].příznaky = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Nastavithandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) GetmacAdresa() uint64 {

	return initBlokový.physicalAdresa
}
func (self *Tamdam79c973) NastavitipAdresa(ip uint64) {
	initBlokový.logickáAdresa = ip
}
func (self *Tamdam79c973) GetipAdresa() uint64 {
	return initBlokový.logickáAdresa
}
