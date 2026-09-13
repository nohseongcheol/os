package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "port"
import . "pci"

var tarmoqcardconsole TConsole = TConsole{}

type TInitializationBlok struct {
	rejim			uint16
	rAQAMJoʻnatishbuffer	uint8
	rAQAMrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferTaʼrifiaddress	uintptr
	joʻnatishbufferTaʼrifiaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	bayroqlar	uint32
	bayroqlar2	uint32
	mavjud		uint32
}

type IRawdatahandler interface {
	Yoqishrawdatareceive(dataKorsatgich uintptr, hajmi int) bool
	Joʻnatish(dataKorsatgich uintptr, hajmi uint32)
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
func (self *TRawdatahandler) Yoqishrawdatareceive(dataKorsatgich uintptr, hajmi int) bool {
	tarmoqcardconsole.MChopetishxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Joʻnatish(dataKorsatgich uintptr, hajmi uint32) {
	tarmoqcardconsole.MChopetishxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Joʻnatish(dataKorsatgich, hajmi)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var tiklashport uint16
var buscontrolregisterdataport uint16

var initBlok TInitializationBlok

var joʻnatishbufferTaʼrifi [8]TBufferdescriptor
var joʻnatishbufferTaʼrifiXotira [2048 + 15]byte
var joʻnatishbuffer [2*1024 + 15][8]uint8
var currentJoʻnatishbuffer uint8

var recvbufferTaʼrifi [8]TBufferdescriptor
var recvbufferTaʼrifiXotira [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcQiymat func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	uskunadescriptor	TPeripheralcomponentinterconnectUskunadescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, uskunadescriptor TPeripheralcomponentinterconnectUskunadescriptor, handler IRawdatahandler) {

	self.uskunadescriptor = uskunadescriptor

	funcQiymat = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcQiymat))

	self.Init(uint8(0x20+uskunadescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0port = uint16(uskunadescriptor.Portbase)
	Macaddress2port = uint16(uskunadescriptor.Portbase) + 0x02
	Macaddress4port = uint16(uskunadescriptor.Portbase) + 0x04
	registerdataport = uint16(uskunadescriptor.Portbase) + 0x10
	registeraddressport = uint16(uskunadescriptor.Portbase) + 0x12
	tiklashport = uint16(uskunadescriptor.Portbase) + 0x14
	buscontrolregisterdataport = uint16(uskunadescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentJoʻnatishbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(PortOʻqishsoz(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortOʻqishsoz(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortOʻqishsoz(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortOʻqishsoz(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortOʻqishsoz(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortOʻqishsoz(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MChopetishxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalChopetish(uint8(uskunadescriptor.Interrupt))
	console_2.MChopetish(([]byte)("]"))
	console_2.MChopetish(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Chopetish(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Chopetish(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MChopetish(([]byte)("]"))

	PortYozishsoz(registeraddressport, 20)
	PortYozishsoz(buscontrolregisterdataport, 0x102)

	PortYozishsoz(registeraddressport, 0)
	PortYozishsoz(registerdataport, 0x04)

	initBlok.rejim = 0x0000
	initBlok.rAQAMJoʻnatishbuffer = 3
	initBlok.rAQAMrecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logicaladdress = 0

	joʻnatishbufferTaʼrifi = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&joʻnatishbufferTaʼrifiXotira)) + 15) & ^(uintptr)(0xF)))
	initBlok.joʻnatishbufferTaʼrifiaddress = uintptr(Pointer(&joʻnatishbufferTaʼrifi))
	recvbufferTaʼrifi = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferTaʼrifiXotira)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferTaʼrifiaddress = uintptr(Pointer(&recvbufferTaʼrifi))

	for i := 0; i < 8; i++ {
		joʻnatishbufferTaʼrifi[i].address_2 = uint32((uintptr(Pointer(&joʻnatishbuffer[i])) + 15) & ^(uintptr(0xF)))
		joʻnatishbufferTaʼrifi[i].bayroqlar = 0x7FF | 0xF000
		joʻnatishbufferTaʼrifi[i].bayroqlar2 = 0
		joʻnatishbufferTaʼrifi[i].mavjud = 0

		recvbufferTaʼrifi[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferTaʼrifi[i].bayroqlar = 0xF7FF | 0x80000000

	}

	PortYozishsoz(registeraddressport, 1)
	PortYozishsoz(registerdataport, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PortYozishsoz(registeraddressport, 2)
	PortYozishsoz(registerdataport, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Faollashtirish() {
	PortYozishsoz(registeraddressport, 0)
	PortYozishsoz(registerdataport, 0x41)

	PortYozishsoz(registeraddressport, 4)
	temporary := PortOʻqishsoz(registerdataport)
	PortYozishsoz(registeraddressport, 4)
	PortYozishsoz(registerdataport, temporary|0xC00)

	PortYozishsoz(registeraddressport, 0)
	PortYozishsoz(registerdataport, 0x42)

}
func (self *Tamdam79c973) Tiklash() int {
	PortOʻqishsoz(tiklashport)
	PortYozishsoz(tiklashport, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	PortYozishsoz(registeraddressport, 0)
	temporary := uint32(PortOʻqishsoz(registerdataport))
	console_2.MChopetish(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Chopetish(esp)
	console_2.MChopetish(([]byte)(":"))
	console_2.MUnsignedinteger32Chopetish(temporary)
	console_2.MChopetish(([]byte)(":"))
	console_2.MUnsignedinteger16Chopetish(count)
	count++
	console_2.MChopetish(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MChopetish(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MChopetish(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MChopetish(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MChopetish(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MChopetish(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MChopetish(([]byte)("am79c973 data sent"))
	}

	PortYozishsoz(registeraddressport, 0)
	PortYozishsoz(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MChopetish(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Joʻnatish(dataKorsatgich uintptr, hajmi uint32) {
	var joʻnatishdescriptor uint16 = uint16(currentJoʻnatishbuffer)
	currentJoʻnatishbuffer = 0

	if hajmi > 1518 {
		hajmi = 1518
	}

	var source_2 [4096]byte = *(*([4096]byte))(Pointer(dataKorsatgich))
	var destination_2 uint32 = joʻnatishbufferTaʼrifi[joʻnatishdescriptor].address_2 + hajmi - 1

	for i := 0; i < int(hajmi); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = source_2[int(hajmi)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKorsatgich))
	console_2.MChopetishxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalChopetish(data[i])
		console_2.MChopetish(([]byte)(":"))
	}
	console_2.MChopetish(([]byte)("\n"))

	joʻnatishbufferTaʼrifi[joʻnatishdescriptor].mavjud = 0
	joʻnatishbufferTaʼrifi[joʻnatishdescriptor].bayroqlar2 = 0
	joʻnatishbufferTaʼrifi[joʻnatishdescriptor].bayroqlar = 0x8300F000 | uint32((-hajmi)&0xFFF)

	PortYozishsoz(registeraddressport, 0)
	PortYozishsoz(registerdataport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MChopetish(([]byte)(":"))
	console_2.MUnsignedinteger32Chopetish(uint32(uintptr(Pointer(&joʻnatishbuffer))))
	console_2.MChopetish(([]byte)(":"))
	console_2.MHexadecimalChopetish(joʻnatishbuffer[0][0])
	console_2.MHexadecimalChopetish(joʻnatishbuffer[0][1])
	console_2.MChopetish(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferTaʼrifi[currentrecvbuffer].bayroqlar & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferTaʼrifi[currentrecvbuffer].bayroqlar&0x40000000 != 0) && ((recvbufferTaʼrifi[currentrecvbuffer].bayroqlar & 0x03000000) == 0x03000000) {
			var hajmi uint32 = recvbufferTaʼrifi[currentrecvbuffer].bayroqlar & 0xFFF
			if hajmi > 64 {
				hajmi -= 4
			}

			console_2.MChopetish([]byte(" size : ["))
			console_2.MUnsignedinteger32Chopetish(hajmi)
			console_2.MChopetish([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferTaʼrifi[currentrecvbuffer].address_2)))
			var korsatgich uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Yoqishrawdatareceive(korsatgich, int(hajmi)) {

					console_2.MChopetishxy(([]byte)("self.Send"), 0, 22)

					self.Joʻnatish(korsatgich, hajmi)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalChopetish(buffer_2[i])
				console_2.MChopetish([]byte(":"))
			}

		}
		recvbufferTaʼrifi[currentrecvbuffer].bayroqlar2 = 0
		recvbufferTaʼrifi[currentrecvbuffer].bayroqlar = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (self *Tamdam79c973) Setipaddress(ip uint64) {
	initBlok.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logicaladdress
}
