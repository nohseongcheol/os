package amdam79c973

import . "unsafe"
import . "interrupt"
import . "konsoly"
import . "irika"
import . "pci"

var rezocardKonsoly TKonsoly = TKonsoly{}

type TInitializationblock struct {
	fomba			uint16
	numbersendbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress				uint64
	recvbufferFanoritsoritanaaddress	uintptr
	sendbufferFanoritsoritanaaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	saina		uint32
	saina2		uint32
	azoampiasaina	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(datapointer uintptr, habe int) bool
	Send(datapointer uintptr, habe uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (nytena *TRawdatahandler) Setbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (nytena *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (nytena *TRawdatahandler) Onrawdatareceive(datapointer uintptr, habe int) bool {
	rezocardKonsoly.MAtontayxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (nytena *TRawdatahandler) Send(datapointer uintptr, habe uint32) {
	rezocardKonsoly.MAtontayxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(datapointer, habe)
}

var Macaddress0Irika uint16
var Macaddress2Irika uint16
var Macaddress4Irika uint16
var registerdataIrika uint16
var registeraddressIrika uint16
var averenoIrika uint16
var buscontrolregisterdataIrika uint16

var initblock TInitializationblock

var sendbufferFanoritsoritana [8]TBufferdescriptor
var sendbufferFanoritsoritanaArika [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferFanoritsoritana [8]TBufferdescriptor
var recvbufferFanoritsoritanaArika [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcSanda func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	periferikadescriptor	TPeripheralcomponentinterconnectPeriferikadescriptor
	interrupt		*TInterruptMpandrindra
	handler			*TRawdatahandler
}

var konsoly_2 TKonsoly = TKonsoly{}
var irawdatahandler IRawdatahandler

func (nytena *Tamdam79c973) Initdriver(interrupt *TInterruptMpandrindra, periferikadescriptor TPeripheralcomponentinterconnectPeriferikadescriptor, handler IRawdatahandler) {

	nytena.periferikadescriptor = periferikadescriptor

	funcSanda = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcSanda))

	nytena.Init(uint8(0x20+periferikadescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Irika = uint16(periferikadescriptor.Irikabase)
	Macaddress2Irika = uint16(periferikadescriptor.Irikabase) + 0x02
	Macaddress4Irika = uint16(periferikadescriptor.Irikabase) + 0x04
	registerdataIrika = uint16(periferikadescriptor.Irikabase) + 0x10
	registeraddressIrika = uint16(periferikadescriptor.Irikabase) + 0x12
	averenoIrika = uint16(periferikadescriptor.Irikabase) + 0x14
	buscontrolregisterdataIrika = uint16(periferikadescriptor.Irikabase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(IrikaMamakyteny(Macaddress0Irika) % 256)
	var Mac1 uint64 = uint64(IrikaMamakyteny(Macaddress0Irika) / 256)
	var Mac2 uint64 = uint64(IrikaMamakyteny(Macaddress2Irika) % 256)
	var Mac3 uint64 = uint64(IrikaMamakyteny(Macaddress2Irika) / 256)
	var Mac4 uint64 = uint64(IrikaMamakyteny(Macaddress4Irika) % 256)
	var Mac5 uint64 = uint64(IrikaMamakyteny(Macaddress4Irika) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konsoly_2.MAtontayxy(([]byte)("[interrupt num : "), 0, 13)
	konsoly_2.MHexadecimalAtontay(uint8(periferikadescriptor.Interrupt))
	konsoly_2.MAtontay(([]byte)("]"))
	konsoly_2.MAtontay(([]byte)("[mac address : "))
	konsoly_2.MUnsignedinteger16Atontay(uint16(macaddress >> 32))
	konsoly_2.MUnsignedinteger32Atontay(uint32(macaddress & 0x00000000FFFFFFFF))
	konsoly_2.MAtontay(([]byte)("]"))

	IrikaManoratrateny(registeraddressIrika, 20)
	IrikaManoratrateny(buscontrolregisterdataIrika, 0x102)

	IrikaManoratrateny(registeraddressIrika, 0)
	IrikaManoratrateny(registerdataIrika, 0x04)

	initblock.fomba = 0x0000
	initblock.numbersendbuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	sendbufferFanoritsoritana = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferFanoritsoritanaArika)) + 15) & ^(uintptr)(0xF)))
	initblock.sendbufferFanoritsoritanaaddress = uintptr(Pointer(&sendbufferFanoritsoritana))
	recvbufferFanoritsoritana = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferFanoritsoritanaArika)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferFanoritsoritanaaddress = uintptr(Pointer(&recvbufferFanoritsoritana))

	for i := 0; i < 8; i++ {
		sendbufferFanoritsoritana[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferFanoritsoritana[i].saina = 0x7FF | 0xF000
		sendbufferFanoritsoritana[i].saina2 = 0
		sendbufferFanoritsoritana[i].azoampiasaina = 0

		recvbufferFanoritsoritana[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferFanoritsoritana[i].saina = 0xF7FF | 0x80000000

	}

	IrikaManoratrateny(registeraddressIrika, 1)
	IrikaManoratrateny(registerdataIrika, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	IrikaManoratrateny(registeraddressIrika, 2)
	IrikaManoratrateny(registerdataIrika, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (nytena *Tamdam79c973) Alefaso() {
	IrikaManoratrateny(registeraddressIrika, 0)
	IrikaManoratrateny(registerdataIrika, 0x41)

	IrikaManoratrateny(registeraddressIrika, 4)
	temporary := IrikaMamakyteny(registerdataIrika)
	IrikaManoratrateny(registeraddressIrika, 4)
	IrikaManoratrateny(registerdataIrika, temporary|0xC00)

	IrikaManoratrateny(registeraddressIrika, 0)
	IrikaManoratrateny(registerdataIrika, 0x42)

}
func (nytena *Tamdam79c973) Avereno() int {
	IrikaMamakyteny(averenoIrika)
	IrikaManoratrateny(averenoIrika, 0)
	return 10
}

var count uint16 = 0

func (nytena *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	IrikaManoratrateny(registeraddressIrika, 0)
	temporary := uint32(IrikaMamakyteny(registerdataIrika))
	konsoly_2.MAtontay(([]byte)("interrupt("))
	konsoly_2.MUnsignedinteger32Atontay(esp)
	konsoly_2.MAtontay(([]byte)(":"))
	konsoly_2.MUnsignedinteger32Atontay(temporary)
	konsoly_2.MAtontay(([]byte)(":"))
	konsoly_2.MUnsignedinteger16Atontay(count)
	count++
	konsoly_2.MAtontay(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konsoly_2.MAtontay(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konsoly_2.MAtontay(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konsoly_2.MAtontay(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konsoly_2.MAtontay(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konsoly_2.MAtontay(([]byte)("am79c973 data received"))
		nytena.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konsoly_2.MAtontay(([]byte)("am79c973 data sent"))
	}

	IrikaManoratrateny(registeraddressIrika, 0)
	IrikaManoratrateny(registerdataIrika, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konsoly_2.MAtontay(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (nytena *Tamdam79c973) Send(datapointer uintptr, habe uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if habe > 1518 {
		habe = 1518
	}

	var loharano_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var destination_2 uint32 = sendbufferFanoritsoritana[senddescriptor].address_2 + habe - 1

	for i := 0; i < int(habe); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = loharano_2[int(habe)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	konsoly_2.MAtontayxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konsoly_2.MHexadecimalAtontay(data[i])
		konsoly_2.MAtontay(([]byte)(":"))
	}
	konsoly_2.MAtontay(([]byte)("\n"))

	sendbufferFanoritsoritana[senddescriptor].azoampiasaina = 0
	sendbufferFanoritsoritana[senddescriptor].saina2 = 0
	sendbufferFanoritsoritana[senddescriptor].saina = 0x8300F000 | uint32((-habe)&0xFFF)

	IrikaManoratrateny(registeraddressIrika, 0)
	IrikaManoratrateny(registerdataIrika, 0x48)

}
func (nytena *Tamdam79c973) Receive() {
	konsoly_2.MAtontay(([]byte)(":"))
	konsoly_2.MUnsignedinteger32Atontay(uint32(uintptr(Pointer(&sendbuffer))))
	konsoly_2.MAtontay(([]byte)(":"))
	konsoly_2.MHexadecimalAtontay(sendbuffer[0][0])
	konsoly_2.MHexadecimalAtontay(sendbuffer[0][1])
	konsoly_2.MAtontay(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferFanoritsoritana[currentrecvbuffer].saina & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferFanoritsoritana[currentrecvbuffer].saina&0x40000000 != 0) && ((recvbufferFanoritsoritana[currentrecvbuffer].saina & 0x03000000) == 0x03000000) {
			var habe uint32 = recvbufferFanoritsoritana[currentrecvbuffer].saina & 0xFFF
			if habe > 64 {
				habe -= 4
			}

			konsoly_2.MAtontay([]byte(" size : ["))
			konsoly_2.MUnsignedinteger32Atontay(habe)
			konsoly_2.MAtontay([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferFanoritsoritana[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(pointer, int(habe)) {

					konsoly_2.MAtontayxy(([]byte)("self.Send"), 0, 22)

					nytena.Send(pointer, habe)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konsoly_2.MHexadecimalAtontay(buffer_2[i])
				konsoly_2.MAtontay([]byte(":"))
			}

		}
		recvbufferFanoritsoritana[currentrecvbuffer].saina2 = 0
		recvbufferFanoritsoritana[currentrecvbuffer].saina = 0x8000F7FF
	}
}
func (nytena *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	nytena.handler = handler
}
func (nytena *Tamdam79c973) Getmacaddress() uint64 {

	return initblock.physicaladdress
}
func (nytena *Tamdam79c973) Setipaddress(ip uint64) {
	initblock.logicaladdress = ip
}
func (nytena *Tamdam79c973) Getipaddress() uint64 {
	return initblock.logicaladdress
}
