/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "прекъсване"
import . "console"
import . "порт"
import . "pci"

var мрежаКартиconsole TConsole = TConsole{}

type TInitializationБлок struct {
	рЕЖИМ			uint16
	числоИзпращанеbuffer	uint8
	числоrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferОписаниеaddress	uintptr
	изпращанеbufferОписаниеaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	флагове		uint32
	флагове2	uint32
	налично		uint32
}

type IRawdatahandler interface {
	Вклrawdatareceive(dataПоказалци uintptr, размер int) bool
	Изпращане(dataПоказалци uintptr, размер uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (себеси *TRawdatahandler) Задайbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (себеси *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (себеси *TRawdatahandler) Вклrawdatareceive(dataПоказалци uintptr, размер int) bool {
	мрежаКартиconsole.MПечатxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (себеси *TRawdatahandler) Изпращане(dataПоказалци uintptr, размер uint32) {
	мрежаКартиconsole.MПечатxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Изпращане(dataПоказалци, размер)
}

var Macaddress0Порт uint16
var Macaddress2Порт uint16
var Macaddress4Порт uint16
var registerdataПорт uint16
var registeraddressПорт uint16
var възстановяванеПорт uint16
var busCtrlregisterdataПорт uint16

var initБлок TInitializationБлок

var изпращанеbufferОписание [8]TBufferdescriptor
var изпращанеbufferОписаниеПамет [2048 + 15]byte
var изпращанеbuffer [2*1024 + 15][8]uint8
var текущадатаИзпращанеbuffer uint8

var recvbufferОписание [8]TBufferdescriptor
var recvbufferОписаниеПамет [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var текущадатаrecvbuffer uint8
var funcСтойност func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TПрекъсванеhandler
	устройствоdescriptor	TPeripheralcomponentinterconnectУстройствоdescriptor
	прекъсване		*TПрекъсванеmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (себеси *Tamdam79c973) Initdriver(прекъсване *TПрекъсванеmanager, устройствоdescriptor TPeripheralcomponentinterconnectУстройствоdescriptor, handler IRawdatahandler) {

	себеси.устройствоdescriptor = устройствоdescriptor

	funcСтойност = (*Tamdam79c973).РъкохваткаПрекъсване
	var address uintptr
	address = uintptr(Pointer(&funcСтойност))

	себеси.Init(uint8(0x20+устройствоdescriptor.Прекъсване), uintptr(Pointer(прекъсване)), address)

	Macaddress0Порт = uint16(устройствоdescriptor.Портbase)
	Macaddress2Порт = uint16(устройствоdescriptor.Портbase) + 0x02
	Macaddress4Порт = uint16(устройствоdescriptor.Портbase) + 0x04
	registerdataПорт = uint16(устройствоdescriptor.Портbase) + 0x10
	registeraddressПорт = uint16(устройствоdescriptor.Портbase) + 0x12
	възстановяванеПорт = uint16(устройствоdescriptor.Портbase) + 0x14
	busCtrlregisterdataПорт = uint16(устройствоdescriptor.Портbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	текущадатаИзпращанеbuffer = 0
	текущадатаrecvbuffer = 0

	var Mac0 uint64 = uint64(ПортЧетенедума(Macaddress0Порт) % 256)
	var Mac1 uint64 = uint64(ПортЧетенедума(Macaddress0Порт) / 256)
	var Mac2 uint64 = uint64(ПортЧетенедума(Macaddress2Порт) % 256)
	var Mac3 uint64 = uint64(ПортЧетенедума(Macaddress2Порт) / 256)
	var Mac4 uint64 = uint64(ПортЧетенедума(Macaddress4Порт) % 256)
	var Mac5 uint64 = uint64(ПортЧетенедума(Macaddress4Порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MПечатxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalПечат(uint8(устройствоdescriptor.Прекъсване))
	console_2.MПечат(([]byte)("]"))
	console_2.MПечат(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Печат(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Печат(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MПечат(([]byte)("]"))

	ПортПисанедума(registeraddressПорт, 20)
	ПортПисанедума(busCtrlregisterdataПорт, 0x102)

	ПортПисанедума(registeraddressПорт, 0)
	ПортПисанедума(registerdataПорт, 0x04)

	initБлок.рЕЖИМ = 0x0000
	initБлок.числоИзпращанеbuffer = 3
	initБлок.числоrecvbuffer = 3

	initБлок.physicaladdress = Mac

	initБлок.logicaladdress = 0

	изпращанеbufferОписание = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&изпращанеbufferОписаниеПамет)) + 15) & ^(uintptr)(0xF)))
	initБлок.изпращанеbufferОписаниеaddress = uintptr(Pointer(&изпращанеbufferОписание))
	recvbufferОписание = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferОписаниеПамет)) + 15) & ^(uintptr)(0xF)))
	initБлок.recvbufferОписаниеaddress = uintptr(Pointer(&recvbufferОписание))

	for i := 0; i < 8; i++ {
		изпращанеbufferОписание[i].address_2 = uint32((uintptr(Pointer(&изпращанеbuffer[i])) + 15) & ^(uintptr(0xF)))
		изпращанеbufferОписание[i].флагове = 0x7FF | 0xF000
		изпращанеbufferОписание[i].флагове2 = 0
		изпращанеbufferОписание[i].налично = 0

		recvbufferОписание[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferОписание[i].флагове = 0xF7FF | 0x80000000

	}

	ПортПисанедума(registeraddressПорт, 1)
	ПортПисанедума(registerdataПорт, uint16(uintptr(Pointer(&initБлок))&0xFFFF))

	ПортПисанедума(registeraddressПорт, 2)
	ПортПисанедума(registerdataПорт, uint16((uintptr(Pointer(&initБлок))>>16)&0xFFFF))

}
func (себеси *Tamdam79c973) Активиране() {
	ПортПисанедума(registeraddressПорт, 0)
	ПортПисанедума(registerdataПорт, 0x41)

	ПортПисанедума(registeraddressПорт, 4)
	temporary := ПортЧетенедума(registerdataПорт)
	ПортПисанедума(registeraddressПорт, 4)
	ПортПисанедума(registerdataПорт, temporary|0xC00)

	ПортПисанедума(registeraddressПорт, 0)
	ПортПисанедума(registerdataПорт, 0x42)

}
func (себеси *Tamdam79c973) Възстановяване() int {
	ПортЧетенедума(възстановяванеПорт)
	ПортПисанедума(възстановяванеПорт, 0)
	return 10
}

var count uint16 = 0

func (себеси *Tamdam79c973) РъкохваткаПрекъсване(esp uint32) uint32 {

	ПортПисанедума(registeraddressПорт, 0)
	temporary := uint32(ПортЧетенедума(registerdataПорт))
	console_2.MПечат(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Печат(esp)
	console_2.MПечат(([]byte)(":"))
	console_2.MUnsignedinteger32Печат(temporary)
	console_2.MПечат(([]byte)(":"))
	console_2.MUnsignedinteger16Печат(count)
	count++
	console_2.MПечат(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MПечат(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MПечат(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MПечат(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MПечат(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MПечат(([]byte)("am79c973 data received"))
		себеси.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MПечат(([]byte)("am79c973 data sent"))
	}

	ПортПисанедума(registeraddressПорт, 0)
	ПортПисанедума(registerdataПорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MПечат(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (себеси *Tamdam79c973) Изпращане(dataПоказалци uintptr, размер uint32) {
	var изпращанеdescriptor uint16 = uint16(текущадатаИзпращанеbuffer)
	текущадатаИзпращанеbuffer = 0

	if размер > 1518 {
		размер = 1518
	}

	var източник_2 [4096]byte = *(*([4096]byte))(Pointer(dataПоказалци))
	var назначение_2 uint32 = изпращанеbufferОписание[изпращанеdescriptor].address_2 + размер - 1

	for i := 0; i < int(размер); i++ {

		*(*byte)(Pointer(uintptr(назначение_2))) = източник_2[int(размер)-i-1]

		назначение_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataПоказалци))
	console_2.MПечатxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalПечат(data[i])
		console_2.MПечат(([]byte)(":"))
	}
	console_2.MПечат(([]byte)("\n"))

	изпращанеbufferОписание[изпращанеdescriptor].налично = 0
	изпращанеbufferОписание[изпращанеdescriptor].флагове2 = 0
	изпращанеbufferОписание[изпращанеdescriptor].флагове = 0x8300F000 | uint32((-размер)&0xFFF)

	ПортПисанедума(registeraddressПорт, 0)
	ПортПисанедума(registerdataПорт, 0x48)

}
func (себеси *Tamdam79c973) Receive() {
	console_2.MПечат(([]byte)(":"))
	console_2.MUnsignedinteger32Печат(uint32(uintptr(Pointer(&изпращанеbuffer))))
	console_2.MПечат(([]byte)(":"))
	console_2.MHexadecimalПечат(изпращанеbuffer[0][0])
	console_2.MHexadecimalПечат(изпращанеbuffer[0][1])
	console_2.MПечат(([]byte)(":"))
	текущадатаrecvbuffer = 0

	for ; (recvbufferОписание[текущадатаrecvbuffer].флагове & 0x80000000) == 0; текущадатаrecvbuffer = (текущадатаrecvbuffer + 1) % 8 {

		if !(recvbufferОписание[текущадатаrecvbuffer].флагове&0x40000000 != 0) && ((recvbufferОписание[текущадатаrecvbuffer].флагове & 0x03000000) == 0x03000000) {
			var размер uint32 = recvbufferОписание[текущадатаrecvbuffer].флагове & 0xFFF
			if размер > 64 {
				размер -= 4
			}

			console_2.MПечат([]byte(" size : ["))
			console_2.MUnsignedinteger32Печат(размер)
			console_2.MПечат([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferОписание[текущадатаrecvbuffer].address_2)))
			var показалци uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Вклrawdatareceive(показалци, int(размер)) {

					console_2.MПечатxy(([]byte)("self.Send"), 0, 22)

					себеси.Изпращане(показалци, размер)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalПечат(buffer_2[i])
				console_2.MПечат([]byte(":"))
			}

		}
		recvbufferОписание[текущадатаrecvbuffer].флагове2 = 0
		recvbufferОписание[текущадатаrecvbuffer].флагове = 0x8000F7FF
	}
}
func (себеси *Tamdam79c973) Задайhandler(handler *TRawdatahandler) {
	себеси.handler = handler
}
func (себеси *Tamdam79c973) Getmacaddress() uint64 {

	return initБлок.physicaladdress
}
func (себеси *Tamdam79c973) Задайipaddress(ip uint64) {
	initБлок.logicaladdress = ip
}
func (себеси *Tamdam79c973) Getipaddress() uint64 {
	return initБлок.logicaladdress
}
