/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "port"
import . "pci"

var netværkKortspilconsole TConsole = TConsole{}

type TInitializationBlok struct {
	tilstand	uint16
	talsendbuffer	uint8
	talrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferBeskrivelseaddress	uintptr
	sendbufferBeskrivelseaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flag		uint32
	flag2		uint32
	tilgængelig	uint32
}

type IRawdatahandler interface {
	Tændtrawdatareceive(dataMarkør uintptr, størrelse int) bool
	Send(dataMarkør uintptr, størrelse uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (selv *TRawdatahandler) Satbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (selv *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (selv *TRawdatahandler) Tændtrawdatareceive(dataMarkør uintptr, størrelse int) bool {
	netværkKortspilconsole.MUdskrivxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (selv *TRawdatahandler) Send(dataMarkør uintptr, størrelse uint32) {
	netværkKortspilconsole.MUdskrivxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(dataMarkør, størrelse)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var nulstilport uint16
var busKontrolregisterdataport uint16

var initBlok TInitializationBlok

var sendbufferBeskrivelse [8]TBufferdescriptor
var sendbufferBeskrivelseHukommelse [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var aktivesendbuffer uint8

var recvbufferBeskrivelse [8]TBufferdescriptor
var recvbufferBeskrivelseHukommelse [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var aktiverecvbuffer uint8
var funcVærdi func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	enheddescriptor	TPeripheralcomponentinterconnectEnheddescriptor
	interrupt	*TInterruptmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (selv *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, enheddescriptor TPeripheralcomponentinterconnectEnheddescriptor, handler IRawdatahandler) {

	selv.enheddescriptor = enheddescriptor

	funcVærdi = (*Tamdam79c973).Håndtaginterrupt
	var address uintptr
	address = uintptr(Pointer(&funcVærdi))

	selv.Init(uint8(0x20+enheddescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0port = uint16(enheddescriptor.Portbase)
	Macaddress2port = uint16(enheddescriptor.Portbase) + 0x02
	Macaddress4port = uint16(enheddescriptor.Portbase) + 0x04
	registerdataport = uint16(enheddescriptor.Portbase) + 0x10
	registeraddressport = uint16(enheddescriptor.Portbase) + 0x12
	nulstilport = uint16(enheddescriptor.Portbase) + 0x14
	busKontrolregisterdataport = uint16(enheddescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	aktivesendbuffer = 0
	aktiverecvbuffer = 0

	var Mac0 uint64 = uint64(PortLæseord(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortLæseord(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortLæseord(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortLæseord(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortLæseord(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortLæseord(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MUdskrivxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalUdskriv(uint8(enheddescriptor.Interrupt))
	console_2.MUdskriv(([]byte)("]"))
	console_2.MUdskriv(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Udskriv(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Udskriv(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MUdskriv(([]byte)("]"))

	PortSkriveord(registeraddressport, 20)
	PortSkriveord(busKontrolregisterdataport, 0x102)

	PortSkriveord(registeraddressport, 0)
	PortSkriveord(registerdataport, 0x04)

	initBlok.tilstand = 0x0000
	initBlok.talsendbuffer = 3
	initBlok.talrecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logicaladdress = 0

	sendbufferBeskrivelse = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferBeskrivelseHukommelse)) + 15) & ^(uintptr)(0xF)))
	initBlok.sendbufferBeskrivelseaddress = uintptr(Pointer(&sendbufferBeskrivelse))
	recvbufferBeskrivelse = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferBeskrivelseHukommelse)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferBeskrivelseaddress = uintptr(Pointer(&recvbufferBeskrivelse))

	for i := 0; i < 8; i++ {
		sendbufferBeskrivelse[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferBeskrivelse[i].flag = 0x7FF | 0xF000
		sendbufferBeskrivelse[i].flag2 = 0
		sendbufferBeskrivelse[i].tilgængelig = 0

		recvbufferBeskrivelse[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferBeskrivelse[i].flag = 0xF7FF | 0x80000000

	}

	PortSkriveord(registeraddressport, 1)
	PortSkriveord(registerdataport, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PortSkriveord(registeraddressport, 2)
	PortSkriveord(registerdataport, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (selv *Tamdam79c973) Aktiver() {
	PortSkriveord(registeraddressport, 0)
	PortSkriveord(registerdataport, 0x41)

	PortSkriveord(registeraddressport, 4)
	temporary := PortLæseord(registerdataport)
	PortSkriveord(registeraddressport, 4)
	PortSkriveord(registerdataport, temporary|0xC00)

	PortSkriveord(registeraddressport, 0)
	PortSkriveord(registerdataport, 0x42)

}
func (selv *Tamdam79c973) Nulstil() int {
	PortLæseord(nulstilport)
	PortSkriveord(nulstilport, 0)
	return 10
}

var antal uint16 = 0

func (selv *Tamdam79c973) Håndtaginterrupt(esp uint32) uint32 {

	PortSkriveord(registeraddressport, 0)
	temporary := uint32(PortLæseord(registerdataport))
	console_2.MUdskriv(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Udskriv(esp)
	console_2.MUdskriv(([]byte)(":"))
	console_2.MUnsignedinteger32Udskriv(temporary)
	console_2.MUdskriv(([]byte)(":"))
	console_2.MUnsignedinteger16Udskriv(antal)
	antal++
	console_2.MUdskriv(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MUdskriv(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MUdskriv(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MUdskriv(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MUdskriv(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MUdskriv(([]byte)("am79c973 data received"))
		selv.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MUdskriv(([]byte)("am79c973 data sent"))
	}

	PortSkriveord(registeraddressport, 0)
	PortSkriveord(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MUdskriv(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (selv *Tamdam79c973) Send(dataMarkør uintptr, størrelse uint32) {
	var senddescriptor uint16 = uint16(aktivesendbuffer)
	aktivesendbuffer = 0

	if størrelse > 1518 {
		størrelse = 1518
	}

	var kilde_2 [4096]byte = *(*([4096]byte))(Pointer(dataMarkør))
	var destination_2 uint32 = sendbufferBeskrivelse[senddescriptor].address_2 + størrelse - 1

	for i := 0; i < int(størrelse); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = kilde_2[int(størrelse)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataMarkør))
	console_2.MUdskrivxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalUdskriv(data[i])
		console_2.MUdskriv(([]byte)(":"))
	}
	console_2.MUdskriv(([]byte)("\n"))

	sendbufferBeskrivelse[senddescriptor].tilgængelig = 0
	sendbufferBeskrivelse[senddescriptor].flag2 = 0
	sendbufferBeskrivelse[senddescriptor].flag = 0x8300F000 | uint32((-størrelse)&0xFFF)

	PortSkriveord(registeraddressport, 0)
	PortSkriveord(registerdataport, 0x48)

}
func (selv *Tamdam79c973) Receive() {
	console_2.MUdskriv(([]byte)(":"))
	console_2.MUnsignedinteger32Udskriv(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.MUdskriv(([]byte)(":"))
	console_2.MHexadecimalUdskriv(sendbuffer[0][0])
	console_2.MHexadecimalUdskriv(sendbuffer[0][1])
	console_2.MUdskriv(([]byte)(":"))
	aktiverecvbuffer = 0

	for ; (recvbufferBeskrivelse[aktiverecvbuffer].flag & 0x80000000) == 0; aktiverecvbuffer = (aktiverecvbuffer + 1) % 8 {

		if !(recvbufferBeskrivelse[aktiverecvbuffer].flag&0x40000000 != 0) && ((recvbufferBeskrivelse[aktiverecvbuffer].flag & 0x03000000) == 0x03000000) {
			var størrelse uint32 = recvbufferBeskrivelse[aktiverecvbuffer].flag & 0xFFF
			if størrelse > 64 {
				størrelse -= 4
			}

			console_2.MUdskriv([]byte(" size : ["))
			console_2.MUnsignedinteger32Udskriv(størrelse)
			console_2.MUdskriv([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferBeskrivelse[aktiverecvbuffer].address_2)))
			var markør uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Tændtrawdatareceive(markør, int(størrelse)) {

					console_2.MUdskrivxy(([]byte)("self.Send"), 0, 22)

					selv.Send(markør, størrelse)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalUdskriv(buffer_2[i])
				console_2.MUdskriv([]byte(":"))
			}

		}
		recvbufferBeskrivelse[aktiverecvbuffer].flag2 = 0
		recvbufferBeskrivelse[aktiverecvbuffer].flag = 0x8000F7FF
	}
}
func (selv *Tamdam79c973) Sathandler(handler *TRawdatahandler) {
	selv.handler = handler
}
func (selv *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (selv *Tamdam79c973) Satipaddress(ip uint64) {
	initBlok.logicaladdress = ip
}
func (selv *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logicaladdress
}
