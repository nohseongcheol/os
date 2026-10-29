/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "مقاطعة"
import . "طرفية"
import . "منفذ"
import . "pci"

var شبكةورقطرفية Tطرفية = Tطرفية{}

type TInitializationحظر struct {
	وضع			uint16
	الأرقامأرسلbuffer	uint8
	الأرقامrecvbuffer	uint8

	ماديaddress	uint64

	logicaladdress		uint64
	recvbufferالوصفaddress	uintptr
	أرسلbufferالوصفaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	خيارات		uint32
	خيارات2		uint32
	متوفر		uint32
}

type IRawبياناتhandler interface {
	Oعندrawبياناتreceive(بياناتالمؤشر uintptr, الحجم int) bool
	Sأرسل(بياناتالمؤشر uintptr, الحجم uint32)
}

var rawبياناتbackend Tamdam79c973

type TRawبياناتhandler struct {
}

func (نفسه *TRawبياناتhandler) Sتحديدbackend(backend Tamdam79c973) {

	rawبياناتbackend = backend
}
func (نفسه *TRawبياناتhandler) Getbackend() Tamdam79c973 {
	return rawبياناتbackend
}
func (نفسه *TRawبياناتhandler) Oعندrawبياناتreceive(بياناتالمؤشر uintptr, الحجم int) bool {
	شبكةورقطرفية.Mاطبعxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (نفسه *TRawبياناتhandler) Sأرسل(بياناتالمؤشر uintptr, الحجم uint32) {
	شبكةورقطرفية.Mاطبعxy(([]byte)("TRawDataSend"), 10, 10)
	rawبياناتbackend.Sأرسل(بياناتالمؤشر, الحجم)
}

var Macaddress0منفذ uint16
var Macaddress2منفذ uint16
var Macaddress4منفذ uint16
var سجلبياناتمنفذ uint16
var سجلaddressمنفذ uint16
var أعدالضبطمنفذ uint16
var busتحكمسجلبياناتمنفذ uint16

var initحظر TInitializationحظر

var أرسلbufferالوصف [8]TBufferdescriptor
var أرسلbufferالوصفذاكرة [2048 + 15]byte
var أرسلbuffer [2*1024 + 15][8]uint8
var الحاليأرسلbuffer uint8

var recvbufferالوصف [8]TBufferdescriptor
var recvbufferالوصفذاكرة [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var الحاليrecvbuffer uint8
var funcالقيمة func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	Tمقاطعةhandler
	الجهازdescriptor	TPeripheralcomponentinterconnectالجهازdescriptor
	مقاطعة			*Tمقاطعةمدير
	handler			*TRawبياناتhandler
}

var طرفية_2 Tطرفية = Tطرفية{}
var irawبياناتhandler IRawبياناتhandler

func (نفسه *Tamdam79c973) Initمشغل(مقاطعة *Tمقاطعةمدير, الجهازdescriptor TPeripheralcomponentinterconnectالجهازdescriptor, handler IRawبياناتhandler) {

	نفسه.الجهازdescriptor = الجهازdescriptor

	funcالقيمة = (*Tamdam79c973).Hالتعاملمقاطعة
	var address uintptr
	address = uintptr(Pointer(&funcالقيمة))

	نفسه.Init(uint8(0x20+الجهازdescriptor.Iمقاطعة), uintptr(Pointer(مقاطعة)), address)

	Macaddress0منفذ = uint16(الجهازdescriptor.Pمنفذbase)
	Macaddress2منفذ = uint16(الجهازdescriptor.Pمنفذbase) + 0x02
	Macaddress4منفذ = uint16(الجهازdescriptor.Pمنفذbase) + 0x04
	سجلبياناتمنفذ = uint16(الجهازdescriptor.Pمنفذbase) + 0x10
	سجلaddressمنفذ = uint16(الجهازdescriptor.Pمنفذbase) + 0x12
	أعدالضبطمنفذ = uint16(الجهازdescriptor.Pمنفذbase) + 0x14
	busتحكمسجلبياناتمنفذ = uint16(الجهازdescriptor.Pمنفذbase) + 0x16

	irawبياناتhandler = &TRawبياناتhandler{}
	if handler != nil {
		irawبياناتhandler = handler
	}

	الحاليأرسلbuffer = 0
	الحاليrecvbuffer = 0

	var Mac0 uint64 = uint64(Pمنفذقراءةكلمة(Macaddress0منفذ) % 256)
	var Mac1 uint64 = uint64(Pمنفذقراءةكلمة(Macaddress0منفذ) / 256)
	var Mac2 uint64 = uint64(Pمنفذقراءةكلمة(Macaddress2منفذ) % 256)
	var Mac3 uint64 = uint64(Pمنفذقراءةكلمة(Macaddress2منفذ) / 256)
	var Mac4 uint64 = uint64(Pمنفذقراءةكلمة(Macaddress4منفذ) % 256)
	var Mac5 uint64 = uint64(Pمنفذقراءةكلمة(Macaddress4منفذ) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	طرفية_2.Mاطبعxy(([]byte)("[interrupt num : "), 0, 13)
	طرفية_2.MHexadecimalاطبع(uint8(الجهازdescriptor.Iمقاطعة))
	طرفية_2.Mاطبع(([]byte)("]"))
	طرفية_2.Mاطبع(([]byte)("[mac address : "))
	طرفية_2.MUnsignedinteger16اطبع(uint16(macaddress >> 32))
	طرفية_2.MUnsignedinteger32اطبع(uint32(macaddress & 0x00000000FFFFFFFF))
	طرفية_2.Mاطبع(([]byte)("]"))

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 20)
	Pمنفذكتابةكلمة(busتحكمسجلبياناتمنفذ, 0x102)

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 0)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, 0x04)

	initحظر.وضع = 0x0000
	initحظر.الأرقامأرسلbuffer = 3
	initحظر.الأرقامrecvbuffer = 3

	initحظر.ماديaddress = Mac

	initحظر.logicaladdress = 0

	أرسلbufferالوصف = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&أرسلbufferالوصفذاكرة)) + 15) & ^(uintptr)(0xF)))
	initحظر.أرسلbufferالوصفaddress = uintptr(Pointer(&أرسلbufferالوصف))
	recvbufferالوصف = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferالوصفذاكرة)) + 15) & ^(uintptr)(0xF)))
	initحظر.recvbufferالوصفaddress = uintptr(Pointer(&recvbufferالوصف))

	for i := 0; i < 8; i++ {
		أرسلbufferالوصف[i].address_2 = uint32((uintptr(Pointer(&أرسلbuffer[i])) + 15) & ^(uintptr(0xF)))
		أرسلbufferالوصف[i].خيارات = 0x7FF | 0xF000
		أرسلbufferالوصف[i].خيارات2 = 0
		أرسلbufferالوصف[i].متوفر = 0

		recvbufferالوصف[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferالوصف[i].خيارات = 0xF7FF | 0x80000000

	}

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 1)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, uint16(uintptr(Pointer(&initحظر))&0xFFFF))

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 2)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, uint16((uintptr(Pointer(&initحظر))>>16)&0xFFFF))

}
func (نفسه *Tamdam79c973) Activate() {
	Pمنفذكتابةكلمة(سجلaddressمنفذ, 0)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, 0x41)

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 4)
	temporary := Pمنفذقراءةكلمة(سجلبياناتمنفذ)
	Pمنفذكتابةكلمة(سجلaddressمنفذ, 4)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, temporary|0xC00)

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 0)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, 0x42)

}
func (نفسه *Tamdam79c973) Rأعدالضبط() int {
	Pمنفذقراءةكلمة(أعدالضبطمنفذ)
	Pمنفذكتابةكلمة(أعدالضبطمنفذ, 0)
	return 10
}

var count uint16 = 0

func (نفسه *Tamdam79c973) Hالتعاملمقاطعة(esp uint32) uint32 {

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 0)
	temporary := uint32(Pمنفذقراءةكلمة(سجلبياناتمنفذ))
	طرفية_2.Mاطبع(([]byte)("interrupt("))
	طرفية_2.MUnsignedinteger32اطبع(esp)
	طرفية_2.Mاطبع(([]byte)(":"))
	طرفية_2.MUnsignedinteger32اطبع(temporary)
	طرفية_2.Mاطبع(([]byte)(":"))
	طرفية_2.MUnsignedinteger16اطبع(count)
	count++
	طرفية_2.Mاطبع(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		طرفية_2.Mاطبع(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		طرفية_2.Mاطبع(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		طرفية_2.Mاطبع(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		طرفية_2.Mاطبع(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		طرفية_2.Mاطبع(([]byte)("am79c973 data received"))
		نفسه.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		طرفية_2.Mاطبع(([]byte)("am79c973 data sent"))
	}

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 0)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		طرفية_2.Mاطبع(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (نفسه *Tamdam79c973) Sأرسل(بياناتالمؤشر uintptr, الحجم uint32) {
	var أرسلdescriptor uint16 = uint16(الحاليأرسلbuffer)
	الحاليأرسلbuffer = 0

	if الحجم > 1518 {
		الحجم = 1518
	}

	var المصدر_2 [4096]byte = *(*([4096]byte))(Pointer(بياناتالمؤشر))
	var المقصد_2 uint32 = أرسلbufferالوصف[أرسلdescriptor].address_2 + الحجم - 1

	for i := 0; i < int(الحجم); i++ {

		*(*byte)(Pointer(uintptr(المقصد_2))) = المصدر_2[int(الحجم)-i-1]

		المقصد_2--
	}

	var بيانات [4096]byte = *(*([4096]byte))(Pointer(بياناتالمؤشر))
	طرفية_2.Mاطبعxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		طرفية_2.MHexadecimalاطبع(بيانات[i])
		طرفية_2.Mاطبع(([]byte)(":"))
	}
	طرفية_2.Mاطبع(([]byte)("\n"))

	أرسلbufferالوصف[أرسلdescriptor].متوفر = 0
	أرسلbufferالوصف[أرسلdescriptor].خيارات2 = 0
	أرسلbufferالوصف[أرسلdescriptor].خيارات = 0x8300F000 | uint32((-الحجم)&0xFFF)

	Pمنفذكتابةكلمة(سجلaddressمنفذ, 0)
	Pمنفذكتابةكلمة(سجلبياناتمنفذ, 0x48)

}
func (نفسه *Tamdam79c973) Receive() {
	طرفية_2.Mاطبع(([]byte)(":"))
	طرفية_2.MUnsignedinteger32اطبع(uint32(uintptr(Pointer(&أرسلbuffer))))
	طرفية_2.Mاطبع(([]byte)(":"))
	طرفية_2.MHexadecimalاطبع(أرسلbuffer[0][0])
	طرفية_2.MHexadecimalاطبع(أرسلbuffer[0][1])
	طرفية_2.Mاطبع(([]byte)(":"))
	الحاليrecvbuffer = 0

	for ; (recvbufferالوصف[الحاليrecvbuffer].خيارات & 0x80000000) == 0; الحاليrecvbuffer = (الحاليrecvbuffer + 1) % 8 {

		if !(recvbufferالوصف[الحاليrecvbuffer].خيارات&0x40000000 != 0) && ((recvbufferالوصف[الحاليrecvbuffer].خيارات & 0x03000000) == 0x03000000) {
			var الحجم uint32 = recvbufferالوصف[الحاليrecvbuffer].خيارات & 0xFFF
			if الحجم > 64 {
				الحجم -= 4
			}

			طرفية_2.Mاطبع([]byte(" size : ["))
			طرفية_2.MUnsignedinteger32اطبع(الحجم)
			طرفية_2.Mاطبع([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferالوصف[الحاليrecvbuffer].address_2)))
			var مرجع_عنوان uintptr = uintptr(Pointer(&buffer_2))
			if irawبياناتhandler != nil {
				if irawبياناتhandler.Oعندrawبياناتreceive(مرجع_عنوان, int(الحجم)) {

					طرفية_2.Mاطبعxy(([]byte)("self.Send"), 0, 22)

					نفسه.Sأرسل(مرجع_عنوان, الحجم)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				طرفية_2.MHexadecimalاطبع(buffer_2[i])
				طرفية_2.Mاطبع([]byte(":"))
			}

		}
		recvbufferالوصف[الحاليrecvbuffer].خيارات2 = 0
		recvbufferالوصف[الحاليrecvbuffer].خيارات = 0x8000F7FF
	}
}
func (نفسه *Tamdam79c973) Sتحديدhandler(handler *TRawبياناتhandler) {
	نفسه.handler = handler
}
func (نفسه *Tamdam79c973) Getmacaddress() uint64 {

	return initحظر.ماديaddress
}
func (نفسه *Tamdam79c973) Sتحديدipaddress(ip uint64) {
	initحظر.logicaladdress = ip
}
func (نفسه *Tamdam79c973) Getipaddress() uint64 {
	return initحظر.logicaladdress
}
