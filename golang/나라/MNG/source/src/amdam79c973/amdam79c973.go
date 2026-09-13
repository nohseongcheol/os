package amdam79c973

import . "unsafe"
import . "interrupt"
import . "консол"
import . "порт"
import . "pci"

var сүлжээcardКонсол TКонсол = TКонсол{}

type TInitializationblock struct {
	горим			uint16
	numbersendbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferТодорхойлолтaddress	uintptr
	sendbufferТодорхойлолтaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	төлвүүд		uint32
	төлвүүд2	uint32
	available	uint32
}

type IRawdatahandler interface {
	Onrawdatareceive(datapointer uintptr, хэмжээ int) bool
	Send(datapointer uintptr, хэмжээ uint32)
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
func (self *TRawdatahandler) Onrawdatareceive(datapointer uintptr, хэмжээ int) bool {
	сүлжээcardКонсол.MХэвлэхxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Send(datapointer uintptr, хэмжээ uint32) {
	сүлжээcardКонсол.MХэвлэхxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(datapointer, хэмжээ)
}

var Macaddress0Порт uint16
var Macaddress2Порт uint16
var Macaddress4Порт uint16
var registerdataПорт uint16
var registeraddressПорт uint16
var суллахПорт uint16
var buscontrolregisterdataПорт uint16

var initblock TInitializationblock

var sendbufferТодорхойлолт [8]TBufferdescriptor
var sendbufferТодорхойлолтСанахой [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferТодорхойлолт [8]TBufferdescriptor
var recvbufferТодорхойлолтСанахой [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcУтга func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	төхөөрөмжdescriptor	TPeripheralcomponentinterconnectТөхөөрөмжdescriptor
	interrupt		*TInterruptЗохицуулагч
	handler			*TRawdatahandler
}

var консол_2 TКонсол = TКонсол{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptЗохицуулагч, төхөөрөмжdescriptor TPeripheralcomponentinterconnectТөхөөрөмжdescriptor, handler IRawdatahandler) {

	self.төхөөрөмжdescriptor = төхөөрөмжdescriptor

	funcУтга = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcУтга))

	self.Init(uint8(0x20+төхөөрөмжdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Порт = uint16(төхөөрөмжdescriptor.Портbase)
	Macaddress2Порт = uint16(төхөөрөмжdescriptor.Портbase) + 0x02
	Macaddress4Порт = uint16(төхөөрөмжdescriptor.Портbase) + 0x04
	registerdataПорт = uint16(төхөөрөмжdescriptor.Портbase) + 0x10
	registeraddressПорт = uint16(төхөөрөмжdescriptor.Портbase) + 0x12
	суллахПорт = uint16(төхөөрөмжdescriptor.Портbase) + 0x14
	buscontrolregisterdataПорт = uint16(төхөөрөмжdescriptor.Портbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(ПортУншихword(Macaddress0Порт) % 256)
	var Mac1 uint64 = uint64(ПортУншихword(Macaddress0Порт) / 256)
	var Mac2 uint64 = uint64(ПортУншихword(Macaddress2Порт) % 256)
	var Mac3 uint64 = uint64(ПортУншихword(Macaddress2Порт) / 256)
	var Mac4 uint64 = uint64(ПортУншихword(Macaddress4Порт) % 256)
	var Mac5 uint64 = uint64(ПортУншихword(Macaddress4Порт) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	консол_2.MХэвлэхxy(([]byte)("[interrupt num : "), 0, 13)
	консол_2.MHexadecimalХэвлэх(uint8(төхөөрөмжdescriptor.Interrupt))
	консол_2.MХэвлэх(([]byte)("]"))
	консол_2.MХэвлэх(([]byte)("[mac address : "))
	консол_2.MUnsignedinteger16Хэвлэх(uint16(macaddress >> 32))
	консол_2.MUnsignedinteger32Хэвлэх(uint32(macaddress & 0x00000000FFFFFFFF))
	консол_2.MХэвлэх(([]byte)("]"))

	ПортБичихword(registeraddressПорт, 20)
	ПортБичихword(buscontrolregisterdataПорт, 0x102)

	ПортБичихword(registeraddressПорт, 0)
	ПортБичихword(registerdataПорт, 0x04)

	initblock.горим = 0x0000
	initblock.numbersendbuffer = 3
	initblock.numberrecvbuffer = 3

	initblock.physicaladdress = Mac

	initblock.logicaladdress = 0

	sendbufferТодорхойлолт = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferТодорхойлолтСанахой)) + 15) & ^(uintptr)(0xF)))
	initblock.sendbufferТодорхойлолтaddress = uintptr(Pointer(&sendbufferТодорхойлолт))
	recvbufferТодорхойлолт = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferТодорхойлолтСанахой)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferТодорхойлолтaddress = uintptr(Pointer(&recvbufferТодорхойлолт))

	for i := 0; i < 8; i++ {
		sendbufferТодорхойлолт[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferТодорхойлолт[i].төлвүүд = 0x7FF | 0xF000
		sendbufferТодорхойлолт[i].төлвүүд2 = 0
		sendbufferТодорхойлолт[i].available = 0

		recvbufferТодорхойлолт[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferТодорхойлолт[i].төлвүүд = 0xF7FF | 0x80000000

	}

	ПортБичихword(registeraddressПорт, 1)
	ПортБичихword(registerdataПорт, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	ПортБичихword(registeraddressПорт, 2)
	ПортБичихword(registerdataПорт, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Идэвхжүүлэх() {
	ПортБичихword(registeraddressПорт, 0)
	ПортБичихword(registerdataПорт, 0x41)

	ПортБичихword(registeraddressПорт, 4)
	temporary := ПортУншихword(registerdataПорт)
	ПортБичихword(registeraddressПорт, 4)
	ПортБичихword(registerdataПорт, temporary|0xC00)

	ПортБичихword(registeraddressПорт, 0)
	ПортБичихword(registerdataПорт, 0x42)

}
func (self *Tamdam79c973) Суллах() int {
	ПортУншихword(суллахПорт)
	ПортБичихword(суллахПорт, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	ПортБичихword(registeraddressПорт, 0)
	temporary := uint32(ПортУншихword(registerdataПорт))
	консол_2.MХэвлэх(([]byte)("interrupt("))
	консол_2.MUnsignedinteger32Хэвлэх(esp)
	консол_2.MХэвлэх(([]byte)(":"))
	консол_2.MUnsignedinteger32Хэвлэх(temporary)
	консол_2.MХэвлэх(([]byte)(":"))
	консол_2.MUnsignedinteger16Хэвлэх(count)
	count++
	консол_2.MХэвлэх(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		консол_2.MХэвлэх(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		консол_2.MХэвлэх(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		консол_2.MХэвлэх(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		консол_2.MХэвлэх(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		консол_2.MХэвлэх(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		консол_2.MХэвлэх(([]byte)("am79c973 data sent"))
	}

	ПортБичихword(registeraddressПорт, 0)
	ПортБичихword(registerdataПорт, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		консол_2.MХэвлэх(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Send(datapointer uintptr, хэмжээ uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if хэмжээ > 1518 {
		хэмжээ = 1518
	}

	var эх_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var destination_2 uint32 = sendbufferТодорхойлолт[senddescriptor].address_2 + хэмжээ - 1

	for i := 0; i < int(хэмжээ); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = эх_2[int(хэмжээ)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	консол_2.MХэвлэхxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		консол_2.MHexadecimalХэвлэх(data[i])
		консол_2.MХэвлэх(([]byte)(":"))
	}
	консол_2.MХэвлэх(([]byte)("\n"))

	sendbufferТодорхойлолт[senddescriptor].available = 0
	sendbufferТодорхойлолт[senddescriptor].төлвүүд2 = 0
	sendbufferТодорхойлолт[senddescriptor].төлвүүд = 0x8300F000 | uint32((-хэмжээ)&0xFFF)

	ПортБичихword(registeraddressПорт, 0)
	ПортБичихword(registerdataПорт, 0x48)

}
func (self *Tamdam79c973) Receive() {
	консол_2.MХэвлэх(([]byte)(":"))
	консол_2.MUnsignedinteger32Хэвлэх(uint32(uintptr(Pointer(&sendbuffer))))
	консол_2.MХэвлэх(([]byte)(":"))
	консол_2.MHexadecimalХэвлэх(sendbuffer[0][0])
	консол_2.MHexadecimalХэвлэх(sendbuffer[0][1])
	консол_2.MХэвлэх(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferТодорхойлолт[currentrecvbuffer].төлвүүд & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferТодорхойлолт[currentrecvbuffer].төлвүүд&0x40000000 != 0) && ((recvbufferТодорхойлолт[currentrecvbuffer].төлвүүд & 0x03000000) == 0x03000000) {
			var хэмжээ uint32 = recvbufferТодорхойлолт[currentrecvbuffer].төлвүүд & 0xFFF
			if хэмжээ > 64 {
				хэмжээ -= 4
			}

			консол_2.MХэвлэх([]byte(" size : ["))
			консол_2.MUnsignedinteger32Хэвлэх(хэмжээ)
			консол_2.MХэвлэх([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferТодорхойлолт[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Onrawdatareceive(pointer, int(хэмжээ)) {

					консол_2.MХэвлэхxy(([]byte)("self.Send"), 0, 22)

					self.Send(pointer, хэмжээ)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				консол_2.MHexadecimalХэвлэх(buffer_2[i])
				консол_2.MХэвлэх([]byte(":"))
			}

		}
		recvbufferТодорхойлолт[currentrecvbuffer].төлвүүд2 = 0
		recvbufferТодорхойлолт[currentrecvbuffer].төлвүүд = 0x8000F7FF
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
