package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "port"
import . "pci"

var netcardconsole TConsole = TConsole{}

type TInitializationBlokkur struct {
	mode			uint16
	numbersendbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferFrágreiðingaddress	uintptr
	sendbufferFrágreiðingaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flags		uint32
	flags2		uint32
	available	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(datapointer uintptr, stødd int) bool
	Send(datapointer uintptr, stødd uint32)
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
func (self *TRawdatahandler) Onrawdatareceive(datapointer uintptr, stødd int) bool {
	netcardconsole.MPrintxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Send(datapointer uintptr, stødd uint32) {
	netcardconsole.MPrintxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(datapointer, stødd)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var resetport uint16
var buscontrolregisterdataport uint16

var initBlokkur TInitializationBlokkur

var sendbufferFrágreiðing [8]TBufferdescriptor
var sendbufferFrágreiðingmemory [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferFrágreiðing [8]TBufferdescriptor
var recvbufferFrágreiðingmemory [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcvalue func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	devicedescriptor	TPeripheralcomponentinterconnectdevicedescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, devicedescriptor TPeripheralcomponentinterconnectdevicedescriptor, handler IRawdatahandler) {

	self.devicedescriptor = devicedescriptor

	funcvalue = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcvalue))

	self.Init(uint8(0x20+devicedescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0port = uint16(devicedescriptor.Portbase)
	Macaddress2port = uint16(devicedescriptor.Portbase) + 0x02
	Macaddress4port = uint16(devicedescriptor.Portbase) + 0x04
	registerdataport = uint16(devicedescriptor.Portbase) + 0x10
	registeraddressport = uint16(devicedescriptor.Portbase) + 0x12
	resetport = uint16(devicedescriptor.Portbase) + 0x14
	buscontrolregisterdataport = uint16(devicedescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(Portlesaword(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(Portlesaword(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(Portlesaword(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(Portlesaword(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(Portlesaword(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(Portlesaword(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MPrintxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalprint(uint8(devicedescriptor.Interrupt))
	console_2.MPrint(([]byte)("]"))
	console_2.MPrint(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16print(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32print(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MPrint(([]byte)("]"))

	Portskrivaword(registeraddressport, 20)
	Portskrivaword(buscontrolregisterdataport, 0x102)

	Portskrivaword(registeraddressport, 0)
	Portskrivaword(registerdataport, 0x04)

	initBlokkur.mode = 0x0000
	initBlokkur.numbersendbuffer = 3
	initBlokkur.numberrecvbuffer = 3

	initBlokkur.physicaladdress = Mac

	initBlokkur.logicaladdress = 0

	sendbufferFrágreiðing = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferFrágreiðingmemory)) + 15) & ^(uintptr)(0xF)))
	initBlokkur.sendbufferFrágreiðingaddress = uintptr(Pointer(&sendbufferFrágreiðing))
	recvbufferFrágreiðing = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferFrágreiðingmemory)) + 15) & ^(uintptr)(0xF)))
	initBlokkur.recvbufferFrágreiðingaddress = uintptr(Pointer(&recvbufferFrágreiðing))

	for i := 0; i < 8; i++ {
		sendbufferFrágreiðing[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferFrágreiðing[i].flags = 0x7FF | 0xF000
		sendbufferFrágreiðing[i].flags2 = 0
		sendbufferFrágreiðing[i].available = 0

		recvbufferFrágreiðing[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferFrágreiðing[i].flags = 0xF7FF | 0x80000000

	}

	Portskrivaword(registeraddressport, 1)
	Portskrivaword(registerdataport, uint16(uintptr(Pointer(&initBlokkur))&0xFFFF))

	Portskrivaword(registeraddressport, 2)
	Portskrivaword(registerdataport, uint16((uintptr(Pointer(&initBlokkur))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Activate() {
	Portskrivaword(registeraddressport, 0)
	Portskrivaword(registerdataport, 0x41)

	Portskrivaword(registeraddressport, 4)
	temporary := Portlesaword(registerdataport)
	Portskrivaword(registeraddressport, 4)
	Portskrivaword(registerdataport, temporary|0xC00)

	Portskrivaword(registeraddressport, 0)
	Portskrivaword(registerdataport, 0x42)

}
func (self *Tamdam79c973) Reset() int {
	Portlesaword(resetport)
	Portskrivaword(resetport, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	Portskrivaword(registeraddressport, 0)
	temporary := uint32(Portlesaword(registerdataport))
	console_2.MPrint(([]byte)("interrupt("))
	console_2.MUnsignedinteger32print(esp)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(temporary)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger16print(count)
	count++
	console_2.MPrint(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MPrint(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MPrint(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MPrint(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MPrint(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MPrint(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MPrint(([]byte)("am79c973 data sent"))
	}

	Portskrivaword(registeraddressport, 0)
	Portskrivaword(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MPrint(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Send(datapointer uintptr, stødd uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if stødd > 1518 {
		stødd = 1518
	}

	var source_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var destination_2 uint32 = sendbufferFrágreiðing[senddescriptor].address_2 + stødd - 1

	for i := 0; i < int(stødd); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = source_2[int(stødd)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	console_2.MPrintxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalprint(data[i])
		console_2.MPrint(([]byte)(":"))
	}
	console_2.MPrint(([]byte)("\n"))

	sendbufferFrágreiðing[senddescriptor].available = 0
	sendbufferFrágreiðing[senddescriptor].flags2 = 0
	sendbufferFrágreiðing[senddescriptor].flags = 0x8300F000 | uint32((-stødd)&0xFFF)

	Portskrivaword(registeraddressport, 0)
	Portskrivaword(registerdataport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.MPrint(([]byte)(":"))
	console_2.MHexadecimalprint(sendbuffer[0][0])
	console_2.MHexadecimalprint(sendbuffer[0][1])
	console_2.MPrint(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferFrágreiðing[currentrecvbuffer].flags & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferFrágreiðing[currentrecvbuffer].flags&0x40000000 != 0) && ((recvbufferFrágreiðing[currentrecvbuffer].flags & 0x03000000) == 0x03000000) {
			var stødd uint32 = recvbufferFrágreiðing[currentrecvbuffer].flags & 0xFFF
			if stødd > 64 {
				stødd -= 4
			}

			console_2.MPrint([]byte(" size : ["))
			console_2.MUnsignedinteger32print(stødd)
			console_2.MPrint([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferFrágreiðing[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(pointer, int(stødd)) {

					console_2.MPrintxy(([]byte)("self.Send"), 0, 22)

					self.Send(pointer, stødd)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalprint(buffer_2[i])
				console_2.MPrint([]byte(":"))
			}

		}
		recvbufferFrágreiðing[currentrecvbuffer].flags2 = 0
		recvbufferFrágreiðing[currentrecvbuffer].flags = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initBlokkur.physicaladdress
}
func (self *Tamdam79c973) Setipaddress(ip uint64) {
	initBlokkur.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initBlokkur.logicaladdress
}
