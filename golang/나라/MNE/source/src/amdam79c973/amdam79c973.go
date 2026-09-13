package amdam79c973

import . "unsafe"
import . "ометање"
import . "конзола"
import . "порт"
import . "pci"

var мрежаcardКонзола TКонзола = TКонзола{}

type TInitializationBlok struct {
	rEŽIM			uint16
	бројПошаљиbuffer	uint8
	бројrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferОписaddress	uintptr
	пошаљиbufferОписaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	parametri	uint32
	parametri2	uint32
	raspoloživo	uint32
}

type IRawdatahandler interface {
	Narawdatareceive(dataPokazivač uintptr, величина int) bool
	Пошаљи(dataPokazivač uintptr, величина uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (isti *TRawdatahandler) Скупbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (isti *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (isti *TRawdatahandler) Narawdatareceive(dataPokazivač uintptr, величина int) bool {
	мрежаcardКонзола.MŠtampajxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (isti *TRawdatahandler) Пошаљи(dataPokazivač uintptr, величина uint32) {
	мрежаcardКонзола.MŠtampajxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Пошаљи(dataPokazivač, величина)
}

var Macaddress0Порт uint16
var Macaddress2Порт uint16
var Macaddress4Порт uint16
var registerdataПорт uint16
var registeraddressПорт uint16
var ponovopostaviПорт uint16
var busКонтролregisterdataПорт uint16

var initBlok TInitializationBlok

var пошаљиbufferОпис [8]TBufferdescriptor
var пошаљиbufferОписMemorija [2048 + 15]byte
var пошаљиbuffer [2*1024 + 15][8]uint8
var тренутноПошаљиbuffer uint8

var recvbufferОпис [8]TBufferdescriptor
var recvbufferОписMemorija [2048 + 15]uint8
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

func (isti *Tamdam79c973) Initdriver(ометање *TОметањеmanager, уређајdescriptor TPeripheralcomponentinterconnectУређајdescriptor, handler IRawdatahandler) {

	isti.уређајdescriptor = уређајdescriptor

	funcВредност = (*Tamdam79c973).РучкаОметање
	var address uintptr
	address = uintptr(Pointer(&funcВредност))

	isti.Init(uint8(0x20+уређајdescriptor.Ометање), uintptr(Pointer(ометање)), address)

	Macaddress0Порт = uint16(уређајdescriptor.Портbase)
	Macaddress2Порт = uint16(уређајdescriptor.Портbase) + 0x02
	Macaddress4Порт = uint16(уређајdescriptor.Портbase) + 0x04
	registerdataПорт = uint16(уређајdescriptor.Портbase) + 0x10
	registeraddressПорт = uint16(уређајdescriptor.Портbase) + 0x12
	ponovopostaviПорт = uint16(уређајdescriptor.Портbase) + 0x14
	busКонтролregisterdataПорт = uint16(уређајdescriptor.Портbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	тренутноПошаљиbuffer = 0
	тренутноrecvbuffer = 0

	var Mac0 uint64 = uint64(Портчитањеreč(Macaddress0Порт) % 256)
	var Mac1 uint64 = uint64(Портчитањеreč(Macaddress0Порт) / 256)
	var Mac2 uint64 = uint64(Портчитањеreč(Macaddress2Порт) % 256)
	var Mac3 uint64 = uint64(Портчитањеreč(Macaddress2Порт) / 256)
	var Mac4 uint64 = uint64(Портчитањеreč(Macaddress4Порт) % 256)
	var Mac5 uint64 = uint64(Портчитањеreč(Macaddress4Порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	конзола_2.MŠtampajxy(([]byte)("[interrupt num : "), 0, 13)
	конзола_2.MHexadecimalŠtampaj(uint8(уређајdescriptor.Ометање))
	конзола_2.MŠtampaj(([]byte)("]"))
	конзола_2.MŠtampaj(([]byte)("[mac address : "))
	конзола_2.MUnsignedinteger16Štampaj(uint16(macaddress >> 32))
	конзола_2.MUnsignedinteger32Štampaj(uint32(macaddress & 0x00000000FFFFFFFF))
	конзола_2.MŠtampaj(([]byte)("]"))

	Портupisreč(registeraddressПорт, 20)
	Портupisreč(busКонтролregisterdataПорт, 0x102)

	Портupisreč(registeraddressПорт, 0)
	Портupisreč(registerdataПорт, 0x04)

	initBlok.rEŽIM = 0x0000
	initBlok.бројПошаљиbuffer = 3
	initBlok.бројrecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logicaladdress = 0

	пошаљиbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&пошаљиbufferОписMemorija)) + 15) & ^(uintptr)(0xF)))
	initBlok.пошаљиbufferОписaddress = uintptr(Pointer(&пошаљиbufferОпис))
	recvbufferОпис = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferОписMemorija)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferОписaddress = uintptr(Pointer(&recvbufferОпис))

	for i := 0; i < 8; i++ {
		пошаљиbufferОпис[i].address_2 = uint32((uintptr(Pointer(&пошаљиbuffer[i])) + 15) & ^(uintptr(0xF)))
		пошаљиbufferОпис[i].parametri = 0x7FF | 0xF000
		пошаљиbufferОпис[i].parametri2 = 0
		пошаљиbufferОпис[i].raspoloživo = 0

		recvbufferОпис[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferОпис[i].parametri = 0xF7FF | 0x80000000

	}

	Портupisreč(registeraddressПорт, 1)
	Портupisreč(registerdataПорт, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	Портupisreč(registeraddressПорт, 2)
	Портupisreč(registerdataПорт, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (isti *Tamdam79c973) Pokreni() {
	Портupisreč(registeraddressПорт, 0)
	Портupisreč(registerdataПорт, 0x41)

	Портupisreč(registeraddressПорт, 4)
	temporary := Портчитањеreč(registerdataПорт)
	Портupisreč(registeraddressПорт, 4)
	Портupisreč(registerdataПорт, temporary|0xC00)

	Портupisreč(registeraddressПорт, 0)
	Портupisreč(registerdataПорт, 0x42)

}
func (isti *Tamdam79c973) Ponovopostavi() int {
	Портчитањеreč(ponovopostaviПорт)
	Портupisreč(ponovopostaviПорт, 0)
	return 10
}

var count uint16 = 0

func (isti *Tamdam79c973) РучкаОметање(esp uint32) uint32 {

	Портupisreč(registeraddressПорт, 0)
	temporary := uint32(Портчитањеreč(registerdataПорт))
	конзола_2.MŠtampaj(([]byte)("interrupt("))
	конзола_2.MUnsignedinteger32Štampaj(esp)
	конзола_2.MŠtampaj(([]byte)(":"))
	конзола_2.MUnsignedinteger32Štampaj(temporary)
	конзола_2.MŠtampaj(([]byte)(":"))
	конзола_2.MUnsignedinteger16Štampaj(count)
	count++
	конзола_2.MŠtampaj(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		конзола_2.MŠtampaj(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		конзола_2.MŠtampaj(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		конзола_2.MŠtampaj(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		конзола_2.MŠtampaj(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		конзола_2.MŠtampaj(([]byte)("am79c973 data received"))
		isti.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		конзола_2.MŠtampaj(([]byte)("am79c973 data sent"))
	}

	Портupisreč(registeraddressПорт, 0)
	Портupisreč(registerdataПорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		конзола_2.MŠtampaj(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (isti *Tamdam79c973) Пошаљи(dataPokazivač uintptr, величина uint32) {
	var пошаљиdescriptor uint16 = uint16(тренутноПошаљиbuffer)
	тренутноПошаљиbuffer = 0

	if величина > 1518 {
		величина = 1518
	}

	var izvor_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))
	var odredište_2 uint32 = пошаљиbufferОпис[пошаљиdescriptor].address_2 + величина - 1

	for i := 0; i < int(величина); i++ {

		*(*byte)(Pointer(uintptr(odredište_2))) = izvor_2[int(величина)-i-1]

		odredište_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))
	конзола_2.MŠtampajxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		конзола_2.MHexadecimalŠtampaj(data[i])
		конзола_2.MŠtampaj(([]byte)(":"))
	}
	конзола_2.MŠtampaj(([]byte)("\n"))

	пошаљиbufferОпис[пошаљиdescriptor].raspoloživo = 0
	пошаљиbufferОпис[пошаљиdescriptor].parametri2 = 0
	пошаљиbufferОпис[пошаљиdescriptor].parametri = 0x8300F000 | uint32((-величина)&0xFFF)

	Портupisreč(registeraddressПорт, 0)
	Портupisreč(registerdataПорт, 0x48)

}
func (isti *Tamdam79c973) Receive() {
	конзола_2.MŠtampaj(([]byte)(":"))
	конзола_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&пошаљиbuffer))))
	конзола_2.MŠtampaj(([]byte)(":"))
	конзола_2.MHexadecimalŠtampaj(пошаљиbuffer[0][0])
	конзола_2.MHexadecimalŠtampaj(пошаљиbuffer[0][1])
	конзола_2.MŠtampaj(([]byte)(":"))
	тренутноrecvbuffer = 0

	for ; (recvbufferОпис[тренутноrecvbuffer].parametri & 0x80000000) == 0; тренутноrecvbuffer = (тренутноrecvbuffer + 1) % 8 {

		if !(recvbufferОпис[тренутноrecvbuffer].parametri&0x40000000 != 0) && ((recvbufferОпис[тренутноrecvbuffer].parametri & 0x03000000) == 0x03000000) {
			var величина uint32 = recvbufferОпис[тренутноrecvbuffer].parametri & 0xFFF
			if величина > 64 {
				величина -= 4
			}

			конзола_2.MŠtampaj([]byte(" size : ["))
			конзола_2.MUnsignedinteger32Štampaj(величина)
			конзола_2.MŠtampaj([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferОпис[тренутноrecvbuffer].address_2)))
			var pokazivač uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Narawdatareceive(pokazivač, int(величина)) {

					конзола_2.MŠtampajxy(([]byte)("self.Send"), 0, 22)

					isti.Пошаљи(pokazivač, величина)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				конзола_2.MHexadecimalŠtampaj(buffer_2[i])
				конзола_2.MŠtampaj([]byte(":"))
			}

		}
		recvbufferОпис[тренутноrecvbuffer].parametri2 = 0
		recvbufferОпис[тренутноrecvbuffer].parametri = 0x8000F7FF
	}
}
func (isti *Tamdam79c973) Скупhandler(handler *TRawdatahandler) {
	isti.handler = handler
}
func (isti *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (isti *Tamdam79c973) Скупipaddress(ip uint64) {
	initBlok.logicaladdress = ip
}
func (isti *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logicaladdress
}
