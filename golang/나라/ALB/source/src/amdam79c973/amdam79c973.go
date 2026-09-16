/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "interrupt"
import . "konsolë"
import . "porta"
import . "pci"

var rrjetiLetraKonsolë TKonsolë = TKonsolë{}

type TInitializationblock struct {
	mënyrë			uint16
	numberDërgobuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferPërshkrimiaddress	uintptr
	dërgobufferPërshkrimiaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flamurka	uint32
	flamurka2	uint32
	nëdispozicion	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(dataKursori uintptr, madhësia int) bool
	Dërgo(dataKursori uintptr, madhësia uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (vetvetja *TRawdatahandler) Caktonibackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (vetvetja *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (vetvetja *TRawdatahandler) Onrawdatareceive(dataKursori uintptr, madhësia int) bool {
	rrjetiLetraKonsolë.MPrintoxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (vetvetja *TRawdatahandler) Dërgo(dataKursori uintptr, madhësia uint32) {
	rrjetiLetraKonsolë.MPrintoxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Dërgo(dataKursori, madhësia)
}

var Macaddress0Porta uint16
var Macaddress2Porta uint16
var Macaddress4Porta uint16
var registerdataPorta uint16
var registeraddressPorta uint16
var ngafillimiPorta uint16
var buscontrolregisterdataPorta uint16

var initblock TInitializationblock

var dërgobufferPërshkrimi [8]TBufferdescriptor
var dërgobufferPërshkrimiMemoria [2048 + 15]byte
var dërgobuffer [2*1024 + 15][8]uint8
var etanishmeDërgobuffer uint8

var recvbufferPërshkrimi [8]TBufferdescriptor
var recvbufferPërshkrimiMemoria [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var etanishmerecvbuffer uint8
var funcVlera func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	dispozitividescriptor	TPeripheralcomponentinterconnectDispozitividescriptor
	interrupt		*TInterruptManazhuesi
	handler			*TRawdatahandler
}

var konsolë_2 TKonsolë = TKonsolë{}
var irawdatahandler IRawdatahandler

func (vetvetja *Tamdam79c973) Initdriver(interrupt *TInterruptManazhuesi, dispozitividescriptor TPeripheralcomponentinterconnectDispozitividescriptor, handler IRawdatahandler) {

	vetvetja.dispozitividescriptor = dispozitividescriptor

	funcVlera = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcVlera))

	vetvetja.Init(uint8(0x20+dispozitividescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Porta = uint16(dispozitividescriptor.Portabase)
	Macaddress2Porta = uint16(dispozitividescriptor.Portabase) + 0x02
	Macaddress4Porta = uint16(dispozitividescriptor.Portabase) + 0x04
	registerdataPorta = uint16(dispozitividescriptor.Portabase) + 0x10
	registeraddressPorta = uint16(dispozitividescriptor.Portabase) + 0x12
	ngafillimiPorta = uint16(dispozitividescriptor.Portabase) + 0x14
	buscontrolregisterdataPorta = uint16(dispozitividescriptor.Portabase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	etanishmeDërgobuffer = 0
	etanishmerecvbuffer = 0

	var Mac0 uint64 = uint64(PortaLeximiFjalë(Macaddress0Porta) % 256)
	var Mac1 uint64 = uint64(PortaLeximiFjalë(Macaddress0Porta) / 256)
	var Mac2 uint64 = uint64(PortaLeximiFjalë(Macaddress2Porta) % 256)
	var Mac3 uint64 = uint64(PortaLeximiFjalë(Macaddress2Porta) / 256)
	var Mac4 uint64 = uint64(PortaLeximiFjalë(Macaddress4Porta) % 256)
	var Mac5 uint64 = uint64(PortaLeximiFjalë(Macaddress4Porta) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konsolë_2.MPrintoxy(([]byte)("[interrupt num : "), 0, 13)
	konsolë_2.MHexadecimalPrinto(uint8(dispozitividescriptor.Interrupt))
	konsolë_2.MPrinto(([]byte)("]"))
	konsolë_2.MPrinto(([]byte)("[mac address : "))
	konsolë_2.MUnsignedinteger16Printo(uint16(macaddress >> 32))
	konsolë_2.MUnsignedinteger32Printo(uint32(macaddress & 0x00000000FFFFFFFF))
	konsolë_2.MPrinto(([]byte)("]"))

	PortaShkrimiFjalë(registeraddressPorta, 20)
	PortaShkrimiFjalë(buscontrolregisterdataPorta, 0x102)

	PortaShkrimiFjalë(registeraddressPorta, 0)
	PortaShkrimiFjalë(registerdataPorta, 0x04)

	initblock.mënyrë = 0x0000
	initblock.numberDërgobuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	dërgobufferPërshkrimi = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&dërgobufferPërshkrimiMemoria)) + 15) & ^(uintptr)(0xF)))
	initblock.dërgobufferPërshkrimiaddress = uintptr(Pointer(&dërgobufferPërshkrimi))
	recvbufferPërshkrimi = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferPërshkrimiMemoria)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferPërshkrimiaddress = uintptr(Pointer(&recvbufferPërshkrimi))

	for i := 0; i < 8; i++ {
		dërgobufferPërshkrimi[i].address_2 = uint32((uintptr(Pointer(&dërgobuffer[i])) + 15) & ^(uintptr(0xF)))
		dërgobufferPërshkrimi[i].flamurka = 0x7FF | 0xF000
		dërgobufferPërshkrimi[i].flamurka2 = 0
		dërgobufferPërshkrimi[i].nëdispozicion = 0

		recvbufferPërshkrimi[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferPërshkrimi[i].flamurka = 0xF7FF | 0x80000000

	}

	PortaShkrimiFjalë(registeraddressPorta, 1)
	PortaShkrimiFjalë(registerdataPorta, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	PortaShkrimiFjalë(registeraddressPorta, 2)
	PortaShkrimiFjalë(registerdataPorta, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (vetvetja *Tamdam79c973) Aktivo() {
	PortaShkrimiFjalë(registeraddressPorta, 0)
	PortaShkrimiFjalë(registerdataPorta, 0x41)

	PortaShkrimiFjalë(registeraddressPorta, 4)
	temporary := PortaLeximiFjalë(registerdataPorta)
	PortaShkrimiFjalë(registeraddressPorta, 4)
	PortaShkrimiFjalë(registerdataPorta, temporary|0xC00)

	PortaShkrimiFjalë(registeraddressPorta, 0)
	PortaShkrimiFjalë(registerdataPorta, 0x42)

}
func (vetvetja *Tamdam79c973) Ngafillimi() int {
	PortaLeximiFjalë(ngafillimiPorta)
	PortaShkrimiFjalë(ngafillimiPorta, 0)
	return 10
}

var count uint16 = 0

func (vetvetja *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	PortaShkrimiFjalë(registeraddressPorta, 0)
	temporary := uint32(PortaLeximiFjalë(registerdataPorta))
	konsolë_2.MPrinto(([]byte)("interrupt("))
	konsolë_2.MUnsignedinteger32Printo(esp)
	konsolë_2.MPrinto(([]byte)(":"))
	konsolë_2.MUnsignedinteger32Printo(temporary)
	konsolë_2.MPrinto(([]byte)(":"))
	konsolë_2.MUnsignedinteger16Printo(count)
	count++
	konsolë_2.MPrinto(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konsolë_2.MPrinto(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konsolë_2.MPrinto(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konsolë_2.MPrinto(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konsolë_2.MPrinto(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konsolë_2.MPrinto(([]byte)("am79c973 data received"))
		vetvetja.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konsolë_2.MPrinto(([]byte)("am79c973 data sent"))
	}

	PortaShkrimiFjalë(registeraddressPorta, 0)
	PortaShkrimiFjalë(registerdataPorta, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konsolë_2.MPrinto(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (vetvetja *Tamdam79c973) Dërgo(dataKursori uintptr, madhësia uint32) {
	var dërgodescriptor uint16 = uint16(etanishmeDërgobuffer)
	etanishmeDërgobuffer = 0

	if madhësia > 1518 {
		madhësia = 1518
	}

	var burimi_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursori))
	var destinacioni_2 uint32 = dërgobufferPërshkrimi[dërgodescriptor].address_2 + madhësia - 1

	for i := 0; i < int(madhësia); i++ {

		*(*byte)(Pointer(uintptr(destinacioni_2))) = burimi_2[int(madhësia)-i-1]

		destinacioni_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKursori))
	konsolë_2.MPrintoxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konsolë_2.MHexadecimalPrinto(data[i])
		konsolë_2.MPrinto(([]byte)(":"))
	}
	konsolë_2.MPrinto(([]byte)("\n"))

	dërgobufferPërshkrimi[dërgodescriptor].nëdispozicion = 0
	dërgobufferPërshkrimi[dërgodescriptor].flamurka2 = 0
	dërgobufferPërshkrimi[dërgodescriptor].flamurka = 0x8300F000 | uint32((-madhësia)&0xFFF)

	PortaShkrimiFjalë(registeraddressPorta, 0)
	PortaShkrimiFjalë(registerdataPorta, 0x48)

}
func (vetvetja *Tamdam79c973) Receive() {
	konsolë_2.MPrinto(([]byte)(":"))
	konsolë_2.MUnsignedinteger32Printo(uint32(uintptr(Pointer(&dërgobuffer))))
	konsolë_2.MPrinto(([]byte)(":"))
	konsolë_2.MHexadecimalPrinto(dërgobuffer[0][0])
	konsolë_2.MHexadecimalPrinto(dërgobuffer[0][1])
	konsolë_2.MPrinto(([]byte)(":"))
	etanishmerecvbuffer = 0

	for ; (recvbufferPërshkrimi[etanishmerecvbuffer].flamurka & 0x80000000) == 0; etanishmerecvbuffer = (etanishmerecvbuffer + 1) % 8 {

		if !(recvbufferPërshkrimi[etanishmerecvbuffer].flamurka&0x40000000 != 0) && ((recvbufferPërshkrimi[etanishmerecvbuffer].flamurka & 0x03000000) == 0x03000000) {
			var madhësia uint32 = recvbufferPërshkrimi[etanishmerecvbuffer].flamurka & 0xFFF
			if madhësia > 64 {
				madhësia -= 4
			}

			konsolë_2.MPrinto([]byte(" size : ["))
			konsolë_2.MUnsignedinteger32Printo(madhësia)
			konsolë_2.MPrinto([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferPërshkrimi[etanishmerecvbuffer].address_2)))
			var kursori uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(kursori, int(madhësia)) {

					konsolë_2.MPrintoxy(([]byte)("self.Send"), 0, 22)

					vetvetja.Dërgo(kursori, madhësia)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konsolë_2.MHexadecimalPrinto(buffer_2[i])
				konsolë_2.MPrinto([]byte(":"))
			}

		}
		recvbufferPërshkrimi[etanishmerecvbuffer].flamurka2 = 0
		recvbufferPërshkrimi[etanishmerecvbuffer].flamurka = 0x8000F7FF
	}
}
func (vetvetja *Tamdam79c973) Caktonihandler(handler *TRawdatahandler) {
	vetvetja.handler = handler
}
func (vetvetja *Tamdam79c973) Getmacaddress() uint64 {

	return initblock.physicaladdress
}
func (vetvetja *Tamdam79c973) Caktoniipaddress(ip uint64) {
	initblock.logicaladdress = ip
}
func (vetvetja *Tamdam79c973) Getipaddress() uint64 {
	return initblock.logicaladdress
}
