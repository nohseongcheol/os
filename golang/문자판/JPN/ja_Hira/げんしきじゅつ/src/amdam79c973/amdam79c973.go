/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "わりこみ"
import . "こんそーる"
import . "ぽーと"
import . "pci"

var ねっとわーくかーどげーむこんそーる Tこんそーる = Tこんそーる{}

type TInitializationぶろっく struct {
	もーど			uint16
	numberそうしんbuffer		uint8
	numberrecvbuffer	uint8

	ぶつりaddress	uint64

	ろんりえんざんaddress		uint64
	recvbufferせつめいaddress	uintptr
	そうしんbufferせつめいaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	ふらぐ		uint32
	ふらぐ2		uint32
	しようかのう		uint32
}

type IRawでーたhandler interface {
	Oときrawでーたreceive(でーたぽいんた uintptr, さいず int) bool
	Sそうしん(でーたぽいんた uintptr, さいず uint32)
}

var rawでーたbackend Tamdam79c973

type TRawでーたhandler struct {
}

func (self *TRawでーたhandler) Sありbackend(backend Tamdam79c973) {

	rawでーたbackend = backend
}
func (self *TRawでーたhandler) Getbackend() Tamdam79c973 {
	return rawでーたbackend
}
func (self *TRawでーたhandler) Oときrawでーたreceive(でーたぽいんた uintptr, さいず int) bool {
	ねっとわーくかーどげーむこんそーる.Mいんさつxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawでーたhandler) Sそうしん(でーたぽいんた uintptr, さいず uint32) {
	ねっとわーくかーどげーむこんそーる.Mいんさつxy(([]byte)("TRawDataSend"), 10, 10)
	rawでーたbackend.Sそうしん(でーたぽいんた, さいず)
}

var Macaddress0ぽーと uint16
var Macaddress2ぽーと uint16
var Macaddress4ぽーと uint16
var れじすたでーたぽーと uint16
var れじすたaddressぽーと uint16
var りせっとぽーと uint16
var busせいぎょれじすたでーたぽーと uint16

var initぶろっく TInitializationぶろっく

var そうしんbufferせつめい [8]TBufferdescriptor
var そうしんbufferせつめいめもり [2048 + 15]byte
var そうしんbuffer [2*1024 + 15][8]uint8
var げんざいのにちじそうしんbuffer uint8

var recvbufferせつめい [8]TBufferdescriptor
var recvbufferせつめいめもり [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var げんざいのにちじrecvbuffer uint8
var funcあたい func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	Tわりこみhandler
	でばいすdescriptor	TPeripheralcomponentinterconnectでばいすdescriptor
	わりこみ		*Tわりこみかんりしゃ
	handler		*TRawでーたhandler
}

var こんそーる_2 Tこんそーる = Tこんそーる{}
var irawでーたhandler IRawでーたhandler

func (self *Tamdam79c973) Initどらいばー(わりこみ *Tわりこみかんりしゃ, でばいすdescriptor TPeripheralcomponentinterconnectでばいすdescriptor, handler IRawでーたhandler) {

	self.でばいすdescriptor = でばいすdescriptor

	funcあたい = (*Tamdam79c973).Hとってわりこみ
	var address uintptr
	address = uintptr(Pointer(&funcあたい))

	self.Init(uint8(0x20+でばいすdescriptor.Iわりこみ), uintptr(Pointer(わりこみ)), address)

	Macaddress0ぽーと = uint16(でばいすdescriptor.Pぽーとbase)
	Macaddress2ぽーと = uint16(でばいすdescriptor.Pぽーとbase) + 0x02
	Macaddress4ぽーと = uint16(でばいすdescriptor.Pぽーとbase) + 0x04
	れじすたでーたぽーと = uint16(でばいすdescriptor.Pぽーとbase) + 0x10
	れじすたaddressぽーと = uint16(でばいすdescriptor.Pぽーとbase) + 0x12
	りせっとぽーと = uint16(でばいすdescriptor.Pぽーとbase) + 0x14
	busせいぎょれじすたでーたぽーと = uint16(でばいすdescriptor.Pぽーとbase) + 0x16

	irawでーたhandler = &TRawでーたhandler{}
	if handler != nil {
		irawでーたhandler = handler
	}

	げんざいのにちじそうしんbuffer = 0
	げんざいのにちじrecvbuffer = 0

	var Mac0 uint64 = uint64(Pぽーとよみこみご(Macaddress0ぽーと) % 256)
	var Mac1 uint64 = uint64(Pぽーとよみこみご(Macaddress0ぽーと) / 256)
	var Mac2 uint64 = uint64(Pぽーとよみこみご(Macaddress2ぽーと) % 256)
	var Mac3 uint64 = uint64(Pぽーとよみこみご(Macaddress2ぽーと) / 256)
	var Mac4 uint64 = uint64(Pぽーとよみこみご(Macaddress4ぽーと) % 256)
	var Mac5 uint64 = uint64(Pぽーとよみこみご(Macaddress4ぽーと) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	こんそーる_2.Mいんさつxy(([]byte)("[interrupt num : "), 0, 13)
	こんそーる_2.MHexadecimalいんさつ(uint8(でばいすdescriptor.Iわりこみ))
	こんそーる_2.Mいんさつ(([]byte)("]"))
	こんそーる_2.Mいんさつ(([]byte)("[mac address : "))
	こんそーる_2.MUnsignedinteger16いんさつ(uint16(macaddress >> 32))
	こんそーる_2.MUnsignedinteger32いんさつ(uint32(macaddress & 0x00000000FFFFFFFF))
	こんそーる_2.Mいんさつ(([]byte)("]"))

	Pぽーとかきこみご(れじすたaddressぽーと, 20)
	Pぽーとかきこみご(busせいぎょれじすたでーたぽーと, 0x102)

	Pぽーとかきこみご(れじすたaddressぽーと, 0)
	Pぽーとかきこみご(れじすたでーたぽーと, 0x04)

	initぶろっく.もーど = 0x0000
	initぶろっく.numberそうしんbuffer = 3
	initぶろっく.numberrecvbuffer = 3

	initぶろっく.ぶつりaddress = Mac

	initぶろっく.ろんりえんざんaddress = 0

	そうしんbufferせつめい = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&そうしんbufferせつめいめもり)) + 15) & ^(uintptr)(0xF)))
	initぶろっく.そうしんbufferせつめいaddress = uintptr(Pointer(&そうしんbufferせつめい))
	recvbufferせつめい = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferせつめいめもり)) + 15) & ^(uintptr)(0xF)))
	initぶろっく.recvbufferせつめいaddress = uintptr(Pointer(&recvbufferせつめい))

	for i := 0; i < 8; i++ {
		そうしんbufferせつめい[i].address_2 = uint32((uintptr(Pointer(&そうしんbuffer[i])) + 15) & ^(uintptr(0xF)))
		そうしんbufferせつめい[i].ふらぐ = 0x7FF | 0xF000
		そうしんbufferせつめい[i].ふらぐ2 = 0
		そうしんbufferせつめい[i].しようかのう = 0

		recvbufferせつめい[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferせつめい[i].ふらぐ = 0xF7FF | 0x80000000

	}

	Pぽーとかきこみご(れじすたaddressぽーと, 1)
	Pぽーとかきこみご(れじすたでーたぽーと, uint16(uintptr(Pointer(&initぶろっく))&0xFFFF))

	Pぽーとかきこみご(れじすたaddressぽーと, 2)
	Pぽーとかきこみご(れじすたでーたぽーと, uint16((uintptr(Pointer(&initぶろっく))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aゆうこうにする() {
	Pぽーとかきこみご(れじすたaddressぽーと, 0)
	Pぽーとかきこみご(れじすたでーたぽーと, 0x41)

	Pぽーとかきこみご(れじすたaddressぽーと, 4)
	temporary := Pぽーとよみこみご(れじすたでーたぽーと)
	Pぽーとかきこみご(れじすたaddressぽーと, 4)
	Pぽーとかきこみご(れじすたでーたぽーと, temporary|0xC00)

	Pぽーとかきこみご(れじすたaddressぽーと, 0)
	Pぽーとかきこみご(れじすたでーたぽーと, 0x42)

}
func (self *Tamdam79c973) Rりせっと() int {
	Pぽーとよみこみご(りせっとぽーと)
	Pぽーとかきこみご(りせっとぽーと, 0)
	return 10
}

var かうんと uint16 = 0

func (self *Tamdam79c973) Hとってわりこみ(esp uint32) uint32 {

	Pぽーとかきこみご(れじすたaddressぽーと, 0)
	temporary := uint32(Pぽーとよみこみご(れじすたでーたぽーと))
	こんそーる_2.Mいんさつ(([]byte)("interrupt("))
	こんそーる_2.MUnsignedinteger32いんさつ(esp)
	こんそーる_2.Mいんさつ(([]byte)(":"))
	こんそーる_2.MUnsignedinteger32いんさつ(temporary)
	こんそーる_2.Mいんさつ(([]byte)(":"))
	こんそーる_2.MUnsignedinteger16いんさつ(かうんと)
	かうんと++
	こんそーる_2.Mいんさつ(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		こんそーる_2.Mいんさつ(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		こんそーる_2.Mいんさつ(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		こんそーる_2.Mいんさつ(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		こんそーる_2.Mいんさつ(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		こんそーる_2.Mいんさつ(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		こんそーる_2.Mいんさつ(([]byte)("am79c973 data sent"))
	}

	Pぽーとかきこみご(れじすたaddressぽーと, 0)
	Pぽーとかきこみご(れじすたでーたぽーと, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		こんそーる_2.Mいんさつ(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Sそうしん(でーたぽいんた uintptr, さいず uint32) {
	var そうしんdescriptor uint16 = uint16(げんざいのにちじそうしんbuffer)
	げんざいのにちじそうしんbuffer = 0

	if さいず > 1518 {
		さいず = 1518
	}

	var てんそうもと_2 [4096]byte = *(*([4096]byte))(Pointer(でーたぽいんた))
	var てんそうさき_2 uint32 = そうしんbufferせつめい[そうしんdescriptor].address_2 + さいず - 1

	for i := 0; i < int(さいず); i++ {

		*(*byte)(Pointer(uintptr(てんそうさき_2))) = てんそうもと_2[int(さいず)-i-1]

		てんそうさき_2--
	}

	var でーた [4096]byte = *(*([4096]byte))(Pointer(でーたぽいんた))
	こんそーる_2.Mいんさつxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		こんそーる_2.MHexadecimalいんさつ(でーた[i])
		こんそーる_2.Mいんさつ(([]byte)(":"))
	}
	こんそーる_2.Mいんさつ(([]byte)("\n"))

	そうしんbufferせつめい[そうしんdescriptor].しようかのう = 0
	そうしんbufferせつめい[そうしんdescriptor].ふらぐ2 = 0
	そうしんbufferせつめい[そうしんdescriptor].ふらぐ = 0x8300F000 | uint32((-さいず)&0xFFF)

	Pぽーとかきこみご(れじすたaddressぽーと, 0)
	Pぽーとかきこみご(れじすたでーたぽーと, 0x48)

}
func (self *Tamdam79c973) Receive() {
	こんそーる_2.Mいんさつ(([]byte)(":"))
	こんそーる_2.MUnsignedinteger32いんさつ(uint32(uintptr(Pointer(&そうしんbuffer))))
	こんそーる_2.Mいんさつ(([]byte)(":"))
	こんそーる_2.MHexadecimalいんさつ(そうしんbuffer[0][0])
	こんそーる_2.MHexadecimalいんさつ(そうしんbuffer[0][1])
	こんそーる_2.Mいんさつ(([]byte)(":"))
	げんざいのにちじrecvbuffer = 0

	for ; (recvbufferせつめい[げんざいのにちじrecvbuffer].ふらぐ & 0x80000000) == 0; げんざいのにちじrecvbuffer = (げんざいのにちじrecvbuffer + 1) % 8 {

		if !(recvbufferせつめい[げんざいのにちじrecvbuffer].ふらぐ&0x40000000 != 0) && ((recvbufferせつめい[げんざいのにちじrecvbuffer].ふらぐ & 0x03000000) == 0x03000000) {
			var さいず uint32 = recvbufferせつめい[げんざいのにちじrecvbuffer].ふらぐ & 0xFFF
			if さいず > 64 {
				さいず -= 4
			}

			こんそーる_2.Mいんさつ([]byte(" size : ["))
			こんそーる_2.MUnsignedinteger32いんさつ(さいず)
			こんそーる_2.Mいんさつ([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferせつめい[げんざいのにちじrecvbuffer].address_2)))
			var ばんちさんしょう uintptr = uintptr(Pointer(&buffer_2))
			if irawでーたhandler != nil {
				if irawでーたhandler.Oときrawでーたreceive(ばんちさんしょう, int(さいず)) {

					こんそーる_2.Mいんさつxy(([]byte)("self.Send"), 0, 22)

					self.Sそうしん(ばんちさんしょう, さいず)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				こんそーる_2.MHexadecimalいんさつ(buffer_2[i])
				こんそーる_2.Mいんさつ([]byte(":"))
			}

		}
		recvbufferせつめい[げんざいのにちじrecvbuffer].ふらぐ2 = 0
		recvbufferせつめい[げんざいのにちじrecvbuffer].ふらぐ = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sありhandler(handler *TRawでーたhandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initぶろっく.ぶつりaddress
}
func (self *Tamdam79c973) Sありipaddress(ip uint64) {
	initぶろっく.ろんりえんざんaddress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initぶろっく.ろんりえんざんaddress
}
