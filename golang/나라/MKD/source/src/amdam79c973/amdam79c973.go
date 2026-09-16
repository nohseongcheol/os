/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "порта"
import . "pci"

var мрежаКартиconsole TConsole = TConsole{}

type TInitializationblock struct {
	режим			uint16
	numberИспратиbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferОписaddress		uintptr
	испратиbufferОписaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	атрибути	uint32
	атрибути2	uint32
	достапно	uint32
}

type IRawdatahandler interface {
	Вклученоrawdatareceive(dataСтрелка uintptr, големина int) bool
	Испрати(dataСтрелка uintptr, големина uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (само *TRawdatahandler) Поставиbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (само *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (само *TRawdatahandler) Вклученоrawdatareceive(dataСтрелка uintptr, големина int) bool {
	мрежаКартиconsole.MПечатиxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (само *TRawdatahandler) Испрати(dataСтрелка uintptr, големина uint32) {
	мрежаКартиconsole.MПечатиxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Испрати(dataСтрелка, големина)
}

var Macaddress0Порта uint16
var Macaddress2Порта uint16
var Macaddress4Порта uint16
var registerdataПорта uint16
var registeraddressПорта uint16
var ресетирајПорта uint16
var buscontrolregisterdataПорта uint16

var initblock TInitializationblock

var испратиbufferОпис [8]TBufferdescriptor
var испратиbufferОписМеморија [2048 + 15]byte
var испратиbuffer [2*1024 + 15][8]uint8
var currentИспратиbuffer uint8

var recvbufferОпис [8]TBufferdescriptor
var recvbufferОписМеморија [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcВредност func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	уредdescriptor	TPeripheralcomponentinterconnectУредdescriptor
	interrupt	*TInterruptmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (само *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, уредdescriptor TPeripheralcomponentinterconnectУредdescriptor, handler IRawdatahandler) {

	само.уредdescriptor = уредdescriptor

	funcВредност = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcВредност))

	само.Init(uint8(0x20+уредdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Порта = uint16(уредdescriptor.Портаbase)
	Macaddress2Порта = uint16(уредdescriptor.Портаbase) + 0x02
	Macaddress4Порта = uint16(уредdescriptor.Портаbase) + 0x04
	registerdataПорта = uint16(уредdescriptor.Портаbase) + 0x10
	registeraddressПорта = uint16(уредdescriptor.Портаbase) + 0x12
	ресетирајПорта = uint16(уредdescriptor.Портаbase) + 0x14
	buscontrolregisterdataПорта = uint16(уредdescriptor.Портаbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentИспратиbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(ПортаЧитајзбор(Macaddress0Порта) % 256)
	var Mac1 uint64 = uint64(ПортаЧитајзбор(Macaddress0Порта) / 256)
	var Mac2 uint64 = uint64(ПортаЧитајзбор(Macaddress2Порта) % 256)
	var Mac3 uint64 = uint64(ПортаЧитајзбор(Macaddress2Порта) / 256)
	var Mac4 uint64 = uint64(ПортаЧитајзбор(Macaddress4Порта) % 256)
	var Mac5 uint64 = uint64(ПортаЧитајзбор(Macaddress4Порта) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MПечатиxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalПечати(uint8(уредdescriptor.Interrupt))
	console_2.MПечати(([]byte)("]"))
	console_2.MПечати(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Печати(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Печати(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MПечати(([]byte)("]"))

	ПортаЗапишизбор(registeraddressПорта, 20)
	ПортаЗапишизбор(buscontrolregisterdataПорта, 0x102)

	ПортаЗапишизбор(registeraddressПорта, 0)
	ПортаЗапишизбор(registerdataПорта, 0x04)

	initblock.режим = 0x0000
	initblock.numberИспратиbuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	испратиbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&испратиbufferОписМеморија)) + 15) & ^(uintptr)(0xF)))
	initblock.испратиbufferОписaddress = uintptr(Pointer(&испратиbufferОпис))
	recvbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferОписМеморија)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferОписaddress = uintptr(Pointer(&recvbufferОпис))

	for i := 0; i < 8; i++ {
		испратиbufferОпис[i].address_2 = uint32((uintptr(Pointer(&испратиbuffer[i])) + 15) & ^(uintptr(0xF)))
		испратиbufferОпис[i].атрибути = 0x7FF | 0xF000
		испратиbufferОпис[i].атрибути2 = 0
		испратиbufferОпис[i].достапно = 0

		recvbufferОпис[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferОпис[i].атрибути = 0xF7FF | 0x80000000

	}

	ПортаЗапишизбор(registeraddressПорта, 1)
	ПортаЗапишизбор(registerdataПорта, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	ПортаЗапишизбор(registeraddressПорта, 2)
	ПортаЗапишизбор(registerdataПорта, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (само *Tamdam79c973) Активирај() {
	ПортаЗапишизбор(registeraddressПорта, 0)
	ПортаЗапишизбор(registerdataПорта, 0x41)

	ПортаЗапишизбор(registeraddressПорта, 4)
	temporary := ПортаЧитајзбор(registerdataПорта)
	ПортаЗапишизбор(registeraddressПорта, 4)
	ПортаЗапишизбор(registerdataПорта, temporary|0xC00)

	ПортаЗапишизбор(registeraddressПорта, 0)
	ПортаЗапишизбор(registerdataПорта, 0x42)

}
func (само *Tamdam79c973) Ресетирај() int {
	ПортаЧитајзбор(ресетирајПорта)
	ПортаЗапишизбор(ресетирајПорта, 0)
	return 10
}

var count uint16 = 0

func (само *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	ПортаЗапишизбор(registeraddressПорта, 0)
	temporary := uint32(ПортаЧитајзбор(registerdataПорта))
	console_2.MПечати(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Печати(esp)
	console_2.MПечати(([]byte)(":"))
	console_2.MUnsignedinteger32Печати(temporary)
	console_2.MПечати(([]byte)(":"))
	console_2.MUnsignedinteger16Печати(count)
	count++
	console_2.MПечати(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MПечати(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MПечати(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MПечати(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MПечати(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MПечати(([]byte)("am79c973 data received"))
		само.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MПечати(([]byte)("am79c973 data sent"))
	}

	ПортаЗапишизбор(registeraddressПорта, 0)
	ПортаЗапишизбор(registerdataПорта, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MПечати(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (само *Tamdam79c973) Испрати(dataСтрелка uintptr, големина uint32) {
	var испратиdescriptor uint16 = uint16(currentИспратиbuffer)
	currentИспратиbuffer = 0

	if големина > 1518 {
		големина = 1518
	}

	var извор_2 [4096]byte = *(*([4096]byte))(Pointer(dataСтрелка))
	var одредиште_2 uint32 = испратиbufferОпис[испратиdescriptor].address_2 + големина - 1

	for i := 0; i < int(големина); i++ {

		*(*byte)(Pointer(uintptr(одредиште_2))) = извор_2[int(големина)-i-1]

		одредиште_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataСтрелка))
	console_2.MПечатиxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalПечати(data[i])
		console_2.MПечати(([]byte)(":"))
	}
	console_2.MПечати(([]byte)("\n"))

	испратиbufferОпис[испратиdescriptor].достапно = 0
	испратиbufferОпис[испратиdescriptor].атрибути2 = 0
	испратиbufferОпис[испратиdescriptor].атрибути = 0x8300F000 | uint32((-големина)&0xFFF)

	ПортаЗапишизбор(registeraddressПорта, 0)
	ПортаЗапишизбор(registerdataПорта, 0x48)

}
func (само *Tamdam79c973) Receive() {
	console_2.MПечати(([]byte)(":"))
	console_2.MUnsignedinteger32Печати(uint32(uintptr(Pointer(&испратиbuffer))))
	console_2.MПечати(([]byte)(":"))
	console_2.MHexadecimalПечати(испратиbuffer[0][0])
	console_2.MHexadecimalПечати(испратиbuffer[0][1])
	console_2.MПечати(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferОпис[currentrecvbuffer].атрибути & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferОпис[currentrecvbuffer].атрибути&0x40000000 != 0) && ((recvbufferОпис[currentrecvbuffer].атрибути & 0x03000000) == 0x03000000) {
			var големина uint32 = recvbufferОпис[currentrecvbuffer].атрибути & 0xFFF
			if големина > 64 {
				големина -= 4
			}

			console_2.MПечати([]byte(" size : ["))
			console_2.MUnsignedinteger32Печати(големина)
			console_2.MПечати([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferОпис[currentrecvbuffer].address_2)))
			var стрелка uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Вклученоrawdatareceive(стрелка, int(големина)) {

					console_2.MПечатиxy(([]byte)("self.Send"), 0, 22)

					само.Испрати(стрелка, големина)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalПечати(buffer_2[i])
				console_2.MПечати([]byte(":"))
			}

		}
		recvbufferОпис[currentrecvbuffer].атрибути2 = 0
		recvbufferОпис[currentrecvbuffer].атрибути = 0x8000F7FF
	}
}
func (само *Tamdam79c973) Поставиhandler(handler *TRawdatahandler) {
	само.handler = handler
}
func (само *Tamdam79c973) Getmacaddress() uint64 {

	return initblock.physicaladdress
}
func (само *Tamdam79c973) Поставиipaddress(ip uint64) {
	initblock.logicaladdress = ip
}
func (само *Tamdam79c973) Getipaddress() uint64 {
	return initblock.logicaladdress
}
