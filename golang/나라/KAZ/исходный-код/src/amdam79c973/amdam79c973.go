/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "прерывание"
import . "консоль"
import . "порт"
import . "pci"

var сетьКарточныеконсоль TКонсоль = TКонсоль{}

type TInitializationБлок struct {
	режим			uint16
	числоОтправитьbuffer	uint8
	числоrecvbuffer		uint8

	физическийaddress	uint64

	логическиеоперацииaddress	uint64
	recvbufferОписаниеaddress	uintptr
	отправитьbufferОписаниеaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	флаги		uint32
	флаги2		uint32
	доступно	uint32
}

type IRawданныеhandler interface {
	Приrawданныеreceive(данныеУказатели uintptr, размер int) bool
	Отправить(данныеУказатели uintptr, размер uint32)
}

var rawданныеbackend Tamdam79c973

type TRawданныеhandler struct {
}

func (текущий *TRawданныеhandler) Указатьbackend(backend Tamdam79c973) {

	rawданныеbackend = backend
}
func (текущий *TRawданныеhandler) Getbackend() Tamdam79c973 {
	return rawданныеbackend
}
func (текущий *TRawданныеhandler) Приrawданныеreceive(данныеУказатели uintptr, размер int) bool {
	сетьКарточныеконсоль.MПечатьxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (текущий *TRawданныеhandler) Отправить(данныеУказатели uintptr, размер uint32) {
	сетьКарточныеконсоль.MПечатьxy(([]byte)("TRawDataSend"), 10, 10)
	rawданныеbackend.Отправить(данныеУказатели, размер)
}

var Macaddress0порт uint16
var Macaddress2порт uint16
var Macaddress4порт uint16
var регистрданныепорт uint16
var регистрaddressпорт uint16
var сброспорт uint16
var busCtrlрегистрданныепорт uint16

var initБлок TInitializationБлок

var отправитьbufferОписание [8]TBufferdescriptor
var отправитьbufferОписаниепамять [2048 + 15]byte
var отправитьbuffer [2*1024 + 15][8]uint8
var текущаядатаОтправитьbuffer uint8

var recvbufferОписание [8]TBufferdescriptor
var recvbufferОписаниепамять [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var текущаядатаrecvbuffer uint8
var funcЗначение func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TПрерываниеhandler
	устройствоdescriptor	TPeripheralcomponentinterconnectУстройствоdescriptor
	прерывание		*TПрерываниедиспетчер
	handler			*TRawданныеhandler
}

var консоль_2 TКонсоль = TКонсоль{}
var irawданныеhandler IRawданныеhandler

func (текущий *Tamdam79c973) Initдрайвер(прерывание *TПрерываниедиспетчер, устройствоdescriptor TPeripheralcomponentinterconnectУстройствоdescriptor, handler IRawданныеhandler) {

	текущий.устройствоdescriptor = устройствоdescriptor

	funcЗначение = (*Tamdam79c973).Ручкапрерывание
	var address uintptr
	address = uintptr(Pointer(&funcЗначение))

	текущий.Init(uint8(0x20+устройствоdescriptor.Прерывание), uintptr(Pointer(прерывание)), address)

	Macaddress0порт = uint16(устройствоdescriptor.Портbase)
	Macaddress2порт = uint16(устройствоdescriptor.Портbase) + 0x02
	Macaddress4порт = uint16(устройствоdescriptor.Портbase) + 0x04
	регистрданныепорт = uint16(устройствоdescriptor.Портbase) + 0x10
	регистрaddressпорт = uint16(устройствоdescriptor.Портbase) + 0x12
	сброспорт = uint16(устройствоdescriptor.Портbase) + 0x14
	busCtrlрегистрданныепорт = uint16(устройствоdescriptor.Портbase) + 0x16

	irawданныеhandler = &TRawданныеhandler{}
	if handler != nil {
		irawданныеhandler = handler
	}

	текущаядатаОтправитьbuffer = 0
	текущаядатаrecvbuffer = 0

	var Mac0 uint64 = uint64(Портчитатьслово(Macaddress0порт) % 256)
	var Mac1 uint64 = uint64(Портчитатьслово(Macaddress0порт) / 256)
	var Mac2 uint64 = uint64(Портчитатьслово(Macaddress2порт) % 256)
	var Mac3 uint64 = uint64(Портчитатьслово(Macaddress2порт) / 256)
	var Mac4 uint64 = uint64(Портчитатьслово(Macaddress4порт) % 256)
	var Mac5 uint64 = uint64(Портчитатьслово(Macaddress4порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	консоль_2.MПечатьxy(([]byte)("[interrupt num : "), 0, 13)
	консоль_2.MHexadecimalПечать(uint8(устройствоdescriptor.Прерывание))
	консоль_2.MПечать(([]byte)("]"))
	консоль_2.MПечать(([]byte)("[mac address : "))
	консоль_2.MUnsignedinteger16Печать(uint16(macaddress >> 32))
	консоль_2.MUnsignedinteger32Печать(uint32(macaddress & 0x00000000FFFFFFFF))
	консоль_2.MПечать(([]byte)("]"))

	Портписатьслово(регистрaddressпорт, 20)
	Портписатьслово(busCtrlрегистрданныепорт, 0x102)

	Портписатьслово(регистрaddressпорт, 0)
	Портписатьслово(регистрданныепорт, 0x04)

	initБлок.режим = 0x0000
	initБлок.числоОтправитьbuffer = 3
	initБлок.числоrecvbuffer = 3

	initБлок.физическийaddress = Mac

	initБлок.логическиеоперацииaddress = 0

	отправитьbufferОписание = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&отправитьbufferОписаниепамять)) + 15) & ^(uintptr)(0xF)))
	initБлок.отправитьbufferОписаниеaddress = uintptr(Pointer(&отправитьbufferОписание))
	recvbufferОписание = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferОписаниепамять)) + 15) & ^(uintptr)(0xF)))
	initБлок.recvbufferОписаниеaddress = uintptr(Pointer(&recvbufferОписание))

	for i := 0; i < 8; i++ {
		отправитьbufferОписание[i].address_2 = uint32((uintptr(Pointer(&отправитьbuffer[i])) + 15) & ^(uintptr(0xF)))
		отправитьbufferОписание[i].флаги = 0x7FF | 0xF000
		отправитьbufferОписание[i].флаги2 = 0
		отправитьbufferОписание[i].доступно = 0

		recvbufferОписание[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferОписание[i].флаги = 0xF7FF | 0x80000000

	}

	Портписатьслово(регистрaddressпорт, 1)
	Портписатьслово(регистрданныепорт, uint16(uintptr(Pointer(&initБлок))&0xFFFF))

	Портписатьслово(регистрaddressпорт, 2)
	Портписатьслово(регистрданныепорт, uint16((uintptr(Pointer(&initБлок))>>16)&0xFFFF))

}
func (текущий *Tamdam79c973) Включить() {
	Портписатьслово(регистрaddressпорт, 0)
	Портписатьслово(регистрданныепорт, 0x41)

	Портписатьслово(регистрaddressпорт, 4)
	temporary := Портчитатьслово(регистрданныепорт)
	Портписатьслово(регистрaddressпорт, 4)
	Портписатьслово(регистрданныепорт, temporary|0xC00)

	Портписатьслово(регистрaddressпорт, 0)
	Портписатьслово(регистрданныепорт, 0x42)

}
func (текущий *Tamdam79c973) Сброс() int {
	Портчитатьслово(сброспорт)
	Портписатьслово(сброспорт, 0)
	return 10
}

var количество uint16 = 0

func (текущий *Tamdam79c973) Ручкапрерывание(esp uint32) uint32 {

	Портписатьслово(регистрaddressпорт, 0)
	temporary := uint32(Портчитатьслово(регистрданныепорт))
	консоль_2.MПечать(([]byte)("interrupt("))
	консоль_2.MUnsignedinteger32Печать(esp)
	консоль_2.MПечать(([]byte)(":"))
	консоль_2.MUnsignedinteger32Печать(temporary)
	консоль_2.MПечать(([]byte)(":"))
	консоль_2.MUnsignedinteger16Печать(количество)
	количество++
	консоль_2.MПечать(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		консоль_2.MПечать(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		консоль_2.MПечать(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		консоль_2.MПечать(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		консоль_2.MПечать(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		консоль_2.MПечать(([]byte)("am79c973 data received"))
		текущий.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		консоль_2.MПечать(([]byte)("am79c973 data sent"))
	}

	Портписатьслово(регистрaddressпорт, 0)
	Портписатьслово(регистрданныепорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		консоль_2.MПечать(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (текущий *Tamdam79c973) Отправить(данныеУказатели uintptr, размер uint32) {
	var отправитьdescriptor uint16 = uint16(текущаядатаОтправитьbuffer)
	текущаядатаОтправитьbuffer = 0

	if размер > 1518 {
		размер = 1518
	}

	var источник_2 [4096]byte = *(*([4096]byte))(Pointer(данныеУказатели))
	var назначение_2 uint32 = отправитьbufferОписание[отправитьdescriptor].address_2 + размер - 1

	for i := 0; i < int(размер); i++ {

		*(*byte)(Pointer(uintptr(назначение_2))) = источник_2[int(размер)-i-1]

		назначение_2--
	}

	var данные [4096]byte = *(*([4096]byte))(Pointer(данныеУказатели))
	консоль_2.MПечатьxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		консоль_2.MHexadecimalПечать(данные[i])
		консоль_2.MПечать(([]byte)(":"))
	}
	консоль_2.MПечать(([]byte)("\n"))

	отправитьbufferОписание[отправитьdescriptor].доступно = 0
	отправитьbufferОписание[отправитьdescriptor].флаги2 = 0
	отправитьbufferОписание[отправитьdescriptor].флаги = 0x8300F000 | uint32((-размер)&0xFFF)

	Портписатьслово(регистрaddressпорт, 0)
	Портписатьслово(регистрданныепорт, 0x48)

}
func (текущий *Tamdam79c973) Receive() {
	консоль_2.MПечать(([]byte)(":"))
	консоль_2.MUnsignedinteger32Печать(uint32(uintptr(Pointer(&отправитьbuffer))))
	консоль_2.MПечать(([]byte)(":"))
	консоль_2.MHexadecimalПечать(отправитьbuffer[0][0])
	консоль_2.MHexadecimalПечать(отправитьbuffer[0][1])
	консоль_2.MПечать(([]byte)(":"))
	текущаядатаrecvbuffer = 0

	for ; (recvbufferОписание[текущаядатаrecvbuffer].флаги & 0x80000000) == 0; текущаядатаrecvbuffer = (текущаядатаrecvbuffer + 1) % 8 {

		if !(recvbufferОписание[текущаядатаrecvbuffer].флаги&0x40000000 != 0) && ((recvbufferОписание[текущаядатаrecvbuffer].флаги & 0x03000000) == 0x03000000) {
			var размер uint32 = recvbufferОписание[текущаядатаrecvbuffer].флаги & 0xFFF
			if размер > 64 {
				размер -= 4
			}

			консоль_2.MПечать([]byte(" size : ["))
			консоль_2.MUnsignedinteger32Печать(размер)
			консоль_2.MПечать([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferОписание[текущаядатаrecvbuffer].address_2)))
			var ссылка_на_адрес uintptr = uintptr(Pointer(&buffer_2))
			if irawданныеhandler != nil {
				if irawданныеhandler.Приrawданныеreceive(ссылка_на_адрес, int(размер)) {

					консоль_2.MПечатьxy(([]byte)("self.Send"), 0, 22)

					текущий.Отправить(ссылка_на_адрес, размер)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				консоль_2.MHexadecimalПечать(buffer_2[i])
				консоль_2.MПечать([]byte(":"))
			}

		}
		recvbufferОписание[текущаядатаrecvbuffer].флаги2 = 0
		recvbufferОписание[текущаядатаrecvbuffer].флаги = 0x8000F7FF
	}
}
func (текущий *Tamdam79c973) Указатьhandler(handler *TRawданныеhandler) {
	текущий.handler = handler
}
func (текущий *Tamdam79c973) Getmacaddress() uint64 {

	return initБлок.физическийaddress
}
func (текущий *Tamdam79c973) Указатьipaddress(ip uint64) {
	initБлок.логическиеоперацииaddress = ip
}
func (текущий *Tamdam79c973) Getipaddress() uint64 {
	return initБлок.логическиеоперацииaddress
}
