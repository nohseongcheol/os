/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "prekinitev"
import . "console"
import . "vrata"
import . "pci"

var omrežjecardconsole TConsole = TConsole{}

type TInitializationBlok struct {
	nAČIN			uint16
	številkaPošljibuffer	uint8
	številkarecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferOpisaddress	uintptr
	pošljibufferOpisaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	zastavice	uint32
	zastavice2	uint32
	razpoložljivo	uint32
}

type IRawdatahandler interface {
	Vključenorawdatareceive(dataKazalnik uintptr, velikost int) bool
	Pošlji(dataKazalnik uintptr, velikost uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (sam *TRawdatahandler) Množicabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (sam *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (sam *TRawdatahandler) Vključenorawdatareceive(dataKazalnik uintptr, velikost int) bool {
	omrežjecardconsole.MNatisnixy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (sam *TRawdatahandler) Pošlji(dataKazalnik uintptr, velikost uint32) {
	omrežjecardconsole.MNatisnixy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Pošlji(dataKazalnik, velikost)
}

var Macaddress0Vrata uint16
var Macaddress2Vrata uint16
var Macaddress4Vrata uint16
var registerdataVrata uint16
var registeraddressVrata uint16
var ponastaviVrata uint16
var busNadzorregisterdataVrata uint16

var initBlok TInitializationBlok

var pošljibufferOpis [8]TBufferdescriptor
var pošljibufferOpisPomnilnik [2048 + 15]byte
var pošljibuffer [2*1024 + 15][8]uint8
var currentPošljibuffer uint8

var recvbufferOpis [8]TBufferdescriptor
var recvbufferOpisPomnilnik [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcVrednost func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TPrekinitevhandler
	napravadescriptor	TPeripheralcomponentinterconnectNapravadescriptor
	prekinitev		*TPrekinitevmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (sam *Tamdam79c973) Initdriver(prekinitev *TPrekinitevmanager, napravadescriptor TPeripheralcomponentinterconnectNapravadescriptor, handler IRawdatahandler) {

	sam.napravadescriptor = napravadescriptor

	funcVrednost = (*Tamdam79c973).RočicaPrekinitev
	var address uintptr
	address = uintptr(Pointer(&funcVrednost))

	sam.Init(uint8(0x20+napravadescriptor.Prekinitev), uintptr(Pointer(prekinitev)), address)

	Macaddress0Vrata = uint16(napravadescriptor.Vratabase)
	Macaddress2Vrata = uint16(napravadescriptor.Vratabase) + 0x02
	Macaddress4Vrata = uint16(napravadescriptor.Vratabase) + 0x04
	registerdataVrata = uint16(napravadescriptor.Vratabase) + 0x10
	registeraddressVrata = uint16(napravadescriptor.Vratabase) + 0x12
	ponastaviVrata = uint16(napravadescriptor.Vratabase) + 0x14
	busNadzorregisterdataVrata = uint16(napravadescriptor.Vratabase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentPošljibuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(VrataBranjebeseda(Macaddress0Vrata) % 256)
	var Mac1 uint64 = uint64(VrataBranjebeseda(Macaddress0Vrata) / 256)
	var Mac2 uint64 = uint64(VrataBranjebeseda(Macaddress2Vrata) % 256)
	var Mac3 uint64 = uint64(VrataBranjebeseda(Macaddress2Vrata) / 256)
	var Mac4 uint64 = uint64(VrataBranjebeseda(Macaddress4Vrata) % 256)
	var Mac5 uint64 = uint64(VrataBranjebeseda(Macaddress4Vrata) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MNatisnixy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalNatisni(uint8(napravadescriptor.Prekinitev))
	console_2.MNatisni(([]byte)("]"))
	console_2.MNatisni(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Natisni(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Natisni(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MNatisni(([]byte)("]"))

	VrataPisanjebeseda(registeraddressVrata, 20)
	VrataPisanjebeseda(busNadzorregisterdataVrata, 0x102)

	VrataPisanjebeseda(registeraddressVrata, 0)
	VrataPisanjebeseda(registerdataVrata, 0x04)

	initBlok.nAČIN = 0x0000
	initBlok.številkaPošljibuffer = 3
	initBlok.številkarecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logicaladdress = 0

	pošljibufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&pošljibufferOpisPomnilnik)) + 15) & ^(uintptr)(0xF)))
	initBlok.pošljibufferOpisaddress = uintptr(Pointer(&pošljibufferOpis))
	recvbufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferOpisPomnilnik)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferOpisaddress = uintptr(Pointer(&recvbufferOpis))

	for i := 0; i < 8; i++ {
		pošljibufferOpis[i].address_2 = uint32((uintptr(Pointer(&pošljibuffer[i])) + 15) & ^(uintptr(0xF)))
		pošljibufferOpis[i].zastavice = 0x7FF | 0xF000
		pošljibufferOpis[i].zastavice2 = 0
		pošljibufferOpis[i].razpoložljivo = 0

		recvbufferOpis[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferOpis[i].zastavice = 0xF7FF | 0x80000000

	}

	VrataPisanjebeseda(registeraddressVrata, 1)
	VrataPisanjebeseda(registerdataVrata, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	VrataPisanjebeseda(registeraddressVrata, 2)
	VrataPisanjebeseda(registerdataVrata, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (sam *Tamdam79c973) Omogoči() {
	VrataPisanjebeseda(registeraddressVrata, 0)
	VrataPisanjebeseda(registerdataVrata, 0x41)

	VrataPisanjebeseda(registeraddressVrata, 4)
	temporary := VrataBranjebeseda(registerdataVrata)
	VrataPisanjebeseda(registeraddressVrata, 4)
	VrataPisanjebeseda(registerdataVrata, temporary|0xC00)

	VrataPisanjebeseda(registeraddressVrata, 0)
	VrataPisanjebeseda(registerdataVrata, 0x42)

}
func (sam *Tamdam79c973) Ponastavi() int {
	VrataBranjebeseda(ponastaviVrata)
	VrataPisanjebeseda(ponastaviVrata, 0)
	return 10
}

var count uint16 = 0

func (sam *Tamdam79c973) RočicaPrekinitev(esp uint32) uint32 {

	VrataPisanjebeseda(registeraddressVrata, 0)
	temporary := uint32(VrataBranjebeseda(registerdataVrata))
	console_2.MNatisni(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Natisni(esp)
	console_2.MNatisni(([]byte)(":"))
	console_2.MUnsignedinteger32Natisni(temporary)
	console_2.MNatisni(([]byte)(":"))
	console_2.MUnsignedinteger16Natisni(count)
	count++
	console_2.MNatisni(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MNatisni(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MNatisni(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MNatisni(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MNatisni(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MNatisni(([]byte)("am79c973 data received"))
		sam.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MNatisni(([]byte)("am79c973 data sent"))
	}

	VrataPisanjebeseda(registeraddressVrata, 0)
	VrataPisanjebeseda(registerdataVrata, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MNatisni(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (sam *Tamdam79c973) Pošlji(dataKazalnik uintptr, velikost uint32) {
	var pošljidescriptor uint16 = uint16(currentPošljibuffer)
	currentPošljibuffer = 0

	if velikost > 1518 {
		velikost = 1518
	}

	var vir_2 [4096]byte = *(*([4096]byte))(Pointer(dataKazalnik))
	var cilj_2 uint32 = pošljibufferOpis[pošljidescriptor].address_2 + velikost - 1

	for i := 0; i < int(velikost); i++ {

		*(*byte)(Pointer(uintptr(cilj_2))) = vir_2[int(velikost)-i-1]

		cilj_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKazalnik))
	console_2.MNatisnixy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalNatisni(data[i])
		console_2.MNatisni(([]byte)(":"))
	}
	console_2.MNatisni(([]byte)("\n"))

	pošljibufferOpis[pošljidescriptor].razpoložljivo = 0
	pošljibufferOpis[pošljidescriptor].zastavice2 = 0
	pošljibufferOpis[pošljidescriptor].zastavice = 0x8300F000 | uint32((-velikost)&0xFFF)

	VrataPisanjebeseda(registeraddressVrata, 0)
	VrataPisanjebeseda(registerdataVrata, 0x48)

}
func (sam *Tamdam79c973) Receive() {
	console_2.MNatisni(([]byte)(":"))
	console_2.MUnsignedinteger32Natisni(uint32(uintptr(Pointer(&pošljibuffer))))
	console_2.MNatisni(([]byte)(":"))
	console_2.MHexadecimalNatisni(pošljibuffer[0][0])
	console_2.MHexadecimalNatisni(pošljibuffer[0][1])
	console_2.MNatisni(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferOpis[currentrecvbuffer].zastavice & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferOpis[currentrecvbuffer].zastavice&0x40000000 != 0) && ((recvbufferOpis[currentrecvbuffer].zastavice & 0x03000000) == 0x03000000) {
			var velikost uint32 = recvbufferOpis[currentrecvbuffer].zastavice & 0xFFF
			if velikost > 64 {
				velikost -= 4
			}

			console_2.MNatisni([]byte(" size : ["))
			console_2.MUnsignedinteger32Natisni(velikost)
			console_2.MNatisni([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferOpis[currentrecvbuffer].address_2)))
			var kazalnik uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Vključenorawdatareceive(kazalnik, int(velikost)) {

					console_2.MNatisnixy(([]byte)("self.Send"), 0, 22)

					sam.Pošlji(kazalnik, velikost)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalNatisni(buffer_2[i])
				console_2.MNatisni([]byte(":"))
			}

		}
		recvbufferOpis[currentrecvbuffer].zastavice2 = 0
		recvbufferOpis[currentrecvbuffer].zastavice = 0x8000F7FF
	}
}
func (sam *Tamdam79c973) Množicahandler(handler *TRawdatahandler) {
	sam.handler = handler
}
func (sam *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (sam *Tamdam79c973) Množicaipaddress(ip uint64) {
	initBlok.logicaladdress = ip
}
func (sam *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logicaladdress
}
