/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "ометање"
import . "конзола"
import . "порт"
import . "pci"

var мрежаcardКонзола TКонзола = TКонзола{}

type TInitializationБлок struct {
	рЕЖИМ			uint16
	бројПошаљиbuffer	uint8
	бројrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferОписaddress	uintptr
	пошаљиbufferОписaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	параметри	uint32
	параметри2	uint32
	расположиво	uint32
}

type IRawdatahandler interface {
	Наrawdatareceive(dataПоказивач uintptr, величина int) bool
	Пошаљи(dataПоказивач uintptr, величина uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (исти *TRawdatahandler) Скупbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (исти *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (исти *TRawdatahandler) Наrawdatareceive(dataПоказивач uintptr, величина int) bool {
	мрежаcardКонзола.MШтампајxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (исти *TRawdatahandler) Пошаљи(dataПоказивач uintptr, величина uint32) {
	мрежаcardКонзола.MШтампајxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Пошаљи(dataПоказивач, величина)
}

var Macaddress0Порт uint16
var Macaddress2Порт uint16
var Macaddress4Порт uint16
var registerdataПорт uint16
var registeraddressПорт uint16
var поновопоставиПорт uint16
var busКонтролregisterdataПорт uint16

var initБлок TInitializationБлок

var пошаљиbufferОпис [8]TBufferdescriptor
var пошаљиbufferОписМеморија [2048 + 15]byte
var пошаљиbuffer [2*1024 + 15][8]uint8
var тренутноПошаљиbuffer uint8

var recvbufferОпис [8]TBufferdescriptor
var recvbufferОписМеморија [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var тренутноrecvbuffer uint8
var funcВредност func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TОметањеhandler
	уређајdescriptor	TPeripheralcomponentinterconnectУређајdescriptor
	ометање			*TОметањеmanager
	handler			*TRawdatahandler
}

var конзола_2 TКонзола = TКонзола{}
var irawdatahandler IRawdatahandler

func (исти *Tamdam79c973) Initdriver(ометање *TОметањеmanager, уређајdescriptor TPeripheralcomponentinterconnectУређајdescriptor, handler IRawdatahandler) {

	исти.уређајdescriptor = уређајdescriptor

	funcВредност = (*Tamdam79c973).РучкаОметање
	var address uintptr
	address = uintptr(Pointer(&funcВредност))

	исти.Init(uint8(0x20+уређајdescriptor.Ометање), uintptr(Pointer(ометање)), address)

	Macaddress0Порт = uint16(уређајdescriptor.Портbase)
	Macaddress2Порт = uint16(уређајdescriptor.Портbase) + 0x02
	Macaddress4Порт = uint16(уређајdescriptor.Портbase) + 0x04
	registerdataПорт = uint16(уређајdescriptor.Портbase) + 0x10
	registeraddressПорт = uint16(уређајdescriptor.Портbase) + 0x12
	поновопоставиПорт = uint16(уређајdescriptor.Портbase) + 0x14
	busКонтролregisterdataПорт = uint16(уређајdescriptor.Портbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	тренутноПошаљиbuffer = 0
	тренутноrecvbuffer = 0

	var Mac0 uint64 = uint64(Портчитањереч(Macaddress0Порт) % 256)
	var Mac1 uint64 = uint64(Портчитањереч(Macaddress0Порт) / 256)
	var Mac2 uint64 = uint64(Портчитањереч(Macaddress2Порт) % 256)
	var Mac3 uint64 = uint64(Портчитањереч(Macaddress2Порт) / 256)
	var Mac4 uint64 = uint64(Портчитањереч(Macaddress4Порт) % 256)
	var Mac5 uint64 = uint64(Портчитањереч(Macaddress4Порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	конзола_2.MШтампајxy(([]byte)("[interrupt num : "), 0, 13)
	конзола_2.MHexadecimalШтампај(uint8(уређајdescriptor.Ометање))
	конзола_2.MШтампај(([]byte)("]"))
	конзола_2.MШтампај(([]byte)("[mac address : "))
	конзола_2.MUnsignedinteger16Штампај(uint16(macaddress >> 32))
	конзола_2.MUnsignedinteger32Штампај(uint32(macaddress & 0x00000000FFFFFFFF))
	конзола_2.MШтампај(([]byte)("]"))

	ПортПишереч(registeraddressПорт, 20)
	ПортПишереч(busКонтролregisterdataПорт, 0x102)

	ПортПишереч(registeraddressПорт, 0)
	ПортПишереч(registerdataПорт, 0x04)

	initБлок.рЕЖИМ = 0x0000
	initБлок.бројПошаљиbuffer = 3
	initБлок.бројrecvbuffer = 3

	initБлок.physicaladdress = Mac

	initБлок.logicaladdress = 0

	пошаљиbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&пошаљиbufferОписМеморија)) + 15) & ^(uintptr)(0xF)))
	initБлок.пошаљиbufferОписaddress = uintptr(Pointer(&пошаљиbufferОпис))
	recvbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferОписМеморија)) + 15) & ^(uintptr)(0xF)))
	initБлок.recvbufferОписaddress = uintptr(Pointer(&recvbufferОпис))

	for i := 0; i < 8; i++ {
		пошаљиbufferОпис[i].address_2 = uint32((uintptr(Pointer(&пошаљиbuffer[i])) + 15) & ^(uintptr(0xF)))
		пошаљиbufferОпис[i].параметри = 0x7FF | 0xF000
		пошаљиbufferОпис[i].параметри2 = 0
		пошаљиbufferОпис[i].расположиво = 0

		recvbufferОпис[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferОпис[i].параметри = 0xF7FF | 0x80000000

	}

	ПортПишереч(registeraddressПорт, 1)
	ПортПишереч(registerdataПорт, uint16(uintptr(Pointer(&initБлок))&0xFFFF))

	ПортПишереч(registeraddressПорт, 2)
	ПортПишереч(registerdataПорт, uint16((uintptr(Pointer(&initБлок))>>16)&0xFFFF))

}
func (исти *Tamdam79c973) Покрени() {
	ПортПишереч(registeraddressПорт, 0)
	ПортПишереч(registerdataПорт, 0x41)

	ПортПишереч(registeraddressПорт, 4)
	temporary := Портчитањереч(registerdataПорт)
	ПортПишереч(registeraddressПорт, 4)
	ПортПишереч(registerdataПорт, temporary|0xC00)

	ПортПишереч(registeraddressПорт, 0)
	ПортПишереч(registerdataПорт, 0x42)

}
func (исти *Tamdam79c973) Поновопостави() int {
	Портчитањереч(поновопоставиПорт)
	ПортПишереч(поновопоставиПорт, 0)
	return 10
}

var count uint16 = 0

func (исти *Tamdam79c973) РучкаОметање(esp uint32) uint32 {

	ПортПишереч(registeraddressПорт, 0)
	temporary := uint32(Портчитањереч(registerdataПорт))
	конзола_2.MШтампај(([]byte)("interrupt("))
	конзола_2.MUnsignedinteger32Штампај(esp)
	конзола_2.MШтампај(([]byte)(":"))
	конзола_2.MUnsignedinteger32Штампај(temporary)
	конзола_2.MШтампај(([]byte)(":"))
	конзола_2.MUnsignedinteger16Штампај(count)
	count++
	конзола_2.MШтампај(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		конзола_2.MШтампај(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		конзола_2.MШтампај(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		конзола_2.MШтампај(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		конзола_2.MШтампај(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		конзола_2.MШтампај(([]byte)("am79c973 data received"))
		исти.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		конзола_2.MШтампај(([]byte)("am79c973 data sent"))
	}

	ПортПишереч(registeraddressПорт, 0)
	ПортПишереч(registerdataПорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		конзола_2.MШтампај(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (исти *Tamdam79c973) Пошаљи(dataПоказивач uintptr, величина uint32) {
	var пошаљиdescriptor uint16 = uint16(тренутноПошаљиbuffer)
	тренутноПошаљиbuffer = 0

	if величина > 1518 {
		величина = 1518
	}

	var извор_2 [4096]byte = *(*([4096]byte))(Pointer(dataПоказивач))
	var одредиште_2 uint32 = пошаљиbufferОпис[пошаљиdescriptor].address_2 + величина - 1

	for i := 0; i < int(величина); i++ {

		*(*byte)(Pointer(uintptr(одредиште_2))) = извор_2[int(величина)-i-1]

		одредиште_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataПоказивач))
	конзола_2.MШтампајxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		конзола_2.MHexadecimalШтампај(data[i])
		конзола_2.MШтампај(([]byte)(":"))
	}
	конзола_2.MШтампај(([]byte)("\n"))

	пошаљиbufferОпис[пошаљиdescriptor].расположиво = 0
	пошаљиbufferОпис[пошаљиdescriptor].параметри2 = 0
	пошаљиbufferОпис[пошаљиdescriptor].параметри = 0x8300F000 | uint32((-величина)&0xFFF)

	ПортПишереч(registeraddressПорт, 0)
	ПортПишереч(registerdataПорт, 0x48)

}
func (исти *Tamdam79c973) Receive() {
	конзола_2.MШтампај(([]byte)(":"))
	конзола_2.MUnsignedinteger32Штампај(uint32(uintptr(Pointer(&пошаљиbuffer))))
	конзола_2.MШтампај(([]byte)(":"))
	конзола_2.MHexadecimalШтампај(пошаљиbuffer[0][0])
	конзола_2.MHexadecimalШтампај(пошаљиbuffer[0][1])
	конзола_2.MШтампај(([]byte)(":"))
	тренутноrecvbuffer = 0

	for ; (recvbufferОпис[тренутноrecvbuffer].параметри & 0x80000000) == 0; тренутноrecvbuffer = (тренутноrecvbuffer + 1) % 8 {

		if !(recvbufferОпис[тренутноrecvbuffer].параметри&0x40000000 != 0) && ((recvbufferОпис[тренутноrecvbuffer].параметри & 0x03000000) == 0x03000000) {
			var величина uint32 = recvbufferОпис[тренутноrecvbuffer].параметри & 0xFFF
			if величина > 64 {
				величина -= 4
			}

			конзола_2.MШтампај([]byte(" size : ["))
			конзола_2.MUnsignedinteger32Штампај(величина)
			конзола_2.MШтампај([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferОпис[тренутноrecvbuffer].address_2)))
			var показивач uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Наrawdatareceive(показивач, int(величина)) {

					конзола_2.MШтампајxy(([]byte)("self.Send"), 0, 22)

					исти.Пошаљи(показивач, величина)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				конзола_2.MHexadecimalШтампај(buffer_2[i])
				конзола_2.MШтампај([]byte(":"))
			}

		}
		recvbufferОпис[тренутноrecvbuffer].параметри2 = 0
		recvbufferОпис[тренутноrecvbuffer].параметри = 0x8000F7FF
	}
}
func (исти *Tamdam79c973) Скупhandler(handler *TRawdatahandler) {
	исти.handler = handler
}
func (исти *Tamdam79c973) Getmacaddress() uint64 {

	return initБлок.physicaladdress
}
func (исти *Tamdam79c973) Скупipaddress(ip uint64) {
	initБлок.logicaladdress = ip
}
func (исти *Tamdam79c973) Getipaddress() uint64 {
	return initБлок.logicaladdress
}
