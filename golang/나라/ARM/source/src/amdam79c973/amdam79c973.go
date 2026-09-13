package amdam79c973

import . "unsafe"
import . "ընդհատել"
import . "console"
import . "պորտ"
import . "pci"

var ցանցcardconsole TConsole = TConsole{}

type TInitializationԱրգելափակել struct {
	ռեժիմ			uint16
	հԱՄԱՐՈՒղարկելbuffer	uint8
	հԱՄԱՐrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress				uint64
	recvbufferՆկարագրությունaddress		uintptr
	ոՒղարկելbufferՆկարագրությունaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	դրոշներ		uint32
	դրոշներ2	uint32
	հասանելի	uint32
}

type IRawdatahandler interface {
	Միացնելrawdatareceive(dataՑուցիչ uintptr, չափս int) bool
	ՈՒղարկել(dataՑուցիչ uintptr, չափս uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (ինքնուրույն *TRawdatahandler) Setbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (ինքնուրույն *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (ինքնուրույն *TRawdatahandler) Միացնելrawdatareceive(dataՑուցիչ uintptr, չափս int) bool {
	ցանցcardconsole.MՏպելxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (ինքնուրույն *TRawdatahandler) ՈՒղարկել(dataՑուցիչ uintptr, չափս uint32) {
	ցանցcardconsole.MՏպելxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.ՈՒղարկել(dataՑուցիչ, չափս)
}

var Macaddress0Պորտ uint16
var Macaddress2Պորտ uint16
var Macaddress4Պորտ uint16
var registerdataՊորտ uint16
var registeraddressՊորտ uint16
var դադարեցնելՊորտ uint16
var buscontrolregisterdataՊորտ uint16

var initԱրգելափակել TInitializationԱրգելափակել

var ոՒղարկելbufferՆկարագրություն [8]TBufferdescriptor
var ոՒղարկելbufferՆկարագրությունՀիշողություն [2048 + 15]byte
var ոՒղարկելbuffer [2*1024 + 15][8]uint8
var currentՈՒղարկելbuffer uint8

var recvbufferՆկարագրություն [8]TBufferdescriptor
var recvbufferՆկարագրությունՀիշողություն [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcԱրժեք func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TԸնդհատելhandler
	սարքdescriptor	TPeripheralcomponentinterconnectՍարքdescriptor
	ընդհատել	*TԸնդհատելmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (ինքնուրույն *Tamdam79c973) Initdriver(ընդհատել *TԸնդհատելmanager, սարքdescriptor TPeripheralcomponentinterconnectՍարքdescriptor, handler IRawdatahandler) {

	ինքնուրույն.սարքdescriptor = սարքdescriptor

	funcԱրժեք = (*Tamdam79c973).HandleԸնդհատել
	var address uintptr
	address = uintptr(Pointer(&funcԱրժեք))

	ինքնուրույն.Init(uint8(0x20+սարքdescriptor.Ընդհատել), uintptr(Pointer(ընդհատել)), address)

	Macaddress0Պորտ = uint16(սարքdescriptor.Պորտbase)
	Macaddress2Պորտ = uint16(սարքdescriptor.Պորտbase) + 0x02
	Macaddress4Պորտ = uint16(սարքdescriptor.Պորտbase) + 0x04
	registerdataՊորտ = uint16(սարքdescriptor.Պորտbase) + 0x10
	registeraddressՊորտ = uint16(սարքdescriptor.Պորտbase) + 0x12
	դադարեցնելՊորտ = uint16(սարքdescriptor.Պորտbase) + 0x14
	buscontrolregisterdataՊորտ = uint16(սարքdescriptor.Պորտbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentՈՒղարկելbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(ՊորտԸնթերցումբառ(Macaddress0Պորտ) % 256)
	var Mac1 uint64 = uint64(ՊորտԸնթերցումբառ(Macaddress0Պորտ) / 256)
	var Mac2 uint64 = uint64(ՊորտԸնթերցումբառ(Macaddress2Պորտ) % 256)
	var Mac3 uint64 = uint64(ՊորտԸնթերցումբառ(Macaddress2Պորտ) / 256)
	var Mac4 uint64 = uint64(ՊորտԸնթերցումբառ(Macaddress4Պորտ) % 256)
	var Mac5 uint64 = uint64(ՊորտԸնթերցումբառ(Macaddress4Պորտ) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MՏպելxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalՏպել(uint8(սարքdescriptor.Ընդհատել))
	console_2.MՏպել(([]byte)("]"))
	console_2.MՏպել(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Տպել(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Տպել(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MՏպել(([]byte)("]"))

	ՊորտԳրելբառ(registeraddressՊորտ, 20)
	ՊորտԳրելբառ(buscontrolregisterdataՊորտ, 0x102)

	ՊորտԳրելբառ(registeraddressՊորտ, 0)
	ՊորտԳրելբառ(registerdataՊորտ, 0x04)

	initԱրգելափակել.ռեժիմ = 0x0000
	initԱրգելափակել.հԱՄԱՐՈՒղարկելbuffer = 3
	initԱրգելափակել.հԱՄԱՐrecvbuffer = 3

	initԱրգելափակել.physicaladdress = Mac

	initԱրգելափակել.logicaladdress = 0

	ոՒղարկելbufferՆկարագրություն = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&ոՒղարկելbufferՆկարագրությունՀիշողություն)) + 15) & ^(uintptr)(0xF)))
	initԱրգելափակել.ոՒղարկելbufferՆկարագրությունaddress = uintptr(Pointer(&ոՒղարկելbufferՆկարագրություն))
	recvbufferՆկարագրություն = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferՆկարագրությունՀիշողություն)) + 15) & ^(uintptr)(0xF)))
	initԱրգելափակել.recvbufferՆկարագրությունaddress = uintptr(Pointer(&recvbufferՆկարագրություն))

	for i := 0; i < 8; i++ {
		ոՒղարկելbufferՆկարագրություն[i].address_2 = uint32((uintptr(Pointer(&ոՒղարկելbuffer[i])) + 15) & ^(uintptr(0xF)))
		ոՒղարկելbufferՆկարագրություն[i].դրոշներ = 0x7FF | 0xF000
		ոՒղարկելbufferՆկարագրություն[i].դրոշներ2 = 0
		ոՒղարկելbufferՆկարագրություն[i].հասանելի = 0

		recvbufferՆկարագրություն[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferՆկարագրություն[i].դրոշներ = 0xF7FF | 0x80000000

	}

	ՊորտԳրելբառ(registeraddressՊորտ, 1)
	ՊորտԳրելբառ(registerdataՊորտ, uint16(uintptr(Pointer(&initԱրգելափակել))&0xFFFF))

	ՊորտԳրելբառ(registeraddressՊորտ, 2)
	ՊորտԳրելբառ(registerdataՊորտ, uint16((uintptr(Pointer(&initԱրգելափակել))>>16)&0xFFFF))

}
func (ինքնուրույն *Tamdam79c973) Ակտիվացնել() {
	ՊորտԳրելբառ(registeraddressՊորտ, 0)
	ՊորտԳրելբառ(registerdataՊորտ, 0x41)

	ՊորտԳրելբառ(registeraddressՊորտ, 4)
	temporary := ՊորտԸնթերցումբառ(registerdataՊորտ)
	ՊորտԳրելբառ(registeraddressՊորտ, 4)
	ՊորտԳրելբառ(registerdataՊորտ, temporary|0xC00)

	ՊորտԳրելբառ(registeraddressՊորտ, 0)
	ՊորտԳրելբառ(registerdataՊորտ, 0x42)

}
func (ինքնուրույն *Tamdam79c973) Դադարեցնել() int {
	ՊորտԸնթերցումբառ(դադարեցնելՊորտ)
	ՊորտԳրելբառ(դադարեցնելՊորտ, 0)
	return 10
}

var count uint16 = 0

func (ինքնուրույն *Tamdam79c973) HandleԸնդհատել(esp uint32) uint32 {

	ՊորտԳրելբառ(registeraddressՊորտ, 0)
	temporary := uint32(ՊորտԸնթերցումբառ(registerdataՊորտ))
	console_2.MՏպել(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Տպել(esp)
	console_2.MՏպել(([]byte)(":"))
	console_2.MUnsignedinteger32Տպել(temporary)
	console_2.MՏպել(([]byte)(":"))
	console_2.MUnsignedinteger16Տպել(count)
	count++
	console_2.MՏպել(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MՏպել(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MՏպել(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MՏպել(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MՏպել(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MՏպել(([]byte)("am79c973 data received"))
		ինքնուրույն.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MՏպել(([]byte)("am79c973 data sent"))
	}

	ՊորտԳրելբառ(registeraddressՊորտ, 0)
	ՊորտԳրելբառ(registerdataՊորտ, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MՏպել(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (ինքնուրույն *Tamdam79c973) ՈՒղարկել(dataՑուցիչ uintptr, չափս uint32) {
	var ոՒղարկելdescriptor uint16 = uint16(currentՈՒղարկելbuffer)
	currentՈՒղարկելbuffer = 0

	if չափս > 1518 {
		չափս = 1518
	}

	var աղբյուր_2 [4096]byte = *(*([4096]byte))(Pointer(dataՑուցիչ))
	var destination_2 uint32 = ոՒղարկելbufferՆկարագրություն[ոՒղարկելdescriptor].address_2 + չափս - 1

	for i := 0; i < int(չափս); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = աղբյուր_2[int(չափս)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataՑուցիչ))
	console_2.MՏպելxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalՏպել(data[i])
		console_2.MՏպել(([]byte)(":"))
	}
	console_2.MՏպել(([]byte)("\n"))

	ոՒղարկելbufferՆկարագրություն[ոՒղարկելdescriptor].հասանելի = 0
	ոՒղարկելbufferՆկարագրություն[ոՒղարկելdescriptor].դրոշներ2 = 0
	ոՒղարկելbufferՆկարագրություն[ոՒղարկելdescriptor].դրոշներ = 0x8300F000 | uint32((-չափս)&0xFFF)

	ՊորտԳրելբառ(registeraddressՊորտ, 0)
	ՊորտԳրելբառ(registerdataՊորտ, 0x48)

}
func (ինքնուրույն *Tamdam79c973) Receive() {
	console_2.MՏպել(([]byte)(":"))
	console_2.MUnsignedinteger32Տպել(uint32(uintptr(Pointer(&ոՒղարկելbuffer))))
	console_2.MՏպել(([]byte)(":"))
	console_2.MHexadecimalՏպել(ոՒղարկելbuffer[0][0])
	console_2.MHexadecimalՏպել(ոՒղարկելbuffer[0][1])
	console_2.MՏպել(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferՆկարագրություն[currentrecvbuffer].դրոշներ & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferՆկարագրություն[currentrecvbuffer].դրոշներ&0x40000000 != 0) && ((recvbufferՆկարագրություն[currentrecvbuffer].դրոշներ & 0x03000000) == 0x03000000) {
			var չափս uint32 = recvbufferՆկարագրություն[currentrecvbuffer].դրոշներ & 0xFFF
			if չափս > 64 {
				չափս -= 4
			}

			console_2.MՏպել([]byte(" size : ["))
			console_2.MUnsignedinteger32Տպել(չափս)
			console_2.MՏպել([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferՆկարագրություն[currentrecvbuffer].address_2)))
			var ցուցիչ uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Միացնելrawdatareceive(ցուցիչ, int(չափս)) {

					console_2.MՏպելxy(([]byte)("self.Send"), 0, 22)

					ինքնուրույն.ՈՒղարկել(ցուցիչ, չափս)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalՏպել(buffer_2[i])
				console_2.MՏպել([]byte(":"))
			}

		}
		recvbufferՆկարագրություն[currentrecvbuffer].դրոշներ2 = 0
		recvbufferՆկարագրություն[currentrecvbuffer].դրոշներ = 0x8000F7FF
	}
}
func (ինքնուրույն *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	ինքնուրույն.handler = handler
}
func (ինքնուրույն *Tamdam79c973) Getmacaddress() uint64 {

	return initԱրգելափակել.physicaladdress
}
func (ինքնուրույն *Tamdam79c973) Setipaddress(ip uint64) {
	initԱրգելափակել.logicaladdress = ip
}
func (ինքնուրույն *Tamdam79c973) Getipaddress() uint64 {
	return initԱրգելափակել.logicaladdress
}
