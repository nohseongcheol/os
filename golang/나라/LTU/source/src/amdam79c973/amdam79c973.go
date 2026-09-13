package amdam79c973

import . "unsafe"
import . "pertraukimas"
import . "console"
import . "prievadas"
import . "pci"

var tinklasKortųconsole TConsole = TConsole{}

type TInitializationBlokas struct {
	rEŽIMAS			uint16
	skaičiusSiųstibuffer	uint8
	skaičiusrecvbuffer	uint8

	physicaladdress	uint64

	loginėsaddress			uint64
	recvbufferAprašymasaddress	uintptr
	siųstibufferAprašymasaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	parametrai	uint32
	parametrai2	uint32
	prieinama	uint32
}

type IRawdatahandler interface {
	Įjungtarawdatareceive(dataRodyklė uintptr, dydis int) bool
	Siųsti(dataRodyklė uintptr, dydis uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Nustatytabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Įjungtarawdatareceive(dataRodyklė uintptr, dydis int) bool {
	tinklasKortųconsole.MSpausdintixy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Siųsti(dataRodyklė uintptr, dydis uint32) {
	tinklasKortųconsole.MSpausdintixy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Siųsti(dataRodyklė, dydis)
}

var Macaddress0Prievadas uint16
var Macaddress2Prievadas uint16
var Macaddress4Prievadas uint16
var registerdataPrievadas uint16
var registeraddressPrievadas uint16
var atstatytiPrievadas uint16
var busValdymasregisterdataPrievadas uint16

var initBlokas TInitializationBlokas

var siųstibufferAprašymas [8]TBufferdescriptor
var siųstibufferAprašymasAtmintis [2048 + 15]byte
var siųstibuffer [2*1024 + 15][8]uint8
var dabartinisSiųstibuffer uint8

var recvbufferAprašymas [8]TBufferdescriptor
var recvbufferAprašymasAtmintis [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var dabartinisrecvbuffer uint8
var funcReikšmė func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TPertraukimashandler
	įrenginysdescriptor	TPeripheralcomponentinterconnectĮrenginysdescriptor
	pertraukimas		*TPertraukimasmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(pertraukimas *TPertraukimasmanager, įrenginysdescriptor TPeripheralcomponentinterconnectĮrenginysdescriptor, handler IRawdatahandler) {

	self.įrenginysdescriptor = įrenginysdescriptor

	funcReikšmė = (*Tamdam79c973).PozicijaPertraukimas
	var address uintptr
	address = uintptr(Pointer(&funcReikšmė))

	self.Init(uint8(0x20+įrenginysdescriptor.Pertraukimas), uintptr(Pointer(pertraukimas)), address)

	Macaddress0Prievadas = uint16(įrenginysdescriptor.Prievadasbase)
	Macaddress2Prievadas = uint16(įrenginysdescriptor.Prievadasbase) + 0x02
	Macaddress4Prievadas = uint16(įrenginysdescriptor.Prievadasbase) + 0x04
	registerdataPrievadas = uint16(įrenginysdescriptor.Prievadasbase) + 0x10
	registeraddressPrievadas = uint16(įrenginysdescriptor.Prievadasbase) + 0x12
	atstatytiPrievadas = uint16(įrenginysdescriptor.Prievadasbase) + 0x14
	busValdymasregisterdataPrievadas = uint16(įrenginysdescriptor.Prievadasbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	dabartinisSiųstibuffer = 0
	dabartinisrecvbuffer = 0

	var Mac0 uint64 = uint64(PrievadasSkaitymasžodis(Macaddress0Prievadas) % 256)
	var Mac1 uint64 = uint64(PrievadasSkaitymasžodis(Macaddress0Prievadas) / 256)
	var Mac2 uint64 = uint64(PrievadasSkaitymasžodis(Macaddress2Prievadas) % 256)
	var Mac3 uint64 = uint64(PrievadasSkaitymasžodis(Macaddress2Prievadas) / 256)
	var Mac4 uint64 = uint64(PrievadasSkaitymasžodis(Macaddress4Prievadas) % 256)
	var Mac5 uint64 = uint64(PrievadasSkaitymasžodis(Macaddress4Prievadas) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MSpausdintixy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalSpausdinti(uint8(įrenginysdescriptor.Pertraukimas))
	console_2.MSpausdinti(([]byte)("]"))
	console_2.MSpausdinti(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Spausdinti(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Spausdinti(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MSpausdinti(([]byte)("]"))

	PrievadasRašymasžodis(registeraddressPrievadas, 20)
	PrievadasRašymasžodis(busValdymasregisterdataPrievadas, 0x102)

	PrievadasRašymasžodis(registeraddressPrievadas, 0)
	PrievadasRašymasžodis(registerdataPrievadas, 0x04)

	initBlokas.rEŽIMAS = 0x0000
	initBlokas.skaičiusSiųstibuffer = 3
	initBlokas.skaičiusrecvbuffer = 3

	initBlokas.physicaladdress = Mac

	initBlokas.loginėsaddress = 0

	siųstibufferAprašymas = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&siųstibufferAprašymasAtmintis)) + 15) & ^(uintptr)(0xF)))
	initBlokas.siųstibufferAprašymasaddress = uintptr(Pointer(&siųstibufferAprašymas))
	recvbufferAprašymas = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferAprašymasAtmintis)) + 15) & ^(uintptr)(0xF)))
	initBlokas.recvbufferAprašymasaddress = uintptr(Pointer(&recvbufferAprašymas))

	for i := 0; i < 8; i++ {
		siųstibufferAprašymas[i].address_2 = uint32((uintptr(Pointer(&siųstibuffer[i])) + 15) & ^(uintptr(0xF)))
		siųstibufferAprašymas[i].parametrai = 0x7FF | 0xF000
		siųstibufferAprašymas[i].parametrai2 = 0
		siųstibufferAprašymas[i].prieinama = 0

		recvbufferAprašymas[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferAprašymas[i].parametrai = 0xF7FF | 0x80000000

	}

	PrievadasRašymasžodis(registeraddressPrievadas, 1)
	PrievadasRašymasžodis(registerdataPrievadas, uint16(uintptr(Pointer(&initBlokas))&0xFFFF))

	PrievadasRašymasžodis(registeraddressPrievadas, 2)
	PrievadasRašymasžodis(registerdataPrievadas, uint16((uintptr(Pointer(&initBlokas))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Įjungti() {
	PrievadasRašymasžodis(registeraddressPrievadas, 0)
	PrievadasRašymasžodis(registerdataPrievadas, 0x41)

	PrievadasRašymasžodis(registeraddressPrievadas, 4)
	temporary := PrievadasSkaitymasžodis(registerdataPrievadas)
	PrievadasRašymasžodis(registeraddressPrievadas, 4)
	PrievadasRašymasžodis(registerdataPrievadas, temporary|0xC00)

	PrievadasRašymasžodis(registeraddressPrievadas, 0)
	PrievadasRašymasžodis(registerdataPrievadas, 0x42)

}
func (self *Tamdam79c973) Atstatyti() int {
	PrievadasSkaitymasžodis(atstatytiPrievadas)
	PrievadasRašymasžodis(atstatytiPrievadas, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) PozicijaPertraukimas(esp uint32) uint32 {

	PrievadasRašymasžodis(registeraddressPrievadas, 0)
	temporary := uint32(PrievadasSkaitymasžodis(registerdataPrievadas))
	console_2.MSpausdinti(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Spausdinti(esp)
	console_2.MSpausdinti(([]byte)(":"))
	console_2.MUnsignedinteger32Spausdinti(temporary)
	console_2.MSpausdinti(([]byte)(":"))
	console_2.MUnsignedinteger16Spausdinti(count)
	count++
	console_2.MSpausdinti(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MSpausdinti(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MSpausdinti(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MSpausdinti(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MSpausdinti(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MSpausdinti(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MSpausdinti(([]byte)("am79c973 data sent"))
	}

	PrievadasRašymasžodis(registeraddressPrievadas, 0)
	PrievadasRašymasžodis(registerdataPrievadas, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MSpausdinti(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Siųsti(dataRodyklė uintptr, dydis uint32) {
	var siųstidescriptor uint16 = uint16(dabartinisSiųstibuffer)
	dabartinisSiųstibuffer = 0

	if dydis > 1518 {
		dydis = 1518
	}

	var šaltinis_2 [4096]byte = *(*([4096]byte))(Pointer(dataRodyklė))
	var tikslas_2 uint32 = siųstibufferAprašymas[siųstidescriptor].address_2 + dydis - 1

	for i := 0; i < int(dydis); i++ {

		*(*byte)(Pointer(uintptr(tikslas_2))) = šaltinis_2[int(dydis)-i-1]

		tikslas_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataRodyklė))
	console_2.MSpausdintixy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalSpausdinti(data[i])
		console_2.MSpausdinti(([]byte)(":"))
	}
	console_2.MSpausdinti(([]byte)("\n"))

	siųstibufferAprašymas[siųstidescriptor].prieinama = 0
	siųstibufferAprašymas[siųstidescriptor].parametrai2 = 0
	siųstibufferAprašymas[siųstidescriptor].parametrai = 0x8300F000 | uint32((-dydis)&0xFFF)

	PrievadasRašymasžodis(registeraddressPrievadas, 0)
	PrievadasRašymasžodis(registerdataPrievadas, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MSpausdinti(([]byte)(":"))
	console_2.MUnsignedinteger32Spausdinti(uint32(uintptr(Pointer(&siųstibuffer))))
	console_2.MSpausdinti(([]byte)(":"))
	console_2.MHexadecimalSpausdinti(siųstibuffer[0][0])
	console_2.MHexadecimalSpausdinti(siųstibuffer[0][1])
	console_2.MSpausdinti(([]byte)(":"))
	dabartinisrecvbuffer = 0

	for ; (recvbufferAprašymas[dabartinisrecvbuffer].parametrai & 0x80000000) == 0; dabartinisrecvbuffer = (dabartinisrecvbuffer + 1) % 8 {

		if !(recvbufferAprašymas[dabartinisrecvbuffer].parametrai&0x40000000 != 0) && ((recvbufferAprašymas[dabartinisrecvbuffer].parametrai & 0x03000000) == 0x03000000) {
			var dydis uint32 = recvbufferAprašymas[dabartinisrecvbuffer].parametrai & 0xFFF
			if dydis > 64 {
				dydis -= 4
			}

			console_2.MSpausdinti([]byte(" size : ["))
			console_2.MUnsignedinteger32Spausdinti(dydis)
			console_2.MSpausdinti([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferAprašymas[dabartinisrecvbuffer].address_2)))
			var rodyklė_2 uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Įjungtarawdatareceive(rodyklė_2, int(dydis)) {

					console_2.MSpausdintixy(([]byte)("self.Send"), 0, 22)

					self.Siųsti(rodyklė_2, dydis)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalSpausdinti(buffer_2[i])
				console_2.MSpausdinti([]byte(":"))
			}

		}
		recvbufferAprašymas[dabartinisrecvbuffer].parametrai2 = 0
		recvbufferAprašymas[dabartinisrecvbuffer].parametrai = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Nustatytahandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initBlokas.physicaladdress
}
func (self *Tamdam79c973) Nustatytaipaddress(ip uint64) {
	initBlokas.loginėsaddress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initBlokas.loginėsaddress
}
