package amdam79c973

import . "unsafe"
import . "переривання"
import . "консоль"
import . "порт"
import . "pci"

var мережаКартковіКонсоль TКонсоль = TКонсоль{}

type TInitializationБлок struct {
	рЕЖИМ			uint16
	числоНадіслатиbuffer	uint8
	числоrecvbuffer		uint8

	physicalАдреса	uint64

	логічніопераціїАдреса		uint64
	recvbufferОписАдреса		uintptr
	надіслатиbufferОписАдреса	uintptr
}
type TBufferdescriptor struct {
	адреса_2	uint32
	прапори		uint32
	прапори2	uint32
	доступно	uint32
}

type IRawdatahandler interface {
	Увімкненоrawdatareceive(dataВказівник uintptr, розмір int) bool
	Надіслати(dataВказівник uintptr, розмір uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (поточний *TRawdatahandler) Множинаbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (поточний *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (поточний *TRawdatahandler) Увімкненоrawdatareceive(dataВказівник uintptr, розмір int) bool {
	мережаКартковіКонсоль.MДрукxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (поточний *TRawdatahandler) Надіслати(dataВказівник uintptr, розмір uint32) {
	мережаКартковіКонсоль.MДрукxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Надіслати(dataВказівник, розмір)
}

var MacАдреса0Порт uint16
var MacАдреса2Порт uint16
var MacАдреса4Порт uint16
var registerdataПорт uint16
var registerАдресаПорт uint16
var скинутиПорт uint16
var busКонтрольregisterdataПорт uint16

var initБлок TInitializationБлок

var надіслатиbufferОпис [8]TBufferdescriptor
var надіслатиbufferОписПамять [2048 + 15]byte
var надіслатиbuffer [2*1024 + 15][8]uint8
var поточнаНадіслатиbuffer uint8

var recvbufferОпис [8]TBufferdescriptor
var recvbufferОписПамять [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var поточнаrecvbuffer uint8
var funcЗначення func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TПерериванняhandler
	пристрійdescriptor	TPeripheralcomponentinterconnectПристрійdescriptor
	переривання		*TПерериванняmanager
	handler			*TRawdatahandler
}

var консоль_2 TКонсоль = TКонсоль{}
var irawdatahandler IRawdatahandler

func (поточний *Tamdam79c973) Initdriver(переривання *TПерериванняmanager, пристрійdescriptor TPeripheralcomponentinterconnectПристрійdescriptor, handler IRawdatahandler) {

	поточний.пристрійdescriptor = пристрійdescriptor

	funcЗначення = (*Tamdam79c973).ЕлементкеруванняПереривання
	var адреса uintptr
	адреса = uintptr(Pointer(&funcЗначення))

	поточний.Init(uint8(0x20+пристрійdescriptor.Переривання), uintptr(Pointer(переривання)), адреса)

	MacАдреса0Порт = uint16(пристрійdescriptor.Портbase)
	MacАдреса2Порт = uint16(пристрійdescriptor.Портbase) + 0x02
	MacАдреса4Порт = uint16(пристрійdescriptor.Портbase) + 0x04
	registerdataПорт = uint16(пристрійdescriptor.Портbase) + 0x10
	registerАдресаПорт = uint16(пристрійdescriptor.Портbase) + 0x12
	скинутиПорт = uint16(пристрійdescriptor.Портbase) + 0x14
	busКонтрольregisterdataПорт = uint16(пристрійdescriptor.Портbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	поточнаНадіслатиbuffer = 0
	поточнаrecvbuffer = 0

	var Mac0 uint64 = uint64(ПортЧитанняслово(MacАдреса0Порт) % 256)
	var Mac1 uint64 = uint64(ПортЧитанняслово(MacАдреса0Порт) / 256)
	var Mac2 uint64 = uint64(ПортЧитанняслово(MacАдреса2Порт) % 256)
	var Mac3 uint64 = uint64(ПортЧитанняслово(MacАдреса2Порт) / 256)
	var Mac4 uint64 = uint64(ПортЧитанняслово(MacАдреса4Порт) % 256)
	var Mac5 uint64 = uint64(ПортЧитанняслово(MacАдреса4Порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macАдреса uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	консоль_2.MДрукxy(([]byte)("[interrupt num : "), 0, 13)
	консоль_2.MHexadecimalДрук(uint8(пристрійdescriptor.Переривання))
	консоль_2.MДрук(([]byte)("]"))
	консоль_2.MДрук(([]byte)("[mac address : "))
	консоль_2.MUnsignedinteger16Друк(uint16(macАдреса >> 32))
	консоль_2.MUnsignedinteger32Друк(uint32(macАдреса & 0x00000000FFFFFFFF))
	консоль_2.MДрук(([]byte)("]"))

	ПортЗаписслово(registerАдресаПорт, 20)
	ПортЗаписслово(busКонтрольregisterdataПорт, 0x102)

	ПортЗаписслово(registerАдресаПорт, 0)
	ПортЗаписслово(registerdataПорт, 0x04)

	initБлок.рЕЖИМ = 0x0000
	initБлок.числоНадіслатиbuffer = 3
	initБлок.числоrecvbuffer = 3

	initБлок.physicalАдреса = Mac

	initБлок.логічніопераціїАдреса = 0

	надіслатиbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&надіслатиbufferОписПамять)) + 15) & ^(uintptr)(0xF)))
	initБлок.надіслатиbufferОписАдреса = uintptr(Pointer(&надіслатиbufferОпис))
	recvbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferОписПамять)) + 15) & ^(uintptr)(0xF)))
	initБлок.recvbufferОписАдреса = uintptr(Pointer(&recvbufferОпис))

	for i := 0; i < 8; i++ {
		надіслатиbufferОпис[i].адреса_2 = uint32((uintptr(Pointer(&надіслатиbuffer[i])) + 15) & ^(uintptr(0xF)))
		надіслатиbufferОпис[i].прапори = 0x7FF | 0xF000
		надіслатиbufferОпис[i].прапори2 = 0
		надіслатиbufferОпис[i].доступно = 0

		recvbufferОпис[i].адреса_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferОпис[i].прапори = 0xF7FF | 0x80000000

	}

	ПортЗаписслово(registerАдресаПорт, 1)
	ПортЗаписслово(registerdataПорт, uint16(uintptr(Pointer(&initБлок))&0xFFFF))

	ПортЗаписслово(registerАдресаПорт, 2)
	ПортЗаписслово(registerdataПорт, uint16((uintptr(Pointer(&initБлок))>>16)&0xFFFF))

}
func (поточний *Tamdam79c973) Активувати() {
	ПортЗаписслово(registerАдресаПорт, 0)
	ПортЗаписслово(registerdataПорт, 0x41)

	ПортЗаписслово(registerАдресаПорт, 4)
	temporary := ПортЧитанняслово(registerdataПорт)
	ПортЗаписслово(registerАдресаПорт, 4)
	ПортЗаписслово(registerdataПорт, temporary|0xC00)

	ПортЗаписслово(registerАдресаПорт, 0)
	ПортЗаписслово(registerdataПорт, 0x42)

}
func (поточний *Tamdam79c973) Скинути() int {
	ПортЧитанняслово(скинутиПорт)
	ПортЗаписслово(скинутиПорт, 0)
	return 10
}

var відлік uint16 = 0

func (поточний *Tamdam79c973) ЕлементкеруванняПереривання(esp uint32) uint32 {

	ПортЗаписслово(registerАдресаПорт, 0)
	temporary := uint32(ПортЧитанняслово(registerdataПорт))
	консоль_2.MДрук(([]byte)("interrupt("))
	консоль_2.MUnsignedinteger32Друк(esp)
	консоль_2.MДрук(([]byte)(":"))
	консоль_2.MUnsignedinteger32Друк(temporary)
	консоль_2.MДрук(([]byte)(":"))
	консоль_2.MUnsignedinteger16Друк(відлік)
	відлік++
	консоль_2.MДрук(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		консоль_2.MДрук(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		консоль_2.MДрук(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		консоль_2.MДрук(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		консоль_2.MДрук(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		консоль_2.MДрук(([]byte)("am79c973 data received"))
		поточний.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		консоль_2.MДрук(([]byte)("am79c973 data sent"))
	}

	ПортЗаписслово(registerАдресаПорт, 0)
	ПортЗаписслово(registerdataПорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		консоль_2.MДрук(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (поточний *Tamdam79c973) Надіслати(dataВказівник uintptr, розмір uint32) {
	var надіслатиdescriptor uint16 = uint16(поточнаНадіслатиbuffer)
	поточнаНадіслатиbuffer = 0

	if розмір > 1518 {
		розмір = 1518
	}

	var джерело_2 [4096]byte = *(*([4096]byte))(Pointer(dataВказівник))
	var призначення_2 uint32 = надіслатиbufferОпис[надіслатиdescriptor].адреса_2 + розмір - 1

	for i := 0; i < int(розмір); i++ {

		*(*byte)(Pointer(uintptr(призначення_2))) = джерело_2[int(розмір)-i-1]

		призначення_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataВказівник))
	консоль_2.MДрукxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		консоль_2.MHexadecimalДрук(data[i])
		консоль_2.MДрук(([]byte)(":"))
	}
	консоль_2.MДрук(([]byte)("\n"))

	надіслатиbufferОпис[надіслатиdescriptor].доступно = 0
	надіслатиbufferОпис[надіслатиdescriptor].прапори2 = 0
	надіслатиbufferОпис[надіслатиdescriptor].прапори = 0x8300F000 | uint32((-розмір)&0xFFF)

	ПортЗаписслово(registerАдресаПорт, 0)
	ПортЗаписслово(registerdataПорт, 0x48)

}
func (поточний *Tamdam79c973) Receive() {
	консоль_2.MДрук(([]byte)(":"))
	консоль_2.MUnsignedinteger32Друк(uint32(uintptr(Pointer(&надіслатиbuffer))))
	консоль_2.MДрук(([]byte)(":"))
	консоль_2.MHexadecimalДрук(надіслатиbuffer[0][0])
	консоль_2.MHexadecimalДрук(надіслатиbuffer[0][1])
	консоль_2.MДрук(([]byte)(":"))
	поточнаrecvbuffer = 0

	for ; (recvbufferОпис[поточнаrecvbuffer].прапори & 0x80000000) == 0; поточнаrecvbuffer = (поточнаrecvbuffer + 1) % 8 {

		if !(recvbufferОпис[поточнаrecvbuffer].прапори&0x40000000 != 0) && ((recvbufferОпис[поточнаrecvbuffer].прапори & 0x03000000) == 0x03000000) {
			var розмір uint32 = recvbufferОпис[поточнаrecvbuffer].прапори & 0xFFF
			if розмір > 64 {
				розмір -= 4
			}

			консоль_2.MДрук([]byte(" size : ["))
			консоль_2.MUnsignedinteger32Друк(розмір)
			консоль_2.MДрук([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferОпис[поточнаrecvbuffer].адреса_2)))
			var посилання_на_адресу uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Увімкненоrawdatareceive(посилання_на_адресу, int(розмір)) {

					консоль_2.MДрукxy(([]byte)("self.Send"), 0, 22)

					поточний.Надіслати(посилання_на_адресу, розмір)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				консоль_2.MHexadecimalДрук(buffer_2[i])
				консоль_2.MДрук([]byte(":"))
			}

		}
		recvbufferОпис[поточнаrecvbuffer].прапори2 = 0
		recvbufferОпис[поточнаrecvbuffer].прапори = 0x8000F7FF
	}
}
func (поточний *Tamdam79c973) Множинаhandler(handler *TRawdatahandler) {
	поточний.handler = handler
}
func (поточний *Tamdam79c973) GetmacАдреса() uint64 {

	return initБлок.physicalАдреса
}
func (поточний *Tamdam79c973) МножинаipАдреса(ip uint64) {
	initБлок.логічніопераціїАдреса = ip
}
func (поточний *Tamdam79c973) GetipАдреса() uint64 {
	return initБлок.логічніопераціїАдреса
}
