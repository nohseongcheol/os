package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "umuyoboro"
import . "pci"

var urusobecardconsole TConsole = TConsole{}

type TInitializationblock struct {
	ubwoko			uint16
	numbersendbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferUmwirondoroaddress	uintptr
	sendbufferUmwirondoroaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	amabendera	uint32
	amabendera2	uint32
	available	uint32
}

type IRawdatahandler interface {
	Kurirawdatareceive(datapointer uintptr, ingano int) bool
	Send(datapointer uintptr, ingano uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Setbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Kurirawdatareceive(datapointer uintptr, ingano int) bool {
	urusobecardconsole.MGucapaxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Send(datapointer uintptr, ingano uint32) {
	urusobecardconsole.MGucapaxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(datapointer, ingano)
}

var Macaddress0Umuyoboro uint16
var Macaddress2Umuyoboro uint16
var Macaddress4Umuyoboro uint16
var registerdataUmuyoboro uint16
var registeraddressUmuyoboro uint16
var kugaruraUmuyoboro uint16
var buscontrolregisterdataUmuyoboro uint16

var initblock TInitializationblock

var sendbufferUmwirondoro [8]TBufferdescriptor
var sendbufferUmwirondoroUbubiko [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferUmwirondoro [8]TBufferdescriptor
var recvbufferUmwirondoroUbubiko [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcAgaciro func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	ububikodescriptor	TPeripheralcomponentinterconnectUbubikodescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, ububikodescriptor TPeripheralcomponentinterconnectUbubikodescriptor, handler IRawdatahandler) {

	self.ububikodescriptor = ububikodescriptor

	funcAgaciro = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcAgaciro))

	self.Init(uint8(0x20+ububikodescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Umuyoboro = uint16(ububikodescriptor.Umuyoborobase)
	Macaddress2Umuyoboro = uint16(ububikodescriptor.Umuyoborobase) + 0x02
	Macaddress4Umuyoboro = uint16(ububikodescriptor.Umuyoborobase) + 0x04
	registerdataUmuyoboro = uint16(ububikodescriptor.Umuyoborobase) + 0x10
	registeraddressUmuyoboro = uint16(ububikodescriptor.Umuyoborobase) + 0x12
	kugaruraUmuyoboro = uint16(ububikodescriptor.Umuyoborobase) + 0x14
	buscontrolregisterdataUmuyoboro = uint16(ububikodescriptor.Umuyoborobase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(Umuyoborogusomaword(Macaddress0Umuyoboro) % 256)
	var Mac1 uint64 = uint64(Umuyoborogusomaword(Macaddress0Umuyoboro) / 256)
	var Mac2 uint64 = uint64(Umuyoborogusomaword(Macaddress2Umuyoboro) % 256)
	var Mac3 uint64 = uint64(Umuyoborogusomaword(Macaddress2Umuyoboro) / 256)
	var Mac4 uint64 = uint64(Umuyoborogusomaword(Macaddress4Umuyoboro) % 256)
	var Mac5 uint64 = uint64(Umuyoborogusomaword(Macaddress4Umuyoboro) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MGucapaxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalGucapa(uint8(ububikodescriptor.Interrupt))
	console_2.MGucapa(([]byte)("]"))
	console_2.MGucapa(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Gucapa(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Gucapa(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MGucapa(([]byte)("]"))

	Umuyoborokwandikaword(registeraddressUmuyoboro, 20)
	Umuyoborokwandikaword(buscontrolregisterdataUmuyoboro, 0x102)

	Umuyoborokwandikaword(registeraddressUmuyoboro, 0)
	Umuyoborokwandikaword(registerdataUmuyoboro, 0x04)

	initblock.ubwoko = 0x0000
	initblock.numbersendbuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	sendbufferUmwirondoro = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferUmwirondoroUbubiko)) + 15) & ^(uintptr)(0xF)))
	initblock.sendbufferUmwirondoroaddress = uintptr(Pointer(&sendbufferUmwirondoro))
	recvbufferUmwirondoro = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferUmwirondoroUbubiko)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferUmwirondoroaddress = uintptr(Pointer(&recvbufferUmwirondoro))

	for i := 0; i < 8; i++ {
		sendbufferUmwirondoro[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferUmwirondoro[i].amabendera = 0x7FF | 0xF000
		sendbufferUmwirondoro[i].amabendera2 = 0
		sendbufferUmwirondoro[i].available = 0

		recvbufferUmwirondoro[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferUmwirondoro[i].amabendera = 0xF7FF | 0x80000000

	}

	Umuyoborokwandikaword(registeraddressUmuyoboro, 1)
	Umuyoborokwandikaword(registerdataUmuyoboro, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	Umuyoborokwandikaword(registeraddressUmuyoboro, 2)
	Umuyoborokwandikaword(registerdataUmuyoboro, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Activate() {
	Umuyoborokwandikaword(registeraddressUmuyoboro, 0)
	Umuyoborokwandikaword(registerdataUmuyoboro, 0x41)

	Umuyoborokwandikaword(registeraddressUmuyoboro, 4)
	temporary := Umuyoborogusomaword(registerdataUmuyoboro)
	Umuyoborokwandikaword(registeraddressUmuyoboro, 4)
	Umuyoborokwandikaword(registerdataUmuyoboro, temporary|0xC00)

	Umuyoborokwandikaword(registeraddressUmuyoboro, 0)
	Umuyoborokwandikaword(registerdataUmuyoboro, 0x42)

}
func (self *Tamdam79c973) Kugarura() int {
	Umuyoborogusomaword(kugaruraUmuyoboro)
	Umuyoborokwandikaword(kugaruraUmuyoboro, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	Umuyoborokwandikaword(registeraddressUmuyoboro, 0)
	temporary := uint32(Umuyoborogusomaword(registerdataUmuyoboro))
	console_2.MGucapa(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Gucapa(esp)
	console_2.MGucapa(([]byte)(":"))
	console_2.MUnsignedinteger32Gucapa(temporary)
	console_2.MGucapa(([]byte)(":"))
	console_2.MUnsignedinteger16Gucapa(count)
	count++
	console_2.MGucapa(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MGucapa(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MGucapa(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MGucapa(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MGucapa(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MGucapa(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MGucapa(([]byte)("am79c973 data sent"))
	}

	Umuyoborokwandikaword(registeraddressUmuyoboro, 0)
	Umuyoborokwandikaword(registerdataUmuyoboro, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MGucapa(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Send(datapointer uintptr, ingano uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if ingano > 1518 {
		ingano = 1518
	}

	var inkomoko_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var destination_2 uint32 = sendbufferUmwirondoro[senddescriptor].address_2 + ingano - 1

	for i := 0; i < int(ingano); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = inkomoko_2[int(ingano)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	console_2.MGucapaxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalGucapa(data[i])
		console_2.MGucapa(([]byte)(":"))
	}
	console_2.MGucapa(([]byte)("\n"))

	sendbufferUmwirondoro[senddescriptor].available = 0
	sendbufferUmwirondoro[senddescriptor].amabendera2 = 0
	sendbufferUmwirondoro[senddescriptor].amabendera = 0x8300F000 | uint32((-ingano)&0xFFF)

	Umuyoborokwandikaword(registeraddressUmuyoboro, 0)
	Umuyoborokwandikaword(registerdataUmuyoboro, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MGucapa(([]byte)(":"))
	console_2.MUnsignedinteger32Gucapa(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.MGucapa(([]byte)(":"))
	console_2.MHexadecimalGucapa(sendbuffer[0][0])
	console_2.MHexadecimalGucapa(sendbuffer[0][1])
	console_2.MGucapa(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferUmwirondoro[currentrecvbuffer].amabendera & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferUmwirondoro[currentrecvbuffer].amabendera&0x40000000 != 0) && ((recvbufferUmwirondoro[currentrecvbuffer].amabendera & 0x03000000) == 0x03000000) {
			var ingano uint32 = recvbufferUmwirondoro[currentrecvbuffer].amabendera & 0xFFF
			if ingano > 64 {
				ingano -= 4
			}

			console_2.MGucapa([]byte(" size : ["))
			console_2.MUnsignedinteger32Gucapa(ingano)
			console_2.MGucapa([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferUmwirondoro[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Kurirawdatareceive(pointer, int(ingano)) {

					console_2.MGucapaxy(([]byte)("self.Send"), 0, 22)

					self.Send(pointer, ingano)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalGucapa(buffer_2[i])
				console_2.MGucapa([]byte(":"))
			}

		}
		recvbufferUmwirondoro[currentrecvbuffer].amabendera2 = 0
		recvbufferUmwirondoro[currentrecvbuffer].amabendera = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initblock.physicaladdress
}
func (self *Tamdam79c973) Setipaddress(ip uint64) {
	initblock.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initblock.logicaladdress
}
