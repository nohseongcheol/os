/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "مداخلت"
import . "console"
import . "پورٹ"
import . "pci"

var نیٹورکcardconsole TConsole = TConsole{}

type TInitializationblock struct {
	mode			uint16
	numbersendbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferتفصیلaddress	uintptr
	sendbufferتفصیلaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	جھنڈیاں		uint32
	جھنڈیاں2	uint32
	دستیاب		uint32
}

type IRawdatahandler interface {
	Oچالوrawdatareceive(dataپؤائنٹر uintptr, حجم int) bool
	Send(dataپؤائنٹر uintptr, حجم uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Sسیٹbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Oچالوrawdatareceive(dataپؤائنٹر uintptr, حجم int) bool {
	نیٹورکcardconsole.Mچھاپیںxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Send(dataپؤائنٹر uintptr, حجم uint32) {
	نیٹورکcardconsole.Mچھاپیںxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(dataپؤائنٹر, حجم)
}

var Macaddress0پورٹ uint16
var Macaddress2پورٹ uint16
var Macaddress4پورٹ uint16
var registerdataپورٹ uint16
var registeraddressپورٹ uint16
var ازسرنوتعینکریںپورٹ uint16
var buscontrolregisterdataپورٹ uint16

var initblock TInitializationblock

var sendbufferتفصیل [8]TBufferdescriptor
var sendbufferتفصیلیادداشت [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var حالیہsendbuffer uint8

var recvbufferتفصیل [8]TBufferdescriptor
var recvbufferتفصیلیادداشت [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var حالیہrecvbuffer uint8
var funcقدر func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	Tمداخلتhandler
	آلہdescriptor	TPeripheralcomponentinterconnectآلہdescriptor
	مداخلت		*Tمداخلتmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(مداخلت *Tمداخلتmanager, آلہdescriptor TPeripheralcomponentinterconnectآلہdescriptor, handler IRawdatahandler) {

	self.آلہdescriptor = آلہdescriptor

	funcقدر = (*Tamdam79c973).Handleمداخلت
	var address uintptr
	address = uintptr(Pointer(&funcقدر))

	self.Init(uint8(0x20+آلہdescriptor.Iمداخلت), uintptr(Pointer(مداخلت)), address)

	Macaddress0پورٹ = uint16(آلہdescriptor.Pپورٹbase)
	Macaddress2پورٹ = uint16(آلہdescriptor.Pپورٹbase) + 0x02
	Macaddress4پورٹ = uint16(آلہdescriptor.Pپورٹbase) + 0x04
	registerdataپورٹ = uint16(آلہdescriptor.Pپورٹbase) + 0x10
	registeraddressپورٹ = uint16(آلہdescriptor.Pپورٹbase) + 0x12
	ازسرنوتعینکریںپورٹ = uint16(آلہdescriptor.Pپورٹbase) + 0x14
	buscontrolregisterdataپورٹ = uint16(آلہdescriptor.Pپورٹbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	حالیہsendbuffer = 0
	حالیہrecvbuffer = 0

	var Mac0 uint64 = uint64(Pپورٹپڑھیںلفظ(Macaddress0پورٹ) % 256)
	var Mac1 uint64 = uint64(Pپورٹپڑھیںلفظ(Macaddress0پورٹ) / 256)
	var Mac2 uint64 = uint64(Pپورٹپڑھیںلفظ(Macaddress2پورٹ) % 256)
	var Mac3 uint64 = uint64(Pپورٹپڑھیںلفظ(Macaddress2پورٹ) / 256)
	var Mac4 uint64 = uint64(Pپورٹپڑھیںلفظ(Macaddress4پورٹ) % 256)
	var Mac5 uint64 = uint64(Pپورٹپڑھیںلفظ(Macaddress4پورٹ) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.Mچھاپیںxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalچھاپیں(uint8(آلہdescriptor.Iمداخلت))
	console_2.Mچھاپیں(([]byte)("]"))
	console_2.Mچھاپیں(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16چھاپیں(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32چھاپیں(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.Mچھاپیں(([]byte)("]"))

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 20)
	Pپورٹلکھیںلفظ(buscontrolregisterdataپورٹ, 0x102)

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 0)
	Pپورٹلکھیںلفظ(registerdataپورٹ, 0x04)

	initblock.mode = 0x0000
	initblock.numbersendbuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	sendbufferتفصیل = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferتفصیلیادداشت)) + 15) & ^(uintptr)(0xF)))
	initblock.sendbufferتفصیلaddress = uintptr(Pointer(&sendbufferتفصیل))
	recvbufferتفصیل = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferتفصیلیادداشت)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferتفصیلaddress = uintptr(Pointer(&recvbufferتفصیل))

	for i := 0; i < 8; i++ {
		sendbufferتفصیل[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferتفصیل[i].جھنڈیاں = 0x7FF | 0xF000
		sendbufferتفصیل[i].جھنڈیاں2 = 0
		sendbufferتفصیل[i].دستیاب = 0

		recvbufferتفصیل[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferتفصیل[i].جھنڈیاں = 0xF7FF | 0x80000000

	}

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 1)
	Pپورٹلکھیںلفظ(registerdataپورٹ, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 2)
	Pپورٹلکھیںلفظ(registerdataپورٹ, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aفعالکریں() {
	Pپورٹلکھیںلفظ(registeraddressپورٹ, 0)
	Pپورٹلکھیںلفظ(registerdataپورٹ, 0x41)

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 4)
	temporary := Pپورٹپڑھیںلفظ(registerdataپورٹ)
	Pپورٹلکھیںلفظ(registeraddressپورٹ, 4)
	Pپورٹلکھیںلفظ(registerdataپورٹ, temporary|0xC00)

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 0)
	Pپورٹلکھیںلفظ(registerdataپورٹ, 0x42)

}
func (self *Tamdam79c973) Rازسرنوتعینکریں() int {
	Pپورٹپڑھیںلفظ(ازسرنوتعینکریںپورٹ)
	Pپورٹلکھیںلفظ(ازسرنوتعینکریںپورٹ, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleمداخلت(esp uint32) uint32 {

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 0)
	temporary := uint32(Pپورٹپڑھیںلفظ(registerdataپورٹ))
	console_2.Mچھاپیں(([]byte)("interrupt("))
	console_2.MUnsignedinteger32چھاپیں(esp)
	console_2.Mچھاپیں(([]byte)(":"))
	console_2.MUnsignedinteger32چھاپیں(temporary)
	console_2.Mچھاپیں(([]byte)(":"))
	console_2.MUnsignedinteger16چھاپیں(count)
	count++
	console_2.Mچھاپیں(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.Mچھاپیں(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.Mچھاپیں(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.Mچھاپیں(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.Mچھاپیں(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.Mچھاپیں(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.Mچھاپیں(([]byte)("am79c973 data sent"))
	}

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 0)
	Pپورٹلکھیںلفظ(registerdataپورٹ, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.Mچھاپیں(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Send(dataپؤائنٹر uintptr, حجم uint32) {
	var senddescriptor uint16 = uint16(حالیہsendbuffer)
	حالیہsendbuffer = 0

	if حجم > 1518 {
		حجم = 1518
	}

	var مصدر_2 [4096]byte = *(*([4096]byte))(Pointer(dataپؤائنٹر))
	var destination_2 uint32 = sendbufferتفصیل[senddescriptor].address_2 + حجم - 1

	for i := 0; i < int(حجم); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = مصدر_2[int(حجم)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataپؤائنٹر))
	console_2.Mچھاپیںxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalچھاپیں(data[i])
		console_2.Mچھاپیں(([]byte)(":"))
	}
	console_2.Mچھاپیں(([]byte)("\n"))

	sendbufferتفصیل[senddescriptor].دستیاب = 0
	sendbufferتفصیل[senddescriptor].جھنڈیاں2 = 0
	sendbufferتفصیل[senddescriptor].جھنڈیاں = 0x8300F000 | uint32((-حجم)&0xFFF)

	Pپورٹلکھیںلفظ(registeraddressپورٹ, 0)
	Pپورٹلکھیںلفظ(registerdataپورٹ, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.Mچھاپیں(([]byte)(":"))
	console_2.MUnsignedinteger32چھاپیں(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.Mچھاپیں(([]byte)(":"))
	console_2.MHexadecimalچھاپیں(sendbuffer[0][0])
	console_2.MHexadecimalچھاپیں(sendbuffer[0][1])
	console_2.Mچھاپیں(([]byte)(":"))
	حالیہrecvbuffer = 0

	for ; (recvbufferتفصیل[حالیہrecvbuffer].جھنڈیاں & 0x80000000) == 0; حالیہrecvbuffer = (حالیہrecvbuffer + 1) % 8 {

		if !(recvbufferتفصیل[حالیہrecvbuffer].جھنڈیاں&0x40000000 != 0) && ((recvbufferتفصیل[حالیہrecvbuffer].جھنڈیاں & 0x03000000) == 0x03000000) {
			var حجم uint32 = recvbufferتفصیل[حالیہrecvbuffer].جھنڈیاں & 0xFFF
			if حجم > 64 {
				حجم -= 4
			}

			console_2.Mچھاپیں([]byte(" size : ["))
			console_2.MUnsignedinteger32چھاپیں(حجم)
			console_2.Mچھاپیں([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferتفصیل[حالیہrecvbuffer].address_2)))
			var پؤائنٹر uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Oچالوrawdatareceive(پؤائنٹر, int(حجم)) {

					console_2.Mچھاپیںxy(([]byte)("self.Send"), 0, 22)

					self.Send(پؤائنٹر, حجم)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalچھاپیں(buffer_2[i])
				console_2.Mچھاپیں([]byte(":"))
			}

		}
		recvbufferتفصیل[حالیہrecvbuffer].جھنڈیاں2 = 0
		recvbufferتفصیل[حالیہrecvbuffer].جھنڈیاں = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sسیٹhandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initblock.physicaladdress
}
func (self *Tamdam79c973) Sسیٹipaddress(ip uint64) {
	initblock.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initblock.logicaladdress
}
