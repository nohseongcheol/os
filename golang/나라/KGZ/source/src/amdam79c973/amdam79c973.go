package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "порт"
import . "pci"

var тармакcardconsole TConsole = TConsole{}

type TInitializationБлок struct {
	режим		uint16
	нОМЕРsendbuffer	uint8
	нОМЕРrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferБаяндамасыaddress	uintptr
	sendbufferБаяндамасыaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	желектери	uint32
	желектери2	uint32
	жеткиликтүүсү	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(dataКөрсөткүч uintptr, өлчөм int) bool
	Send(dataКөрсөткүч uintptr, өлчөм uint32)
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
func (self *TRawdatahandler) Onrawdatareceive(dataКөрсөткүч uintptr, өлчөм int) bool {
	тармакcardconsole.MБасмаxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Send(dataКөрсөткүч uintptr, өлчөм uint32) {
	тармакcardconsole.MБасмаxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(dataКөрсөткүч, өлчөм)
}

var Macaddress0Порт uint16
var Macaddress2Порт uint16
var Macaddress4Порт uint16
var registerdataПорт uint16
var registeraddressПорт uint16
var түшүрүүПорт uint16
var buscontrolregisterdataПорт uint16

var initБлок TInitializationБлок

var sendbufferБаяндамасы [8]TBufferdescriptor
var sendbufferБаяндамасыЭси [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferБаяндамасы [8]TBufferdescriptor
var recvbufferБаяндамасыЭси [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcМааниси func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	түзүлүшүdescriptor	TPeripheralcomponentinterconnectТүзүлүшүdescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, түзүлүшүdescriptor TPeripheralcomponentinterconnectТүзүлүшүdescriptor, handler IRawdatahandler) {

	self.түзүлүшүdescriptor = түзүлүшүdescriptor

	funcМааниси = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcМааниси))

	self.Init(uint8(0x20+түзүлүшүdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Порт = uint16(түзүлүшүdescriptor.Портbase)
	Macaddress2Порт = uint16(түзүлүшүdescriptor.Портbase) + 0x02
	Macaddress4Порт = uint16(түзүлүшүdescriptor.Портbase) + 0x04
	registerdataПорт = uint16(түзүлүшүdescriptor.Портbase) + 0x10
	registeraddressПорт = uint16(түзүлүшүdescriptor.Портbase) + 0x12
	түшүрүүПорт = uint16(түзүлүшүdescriptor.Портbase) + 0x14
	buscontrolregisterdataПорт = uint16(түзүлүшүdescriptor.Портbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(ПортОкуусөз(Macaddress0Порт) % 256)
	var Mac1 uint64 = uint64(ПортОкуусөз(Macaddress0Порт) / 256)
	var Mac2 uint64 = uint64(ПортОкуусөз(Macaddress2Порт) % 256)
	var Mac3 uint64 = uint64(ПортОкуусөз(Macaddress2Порт) / 256)
	var Mac4 uint64 = uint64(ПортОкуусөз(Macaddress4Порт) % 256)
	var Mac5 uint64 = uint64(ПортОкуусөз(Macaddress4Порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MБасмаxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalБасма(uint8(түзүлүшүdescriptor.Interrupt))
	console_2.MБасма(([]byte)("]"))
	console_2.MБасма(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Басма(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Басма(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MБасма(([]byte)("]"))

	ПортЖазуусөз(registeraddressПорт, 20)
	ПортЖазуусөз(buscontrolregisterdataПорт, 0x102)

	ПортЖазуусөз(registeraddressПорт, 0)
	ПортЖазуусөз(registerdataПорт, 0x04)

	initБлок.режим = 0x0000
	initБлок.нОМЕРsendbuffer = 3
	initБлок.нОМЕРrecvbuffer = 3

	initБлок.physicaladdress = Mac

	initБлок.logicaladdress = 0

	sendbufferБаяндамасы = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferБаяндамасыЭси)) + 15) & ^(uintptr)(0xF)))
	initБлок.sendbufferБаяндамасыaddress = uintptr(Pointer(&sendbufferБаяндамасы))
	recvbufferБаяндамасы = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferБаяндамасыЭси)) + 15) & ^(uintptr)(0xF)))
	initБлок.recvbufferБаяндамасыaddress = uintptr(Pointer(&recvbufferБаяндамасы))

	for i := 0; i < 8; i++ {
		sendbufferБаяндамасы[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferБаяндамасы[i].желектери = 0x7FF | 0xF000
		sendbufferБаяндамасы[i].желектери2 = 0
		sendbufferБаяндамасы[i].жеткиликтүүсү = 0

		recvbufferБаяндамасы[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferБаяндамасы[i].желектери = 0xF7FF | 0x80000000

	}

	ПортЖазуусөз(registeraddressПорт, 1)
	ПортЖазуусөз(registerdataПорт, uint16(uintptr(Pointer(&initБлок))&0xFFFF))

	ПортЖазуусөз(registeraddressПорт, 2)
	ПортЖазуусөз(registerdataПорт, uint16((uintptr(Pointer(&initБлок))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Activate() {
	ПортЖазуусөз(registeraddressПорт, 0)
	ПортЖазуусөз(registerdataПорт, 0x41)

	ПортЖазуусөз(registeraddressПорт, 4)
	temporary := ПортОкуусөз(registerdataПорт)
	ПортЖазуусөз(registeraddressПорт, 4)
	ПортЖазуусөз(registerdataПорт, temporary|0xC00)

	ПортЖазуусөз(registeraddressПорт, 0)
	ПортЖазуусөз(registerdataПорт, 0x42)

}
func (self *Tamdam79c973) Түшүрүү() int {
	ПортОкуусөз(түшүрүүПорт)
	ПортЖазуусөз(түшүрүүПорт, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	ПортЖазуусөз(registeraddressПорт, 0)
	temporary := uint32(ПортОкуусөз(registerdataПорт))
	console_2.MБасма(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Басма(esp)
	console_2.MБасма(([]byte)(":"))
	console_2.MUnsignedinteger32Басма(temporary)
	console_2.MБасма(([]byte)(":"))
	console_2.MUnsignedinteger16Басма(count)
	count++
	console_2.MБасма(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MБасма(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MБасма(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MБасма(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MБасма(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MБасма(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MБасма(([]byte)("am79c973 data sent"))
	}

	ПортЖазуусөз(registeraddressПорт, 0)
	ПортЖазуусөз(registerdataПорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MБасма(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Send(dataКөрсөткүч uintptr, өлчөм uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if өлчөм > 1518 {
		өлчөм = 1518
	}

	var баштапкытекст_2 [4096]byte = *(*([4096]byte))(Pointer(dataКөрсөткүч))
	var destination_2 uint32 = sendbufferБаяндамасы[senddescriptor].address_2 + өлчөм - 1

	for i := 0; i < int(өлчөм); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = баштапкытекст_2[int(өлчөм)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataКөрсөткүч))
	console_2.MБасмаxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalБасма(data[i])
		console_2.MБасма(([]byte)(":"))
	}
	console_2.MБасма(([]byte)("\n"))

	sendbufferБаяндамасы[senddescriptor].жеткиликтүүсү = 0
	sendbufferБаяндамасы[senddescriptor].желектери2 = 0
	sendbufferБаяндамасы[senddescriptor].желектери = 0x8300F000 | uint32((-өлчөм)&0xFFF)

	ПортЖазуусөз(registeraddressПорт, 0)
	ПортЖазуусөз(registerdataПорт, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MБасма(([]byte)(":"))
	console_2.MUnsignedinteger32Басма(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.MБасма(([]byte)(":"))
	console_2.MHexadecimalБасма(sendbuffer[0][0])
	console_2.MHexadecimalБасма(sendbuffer[0][1])
	console_2.MБасма(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferБаяндамасы[currentrecvbuffer].желектери & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferБаяндамасы[currentrecvbuffer].желектери&0x40000000 != 0) && ((recvbufferБаяндамасы[currentrecvbuffer].желектери & 0x03000000) == 0x03000000) {
			var өлчөм uint32 = recvbufferБаяндамасы[currentrecvbuffer].желектери & 0xFFF
			if өлчөм > 64 {
				өлчөм -= 4
			}

			console_2.MБасма([]byte(" size : ["))
			console_2.MUnsignedinteger32Басма(өлчөм)
			console_2.MБасма([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferБаяндамасы[currentrecvbuffer].address_2)))
			var көрсөткүч uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(көрсөткүч, int(өлчөм)) {

					console_2.MБасмаxy(([]byte)("self.Send"), 0, 22)

					self.Send(көрсөткүч, өлчөм)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalБасма(buffer_2[i])
				console_2.MБасма([]byte(":"))
			}

		}
		recvbufferБаяндамасы[currentrecvbuffer].желектери2 = 0
		recvbufferБаяндамасы[currentrecvbuffer].желектери = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initБлок.physicaladdress
}
func (self *Tamdam79c973) Setipaddress(ip uint64) {
	initБлок.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initБлок.logicaladdress
}
