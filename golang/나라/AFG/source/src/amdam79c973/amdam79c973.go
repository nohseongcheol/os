package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "درگاه"
import . "pci"

var شبکهcardconsole TConsole = TConsole{}

type TInitializationقطعه struct {
	حالت			uint16
	numbersendbuffer	uint8
	numberrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferشرحaddress	uintptr
	sendbufferشرحaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flags		uint32
	flags2		uint32
	دردسترس		uint32
}

type IRawdatahandler interface {
	Oروشنrawdatareceive(datapointer uintptr, اندازه int) bool
	Send(datapointer uintptr, اندازه uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (خود *TRawdatahandler) Setbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (خود *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (خود *TRawdatahandler) Oروشنrawdatareceive(datapointer uintptr, اندازه int) bool {
	شبکهcardconsole.Mچاپxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (خود *TRawdatahandler) Send(datapointer uintptr, اندازه uint32) {
	شبکهcardconsole.Mچاپxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(datapointer, اندازه)
}

var Macaddress0درگاه uint16
var Macaddress2درگاه uint16
var Macaddress4درگاه uint16
var registerdataدرگاه uint16
var registeraddressدرگاه uint16
var برگرداندنبهمقادیراولیهدرگاه uint16
var busمهارregisterdataدرگاه uint16

var initقطعه TInitializationقطعه

var sendbufferشرح [8]TBufferdescriptor
var sendbufferشرححافظه [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferشرح [8]TBufferdescriptor
var recvbufferشرححافظه [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcمقدار func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	دستگاهdescriptor	TPeripheralcomponentinterconnectدستگاهdescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (خود *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, دستگاهdescriptor TPeripheralcomponentinterconnectدستگاهdescriptor, handler IRawdatahandler) {

	خود.دستگاهdescriptor = دستگاهdescriptor

	funcمقدار = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcمقدار))

	خود.Init(uint8(0x20+دستگاهdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0درگاه = uint16(دستگاهdescriptor.Pدرگاهbase)
	Macaddress2درگاه = uint16(دستگاهdescriptor.Pدرگاهbase) + 0x02
	Macaddress4درگاه = uint16(دستگاهdescriptor.Pدرگاهbase) + 0x04
	registerdataدرگاه = uint16(دستگاهdescriptor.Pدرگاهbase) + 0x10
	registeraddressدرگاه = uint16(دستگاهdescriptor.Pدرگاهbase) + 0x12
	برگرداندنبهمقادیراولیهدرگاه = uint16(دستگاهdescriptor.Pدرگاهbase) + 0x14
	busمهارregisterdataدرگاه = uint16(دستگاهdescriptor.Pدرگاهbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(Pدرگاهخواندنکلمه(Macaddress0درگاه) % 256)
	var Mac1 uint64 = uint64(Pدرگاهخواندنکلمه(Macaddress0درگاه) / 256)
	var Mac2 uint64 = uint64(Pدرگاهخواندنکلمه(Macaddress2درگاه) % 256)
	var Mac3 uint64 = uint64(Pدرگاهخواندنکلمه(Macaddress2درگاه) / 256)
	var Mac4 uint64 = uint64(Pدرگاهخواندنکلمه(Macaddress4درگاه) % 256)
	var Mac5 uint64 = uint64(Pدرگاهخواندنکلمه(Macaddress4درگاه) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.Mچاپxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalچاپ(uint8(دستگاهdescriptor.Interrupt))
	console_2.Mچاپ(([]byte)("]"))
	console_2.Mچاپ(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16چاپ(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32چاپ(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.Mچاپ(([]byte)("]"))

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 20)
	Pدرگاهنوشتنکلمه(busمهارregisterdataدرگاه, 0x102)

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 0)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, 0x04)

	initقطعه.حالت = 0x0000
	initقطعه.numbersendbuffer = 3
	initقطعه.numberrecvbuffer = 3

	initقطعه.physicaladdress = Mac

	initقطعه.logicaladdress = 0

	sendbufferشرح = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferشرححافظه)) + 15) & ^(uintptr)(0xF)))
	initقطعه.sendbufferشرحaddress = uintptr(Pointer(&sendbufferشرح))
	recvbufferشرح = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferشرححافظه)) + 15) & ^(uintptr)(0xF)))
	initقطعه.recvbufferشرحaddress = uintptr(Pointer(&recvbufferشرح))

	for i := 0; i < 8; i++ {
		sendbufferشرح[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferشرح[i].flags = 0x7FF | 0xF000
		sendbufferشرح[i].flags2 = 0
		sendbufferشرح[i].دردسترس = 0

		recvbufferشرح[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferشرح[i].flags = 0xF7FF | 0x80000000

	}

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 1)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, uint16(uintptr(Pointer(&initقطعه))&0xFFFF))

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 2)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, uint16((uintptr(Pointer(&initقطعه))>>16)&0xFFFF))

}
func (خود *Tamdam79c973) Aفعالکردن() {
	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 0)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, 0x41)

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 4)
	temporary := Pدرگاهخواندنکلمه(registerdataدرگاه)
	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 4)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, temporary|0xC00)

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 0)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, 0x42)

}
func (خود *Tamdam79c973) Rبرگرداندنبهمقادیراولیه() int {
	Pدرگاهخواندنکلمه(برگرداندنبهمقادیراولیهدرگاه)
	Pدرگاهنوشتنکلمه(برگرداندنبهمقادیراولیهدرگاه, 0)
	return 10
}

var count uint16 = 0

func (خود *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 0)
	temporary := uint32(Pدرگاهخواندنکلمه(registerdataدرگاه))
	console_2.Mچاپ(([]byte)("interrupt("))
	console_2.MUnsignedinteger32چاپ(esp)
	console_2.Mچاپ(([]byte)(":"))
	console_2.MUnsignedinteger32چاپ(temporary)
	console_2.Mچاپ(([]byte)(":"))
	console_2.MUnsignedinteger16چاپ(count)
	count++
	console_2.Mچاپ(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.Mچاپ(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.Mچاپ(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.Mچاپ(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.Mچاپ(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.Mچاپ(([]byte)("am79c973 data received"))
		خود.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.Mچاپ(([]byte)("am79c973 data sent"))
	}

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 0)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.Mچاپ(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (خود *Tamdam79c973) Send(datapointer uintptr, اندازه uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if اندازه > 1518 {
		اندازه = 1518
	}

	var مبدأ_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var مقصد_2 uint32 = sendbufferشرح[senddescriptor].address_2 + اندازه - 1

	for i := 0; i < int(اندازه); i++ {

		*(*byte)(Pointer(uintptr(مقصد_2))) = مبدأ_2[int(اندازه)-i-1]

		مقصد_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	console_2.Mچاپxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalچاپ(data[i])
		console_2.Mچاپ(([]byte)(":"))
	}
	console_2.Mچاپ(([]byte)("\n"))

	sendbufferشرح[senddescriptor].دردسترس = 0
	sendbufferشرح[senddescriptor].flags2 = 0
	sendbufferشرح[senddescriptor].flags = 0x8300F000 | uint32((-اندازه)&0xFFF)

	Pدرگاهنوشتنکلمه(registeraddressدرگاه, 0)
	Pدرگاهنوشتنکلمه(registerdataدرگاه, 0x48)

}
func (خود *Tamdam79c973) Receive() {
	console_2.Mچاپ(([]byte)(":"))
	console_2.MUnsignedinteger32چاپ(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.Mچاپ(([]byte)(":"))
	console_2.MHexadecimalچاپ(sendbuffer[0][0])
	console_2.MHexadecimalچاپ(sendbuffer[0][1])
	console_2.Mچاپ(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferشرح[currentrecvbuffer].flags & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferشرح[currentrecvbuffer].flags&0x40000000 != 0) && ((recvbufferشرح[currentrecvbuffer].flags & 0x03000000) == 0x03000000) {
			var اندازه uint32 = recvbufferشرح[currentrecvbuffer].flags & 0xFFF
			if اندازه > 64 {
				اندازه -= 4
			}

			console_2.Mچاپ([]byte(" size : ["))
			console_2.MUnsignedinteger32چاپ(اندازه)
			console_2.Mچاپ([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferشرح[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Oروشنrawdatareceive(pointer, int(اندازه)) {

					console_2.Mچاپxy(([]byte)("self.Send"), 0, 22)

					خود.Send(pointer, اندازه)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalچاپ(buffer_2[i])
				console_2.Mچاپ([]byte(":"))
			}

		}
		recvbufferشرح[currentrecvbuffer].flags2 = 0
		recvbufferشرح[currentrecvbuffer].flags = 0x8000F7FF
	}
}
func (خود *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	خود.handler = handler
}
func (خود *Tamdam79c973) Getmacaddress() uint64 {

	return initقطعه.physicaladdress
}
func (خود *Tamdam79c973) Setipaddress(ip uint64) {
	initقطعه.logicaladdress = ip
}
func (خود *Tamdam79c973) Getipaddress() uint64 {
	return initقطعه.logicaladdress
}
