package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "პორტი"
import . "pci"

var ქსელიბანქოconsole TConsole = TConsole{}

type TInitializationblock struct {
	რეჟიმი			uint16
	რიცხვიგაგზავნაbuffer	uint8
	რიცხვიrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferაღწერილობაaddress	uintptr
	გაგზავნაbufferაღწერილობაaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	ალმები		uint32
	ალმები2		uint32
	ხელმისაწვდომი	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(dataკურსორი uintptr, ზომა int) bool
	Sგაგზავნა(dataკურსორი uintptr, ზომა uint32)
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
func (self *TRawdatahandler) Onrawdatareceive(dataკურსორი uintptr, ზომა int) bool {
	ქსელიბანქოconsole.Mბეჭდვაxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Sგაგზავნა(dataკურსორი uintptr, ზომა uint32) {
	ქსელიბანქოconsole.Mბეჭდვაxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Sგაგზავნა(dataკურსორი, ზომა)
}

var Macaddress0პორტი uint16
var Macaddress2პორტი uint16
var Macaddress4პორტი uint16
var registerdataპორტი uint16
var registeraddressპორტი uint16
var განულებაპორტი uint16
var buscontrolregisterdataპორტი uint16

var initblock TInitializationblock

var გაგზავნაbufferაღწერილობა [8]TBufferdescriptor
var გაგზავნაbufferაღწერილობამეხსიერება [2048 + 15]byte
var გაგზავნაbuffer [2*1024 + 15][8]uint8
var currentგაგზავნაbuffer uint8

var recvbufferაღწერილობა [8]TBufferdescriptor
var recvbufferაღწერილობამეხსიერება [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcმნიშვნელობა func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	მოწყობილობაdescriptor	TPeripheralcomponentinterconnectმოწყობილობაdescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, მოწყობილობაdescriptor TPeripheralcomponentinterconnectმოწყობილობაdescriptor, handler IRawdatahandler) {

	self.მოწყობილობაdescriptor = მოწყობილობაdescriptor

	funcმნიშვნელობა = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcმნიშვნელობა))

	self.Init(uint8(0x20+მოწყობილობაdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0პორტი = uint16(მოწყობილობაdescriptor.Pპორტიbase)
	Macaddress2პორტი = uint16(მოწყობილობაdescriptor.Pპორტიbase) + 0x02
	Macaddress4პორტი = uint16(მოწყობილობაdescriptor.Pპორტიbase) + 0x04
	registerdataპორტი = uint16(მოწყობილობაdescriptor.Pპორტიbase) + 0x10
	registeraddressპორტი = uint16(მოწყობილობაdescriptor.Pპორტიbase) + 0x12
	განულებაპორტი = uint16(მოწყობილობაdescriptor.Pპორტიbase) + 0x14
	buscontrolregisterdataპორტი = uint16(მოწყობილობაdescriptor.Pპორტიbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentგაგზავნაbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(Pპორტიკითხვასიტყვა(Macaddress0პორტი) % 256)
	var Mac1 uint64 = uint64(Pპორტიკითხვასიტყვა(Macaddress0პორტი) / 256)
	var Mac2 uint64 = uint64(Pპორტიკითხვასიტყვა(Macaddress2პორტი) % 256)
	var Mac3 uint64 = uint64(Pპორტიკითხვასიტყვა(Macaddress2პორტი) / 256)
	var Mac4 uint64 = uint64(Pპორტიკითხვასიტყვა(Macaddress4პორტი) % 256)
	var Mac5 uint64 = uint64(Pპორტიკითხვასიტყვა(Macaddress4პორტი) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.Mბეჭდვაxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalბეჭდვა(uint8(მოწყობილობაdescriptor.Interrupt))
	console_2.Mბეჭდვა(([]byte)("]"))
	console_2.Mბეჭდვა(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16ბეჭდვა(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32ბეჭდვა(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.Mბეჭდვა(([]byte)("]"))

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 20)
	Pპორტიჩაწერასიტყვა(buscontrolregisterdataპორტი, 0x102)

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 0)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, 0x04)

	initblock.რეჟიმი = 0x0000
	initblock.რიცხვიგაგზავნაbuffer = 3
	initblock.რიცხვიrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	გაგზავნაbufferაღწერილობა = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&გაგზავნაbufferაღწერილობამეხსიერება)) + 15) & ^(uintptr)(0xF)))
	initblock.გაგზავნაbufferაღწერილობაaddress = uintptr(Pointer(&გაგზავნაbufferაღწერილობა))
	recvbufferაღწერილობა = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferაღწერილობამეხსიერება)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferაღწერილობაaddress = uintptr(Pointer(&recvbufferაღწერილობა))

	for i := 0; i < 8; i++ {
		გაგზავნაbufferაღწერილობა[i].address_2 = uint32((uintptr(Pointer(&გაგზავნაbuffer[i])) + 15) & ^(uintptr(0xF)))
		გაგზავნაbufferაღწერილობა[i].ალმები = 0x7FF | 0xF000
		გაგზავნაbufferაღწერილობა[i].ალმები2 = 0
		გაგზავნაbufferაღწერილობა[i].ხელმისაწვდომი = 0

		recvbufferაღწერილობა[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferაღწერილობა[i].ალმები = 0xF7FF | 0x80000000

	}

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 1)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 2)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aგააქტიურება() {
	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 0)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, 0x41)

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 4)
	temporary := Pპორტიკითხვასიტყვა(registerdataპორტი)
	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 4)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, temporary|0xC00)

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 0)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, 0x42)

}
func (self *Tamdam79c973) Rგანულება() int {
	Pპორტიკითხვასიტყვა(განულებაპორტი)
	Pპორტიჩაწერასიტყვა(განულებაპორტი, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 0)
	temporary := uint32(Pპორტიკითხვასიტყვა(registerdataპორტი))
	console_2.Mბეჭდვა(([]byte)("interrupt("))
	console_2.MUnsignedinteger32ბეჭდვა(esp)
	console_2.Mბეჭდვა(([]byte)(":"))
	console_2.MUnsignedinteger32ბეჭდვა(temporary)
	console_2.Mბეჭდვა(([]byte)(":"))
	console_2.MUnsignedinteger16ბეჭდვა(count)
	count++
	console_2.Mბეჭდვა(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.Mბეჭდვა(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.Mბეჭდვა(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.Mბეჭდვა(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.Mბეჭდვა(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.Mბეჭდვა(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.Mბეჭდვა(([]byte)("am79c973 data sent"))
	}

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 0)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.Mბეჭდვა(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Sგაგზავნა(dataკურსორი uintptr, ზომა uint32) {
	var გაგზავნაdescriptor uint16 = uint16(currentგაგზავნაbuffer)
	currentგაგზავნაbuffer = 0

	if ზომა > 1518 {
		ზომა = 1518
	}

	var წყარო_2 [4096]byte = *(*([4096]byte))(Pointer(dataკურსორი))
	var destination_2 uint32 = გაგზავნაbufferაღწერილობა[გაგზავნაdescriptor].address_2 + ზომა - 1

	for i := 0; i < int(ზომა); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = წყარო_2[int(ზომა)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataკურსორი))
	console_2.Mბეჭდვაxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalბეჭდვა(data[i])
		console_2.Mბეჭდვა(([]byte)(":"))
	}
	console_2.Mბეჭდვა(([]byte)("\n"))

	გაგზავნაbufferაღწერილობა[გაგზავნაdescriptor].ხელმისაწვდომი = 0
	გაგზავნაbufferაღწერილობა[გაგზავნაdescriptor].ალმები2 = 0
	გაგზავნაbufferაღწერილობა[გაგზავნაdescriptor].ალმები = 0x8300F000 | uint32((-ზომა)&0xFFF)

	Pპორტიჩაწერასიტყვა(registeraddressპორტი, 0)
	Pპორტიჩაწერასიტყვა(registerdataპორტი, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.Mბეჭდვა(([]byte)(":"))
	console_2.MUnsignedinteger32ბეჭდვა(uint32(uintptr(Pointer(&გაგზავნაbuffer))))
	console_2.Mბეჭდვა(([]byte)(":"))
	console_2.MHexadecimalბეჭდვა(გაგზავნაbuffer[0][0])
	console_2.MHexadecimalბეჭდვა(გაგზავნაbuffer[0][1])
	console_2.Mბეჭდვა(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferაღწერილობა[currentrecvbuffer].ალმები & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferაღწერილობა[currentrecvbuffer].ალმები&0x40000000 != 0) && ((recvbufferაღწერილობა[currentrecvbuffer].ალმები & 0x03000000) == 0x03000000) {
			var ზომა uint32 = recvbufferაღწერილობა[currentrecvbuffer].ალმები & 0xFFF
			if ზომა > 64 {
				ზომა -= 4
			}

			console_2.Mბეჭდვა([]byte(" size : ["))
			console_2.MUnsignedinteger32ბეჭდვა(ზომა)
			console_2.Mბეჭდვა([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferაღწერილობა[currentrecvbuffer].address_2)))
			var კურსორი uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(კურსორი, int(ზომა)) {

					console_2.Mბეჭდვაxy(([]byte)("self.Send"), 0, 22)

					self.Sგაგზავნა(კურსორი, ზომა)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalბეჭდვა(buffer_2[i])
				console_2.Mბეჭდვა([]byte(":"))
			}

		}
		recvbufferაღწერილობა[currentrecvbuffer].ალმები2 = 0
		recvbufferაღწერილობა[currentrecvbuffer].ალმები = 0x8000F7FF
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
