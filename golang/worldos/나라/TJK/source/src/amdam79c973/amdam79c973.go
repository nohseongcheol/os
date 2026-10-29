/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "port"
import . "pci"

var networkcardconsole TConsole = TConsole{}

type TInitializationblock struct {
	mode			uint16
	numberИрсолкунедbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferТасвиротaddress	uintptr
	ирсолкунедbufferТасвиротaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flags		uint32
	flags2		uint32
	available	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(datapointer uintptr, size int) bool
	Ирсолкунед(datapointer uintptr, size uint32)
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
func (self *TRawdatahandler) Onrawdatareceive(datapointer uintptr, size int) bool {
	networkcardconsole.MЧопкарданxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Ирсолкунед(datapointer uintptr, size uint32) {
	networkcardconsole.MЧопкарданxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Ирсолкунед(datapointer, size)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var бозсозӣport uint16
var buscontrolregisterdataport uint16

var initblock TInitializationblock

var ирсолкунедbufferТасвирот [8]TBufferdescriptor
var ирсолкунедbufferТасвиротmemory [2048 + 15]byte
var ирсолкунедbuffer [2*1024 + 15][8]uint8
var currentИрсолкунедbuffer uint8

var recvbufferТасвирот [8]TBufferdescriptor
var recvbufferТасвиротmemory [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcvalue func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	дастгоҳdescriptor	TPeripheralcomponentinterconnectДастгоҳdescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, дастгоҳdescriptor TPeripheralcomponentinterconnectДастгоҳdescriptor, handler IRawdatahandler) {

	self.дастгоҳdescriptor = дастгоҳdescriptor

	funcvalue = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcvalue))

	self.Init(uint8(0x20+дастгоҳdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0port = uint16(дастгоҳdescriptor.Portbase)
	Macaddress2port = uint16(дастгоҳdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(дастгоҳdescriptor.Portbase) + 0x04
	registerdataport = uint16(дастгоҳdescriptor.Portbase) + 0x10
	registeraddressport = uint16(дастгоҳdescriptor.Portbase) + 0x12
	бозсозӣport = uint16(дастгоҳdescriptor.Portbase) + 0x14
	buscontrolregisterdataport = uint16(дастгоҳdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentИрсолкунедbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(PortХонданword(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortХонданword(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortХонданword(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortХонданword(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortХонданword(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortХонданword(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MЧопкарданxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalЧопкардан(uint8(дастгоҳdescriptor.Interrupt))
	console_2.MЧопкардан(([]byte)("]"))
	console_2.MЧопкардан(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Чопкардан(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Чопкардан(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MЧопкардан(([]byte)("]"))

	PortНавиштанword(registeraddressport, 20)
	PortНавиштанword(buscontrolregisterdataport, 0x102)

	PortНавиштанword(registeraddressport, 0)
	PortНавиштанword(registerdataport, 0x04)

	initblock.mode = 0x0000
	initblock.numberИрсолкунедbuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	ирсолкунедbufferТасвирот = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&ирсолкунедbufferТасвиротmemory)) + 15) & ^(uintptr)(0xF)))
	initblock.ирсолкунедbufferТасвиротaddress = uintptr(Pointer(&ирсолкунедbufferТасвирот))
	recvbufferТасвирот = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferТасвиротmemory)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferТасвиротaddress = uintptr(Pointer(&recvbufferТасвирот))

	for i := 0; i < 8; i++ {
		ирсолкунедbufferТасвирот[i].address_2 = uint32((uintptr(Pointer(&ирсолкунедbuffer[i])) + 15) & ^(uintptr(0xF)))
		ирсолкунедbufferТасвирот[i].flags = 0x7FF | 0xF000
		ирсолкунедbufferТасвирот[i].flags2 = 0
		ирсолкунедbufferТасвирот[i].available = 0

		recvbufferТасвирот[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferТасвирот[i].flags = 0xF7FF | 0x80000000

	}

	PortНавиштанword(registeraddressport, 1)
	PortНавиштанword(registerdataport, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	PortНавиштанword(registeraddressport, 2)
	PortНавиштанword(registerdataport, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Activate() {
	PortНавиштанword(registeraddressport, 0)
	PortНавиштанword(registerdataport, 0x41)

	PortНавиштанword(registeraddressport, 4)
	temporary := PortХонданword(registerdataport)
	PortНавиштанword(registeraddressport, 4)
	PortНавиштанword(registerdataport, temporary|0xC00)

	PortНавиштанword(registeraddressport, 0)
	PortНавиштанword(registerdataport, 0x42)

}
func (self *Tamdam79c973) Бозсозӣ() int {
	PortХонданword(бозсозӣport)
	PortНавиштанword(бозсозӣport, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	PortНавиштанword(registeraddressport, 0)
	temporary := uint32(PortХонданword(registerdataport))
	console_2.MЧопкардан(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Чопкардан(esp)
	console_2.MЧопкардан(([]byte)(":"))
	console_2.MUnsignedinteger32Чопкардан(temporary)
	console_2.MЧопкардан(([]byte)(":"))
	console_2.MUnsignedinteger16Чопкардан(count)
	count++
	console_2.MЧопкардан(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MЧопкардан(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MЧопкардан(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MЧопкардан(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MЧопкардан(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MЧопкардан(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MЧопкардан(([]byte)("am79c973 data sent"))
	}

	PortНавиштанword(registeraddressport, 0)
	PortНавиштанword(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MЧопкардан(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Ирсолкунед(datapointer uintptr, size uint32) {
	var ирсолкунедdescriptor uint16 = uint16(currentИрсолкунедbuffer)
	currentИрсолкунедbuffer = 0

	if size > 1518 {
		size = 1518
	}

	var source_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var destination_2 uint32 = ирсолкунедbufferТасвирот[ирсолкунедdescriptor].address_2 + size - 1

	for i := 0; i < int(size); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = source_2[int(size)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	console_2.MЧопкарданxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalЧопкардан(data[i])
		console_2.MЧопкардан(([]byte)(":"))
	}
	console_2.MЧопкардан(([]byte)("\n"))

	ирсолкунедbufferТасвирот[ирсолкунедdescriptor].available = 0
	ирсолкунедbufferТасвирот[ирсолкунедdescriptor].flags2 = 0
	ирсолкунедbufferТасвирот[ирсолкунедdescriptor].flags = 0x8300F000 | uint32((-size)&0xFFF)

	PortНавиштанword(registeraddressport, 0)
	PortНавиштанword(registerdataport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MЧопкардан(([]byte)(":"))
	console_2.MUnsignedinteger32Чопкардан(uint32(uintptr(Pointer(&ирсолкунедbuffer))))
	console_2.MЧопкардан(([]byte)(":"))
	console_2.MHexadecimalЧопкардан(ирсолкунедbuffer[0][0])
	console_2.MHexadecimalЧопкардан(ирсолкунедbuffer[0][1])
	console_2.MЧопкардан(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferТасвирот[currentrecvbuffer].flags & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferТасвирот[currentrecvbuffer].flags&0x40000000 != 0) && ((recvbufferТасвирот[currentrecvbuffer].flags & 0x03000000) == 0x03000000) {
			var size uint32 = recvbufferТасвирот[currentrecvbuffer].flags & 0xFFF
			if size > 64 {
				size -= 4
			}

			console_2.MЧопкардан([]byte(" size : ["))
			console_2.MUnsignedinteger32Чопкардан(size)
			console_2.MЧопкардан([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferТасвирот[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(pointer, int(size)) {

					console_2.MЧопкарданxy(([]byte)("self.Send"), 0, 22)

					self.Ирсолкунед(pointer, size)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalЧопкардан(buffer_2[i])
				console_2.MЧопкардан([]byte(":"))
			}

		}
		recvbufferТасвирот[currentrecvbuffer].flags2 = 0
		recvbufferТасвирот[currentrecvbuffer].flags = 0x8000F7FF
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
