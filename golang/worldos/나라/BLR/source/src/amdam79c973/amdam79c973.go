/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "перарыванне"
import . "console"
import . "порт"
import . "pci"

var сеткаКартачныяconsole TConsole = TConsole{}

type TInitializationБлок struct {
	рЭЖЫМ			uint16
	нУМАРДаслацьbuffer	uint8
	нУМАРrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferАпісаннеaddress	uintptr
	даслацьbufferАпісаннеaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	сцяжкі		uint32
	сцяжкі2		uint32
	даступна	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(dataПаказальнік uintptr, памер int) bool
	Даслаць(dataПаказальнік uintptr, памер uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Вызначанаbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Onrawdatareceive(dataПаказальнік uintptr, памер int) bool {
	сеткаКартачныяconsole.MДрукавацьxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Даслаць(dataПаказальнік uintptr, памер uint32) {
	сеткаКартачныяconsole.MДрукавацьxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Даслаць(dataПаказальнік, памер)
}

var Macaddress0Порт uint16
var Macaddress2Порт uint16
var Macaddress4Порт uint16
var registerdataПорт uint16
var registeraddressПорт uint16
var скінуцьПорт uint16
var busCtrlregisterdataПорт uint16

var initБлок TInitializationБлок

var даслацьbufferАпісанне [8]TBufferdescriptor
var даслацьbufferАпісаннеПамяць [2048 + 15]byte
var даслацьbuffer [2*1024 + 15][8]uint8
var дзейныДаслацьbuffer uint8

var recvbufferАпісанне [8]TBufferdescriptor
var recvbufferАпісаннеПамяць [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var дзейныrecvbuffer uint8
var funcЗначэнне func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TПерарываннеhandler
	прыладаdescriptor	TPeripheralcomponentinterconnectПрыладаdescriptor
	перарыванне		*TПерарываннеmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(перарыванне *TПерарываннеmanager, прыладаdescriptor TPeripheralcomponentinterconnectПрыладаdescriptor, handler IRawdatahandler) {

	self.прыладаdescriptor = прыладаdescriptor

	funcЗначэнне = (*Tamdam79c973).HandleПерарыванне
	var address uintptr
	address = uintptr(Pointer(&funcЗначэнне))

	self.Init(uint8(0x20+прыладаdescriptor.Перарыванне), uintptr(Pointer(перарыванне)), address)

	Macaddress0Порт = uint16(прыладаdescriptor.Портbase)
	Macaddress2Порт = uint16(прыладаdescriptor.Портbase) + 0x02
	Macaddress4Порт = uint16(прыладаdescriptor.Портbase) + 0x04
	registerdataПорт = uint16(прыладаdescriptor.Портbase) + 0x10
	registeraddressПорт = uint16(прыладаdescriptor.Портbase) + 0x12
	скінуцьПорт = uint16(прыладаdescriptor.Портbase) + 0x14
	busCtrlregisterdataПорт = uint16(прыладаdescriptor.Портbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	дзейныДаслацьbuffer = 0
	дзейныrecvbuffer = 0

	var Mac0 uint64 = uint64(ПортЧытаннеслова(Macaddress0Порт) % 256)
	var Mac1 uint64 = uint64(ПортЧытаннеслова(Macaddress0Порт) / 256)
	var Mac2 uint64 = uint64(ПортЧытаннеслова(Macaddress2Порт) % 256)
	var Mac3 uint64 = uint64(ПортЧытаннеслова(Macaddress2Порт) / 256)
	var Mac4 uint64 = uint64(ПортЧытаннеслова(Macaddress4Порт) % 256)
	var Mac5 uint64 = uint64(ПортЧытаннеслова(Macaddress4Порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MДрукавацьxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalДрукаваць(uint8(прыладаdescriptor.Перарыванне))
	console_2.MДрукаваць(([]byte)("]"))
	console_2.MДрукаваць(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Друкаваць(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Друкаваць(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MДрукаваць(([]byte)("]"))

	ПортЗапісслова(registeraddressПорт, 20)
	ПортЗапісслова(busCtrlregisterdataПорт, 0x102)

	ПортЗапісслова(registeraddressПорт, 0)
	ПортЗапісслова(registerdataПорт, 0x04)

	initБлок.рЭЖЫМ = 0x0000
	initБлок.нУМАРДаслацьbuffer = 3
	initБлок.нУМАРrecvbuffer = 3

	initБлок.physicaladdress = Mac

	initБлок.logicaladdress = 0

	даслацьbufferАпісанне = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&даслацьbufferАпісаннеПамяць)) + 15) & ^(uintptr)(0xF)))
	initБлок.даслацьbufferАпісаннеaddress = uintptr(Pointer(&даслацьbufferАпісанне))
	recvbufferАпісанне = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferАпісаннеПамяць)) + 15) & ^(uintptr)(0xF)))
	initБлок.recvbufferАпісаннеaddress = uintptr(Pointer(&recvbufferАпісанне))

	for i := 0; i < 8; i++ {
		даслацьbufferАпісанне[i].address_2 = uint32((uintptr(Pointer(&даслацьbuffer[i])) + 15) & ^(uintptr(0xF)))
		даслацьbufferАпісанне[i].сцяжкі = 0x7FF | 0xF000
		даслацьbufferАпісанне[i].сцяжкі2 = 0
		даслацьbufferАпісанне[i].даступна = 0

		recvbufferАпісанне[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferАпісанне[i].сцяжкі = 0xF7FF | 0x80000000

	}

	ПортЗапісслова(registeraddressПорт, 1)
	ПортЗапісслова(registerdataПорт, uint16(uintptr(Pointer(&initБлок))&0xFFFF))

	ПортЗапісслова(registeraddressПорт, 2)
	ПортЗапісслова(registerdataПорт, uint16((uintptr(Pointer(&initБлок))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Задзейнічаць() {
	ПортЗапісслова(registeraddressПорт, 0)
	ПортЗапісслова(registerdataПорт, 0x41)

	ПортЗапісслова(registeraddressПорт, 4)
	temporary := ПортЧытаннеслова(registerdataПорт)
	ПортЗапісслова(registeraddressПорт, 4)
	ПортЗапісслова(registerdataПорт, temporary|0xC00)

	ПортЗапісслова(registeraddressПорт, 0)
	ПортЗапісслова(registerdataПорт, 0x42)

}
func (self *Tamdam79c973) Скінуць() int {
	ПортЧытаннеслова(скінуцьПорт)
	ПортЗапісслова(скінуцьПорт, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) HandleПерарыванне(esp uint32) uint32 {

	ПортЗапісслова(registeraddressПорт, 0)
	temporary := uint32(ПортЧытаннеслова(registerdataПорт))
	console_2.MДрукаваць(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Друкаваць(esp)
	console_2.MДрукаваць(([]byte)(":"))
	console_2.MUnsignedinteger32Друкаваць(temporary)
	console_2.MДрукаваць(([]byte)(":"))
	console_2.MUnsignedinteger16Друкаваць(count)
	count++
	console_2.MДрукаваць(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MДрукаваць(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MДрукаваць(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MДрукаваць(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MДрукаваць(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MДрукаваць(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MДрукаваць(([]byte)("am79c973 data sent"))
	}

	ПортЗапісслова(registeraddressПорт, 0)
	ПортЗапісслова(registerdataПорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MДрукаваць(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Даслаць(dataПаказальнік uintptr, памер uint32) {
	var даслацьdescriptor uint16 = uint16(дзейныДаслацьbuffer)
	дзейныДаслацьbuffer = 0

	if памер > 1518 {
		памер = 1518
	}

	var крыніца_2 [4096]byte = *(*([4096]byte))(Pointer(dataПаказальнік))
	var destination_2 uint32 = даслацьbufferАпісанне[даслацьdescriptor].address_2 + памер - 1

	for i := 0; i < int(памер); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = крыніца_2[int(памер)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataПаказальнік))
	console_2.MДрукавацьxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalДрукаваць(data[i])
		console_2.MДрукаваць(([]byte)(":"))
	}
	console_2.MДрукаваць(([]byte)("\n"))

	даслацьbufferАпісанне[даслацьdescriptor].даступна = 0
	даслацьbufferАпісанне[даслацьdescriptor].сцяжкі2 = 0
	даслацьbufferАпісанне[даслацьdescriptor].сцяжкі = 0x8300F000 | uint32((-памер)&0xFFF)

	ПортЗапісслова(registeraddressПорт, 0)
	ПортЗапісслова(registerdataПорт, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MДрукаваць(([]byte)(":"))
	console_2.MUnsignedinteger32Друкаваць(uint32(uintptr(Pointer(&даслацьbuffer))))
	console_2.MДрукаваць(([]byte)(":"))
	console_2.MHexadecimalДрукаваць(даслацьbuffer[0][0])
	console_2.MHexadecimalДрукаваць(даслацьbuffer[0][1])
	console_2.MДрукаваць(([]byte)(":"))
	дзейныrecvbuffer = 0

	for ; (recvbufferАпісанне[дзейныrecvbuffer].сцяжкі & 0x80000000) == 0; дзейныrecvbuffer = (дзейныrecvbuffer + 1) % 8 {

		if !(recvbufferАпісанне[дзейныrecvbuffer].сцяжкі&0x40000000 != 0) && ((recvbufferАпісанне[дзейныrecvbuffer].сцяжкі & 0x03000000) == 0x03000000) {
			var памер uint32 = recvbufferАпісанне[дзейныrecvbuffer].сцяжкі & 0xFFF
			if памер > 64 {
				памер -= 4
			}

			console_2.MДрукаваць([]byte(" size : ["))
			console_2.MUnsignedinteger32Друкаваць(памер)
			console_2.MДрукаваць([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferАпісанне[дзейныrecvbuffer].address_2)))
			var паказальнік uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(паказальнік, int(памер)) {

					console_2.MДрукавацьxy(([]byte)("self.Send"), 0, 22)

					self.Даслаць(паказальнік, памер)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalДрукаваць(buffer_2[i])
				console_2.MДрукаваць([]byte(":"))
			}

		}
		recvbufferАпісанне[дзейныrecvbuffer].сцяжкі2 = 0
		recvbufferАпісанне[дзейныrecvbuffer].сцяжкі = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Вызначанаhandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initБлок.physicaladdress
}
func (self *Tamdam79c973) Вызначанаipaddress(ip uint64) {
	initБлок.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initБлок.logicaladdress
}
