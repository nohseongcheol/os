package amdam79c973

import . "unsafe"
import . "sampuk"
import . "console"
import . "port"
import . "pci"

var rangkaiancardconsole TConsole = TConsole{}

type TInitializationBlok struct {
	mod			uint16
	nOMBORHantarbuffer	uint8
	nOMBORrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferKeteranganaddress	uintptr
	hantarbufferKeteranganaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	bendera		uint32
	bendera2	uint32
	tersedia	uint32
}

type IRawdatahandler interface {
	Bukarawdatareceive(dataPenuding uintptr, saiz int) bool
	Hantar(dataPenuding uintptr, saiz uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (diri *TRawdatahandler) Tetapkanbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (diri *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (diri *TRawdatahandler) Bukarawdatareceive(dataPenuding uintptr, saiz int) bool {
	rangkaiancardconsole.MCetakxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (diri *TRawdatahandler) Hantar(dataPenuding uintptr, saiz uint32) {
	rangkaiancardconsole.MCetakxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Hantar(dataPenuding, saiz)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var tetapSemulaport uint16
var busKawalanregisterdataport uint16

var initBlok TInitializationBlok

var hantarbufferKeterangan [8]TBufferdescriptor
var hantarbufferKeteranganIngatan [2048 + 15]byte
var hantarbuffer [2*1024 + 15][8]uint8
var semasaHantarbuffer uint8

var recvbufferKeterangan [8]TBufferdescriptor
var recvbufferKeteranganIngatan [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var semasarecvbuffer uint8
var funcNilai func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TSampukhandler
	perantidescriptor	TPeripheralcomponentinterconnectPerantidescriptor
	sampuk			*TSampukmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (diri *Tamdam79c973) Initdriver(sampuk *TSampukmanager, perantidescriptor TPeripheralcomponentinterconnectPerantidescriptor, handler IRawdatahandler) {

	diri.perantidescriptor = perantidescriptor

	funcNilai = (*Tamdam79c973).KendaliSampuk
	var address uintptr
	address = uintptr(Pointer(&funcNilai))

	diri.Init(uint8(0x20+perantidescriptor.Sampuk), uintptr(Pointer(sampuk)), address)

	Macaddress0port = uint16(perantidescriptor.Portbase)
	Macaddress2port = uint16(perantidescriptor.Portbase) + 0x02
	Macaddress4port = uint16(perantidescriptor.Portbase) + 0x04
	registerdataport = uint16(perantidescriptor.Portbase) + 0x10
	registeraddressport = uint16(perantidescriptor.Portbase) + 0x12
	tetapSemulaport = uint16(perantidescriptor.Portbase) + 0x14
	busKawalanregisterdataport = uint16(perantidescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	semasaHantarbuffer = 0
	semasarecvbuffer = 0

	var Mac0 uint64 = uint64(PortBacaperkataan(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortBacaperkataan(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortBacaperkataan(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortBacaperkataan(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortBacaperkataan(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortBacaperkataan(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MCetakxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalCetak(uint8(perantidescriptor.Sampuk))
	console_2.MCetak(([]byte)("]"))
	console_2.MCetak(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Cetak(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Cetak(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MCetak(([]byte)("]"))

	PortTulisperkataan(registeraddressport, 20)
	PortTulisperkataan(busKawalanregisterdataport, 0x102)

	PortTulisperkataan(registeraddressport, 0)
	PortTulisperkataan(registerdataport, 0x04)

	initBlok.mod = 0x0000
	initBlok.nOMBORHantarbuffer = 3
	initBlok.nOMBORrecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logicaladdress = 0

	hantarbufferKeterangan = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&hantarbufferKeteranganIngatan)) + 15) & ^(uintptr)(0xF)))
	initBlok.hantarbufferKeteranganaddress = uintptr(Pointer(&hantarbufferKeterangan))
	recvbufferKeterangan = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferKeteranganIngatan)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferKeteranganaddress = uintptr(Pointer(&recvbufferKeterangan))

	for i := 0; i < 8; i++ {
		hantarbufferKeterangan[i].address_2 = uint32((uintptr(Pointer(&hantarbuffer[i])) + 15) & ^(uintptr(0xF)))
		hantarbufferKeterangan[i].bendera = 0x7FF | 0xF000
		hantarbufferKeterangan[i].bendera2 = 0
		hantarbufferKeterangan[i].tersedia = 0

		recvbufferKeterangan[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferKeterangan[i].bendera = 0xF7FF | 0x80000000

	}

	PortTulisperkataan(registeraddressport, 1)
	PortTulisperkataan(registerdataport, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PortTulisperkataan(registeraddressport, 2)
	PortTulisperkataan(registerdataport, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (diri *Tamdam79c973) Aktifkan() {
	PortTulisperkataan(registeraddressport, 0)
	PortTulisperkataan(registerdataport, 0x41)

	PortTulisperkataan(registeraddressport, 4)
	temporary := PortBacaperkataan(registerdataport)
	PortTulisperkataan(registeraddressport, 4)
	PortTulisperkataan(registerdataport, temporary|0xC00)

	PortTulisperkataan(registeraddressport, 0)
	PortTulisperkataan(registerdataport, 0x42)

}
func (diri *Tamdam79c973) TetapSemula() int {
	PortBacaperkataan(tetapSemulaport)
	PortTulisperkataan(tetapSemulaport, 0)
	return 10
}

var count uint16 = 0

func (diri *Tamdam79c973) KendaliSampuk(esp uint32) uint32 {

	PortTulisperkataan(registeraddressport, 0)
	temporary := uint32(PortBacaperkataan(registerdataport))
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
		diri.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MCetak(([]byte)("am79c973 data sent"))
	}

	PortTulisperkataan(registeraddressport, 0)
	PortTulisperkataan(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MCetak(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (diri *Tamdam79c973) Hantar(dataPenuding uintptr, saiz uint32) {
	var hantardescriptor uint16 = uint16(semasaHantarbuffer)
	semasaHantarbuffer = 0

	if saiz > 1518 {
		saiz = 1518
	}

	var sumber_2 [4096]byte = *(*([4096]byte))(Pointer(dataPenuding))
	var destination_2 uint32 = hantarbufferKeterangan[hantardescriptor].address_2 + saiz - 1

	for i := 0; i < int(saiz); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = sumber_2[int(saiz)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPenuding))
	console_2.MCetakxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalCetak(data[i])
		console_2.MCetak(([]byte)(":"))
	}
	console_2.MCetak(([]byte)("\n"))

	hantarbufferKeterangan[hantardescriptor].tersedia = 0
	hantarbufferKeterangan[hantardescriptor].bendera2 = 0
	hantarbufferKeterangan[hantardescriptor].bendera = 0x8300F000 | uint32((-saiz)&0xFFF)

	PortTulisperkataan(registeraddressport, 0)
	PortTulisperkataan(registerdataport, 0x48)

}
func (diri *Tamdam79c973) Receive() {
	console_2.MCetak(([]byte)(":"))
	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(&hantarbuffer))))
	console_2.MCetak(([]byte)(":"))
	console_2.MHexadecimalCetak(hantarbuffer[0][0])
	console_2.MHexadecimalCetak(hantarbuffer[0][1])
	console_2.MCetak(([]byte)(":"))
	semasarecvbuffer = 0

	for ; (recvbufferKeterangan[semasarecvbuffer].bendera & 0x80000000) == 0; semasarecvbuffer = (semasarecvbuffer + 1) % 8 {

		if !(recvbufferKeterangan[semasarecvbuffer].bendera&0x40000000 != 0) && ((recvbufferKeterangan[semasarecvbuffer].bendera & 0x03000000) == 0x03000000) {
			var saiz uint32 = recvbufferKeterangan[semasarecvbuffer].bendera & 0xFFF
			if saiz > 64 {
				saiz -= 4
			}

			console_2.MCetak([]byte(" size : ["))
			console_2.MUnsignedinteger32Cetak(saiz)
			console_2.MCetak([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferKeterangan[semasarecvbuffer].address_2)))
			var rujukan_alamat uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Bukarawdatareceive(rujukan_alamat, int(saiz)) {

					console_2.MCetakxy(([]byte)("self.Send"), 0, 22)

					diri.Hantar(rujukan_alamat, saiz)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalCetak(buffer_2[i])
				console_2.MCetak([]byte(":"))
			}

		}
		recvbufferKeterangan[semasarecvbuffer].bendera2 = 0
		recvbufferKeterangan[semasarecvbuffer].bendera = 0x8000F7FF
	}
}
func (diri *Tamdam79c973) Tetapkanhandler(handler *TRawdatahandler) {
	diri.handler = handler
}
func (diri *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (diri *Tamdam79c973) Tetapkanipaddress(ip uint64) {
	initBlok.logicaladdress = ip
}
func (diri *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logicaladdress
}
