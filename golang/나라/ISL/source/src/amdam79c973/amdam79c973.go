package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "port"
import . "pci"

var netkerficardconsole TConsole = TConsole{}

type TInitializationBlokk struct {
	hAMUR			uint16
	numberSendabuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferLýsingaddress		uintptr
	sendabufferLýsingaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flags		uint32
	flags2		uint32
	available	uint32
}

type IRawdatahandler interface {
	Notarawdatareceive(dataBendill uintptr, stærð int) bool
	Senda(dataBendill uintptr, stærð uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (sjálft *TRawdatahandler) Setjabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (sjálft *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (sjálft *TRawdatahandler) Notarawdatareceive(dataBendill uintptr, stærð int) bool {
	netkerficardconsole.MPrentaxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (sjálft *TRawdatahandler) Senda(dataBendill uintptr, stærð uint32) {
	netkerficardconsole.MPrentaxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Senda(dataBendill, stærð)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var frumstillaport uint16
var busStýringregisterdataport uint16

var initBlokk TInitializationBlokk

var sendabufferLýsing [8]TBufferdescriptor
var sendabufferLýsingMinni [2048 + 15]byte
var sendabuffer [2*1024 + 15][8]uint8
var núverandiSendabuffer uint8

var recvbufferLýsing [8]TBufferdescriptor
var recvbufferLýsingMinni [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var núverandirecvbuffer uint8
var funcGildi func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	tækidescriptor	TPeripheralcomponentinterconnectTækidescriptor
	interrupt	*TInterruptmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (sjálft *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, tækidescriptor TPeripheralcomponentinterconnectTækidescriptor, handler IRawdatahandler) {

	sjálft.tækidescriptor = tækidescriptor

	funcGildi = (*Tamdam79c973).Haldfanginterrupt
	var address uintptr
	address = uintptr(Pointer(&funcGildi))

	sjálft.Init(uint8(0x20+tækidescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0port = uint16(tækidescriptor.Portbase)
	Macaddress2port = uint16(tækidescriptor.Portbase) + 0x02
	Macaddress4port = uint16(tækidescriptor.Portbase) + 0x04
	registerdataport = uint16(tækidescriptor.Portbase) + 0x10
	registeraddressport = uint16(tækidescriptor.Portbase) + 0x12
	frumstillaport = uint16(tækidescriptor.Portbase) + 0x14
	busStýringregisterdataport = uint16(tækidescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	núverandiSendabuffer = 0
	núverandirecvbuffer = 0

	var Mac0 uint64 = uint64(PortLesturorð(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortLesturorð(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortLesturorð(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortLesturorð(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortLesturorð(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortLesturorð(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MPrentaxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalPrenta(uint8(tækidescriptor.Interrupt))
	console_2.MPrenta(([]byte)("]"))
	console_2.MPrenta(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Prenta(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Prenta(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MPrenta(([]byte)("]"))

	PortSkriftorð(registeraddressport, 20)
	PortSkriftorð(busStýringregisterdataport, 0x102)

	PortSkriftorð(registeraddressport, 0)
	PortSkriftorð(registerdataport, 0x04)

	initBlokk.hAMUR = 0x0000
	initBlokk.numberSendabuffer = 3
	initBlokk.numberrecvbuffer = 3

	initBlokk.physicaladdress = Mac

	initBlokk.logicaladdress = 0

	sendabufferLýsing = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendabufferLýsingMinni)) + 15) & ^(uintptr)(0xF)))
	initBlokk.sendabufferLýsingaddress = uintptr(Pointer(&sendabufferLýsing))
	recvbufferLýsing = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferLýsingMinni)) + 15) & ^(uintptr)(0xF)))
	initBlokk.recvbufferLýsingaddress = uintptr(Pointer(&recvbufferLýsing))

	for i := 0; i < 8; i++ {
		sendabufferLýsing[i].address_2 = uint32((uintptr(Pointer(&sendabuffer[i])) + 15) & ^(uintptr(0xF)))
		sendabufferLýsing[i].flags = 0x7FF | 0xF000
		sendabufferLýsing[i].flags2 = 0
		sendabufferLýsing[i].available = 0

		recvbufferLýsing[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferLýsing[i].flags = 0xF7FF | 0x80000000

	}

	PortSkriftorð(registeraddressport, 1)
	PortSkriftorð(registerdataport, uint16(uintptr(Pointer(&initBlokk))&0xFFFF))

	PortSkriftorð(registeraddressport, 2)
	PortSkriftorð(registerdataport, uint16((uintptr(Pointer(&initBlokk))>>16)&0xFFFF))

}
func (sjálft *Tamdam79c973) Virkja() {
	PortSkriftorð(registeraddressport, 0)
	PortSkriftorð(registerdataport, 0x41)

	PortSkriftorð(registeraddressport, 4)
	temporary := PortLesturorð(registerdataport)
	PortSkriftorð(registeraddressport, 4)
	PortSkriftorð(registerdataport, temporary|0xC00)

	PortSkriftorð(registeraddressport, 0)
	PortSkriftorð(registerdataport, 0x42)

}
func (sjálft *Tamdam79c973) Frumstilla() int {
	PortLesturorð(frumstillaport)
	PortSkriftorð(frumstillaport, 0)
	return 10
}

var count uint16 = 0

func (sjálft *Tamdam79c973) Haldfanginterrupt(esp uint32) uint32 {

	PortSkriftorð(registeraddressport, 0)
	temporary := uint32(PortLesturorð(registerdataport))
	console_2.MPrenta(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Prenta(esp)
	console_2.MPrenta(([]byte)(":"))
	console_2.MUnsignedinteger32Prenta(temporary)
	console_2.MPrenta(([]byte)(":"))
	console_2.MUnsignedinteger16Prenta(count)
	count++
	console_2.MPrenta(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MPrenta(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MPrenta(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MPrenta(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MPrenta(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MPrenta(([]byte)("am79c973 data received"))
		sjálft.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MPrenta(([]byte)("am79c973 data sent"))
	}

	PortSkriftorð(registeraddressport, 0)
	PortSkriftorð(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MPrenta(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (sjálft *Tamdam79c973) Senda(dataBendill uintptr, stærð uint32) {
	var sendadescriptor uint16 = uint16(núverandiSendabuffer)
	núverandiSendabuffer = 0

	if stærð > 1518 {
		stærð = 1518
	}

	var uppruni_2 [4096]byte = *(*([4096]byte))(Pointer(dataBendill))
	var áfangastaður_2 uint32 = sendabufferLýsing[sendadescriptor].address_2 + stærð - 1

	for i := 0; i < int(stærð); i++ {

		*(*byte)(Pointer(uintptr(áfangastaður_2))) = uppruni_2[int(stærð)-i-1]

		áfangastaður_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataBendill))
	console_2.MPrentaxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalPrenta(data[i])
		console_2.MPrenta(([]byte)(":"))
	}
	console_2.MPrenta(([]byte)("\n"))

	sendabufferLýsing[sendadescriptor].available = 0
	sendabufferLýsing[sendadescriptor].flags2 = 0
	sendabufferLýsing[sendadescriptor].flags = 0x8300F000 | uint32((-stærð)&0xFFF)

	PortSkriftorð(registeraddressport, 0)
	PortSkriftorð(registerdataport, 0x48)

}
func (sjálft *Tamdam79c973) Receive() {
	console_2.MPrenta(([]byte)(":"))
	console_2.MUnsignedinteger32Prenta(uint32(uintptr(Pointer(&sendabuffer))))
	console_2.MPrenta(([]byte)(":"))
	console_2.MHexadecimalPrenta(sendabuffer[0][0])
	console_2.MHexadecimalPrenta(sendabuffer[0][1])
	console_2.MPrenta(([]byte)(":"))
	núverandirecvbuffer = 0

	for ; (recvbufferLýsing[núverandirecvbuffer].flags & 0x80000000) == 0; núverandirecvbuffer = (núverandirecvbuffer + 1) % 8 {

		if !(recvbufferLýsing[núverandirecvbuffer].flags&0x40000000 != 0) && ((recvbufferLýsing[núverandirecvbuffer].flags & 0x03000000) == 0x03000000) {
			var stærð uint32 = recvbufferLýsing[núverandirecvbuffer].flags & 0xFFF
			if stærð > 64 {
				stærð -= 4
			}

			console_2.MPrenta([]byte(" size : ["))
			console_2.MUnsignedinteger32Prenta(stærð)
			console_2.MPrenta([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferLýsing[núverandirecvbuffer].address_2)))
			var bendill uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Notarawdatareceive(bendill, int(stærð)) {

					console_2.MPrentaxy(([]byte)("self.Send"), 0, 22)

					sjálft.Senda(bendill, stærð)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalPrenta(buffer_2[i])
				console_2.MPrenta([]byte(":"))
			}

		}
		recvbufferLýsing[núverandirecvbuffer].flags2 = 0
		recvbufferLýsing[núverandirecvbuffer].flags = 0x8000F7FF
	}
}
func (sjálft *Tamdam79c973) Setjahandler(handler *TRawdatahandler) {
	sjálft.handler = handler
}
func (sjálft *Tamdam79c973) Getmacaddress() uint64 {

	return initBlokk.physicaladdress
}
func (sjálft *Tamdam79c973) Setjaipaddress(ip uint64) {
	initBlokk.logicaladdress = ip
}
func (sjálft *Tamdam79c973) Getipaddress() uint64 {
	return initBlokk.logicaladdress
}
