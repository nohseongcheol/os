/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "ማቋረጫ"
import . "console"
import . "port"
import . "pci"

var ኔትዎርክcardconsole TConsole = TConsole{}

type TInitializationመከልከያ struct {
	ዘዴ		uint16
	ቁጥርsendbuffer	uint8
	ቁጥርrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferመግለጫaddress	uintptr
	sendbufferመግለጫaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	ባንዲራዎች		uint32
	ባንዲራዎች2		uint32
	ዝግጁ		uint32
}

type IRawdatahandler interface {
	Oማብሪያrawdatareceive(dataጠቋሚ uintptr, መጠን int) bool
	Send(dataጠቋሚ uintptr, መጠን uint32)
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
func (self *TRawdatahandler) Oማብሪያrawdatareceive(dataጠቋሚ uintptr, መጠን int) bool {
	ኔትዎርክcardconsole.Mማተሚያxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Send(dataጠቋሚ uintptr, መጠን uint32) {
	ኔትዎርክcardconsole.Mማተሚያxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(dataጠቋሚ, መጠን)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var እንደነበረመመለሻport uint16
var buscontrolregisterdataport uint16

var initመከልከያ TInitializationመከልከያ

var sendbufferመግለጫ [8]TBufferdescriptor
var sendbufferመግለጫማስታወሻ [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var currentsendbuffer uint8

var recvbufferመግለጫ [8]TBufferdescriptor
var recvbufferመግለጫማስታወሻ [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcዋጋ func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	Tማቋረጫhandler
	ዲቫይስdescriptor	TPeripheralcomponentinterconnectዲቫይስdescriptor
	ማቋረጫ		*Tማቋረጫmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(ማቋረጫ *Tማቋረጫmanager, ዲቫይስdescriptor TPeripheralcomponentinterconnectዲቫይስdescriptor, handler IRawdatahandler) {

	self.ዲቫይስdescriptor = ዲቫይስdescriptor

	funcዋጋ = (*Tamdam79c973).Handleማቋረጫ
	var address uintptr
	address = uintptr(Pointer(&funcዋጋ))

	self.Init(uint8(0x20+ዲቫይስdescriptor.Iማቋረጫ), uintptr(Pointer(ማቋረጫ)), address)

	Macaddress0port = uint16(ዲቫይስdescriptor.Portbase)
	Macaddress2port = uint16(ዲቫይስdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(ዲቫይስdescriptor.Portbase) + 0x04
	registerdataport = uint16(ዲቫይስdescriptor.Portbase) + 0x10
	registeraddressport = uint16(ዲቫይስdescriptor.Portbase) + 0x12
	እንደነበረመመለሻport = uint16(ዲቫይስdescriptor.Portbase) + 0x14
	buscontrolregisterdataport = uint16(ዲቫይስdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentsendbuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(Portማንበቢያቃላት(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(Portማንበቢያቃላት(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(Portማንበቢያቃላት(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(Portማንበቢያቃላት(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(Portማንበቢያቃላት(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(Portማንበቢያቃላት(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.Mማተሚያxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalማተሚያ(uint8(ዲቫይስdescriptor.Iማቋረጫ))
	console_2.Mማተሚያ(([]byte)("]"))
	console_2.Mማተሚያ(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16ማተሚያ(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32ማተሚያ(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.Mማተሚያ(([]byte)("]"))

	Portመጻፊያቃላት(registeraddressport, 20)
	Portመጻፊያቃላት(buscontrolregisterdataport, 0x102)

	Portመጻፊያቃላት(registeraddressport, 0)
	Portመጻፊያቃላት(registerdataport, 0x04)

	initመከልከያ.ዘዴ = 0x0000
	initመከልከያ.ቁጥርsendbuffer = 3
	initመከልከያ.ቁጥርrecvbuffer = 3

	initመከልከያ.physicaladdress = Mac

	initመከልከያ.logicaladdress = 0

	sendbufferመግለጫ = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferመግለጫማስታወሻ)) + 15) & ^(uintptr)(0xF)))
	initመከልከያ.sendbufferመግለጫaddress = uintptr(Pointer(&sendbufferመግለጫ))
	recvbufferመግለጫ = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferመግለጫማስታወሻ)) + 15) & ^(uintptr)(0xF)))
	initመከልከያ.recvbufferመግለጫaddress = uintptr(Pointer(&recvbufferመግለጫ))

	for i := 0; i < 8; i++ {
		sendbufferመግለጫ[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferመግለጫ[i].ባንዲራዎች = 0x7FF | 0xF000
		sendbufferመግለጫ[i].ባንዲራዎች2 = 0
		sendbufferመግለጫ[i].ዝግጁ = 0

		recvbufferመግለጫ[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferመግለጫ[i].ባንዲራዎች = 0xF7FF | 0x80000000

	}

	Portመጻፊያቃላት(registeraddressport, 1)
	Portመጻፊያቃላት(registerdataport, uint16(uintptr(Pointer(&initመከልከያ))&0xFFFF))

	Portመጻፊያቃላት(registeraddressport, 2)
	Portመጻፊያቃላት(registerdataport, uint16((uintptr(Pointer(&initመከልከያ))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aማስጀመሪያ() {
	Portመጻፊያቃላት(registeraddressport, 0)
	Portመጻፊያቃላት(registerdataport, 0x41)

	Portመጻፊያቃላት(registeraddressport, 4)
	temporary := Portማንበቢያቃላት(registerdataport)
	Portመጻፊያቃላት(registeraddressport, 4)
	Portመጻፊያቃላት(registerdataport, temporary|0xC00)

	Portመጻፊያቃላት(registeraddressport, 0)
	Portመጻፊያቃላት(registerdataport, 0x42)

}
func (self *Tamdam79c973) Rእንደነበረመመለሻ() int {
	Portማንበቢያቃላት(እንደነበረመመለሻport)
	Portመጻፊያቃላት(እንደነበረመመለሻport, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleማቋረጫ(esp uint32) uint32 {

	Portመጻፊያቃላት(registeraddressport, 0)
	temporary := uint32(Portማንበቢያቃላት(registerdataport))
	console_2.Mማተሚያ(([]byte)("interrupt("))
	console_2.MUnsignedinteger32ማተሚያ(esp)
	console_2.Mማተሚያ(([]byte)(":"))
	console_2.MUnsignedinteger32ማተሚያ(temporary)
	console_2.Mማተሚያ(([]byte)(":"))
	console_2.MUnsignedinteger16ማተሚያ(count)
	count++
	console_2.Mማተሚያ(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.Mማተሚያ(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.Mማተሚያ(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.Mማተሚያ(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.Mማተሚያ(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.Mማተሚያ(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.Mማተሚያ(([]byte)("am79c973 data sent"))
	}

	Portመጻፊያቃላት(registeraddressport, 0)
	Portመጻፊያቃላት(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.Mማተሚያ(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Send(dataጠቋሚ uintptr, መጠን uint32) {
	var senddescriptor uint16 = uint16(currentsendbuffer)
	currentsendbuffer = 0

	if መጠን > 1518 {
		መጠን = 1518
	}

	var ምንጩ_2 [4096]byte = *(*([4096]byte))(Pointer(dataጠቋሚ))
	var destination_2 uint32 = sendbufferመግለጫ[senddescriptor].address_2 + መጠን - 1

	for i := 0; i < int(መጠን); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = ምንጩ_2[int(መጠን)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataጠቋሚ))
	console_2.Mማተሚያxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalማተሚያ(data[i])
		console_2.Mማተሚያ(([]byte)(":"))
	}
	console_2.Mማተሚያ(([]byte)("\n"))

	sendbufferመግለጫ[senddescriptor].ዝግጁ = 0
	sendbufferመግለጫ[senddescriptor].ባንዲራዎች2 = 0
	sendbufferመግለጫ[senddescriptor].ባንዲራዎች = 0x8300F000 | uint32((-መጠን)&0xFFF)

	Portመጻፊያቃላት(registeraddressport, 0)
	Portመጻፊያቃላት(registerdataport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.Mማተሚያ(([]byte)(":"))
	console_2.MUnsignedinteger32ማተሚያ(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.Mማተሚያ(([]byte)(":"))
	console_2.MHexadecimalማተሚያ(sendbuffer[0][0])
	console_2.MHexadecimalማተሚያ(sendbuffer[0][1])
	console_2.Mማተሚያ(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferመግለጫ[currentrecvbuffer].ባንዲራዎች & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferመግለጫ[currentrecvbuffer].ባንዲራዎች&0x40000000 != 0) && ((recvbufferመግለጫ[currentrecvbuffer].ባንዲራዎች & 0x03000000) == 0x03000000) {
			var መጠን uint32 = recvbufferመግለጫ[currentrecvbuffer].ባንዲራዎች & 0xFFF
			if መጠን > 64 {
				መጠን -= 4
			}

			console_2.Mማተሚያ([]byte(" size : ["))
			console_2.MUnsignedinteger32ማተሚያ(መጠን)
			console_2.Mማተሚያ([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferመግለጫ[currentrecvbuffer].address_2)))
			var ጠቋሚ uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Oማብሪያrawdatareceive(ጠቋሚ, int(መጠን)) {

					console_2.Mማተሚያxy(([]byte)("self.Send"), 0, 22)

					self.Send(ጠቋሚ, መጠን)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalማተሚያ(buffer_2[i])
				console_2.Mማተሚያ([]byte(":"))
			}

		}
		recvbufferመግለጫ[currentrecvbuffer].ባንዲራዎች2 = 0
		recvbufferመግለጫ[currentrecvbuffer].ባንዲራዎች = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sethandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initመከልከያ.physicaladdress
}
func (self *Tamdam79c973) Setipaddress(ip uint64) {
	initመከልከያ.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initመከልከያ.logicaladdress
}
