/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "intrerupere"
import . "console"
import . "port"
import . "pci"

var rețeaCărțiconsole TConsole = TConsole{}

type TInitializationBloc struct {
	mOD			uint16
	numărTrimitebuffer	uint8
	numărrecvbuffer		uint8

	physicaladdress	uint64

	logicaddress			uint64
	recvbufferDescriereaddress	uintptr
	trimitebufferDescriereaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	indicatori	uint32
	indicatori2	uint32
	disponibil	uint32
}

type IRawdatahandler interface {
	Pornitrawdatareceive(dataIndicator uintptr, mărime int) bool
	Trimite(dataIndicator uintptr, mărime uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (sine *TRawdatahandler) Definitbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (sine *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (sine *TRawdatahandler) Pornitrawdatareceive(dataIndicator uintptr, mărime int) bool {
	rețeaCărțiconsole.MTipăreștexy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (sine *TRawdatahandler) Trimite(dataIndicator uintptr, mărime uint32) {
	rețeaCărțiconsole.MTipăreștexy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Trimite(dataIndicator, mărime)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var restabileșteport uint16
var buscontrolregisterdataport uint16

var initBloc TInitializationBloc

var trimitebufferDescriere [8]TBufferdescriptor
var trimitebufferDescriereMemorie [2048 + 15]byte
var trimitebuffer [2*1024 + 15][8]uint8
var curentăTrimitebuffer uint8

var recvbufferDescriere [8]TBufferdescriptor
var recvbufferDescriereMemorie [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var curentărecvbuffer uint8
var funcValoare func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TIntreruperehandler
	dispozitivdescriptor	TPeripheralcomponentinterconnectDispozitivdescriptor
	intrerupere		*TIntreruperemanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (sine *Tamdam79c973) Initdriver(intrerupere *TIntreruperemanager, dispozitivdescriptor TPeripheralcomponentinterconnectDispozitivdescriptor, handler IRawdatahandler) {

	sine.dispozitivdescriptor = dispozitivdescriptor

	funcValoare = (*Tamdam79c973).MânerIntrerupere
	var address uintptr
	address = uintptr(Pointer(&funcValoare))

	sine.Init(uint8(0x20+dispozitivdescriptor.Intrerupere), uintptr(Pointer(intrerupere)), address)

	Macaddress0port = uint16(dispozitivdescriptor.Portbase)
	Macaddress2port = uint16(dispozitivdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(dispozitivdescriptor.Portbase) + 0x04
	registerdataport = uint16(dispozitivdescriptor.Portbase) + 0x10
	registeraddressport = uint16(dispozitivdescriptor.Portbase) + 0x12
	restabileșteport = uint16(dispozitivdescriptor.Portbase) + 0x14
	buscontrolregisterdataport = uint16(dispozitivdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	curentăTrimitebuffer = 0
	curentărecvbuffer = 0

	var Mac0 uint64 = uint64(PortCitirecuvânt(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortCitirecuvânt(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortCitirecuvânt(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortCitirecuvânt(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortCitirecuvânt(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortCitirecuvânt(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MTipăreștexy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalTipărește(uint8(dispozitivdescriptor.Intrerupere))
	console_2.MTipărește(([]byte)("]"))
	console_2.MTipărește(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Tipărește(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Tipărește(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MTipărește(([]byte)("]"))

	PortScrierecuvânt(registeraddressport, 20)
	PortScrierecuvânt(buscontrolregisterdataport, 0x102)

	PortScrierecuvânt(registeraddressport, 0)
	PortScrierecuvânt(registerdataport, 0x04)

	initBloc.mOD = 0x0000
	initBloc.numărTrimitebuffer = 3
	initBloc.numărrecvbuffer = 3

	initBloc.physicaladdress = Mac

	initBloc.logicaddress = 0

	trimitebufferDescriere = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&trimitebufferDescriereMemorie)) + 15) & ^(uintptr)(0xF)))
	initBloc.trimitebufferDescriereaddress = uintptr(Pointer(&trimitebufferDescriere))
	recvbufferDescriere = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferDescriereMemorie)) + 15) & ^(uintptr)(0xF)))
	initBloc.recvbufferDescriereaddress = uintptr(Pointer(&recvbufferDescriere))

	for i := 0; i < 8; i++ {
		trimitebufferDescriere[i].address_2 = uint32((uintptr(Pointer(&trimitebuffer[i])) + 15) & ^(uintptr(0xF)))
		trimitebufferDescriere[i].indicatori = 0x7FF | 0xF000
		trimitebufferDescriere[i].indicatori2 = 0
		trimitebufferDescriere[i].disponibil = 0

		recvbufferDescriere[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferDescriere[i].indicatori = 0xF7FF | 0x80000000

	}

	PortScrierecuvânt(registeraddressport, 1)
	PortScrierecuvânt(registerdataport, uint16(uintptr(Pointer(&initBloc))&0xFFFF))

	PortScrierecuvânt(registeraddressport, 2)
	PortScrierecuvânt(registerdataport, uint16((uintptr(Pointer(&initBloc))>>16)&0xFFFF))

}
func (sine *Tamdam79c973) Activează() {
	PortScrierecuvânt(registeraddressport, 0)
	PortScrierecuvânt(registerdataport, 0x41)

	PortScrierecuvânt(registeraddressport, 4)
	temporary := PortCitirecuvânt(registerdataport)
	PortScrierecuvânt(registeraddressport, 4)
	PortScrierecuvânt(registerdataport, temporary|0xC00)

	PortScrierecuvânt(registeraddressport, 0)
	PortScrierecuvânt(registerdataport, 0x42)

}
func (sine *Tamdam79c973) Restabilește() int {
	PortCitirecuvânt(restabileșteport)
	PortScrierecuvânt(restabileșteport, 0)
	return 10
}

var count uint16 = 0

func (sine *Tamdam79c973) MânerIntrerupere(esp uint32) uint32 {

	PortScrierecuvânt(registeraddressport, 0)
	temporary := uint32(PortCitirecuvânt(registerdataport))
	console_2.MTipărește(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Tipărește(esp)
	console_2.MTipărește(([]byte)(":"))
	console_2.MUnsignedinteger32Tipărește(temporary)
	console_2.MTipărește(([]byte)(":"))
	console_2.MUnsignedinteger16Tipărește(count)
	count++
	console_2.MTipărește(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MTipărește(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MTipărește(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MTipărește(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MTipărește(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MTipărește(([]byte)("am79c973 data received"))
		sine.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MTipărește(([]byte)("am79c973 data sent"))
	}

	PortScrierecuvânt(registeraddressport, 0)
	PortScrierecuvânt(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MTipărește(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (sine *Tamdam79c973) Trimite(dataIndicator uintptr, mărime uint32) {
	var trimitedescriptor uint16 = uint16(curentăTrimitebuffer)
	curentăTrimitebuffer = 0

	if mărime > 1518 {
		mărime = 1518
	}

	var sursă_2 [4096]byte = *(*([4096]byte))(Pointer(dataIndicator))
	var destinație_2 uint32 = trimitebufferDescriere[trimitedescriptor].address_2 + mărime - 1

	for i := 0; i < int(mărime); i++ {

		*(*byte)(Pointer(uintptr(destinație_2))) = sursă_2[int(mărime)-i-1]

		destinație_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataIndicator))
	console_2.MTipăreștexy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalTipărește(data[i])
		console_2.MTipărește(([]byte)(":"))
	}
	console_2.MTipărește(([]byte)("\n"))

	trimitebufferDescriere[trimitedescriptor].disponibil = 0
	trimitebufferDescriere[trimitedescriptor].indicatori2 = 0
	trimitebufferDescriere[trimitedescriptor].indicatori = 0x8300F000 | uint32((-mărime)&0xFFF)

	PortScrierecuvânt(registeraddressport, 0)
	PortScrierecuvânt(registerdataport, 0x48)

}
func (sine *Tamdam79c973) Receive() {
	console_2.MTipărește(([]byte)(":"))
	console_2.MUnsignedinteger32Tipărește(uint32(uintptr(Pointer(&trimitebuffer))))
	console_2.MTipărește(([]byte)(":"))
	console_2.MHexadecimalTipărește(trimitebuffer[0][0])
	console_2.MHexadecimalTipărește(trimitebuffer[0][1])
	console_2.MTipărește(([]byte)(":"))
	curentărecvbuffer = 0

	for ; (recvbufferDescriere[curentărecvbuffer].indicatori & 0x80000000) == 0; curentărecvbuffer = (curentărecvbuffer + 1) % 8 {

		if !(recvbufferDescriere[curentărecvbuffer].indicatori&0x40000000 != 0) && ((recvbufferDescriere[curentărecvbuffer].indicatori & 0x03000000) == 0x03000000) {
			var mărime uint32 = recvbufferDescriere[curentărecvbuffer].indicatori & 0xFFF
			if mărime > 64 {
				mărime -= 4
			}

			console_2.MTipărește([]byte(" size : ["))
			console_2.MUnsignedinteger32Tipărește(mărime)
			console_2.MTipărește([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferDescriere[curentărecvbuffer].address_2)))
			var indicator uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Pornitrawdatareceive(indicator, int(mărime)) {

					console_2.MTipăreștexy(([]byte)("self.Send"), 0, 22)

					sine.Trimite(indicator, mărime)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalTipărește(buffer_2[i])
				console_2.MTipărește([]byte(":"))
			}

		}
		recvbufferDescriere[curentărecvbuffer].indicatori2 = 0
		recvbufferDescriere[curentărecvbuffer].indicatori = 0x8000F7FF
	}
}
func (sine *Tamdam79c973) Definithandler(handler *TRawdatahandler) {
	sine.handler = handler
}
func (sine *Tamdam79c973) Getmacaddress() uint64 {

	return initBloc.physicaladdress
}
func (sine *Tamdam79c973) Definitipaddress(ip uint64) {
	initBloc.logicaddress = ip
}
func (sine *Tamdam79c973) Getipaddress() uint64 {
	return initBloc.logicaddress
}
