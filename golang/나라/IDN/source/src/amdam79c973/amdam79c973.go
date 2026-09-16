/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "interupsi"
import . "console"
import . "port"
import . "pci"

var jaringanKartuconsole TConsole = TConsole{}

type TInitializationBlok struct {
	mode			uint16
	nomorKirimbuffer	uint8
	nomorrecvbuffer		uint8

	physicaladdress	uint64

	logikaaddress			uint64
	recvbufferKeteranganaddress	uintptr
	kirimbufferKeteranganaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	tanda		uint32
	tanda2		uint32
	tersedia	uint32
}

type IRawdatahandler interface {
	Hiduprawdatareceive(dataPenunjuk uintptr, ukuran int) bool
	Kirim(dataPenunjuk uintptr, ukuran uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (dirisendiri *TRawdatahandler) Aturbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (dirisendiri *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (dirisendiri *TRawdatahandler) Hiduprawdatareceive(dataPenunjuk uintptr, ukuran int) bool {
	jaringanKartuconsole.MCetakxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (dirisendiri *TRawdatahandler) Kirim(dataPenunjuk uintptr, ukuran uint32) {
	jaringanKartuconsole.MCetakxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Kirim(dataPenunjuk, ukuran)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var aturUlangport uint16
var busKontrolregisterdataport uint16

var initBlok TInitializationBlok

var kirimbufferKeterangan [8]TBufferdescriptor
var kirimbufferKeteranganMemori [2048 + 15]byte
var kirimbuffer [2*1024 + 15][8]uint8
var sekarangKirimbuffer uint8

var recvbufferKeterangan [8]TBufferdescriptor
var recvbufferKeteranganMemori [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var sekarangrecvbuffer uint8
var funcNilai func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterupsihandler
	perangkatdescriptor	TPeripheralcomponentinterconnectPerangkatdescriptor
	interupsi		*TInterupsimanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (dirisendiri *Tamdam79c973) Initdriver(interupsi *TInterupsimanager, perangkatdescriptor TPeripheralcomponentinterconnectPerangkatdescriptor, handler IRawdatahandler) {

	dirisendiri.perangkatdescriptor = perangkatdescriptor

	funcNilai = (*Tamdam79c973).PenangananInterupsi
	var address uintptr
	address = uintptr(Pointer(&funcNilai))

	dirisendiri.Init(uint8(0x20+perangkatdescriptor.Interupsi), uintptr(Pointer(interupsi)), address)

	Macaddress0port = uint16(perangkatdescriptor.Portbase)
	Macaddress2port = uint16(perangkatdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(perangkatdescriptor.Portbase) + 0x04
	registerdataport = uint16(perangkatdescriptor.Portbase) + 0x10
	registeraddressport = uint16(perangkatdescriptor.Portbase) + 0x12
	aturUlangport = uint16(perangkatdescriptor.Portbase) + 0x14
	busKontrolregisterdataport = uint16(perangkatdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	sekarangKirimbuffer = 0
	sekarangrecvbuffer = 0

	var Mac0 uint64 = uint64(PortBacakata(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortBacakata(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortBacakata(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortBacakata(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortBacakata(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortBacakata(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MCetakxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalCetak(uint8(perangkatdescriptor.Interupsi))
	console_2.MCetak(([]byte)("]"))
	console_2.MCetak(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Cetak(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Cetak(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MCetak(([]byte)("]"))

	PortTuliskata(registeraddressport, 20)
	PortTuliskata(busKontrolregisterdataport, 0x102)

	PortTuliskata(registeraddressport, 0)
	PortTuliskata(registerdataport, 0x04)

	initBlok.mode = 0x0000
	initBlok.nomorKirimbuffer = 3
	initBlok.nomorrecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logikaaddress = 0

	kirimbufferKeterangan = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&kirimbufferKeteranganMemori)) + 15) & ^(uintptr)(0xF)))
	initBlok.kirimbufferKeteranganaddress = uintptr(Pointer(&kirimbufferKeterangan))
	recvbufferKeterangan = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferKeteranganMemori)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferKeteranganaddress = uintptr(Pointer(&recvbufferKeterangan))

	for i := 0; i < 8; i++ {
		kirimbufferKeterangan[i].address_2 = uint32((uintptr(Pointer(&kirimbuffer[i])) + 15) & ^(uintptr(0xF)))
		kirimbufferKeterangan[i].tanda = 0x7FF | 0xF000
		kirimbufferKeterangan[i].tanda2 = 0
		kirimbufferKeterangan[i].tersedia = 0

		recvbufferKeterangan[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferKeterangan[i].tanda = 0xF7FF | 0x80000000

	}

	PortTuliskata(registeraddressport, 1)
	PortTuliskata(registerdataport, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PortTuliskata(registeraddressport, 2)
	PortTuliskata(registerdataport, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (dirisendiri *Tamdam79c973) Aktifkan() {
	PortTuliskata(registeraddressport, 0)
	PortTuliskata(registerdataport, 0x41)

	PortTuliskata(registeraddressport, 4)
	temporary := PortBacakata(registerdataport)
	PortTuliskata(registeraddressport, 4)
	PortTuliskata(registerdataport, temporary|0xC00)

	PortTuliskata(registeraddressport, 0)
	PortTuliskata(registerdataport, 0x42)

}
func (dirisendiri *Tamdam79c973) AturUlang() int {
	PortBacakata(aturUlangport)
	PortTuliskata(aturUlangport, 0)
	return 10
}

var count uint16 = 0

func (dirisendiri *Tamdam79c973) PenangananInterupsi(esp uint32) uint32 {

	PortTuliskata(registeraddressport, 0)
	temporary := uint32(PortBacakata(registerdataport))
	console_2.MCetak(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Cetak(esp)
	console_2.MCetak(([]byte)(":"))
	console_2.MUnsignedinteger32Cetak(temporary)
	console_2.MCetak(([]byte)(":"))
	console_2.MUnsignedinteger16Cetak(count)
	count++
	console_2.MCetak(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MCetak(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MCetak(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MCetak(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MCetak(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MCetak(([]byte)("am79c973 data received"))
		dirisendiri.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MCetak(([]byte)("am79c973 data sent"))
	}

	PortTuliskata(registeraddressport, 0)
	PortTuliskata(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MCetak(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (dirisendiri *Tamdam79c973) Kirim(dataPenunjuk uintptr, ukuran uint32) {
	var kirimdescriptor uint16 = uint16(sekarangKirimbuffer)
	sekarangKirimbuffer = 0

	if ukuran > 1518 {
		ukuran = 1518
	}

	var sumber_2 [4096]byte = *(*([4096]byte))(Pointer(dataPenunjuk))
	var tujuan_2 uint32 = kirimbufferKeterangan[kirimdescriptor].address_2 + ukuran - 1

	for i := 0; i < int(ukuran); i++ {

		*(*byte)(Pointer(uintptr(tujuan_2))) = sumber_2[int(ukuran)-i-1]

		tujuan_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPenunjuk))
	console_2.MCetakxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalCetak(data[i])
		console_2.MCetak(([]byte)(":"))
	}
	console_2.MCetak(([]byte)("\n"))

	kirimbufferKeterangan[kirimdescriptor].tersedia = 0
	kirimbufferKeterangan[kirimdescriptor].tanda2 = 0
	kirimbufferKeterangan[kirimdescriptor].tanda = 0x8300F000 | uint32((-ukuran)&0xFFF)

	PortTuliskata(registeraddressport, 0)
	PortTuliskata(registerdataport, 0x48)

}
func (dirisendiri *Tamdam79c973) Receive() {
	console_2.MCetak(([]byte)(":"))
	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(&kirimbuffer))))
	console_2.MCetak(([]byte)(":"))
	console_2.MHexadecimalCetak(kirimbuffer[0][0])
	console_2.MHexadecimalCetak(kirimbuffer[0][1])
	console_2.MCetak(([]byte)(":"))
	sekarangrecvbuffer = 0

	for ; (recvbufferKeterangan[sekarangrecvbuffer].tanda & 0x80000000) == 0; sekarangrecvbuffer = (sekarangrecvbuffer + 1) % 8 {

		if !(recvbufferKeterangan[sekarangrecvbuffer].tanda&0x40000000 != 0) && ((recvbufferKeterangan[sekarangrecvbuffer].tanda & 0x03000000) == 0x03000000) {
			var ukuran uint32 = recvbufferKeterangan[sekarangrecvbuffer].tanda & 0xFFF
			if ukuran > 64 {
				ukuran -= 4
			}

			console_2.MCetak([]byte(" size : ["))
			console_2.MUnsignedinteger32Cetak(ukuran)
			console_2.MCetak([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferKeterangan[sekarangrecvbuffer].address_2)))
			var acuan_alamat uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Hiduprawdatareceive(acuan_alamat, int(ukuran)) {

					console_2.MCetakxy(([]byte)("self.Send"), 0, 22)

					dirisendiri.Kirim(acuan_alamat, ukuran)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalCetak(buffer_2[i])
				console_2.MCetak([]byte(":"))
			}

		}
		recvbufferKeterangan[sekarangrecvbuffer].tanda2 = 0
		recvbufferKeterangan[sekarangrecvbuffer].tanda = 0x8000F7FF
	}
}
func (dirisendiri *Tamdam79c973) Aturhandler(handler *TRawdatahandler) {
	dirisendiri.handler = handler
}
func (dirisendiri *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (dirisendiri *Tamdam79c973) Aturipaddress(ip uint64) {
	initBlok.logikaaddress = ip
}
func (dirisendiri *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logikaaddress
}
