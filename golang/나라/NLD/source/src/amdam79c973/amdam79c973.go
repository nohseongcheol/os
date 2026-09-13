package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "poort"
import . "pci"

var netwerkKaartconsole TConsole = TConsole{}

type TInitializationBlok struct {
	modus			uint16
	getalVerzendenbuffer	uint8
	getalrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress				uint64
	recvbufferBeschrijvingaddress		uintptr
	verzendenbufferBeschrijvingaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	vlaggen		uint32
	vlaggen2	uint32
	beschikbaar	uint32
}

type IRawdatahandler interface {
	Aanrawdatareceive(dataMuisaanwijzer uintptr, grootte int) bool
	Verzenden(dataMuisaanwijzer uintptr, grootte uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (zelf *TRawdatahandler) Instellenbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (zelf *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (zelf *TRawdatahandler) Aanrawdatareceive(dataMuisaanwijzer uintptr, grootte int) bool {
	netwerkKaartconsole.MAfdrukkenxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (zelf *TRawdatahandler) Verzenden(dataMuisaanwijzer uintptr, grootte uint32) {
	netwerkKaartconsole.MAfdrukkenxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Verzenden(dataMuisaanwijzer, grootte)
}

var Macaddress0Poort uint16
var Macaddress2Poort uint16
var Macaddress4Poort uint16
var registerdataPoort uint16
var registeraddressPoort uint16
var terugzettenPoort uint16
var busBedieningregisterdataPoort uint16

var initBlok TInitializationBlok

var verzendenbufferBeschrijving [8]TBufferdescriptor
var verzendenbufferBeschrijvingGeheugen [2048 + 15]byte
var verzendenbuffer [2*1024 + 15][8]uint8
var huidigVerzendenbuffer uint8

var recvbufferBeschrijving [8]TBufferdescriptor
var recvbufferBeschrijvingGeheugen [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var huidigrecvbuffer uint8
var funcWaarde func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	apparaatdescriptor	TPeripheralcomponentinterconnectApparaatdescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (zelf *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, apparaatdescriptor TPeripheralcomponentinterconnectApparaatdescriptor, handler IRawdatahandler) {

	zelf.apparaatdescriptor = apparaatdescriptor

	funcWaarde = (*Tamdam79c973).Handgreepinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcWaarde))

	zelf.Init(uint8(0x20+apparaatdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Poort = uint16(apparaatdescriptor.Poortbase)
	Macaddress2Poort = uint16(apparaatdescriptor.Poortbase) + 0x02
	Macaddress4Poort = uint16(apparaatdescriptor.Poortbase) + 0x04
	registerdataPoort = uint16(apparaatdescriptor.Poortbase) + 0x10
	registeraddressPoort = uint16(apparaatdescriptor.Poortbase) + 0x12
	terugzettenPoort = uint16(apparaatdescriptor.Poortbase) + 0x14
	busBedieningregisterdataPoort = uint16(apparaatdescriptor.Poortbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	huidigVerzendenbuffer = 0
	huidigrecvbuffer = 0

	var Mac0 uint64 = uint64(PoortLezenWoord(Macaddress0Poort) % 256)
	var Mac1 uint64 = uint64(PoortLezenWoord(Macaddress0Poort) / 256)
	var Mac2 uint64 = uint64(PoortLezenWoord(Macaddress2Poort) % 256)
	var Mac3 uint64 = uint64(PoortLezenWoord(Macaddress2Poort) / 256)
	var Mac4 uint64 = uint64(PoortLezenWoord(Macaddress4Poort) % 256)
	var Mac5 uint64 = uint64(PoortLezenWoord(Macaddress4Poort) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MAfdrukkenxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalAfdrukken(uint8(apparaatdescriptor.Interrupt))
	console_2.MAfdrukken(([]byte)("]"))
	console_2.MAfdrukken(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Afdrukken(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Afdrukken(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MAfdrukken(([]byte)("]"))

	PoortSchrijvenWoord(registeraddressPoort, 20)
	PoortSchrijvenWoord(busBedieningregisterdataPoort, 0x102)

	PoortSchrijvenWoord(registeraddressPoort, 0)
	PoortSchrijvenWoord(registerdataPoort, 0x04)

	initBlok.modus = 0x0000
	initBlok.getalVerzendenbuffer = 3
	initBlok.getalrecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logicaladdress = 0

	verzendenbufferBeschrijving = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&verzendenbufferBeschrijvingGeheugen)) + 15) & ^(uintptr)(0xF)))
	initBlok.verzendenbufferBeschrijvingaddress = uintptr(Pointer(&verzendenbufferBeschrijving))
	recvbufferBeschrijving = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferBeschrijvingGeheugen)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferBeschrijvingaddress = uintptr(Pointer(&recvbufferBeschrijving))

	for i := 0; i < 8; i++ {
		verzendenbufferBeschrijving[i].address_2 = uint32((uintptr(Pointer(&verzendenbuffer[i])) + 15) & ^(uintptr(0xF)))
		verzendenbufferBeschrijving[i].vlaggen = 0x7FF | 0xF000
		verzendenbufferBeschrijving[i].vlaggen2 = 0
		verzendenbufferBeschrijving[i].beschikbaar = 0

		recvbufferBeschrijving[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferBeschrijving[i].vlaggen = 0xF7FF | 0x80000000

	}

	PoortSchrijvenWoord(registeraddressPoort, 1)
	PoortSchrijvenWoord(registerdataPoort, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PoortSchrijvenWoord(registeraddressPoort, 2)
	PoortSchrijvenWoord(registerdataPoort, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (zelf *Tamdam79c973) Activeren() {
	PoortSchrijvenWoord(registeraddressPoort, 0)
	PoortSchrijvenWoord(registerdataPoort, 0x41)

	PoortSchrijvenWoord(registeraddressPoort, 4)
	temporary := PoortLezenWoord(registerdataPoort)
	PoortSchrijvenWoord(registeraddressPoort, 4)
	PoortSchrijvenWoord(registerdataPoort, temporary|0xC00)

	PoortSchrijvenWoord(registeraddressPoort, 0)
	PoortSchrijvenWoord(registerdataPoort, 0x42)

}
func (zelf *Tamdam79c973) Terugzetten() int {
	PoortLezenWoord(terugzettenPoort)
	PoortSchrijvenWoord(terugzettenPoort, 0)
	return 10
}

var aantal uint16 = 0

func (zelf *Tamdam79c973) Handgreepinterrupt(esp uint32) uint32 {

	PoortSchrijvenWoord(registeraddressPoort, 0)
	temporary := uint32(PoortLezenWoord(registerdataPoort))
	console_2.MAfdrukken(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Afdrukken(esp)
	console_2.MAfdrukken(([]byte)(":"))
	console_2.MUnsignedinteger32Afdrukken(temporary)
	console_2.MAfdrukken(([]byte)(":"))
	console_2.MUnsignedinteger16Afdrukken(aantal)
	aantal++
	console_2.MAfdrukken(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MAfdrukken(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MAfdrukken(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MAfdrukken(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MAfdrukken(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MAfdrukken(([]byte)("am79c973 data received"))
		zelf.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MAfdrukken(([]byte)("am79c973 data sent"))
	}

	PoortSchrijvenWoord(registeraddressPoort, 0)
	PoortSchrijvenWoord(registerdataPoort, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MAfdrukken(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (zelf *Tamdam79c973) Verzenden(dataMuisaanwijzer uintptr, grootte uint32) {
	var verzendendescriptor uint16 = uint16(huidigVerzendenbuffer)
	huidigVerzendenbuffer = 0

	if grootte > 1518 {
		grootte = 1518
	}

	var bron_2 [4096]byte = *(*([4096]byte))(Pointer(dataMuisaanwijzer))
	var bestemming_2 uint32 = verzendenbufferBeschrijving[verzendendescriptor].address_2 + grootte - 1

	for i := 0; i < int(grootte); i++ {

		*(*byte)(Pointer(uintptr(bestemming_2))) = bron_2[int(grootte)-i-1]

		bestemming_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataMuisaanwijzer))
	console_2.MAfdrukkenxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalAfdrukken(data[i])
		console_2.MAfdrukken(([]byte)(":"))
	}
	console_2.MAfdrukken(([]byte)("\n"))

	verzendenbufferBeschrijving[verzendendescriptor].beschikbaar = 0
	verzendenbufferBeschrijving[verzendendescriptor].vlaggen2 = 0
	verzendenbufferBeschrijving[verzendendescriptor].vlaggen = 0x8300F000 | uint32((-grootte)&0xFFF)

	PoortSchrijvenWoord(registeraddressPoort, 0)
	PoortSchrijvenWoord(registerdataPoort, 0x48)

}
func (zelf *Tamdam79c973) Receive() {
	console_2.MAfdrukken(([]byte)(":"))
	console_2.MUnsignedinteger32Afdrukken(uint32(uintptr(Pointer(&verzendenbuffer))))
	console_2.MAfdrukken(([]byte)(":"))
	console_2.MHexadecimalAfdrukken(verzendenbuffer[0][0])
	console_2.MHexadecimalAfdrukken(verzendenbuffer[0][1])
	console_2.MAfdrukken(([]byte)(":"))
	huidigrecvbuffer = 0

	for ; (recvbufferBeschrijving[huidigrecvbuffer].vlaggen & 0x80000000) == 0; huidigrecvbuffer = (huidigrecvbuffer + 1) % 8 {

		if !(recvbufferBeschrijving[huidigrecvbuffer].vlaggen&0x40000000 != 0) && ((recvbufferBeschrijving[huidigrecvbuffer].vlaggen & 0x03000000) == 0x03000000) {
			var grootte uint32 = recvbufferBeschrijving[huidigrecvbuffer].vlaggen & 0xFFF
			if grootte > 64 {
				grootte -= 4
			}

			console_2.MAfdrukken([]byte(" size : ["))
			console_2.MUnsignedinteger32Afdrukken(grootte)
			console_2.MAfdrukken([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferBeschrijving[huidigrecvbuffer].address_2)))
			var adresverwijzing uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Aanrawdatareceive(adresverwijzing, int(grootte)) {

					console_2.MAfdrukkenxy(([]byte)("self.Send"), 0, 22)

					zelf.Verzenden(adresverwijzing, grootte)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalAfdrukken(buffer_2[i])
				console_2.MAfdrukken([]byte(":"))
			}

		}
		recvbufferBeschrijving[huidigrecvbuffer].vlaggen2 = 0
		recvbufferBeschrijving[huidigrecvbuffer].vlaggen = 0x8000F7FF
	}
}
func (zelf *Tamdam79c973) Instellenhandler(handler *TRawdatahandler) {
	zelf.handler = handler
}
func (zelf *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (zelf *Tamdam79c973) Instellenipaddress(ip uint64) {
	initBlok.logicaladdress = ip
}
func (zelf *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logicaladdress
}
