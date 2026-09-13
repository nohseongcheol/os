package amdam79c973

import . "unsafe"
import . "prerušenie"
import . "konzola"
import . "port"
import . "pci"

var sieťKartovéKonzola TKonzola = TKonzola{}

type TInitializationBlok struct {
	režim			uint16
	čísloPoslaťbuffer	uint8
	číslorecvbuffer		uint8

	physicaladdress	uint64

	logickéaddress			uint64
	recvbufferPopisaddress		uintptr
	poslaťbufferPopisaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	príznaky	uint32
	príznaky2	uint32
	dostupné	uint32
}

type IRawdatahandler interface {
	Zapnutérawdatareceive(dataKurzor uintptr, veľkosť int) bool
	Poslať(dataKurzor uintptr, veľkosť uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (vlastný *TRawdatahandler) Sadabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (vlastný *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (vlastný *TRawdatahandler) Zapnutérawdatareceive(dataKurzor uintptr, veľkosť int) bool {
	sieťKartovéKonzola.MTlačiťxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (vlastný *TRawdatahandler) Poslať(dataKurzor uintptr, veľkosť uint32) {
	sieťKartovéKonzola.MTlačiťxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Poslať(dataKurzor, veľkosť)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var reštartovaťport uint16
var busOvládanieregisterdataport uint16

var initBlok TInitializationBlok

var poslaťbufferPopis [8]TBufferdescriptor
var poslaťbufferPopisPamäť [2048 + 15]byte
var poslaťbuffer [2*1024 + 15][8]uint8
var aktuálnyPoslaťbuffer uint8

var recvbufferPopis [8]TBufferdescriptor
var recvbufferPopisPamäť [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var aktuálnyrecvbuffer uint8
var funcHodnota func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TPrerušeniehandler
	zariadeniedescriptor	TPeripheralcomponentinterconnectZariadeniedescriptor
	prerušenie		*TPrerušeniemanager
	handler			*TRawdatahandler
}

var konzola_2 TKonzola = TKonzola{}
var irawdatahandler IRawdatahandler

func (vlastný *Tamdam79c973) Initdriver(prerušenie *TPrerušeniemanager, zariadeniedescriptor TPeripheralcomponentinterconnectZariadeniedescriptor, handler IRawdatahandler) {

	vlastný.zariadeniedescriptor = zariadeniedescriptor

	funcHodnota = (*Tamdam79c973).UškoPrerušenie
	var address uintptr
	address = uintptr(Pointer(&funcHodnota))

	vlastný.Init(uint8(0x20+zariadeniedescriptor.Prerušenie), uintptr(Pointer(prerušenie)), address)

	Macaddress0port = uint16(zariadeniedescriptor.Portbase)
	Macaddress2port = uint16(zariadeniedescriptor.Portbase) + 0x02
	Macaddress4port = uint16(zariadeniedescriptor.Portbase) + 0x04
	registerdataport = uint16(zariadeniedescriptor.Portbase) + 0x10
	registeraddressport = uint16(zariadeniedescriptor.Portbase) + 0x12
	reštartovaťport = uint16(zariadeniedescriptor.Portbase) + 0x14
	busOvládanieregisterdataport = uint16(zariadeniedescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	aktuálnyPoslaťbuffer = 0
	aktuálnyrecvbuffer = 0

	var Mac0 uint64 = uint64(PortČítanieslovo(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortČítanieslovo(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortČítanieslovo(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortČítanieslovo(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortČítanieslovo(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortČítanieslovo(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konzola_2.MTlačiťxy(([]byte)("[interrupt num : "), 0, 13)
	konzola_2.MHexadecimalTlačiť(uint8(zariadeniedescriptor.Prerušenie))
	konzola_2.MTlačiť(([]byte)("]"))
	konzola_2.MTlačiť(([]byte)("[mac address : "))
	konzola_2.MUnsignedinteger16Tlačiť(uint16(macaddress >> 32))
	konzola_2.MUnsignedinteger32Tlačiť(uint32(macaddress & 0x00000000FFFFFFFF))
	konzola_2.MTlačiť(([]byte)("]"))

	PortZápisslovo(registeraddressport, 20)
	PortZápisslovo(busOvládanieregisterdataport, 0x102)

	PortZápisslovo(registeraddressport, 0)
	PortZápisslovo(registerdataport, 0x04)

	initBlok.režim = 0x0000
	initBlok.čísloPoslaťbuffer = 3
	initBlok.číslorecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logickéaddress = 0

	poslaťbufferPopis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&poslaťbufferPopisPamäť)) + 15) & ^(uintptr)(0xF)))
	initBlok.poslaťbufferPopisaddress = uintptr(Pointer(&poslaťbufferPopis))
	recvbufferPopis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferPopisPamäť)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferPopisaddress = uintptr(Pointer(&recvbufferPopis))

	for i := 0; i < 8; i++ {
		poslaťbufferPopis[i].address_2 = uint32((uintptr(Pointer(&poslaťbuffer[i])) + 15) & ^(uintptr(0xF)))
		poslaťbufferPopis[i].príznaky = 0x7FF | 0xF000
		poslaťbufferPopis[i].príznaky2 = 0
		poslaťbufferPopis[i].dostupné = 0

		recvbufferPopis[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferPopis[i].príznaky = 0xF7FF | 0x80000000

	}

	PortZápisslovo(registeraddressport, 1)
	PortZápisslovo(registerdataport, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PortZápisslovo(registeraddressport, 2)
	PortZápisslovo(registerdataport, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (vlastný *Tamdam79c973) Aktivovať() {
	PortZápisslovo(registeraddressport, 0)
	PortZápisslovo(registerdataport, 0x41)

	PortZápisslovo(registeraddressport, 4)
	temporary := PortČítanieslovo(registerdataport)
	PortZápisslovo(registeraddressport, 4)
	PortZápisslovo(registerdataport, temporary|0xC00)

	PortZápisslovo(registeraddressport, 0)
	PortZápisslovo(registerdataport, 0x42)

}
func (vlastný *Tamdam79c973) Reštartovať() int {
	PortČítanieslovo(reštartovaťport)
	PortZápisslovo(reštartovaťport, 0)
	return 10
}

var count uint16 = 0

func (vlastný *Tamdam79c973) UškoPrerušenie(esp uint32) uint32 {

	PortZápisslovo(registeraddressport, 0)
	temporary := uint32(PortČítanieslovo(registerdataport))
	konzola_2.MTlačiť(([]byte)("interrupt("))
	konzola_2.MUnsignedinteger32Tlačiť(esp)
	konzola_2.MTlačiť(([]byte)(":"))
	konzola_2.MUnsignedinteger32Tlačiť(temporary)
	konzola_2.MTlačiť(([]byte)(":"))
	konzola_2.MUnsignedinteger16Tlačiť(count)
	count++
	konzola_2.MTlačiť(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konzola_2.MTlačiť(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konzola_2.MTlačiť(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konzola_2.MTlačiť(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konzola_2.MTlačiť(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konzola_2.MTlačiť(([]byte)("am79c973 data received"))
		vlastný.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konzola_2.MTlačiť(([]byte)("am79c973 data sent"))
	}

	PortZápisslovo(registeraddressport, 0)
	PortZápisslovo(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konzola_2.MTlačiť(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (vlastný *Tamdam79c973) Poslať(dataKurzor uintptr, veľkosť uint32) {
	var poslaťdescriptor uint16 = uint16(aktuálnyPoslaťbuffer)
	aktuálnyPoslaťbuffer = 0

	if veľkosť > 1518 {
		veľkosť = 1518
	}

	var zdroj_2 [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))
	var cieľ_2 uint32 = poslaťbufferPopis[poslaťdescriptor].address_2 + veľkosť - 1

	for i := 0; i < int(veľkosť); i++ {

		*(*byte)(Pointer(uintptr(cieľ_2))) = zdroj_2[int(veľkosť)-i-1]

		cieľ_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))
	konzola_2.MTlačiťxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konzola_2.MHexadecimalTlačiť(data[i])
		konzola_2.MTlačiť(([]byte)(":"))
	}
	konzola_2.MTlačiť(([]byte)("\n"))

	poslaťbufferPopis[poslaťdescriptor].dostupné = 0
	poslaťbufferPopis[poslaťdescriptor].príznaky2 = 0
	poslaťbufferPopis[poslaťdescriptor].príznaky = 0x8300F000 | uint32((-veľkosť)&0xFFF)

	PortZápisslovo(registeraddressport, 0)
	PortZápisslovo(registerdataport, 0x48)

}
func (vlastný *Tamdam79c973) Receive() {
	konzola_2.MTlačiť(([]byte)(":"))
	konzola_2.MUnsignedinteger32Tlačiť(uint32(uintptr(Pointer(&poslaťbuffer))))
	konzola_2.MTlačiť(([]byte)(":"))
	konzola_2.MHexadecimalTlačiť(poslaťbuffer[0][0])
	konzola_2.MHexadecimalTlačiť(poslaťbuffer[0][1])
	konzola_2.MTlačiť(([]byte)(":"))
	aktuálnyrecvbuffer = 0

	for ; (recvbufferPopis[aktuálnyrecvbuffer].príznaky & 0x80000000) == 0; aktuálnyrecvbuffer = (aktuálnyrecvbuffer + 1) % 8 {

		if !(recvbufferPopis[aktuálnyrecvbuffer].príznaky&0x40000000 != 0) && ((recvbufferPopis[aktuálnyrecvbuffer].príznaky & 0x03000000) == 0x03000000) {
			var veľkosť uint32 = recvbufferPopis[aktuálnyrecvbuffer].príznaky & 0xFFF
			if veľkosť > 64 {
				veľkosť -= 4
			}

			konzola_2.MTlačiť([]byte(" size : ["))
			konzola_2.MUnsignedinteger32Tlačiť(veľkosť)
			konzola_2.MTlačiť([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferPopis[aktuálnyrecvbuffer].address_2)))
			var kurzor uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Zapnutérawdatareceive(kurzor, int(veľkosť)) {

					konzola_2.MTlačiťxy(([]byte)("self.Send"), 0, 22)

					vlastný.Poslať(kurzor, veľkosť)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konzola_2.MHexadecimalTlačiť(buffer_2[i])
				konzola_2.MTlačiť([]byte(":"))
			}

		}
		recvbufferPopis[aktuálnyrecvbuffer].príznaky2 = 0
		recvbufferPopis[aktuálnyrecvbuffer].príznaky = 0x8000F7FF
	}
}
func (vlastný *Tamdam79c973) Sadahandler(handler *TRawdatahandler) {
	vlastný.handler = handler
}
func (vlastný *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (vlastný *Tamdam79c973) Sadaipaddress(ip uint64) {
	initBlok.logickéaddress = ip
}
func (vlastný *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logickéaddress
}
