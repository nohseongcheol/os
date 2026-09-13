package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "qapı"
import . "pci"

var şəbəkəcardconsole TConsole = TConsole{}

type TInitializationblock struct {
	mod			uint16
	numbersendbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferİzahataddress	uintptr
	sendbufferİzahataddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	bayraqlar	uint32
	bayraqlar2	uint32
	available	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(datapointer uintptr, böyüklük int) bool
	Send(datapointer uintptr, böyüklük uint32)
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
func (self *TRawdatahandler) Onrawdatareceive(datapointer uintptr, böyüklük int) bool {
	şəbəkəcardconsole.MÇapEtxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Send(datapointer uintptr, böyüklük uint32) {
	şəbəkəcardconsole.MÇapEtxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(datapointer, böyüklük)
}

var Macaddress0Qapı uint16
var Macaddress2Qapı uint16
var Macaddress4Qapı uint16
var registerdataQapı uint16
var registeraddressQapı uint16
var sıfırlaQapı uint16
var buscontrolregisterdataQapı uint16

var initblock TInitializationblock

var sendbufferİzahat [8]TBufferdescriptor
var sendbufferİzahatYaddaş [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferİzahat [8]TBufferdescriptor
var recvbufferİzahatYaddaş [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcQiymət func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	avadanlıqdescriptor	TPeripheralcomponentinterconnectAvadanlıqdescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, avadanlıqdescriptor TPeripheralcomponentinterconnectAvadanlıqdescriptor, handler IRawdatahandler) {

	self.avadanlıqdescriptor = avadanlıqdescriptor

	funcQiymət = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcQiymət))

	self.Init(uint8(0x20+avadanlıqdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Qapı = uint16(avadanlıqdescriptor.Qapıbase)
	Macaddress2Qapı = uint16(avadanlıqdescriptor.Qapıbase) + 0x02
	Macaddress4Qapı = uint16(avadanlıqdescriptor.Qapıbase) + 0x04
	registerdataQapı = uint16(avadanlıqdescriptor.Qapıbase) + 0x10
	registeraddressQapı = uint16(avadanlıqdescriptor.Qapıbase) + 0x12
	sıfırlaQapı = uint16(avadanlıqdescriptor.Qapıbase) + 0x14
	buscontrolregisterdataQapı = uint16(avadanlıqdescriptor.Qapıbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(QapıOxumaword(Macaddress0Qapı) % 256)
	var Mac1 uint64 = uint64(QapıOxumaword(Macaddress0Qapı) / 256)
	var Mac2 uint64 = uint64(QapıOxumaword(Macaddress2Qapı) % 256)
	var Mac3 uint64 = uint64(QapıOxumaword(Macaddress2Qapı) / 256)
	var Mac4 uint64 = uint64(QapıOxumaword(Macaddress4Qapı) % 256)
	var Mac5 uint64 = uint64(QapıOxumaword(Macaddress4Qapı) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MÇapEtxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalÇapEt(uint8(avadanlıqdescriptor.Interrupt))
	console_2.MÇapEt(([]byte)("]"))
	console_2.MÇapEt(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16ÇapEt(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32ÇapEt(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MÇapEt(([]byte)("]"))

	QapıYazmaword(registeraddressQapı, 20)
	QapıYazmaword(buscontrolregisterdataQapı, 0x102)

	QapıYazmaword(registeraddressQapı, 0)
	QapıYazmaword(registerdataQapı, 0x04)

	initblock.mod = 0x0000
	initblock.numbersendbuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	sendbufferİzahat = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferİzahatYaddaş)) + 15) & ^(uintptr)(0xF)))
	initblock.sendbufferİzahataddress = uintptr(Pointer(&sendbufferİzahat))
	recvbufferİzahat = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferİzahatYaddaş)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferİzahataddress = uintptr(Pointer(&recvbufferİzahat))

	for i := 0; i < 8; i++ {
		sendbufferİzahat[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferİzahat[i].bayraqlar = 0x7FF | 0xF000
		sendbufferİzahat[i].bayraqlar2 = 0
		sendbufferİzahat[i].available = 0

		recvbufferİzahat[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferİzahat[i].bayraqlar = 0xF7FF | 0x80000000

	}

	QapıYazmaword(registeraddressQapı, 1)
	QapıYazmaword(registerdataQapı, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	QapıYazmaword(registeraddressQapı, 2)
	QapıYazmaword(registerdataQapı, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Activate() {
	QapıYazmaword(registeraddressQapı, 0)
	QapıYazmaword(registerdataQapı, 0x41)

	QapıYazmaword(registeraddressQapı, 4)
	temporary := QapıOxumaword(registerdataQapı)
	QapıYazmaword(registeraddressQapı, 4)
	QapıYazmaword(registerdataQapı, temporary|0xC00)

	QapıYazmaword(registeraddressQapı, 0)
	QapıYazmaword(registerdataQapı, 0x42)

}
func (self *Tamdam79c973) Sıfırla() int {
	QapıOxumaword(sıfırlaQapı)
	QapıYazmaword(sıfırlaQapı, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	QapıYazmaword(registeraddressQapı, 0)
	temporary := uint32(QapıOxumaword(registerdataQapı))
	console_2.MÇapEt(([]byte)("interrupt("))
	console_2.MUnsignedinteger32ÇapEt(esp)
	console_2.MÇapEt(([]byte)(":"))
	console_2.MUnsignedinteger32ÇapEt(temporary)
	console_2.MÇapEt(([]byte)(":"))
	console_2.MUnsignedinteger16ÇapEt(count)
	count++
	console_2.MÇapEt(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MÇapEt(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MÇapEt(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MÇapEt(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MÇapEt(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MÇapEt(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MÇapEt(([]byte)("am79c973 data sent"))
	}

	QapıYazmaword(registeraddressQapı, 0)
	QapıYazmaword(registerdataQapı, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MÇapEt(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Send(datapointer uintptr, böyüklük uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if böyüklük > 1518 {
		böyüklük = 1518
	}

	var mənbə_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var destination_2 uint32 = sendbufferİzahat[senddescriptor].address_2 + böyüklük - 1

	for i := 0; i < int(böyüklük); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = mənbə_2[int(böyüklük)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	console_2.MÇapEtxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalÇapEt(data[i])
		console_2.MÇapEt(([]byte)(":"))
	}
	console_2.MÇapEt(([]byte)("\n"))

	sendbufferİzahat[senddescriptor].available = 0
	sendbufferİzahat[senddescriptor].bayraqlar2 = 0
	sendbufferİzahat[senddescriptor].bayraqlar = 0x8300F000 | uint32((-böyüklük)&0xFFF)

	QapıYazmaword(registeraddressQapı, 0)
	QapıYazmaword(registerdataQapı, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MÇapEt(([]byte)(":"))
	console_2.MUnsignedinteger32ÇapEt(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.MÇapEt(([]byte)(":"))
	console_2.MHexadecimalÇapEt(sendbuffer[0][0])
	console_2.MHexadecimalÇapEt(sendbuffer[0][1])
	console_2.MÇapEt(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferİzahat[currentrecvbuffer].bayraqlar & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferİzahat[currentrecvbuffer].bayraqlar&0x40000000 != 0) && ((recvbufferİzahat[currentrecvbuffer].bayraqlar & 0x03000000) == 0x03000000) {
			var böyüklük uint32 = recvbufferİzahat[currentrecvbuffer].bayraqlar & 0xFFF
			if böyüklük > 64 {
				böyüklük -= 4
			}

			console_2.MÇapEt([]byte(" size : ["))
			console_2.MUnsignedinteger32ÇapEt(böyüklük)
			console_2.MÇapEt([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferİzahat[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(pointer, int(böyüklük)) {

					console_2.MÇapEtxy(([]byte)("self.Send"), 0, 22)

					self.Send(pointer, böyüklük)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalÇapEt(buffer_2[i])
				console_2.MÇapEt([]byte(":"))
			}

		}
		recvbufferİzahat[currentrecvbuffer].bayraqlar2 = 0
		recvbufferİzahat[currentrecvbuffer].bayraqlar = 0x8000F7FF
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
