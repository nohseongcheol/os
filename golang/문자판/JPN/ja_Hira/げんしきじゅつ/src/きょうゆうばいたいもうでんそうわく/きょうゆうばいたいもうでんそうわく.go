/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package きょうゆうばいたいもうでんそうわく

import . "こんそーる"

import . "amdam79c973"
import . "unsafe"
import . "はんよう"

var いーさねっとこんそーる Tこんそーる = Tこんそーる{}

type Tいーさねっとふれーむへっだbuffer struct {
	てんそうさきmacbe	[6]byte
	てんそうもとmacbe	[6]byte
	いーさねっとかたbe	[2]byte
}

var ふれーむへっださいず int = 14

type Tきょうゆうばいたいあみでんそうわくせんとうぶ struct {
	てんそうさきmacbe	uint64
	てんそうもとmacbe	uint64
	いーさねっとかたbe	uint16
}

func (self *Tきょうゆうばいたいあみでんそうわくせんとうぶ) Init(buffer_2 Tいーさねっとふれーむへっだbuffer) {
	self.てんそうさきmacbe = (Aはいれつtounsignedinteger48(buffer_2.てんそうさきmacbe))
	self.てんそうもとmacbe = (Aはいれつtounsignedinteger48(buffer_2.てんそうもとmacbe))
	self.いーさねっとかたbe = (Aはいれつtounsignedinteger16(buffer_2.いーさねっとかたbe))

}
func (self *Tきょうゆうばいたいあみでんそうわくせんとうぶ) Sありbuffer(buffer_2 *Tいーさねっとふれーむへっだbuffer) {
	buffer_2.てんそうさきmacbe = Unsignedinteger48toはいれつ(Unsignedinteger48r(self.てんそうさきmacbe))
	buffer_2.てんそうもとmacbe = Unsignedinteger48toはいれつ(Unsignedinteger48r(self.てんそうもとmacbe))
	buffer_2.いーさねっとかたbe = Unsignedinteger16toはいれつ(Unsignedinteger16r(self.いーさねっとかたbe))
}

type Iいーさねっとふれーむhandler interface {
	Init(backend Tきょうゆうばいたいあみでんそうわくていきょううつわ)
	Sありhandler(handler Iいーさねっとふれーむhandler, いーさねっとかた uint16)
	Oいーさねっとふれーむreceivewhen(でーたぽいんた uintptr, さいず int) bool
	Sそうしん(てんそうさきmacbe uint64, でーたぽいんた uintptr, さいず uint32)
	Sふれーむそうしん(てんそうさきmacbe uint64, いーさねっとかたbe uint16, でーたぽいんた uintptr, さいず uint32)
	Providerget() Tきょうゆうばいたいあみでんそうわくていきょううつわ
	Getmacaddress() uint64
	Getipaddress() uint64
}

type Tいーさねっとふれーむhandler struct {
}

var ふれーむ Tきょうゆうばいたいあみでんそうわくせんとうぶ
var Backend Tきょうゆうばいたいあみでんそうわくていきょううつわ
var handler_2 [65535]Iいーさねっとふれーむhandler
var efhandler *Tいーさねっとふれーむhandler = nil

func (self *Tいーさねっとふれーむhandler) Init(backend Tきょうゆうばいたいあみでんそうわくていきょううつわ) {
	Backend = backend
}

func (self *Tいーさねっとふれーむhandler) Sありhandler(handler Iいーさねっとふれーむhandler, pいーさねっとかた uint16) {
	handler_2[pいーさねっとかた] = handler
}
func (self *Tいーさねっとふれーむhandler) Sありbackend(backend Tきょうゆうばいたいあみでんそうわくていきょううつわ) {
	Backend = backend
}
func (self *Tいーさねっとふれーむhandler) Getbackend() Tきょうゆうばいたいあみでんそうわくていきょううつわ {
	return Backend
}
func (self *Tいーさねっとふれーむhandler) Oいーさねっとふれーむreceivewhen(でーたぽいんた uintptr, さいず int) bool {
	いーさねっとこんそーる.Mいんさつ(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *Tいーさねっとふれーむhandler) Sそうしん(てんそうさきmacbe uint64, でーたぽいんた uintptr, さいず uint32) {
	Backend.Sふれーむそうしん(てんそうさきmacbe, ふれーむ.いーさねっとかたbe, でーたぽいんた, さいず)
}
func (self *Tいーさねっとふれーむhandler) Sふれーむそうしん(てんそうさきmacbe uint64, いーさねっとかたbe uint16, でーたぽいんた uintptr, さいず uint32) {
	Backend.Sふれーむそうしん(てんそうさきmacbe, いーさねっとかたbe, でーたぽいんた, さいず)
}
func (self *Tいーさねっとふれーむhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *Tいーさねっとふれーむhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *Tいーさねっとふれーむhandler) Providerget() Tきょうゆうばいたいあみでんそうわくていきょううつわ {
	return Backend
}

type Tいーさねっとふれーむrawでーたhandler struct {
	TRawでーたhandler
}

var provider Tきょうゆうばいたいあみでんそうわくていきょううつわ

func (self *Tいーさねっとふれーむrawでーたhandler) Init(pprovider Tきょうゆうばいたいあみでんそうわくていきょううつわ, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *Tいーさねっとふれーむrawでーたhandler) Oときrawでーたreceive(でーたぽいんた uintptr, さいず int) bool {
	return provider.Oときrawでーたreceive(でーたぽいんた, さいず)
}
func (self *Tいーさねっとふれーむrawでーたhandler) Sそうしん(でーたぽいんた uintptr, さいず uint32) {
	provider.Sそうしん(でーたぽいんた, さいず)
}
func (self *Tいーさねっとふれーむrawでーたhandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *Tいーさねっとふれーむrawでーたhandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *Tいーさねっとふれーむrawでーたhandler) Providerget() Tきょうゆうばいたいあみでんそうわくていきょううつわ {
	return provider
}

type Tきょうゆうばいたいあみでんそうわくていきょううつわ struct {
	ねっとわーくかーどげーむ	Tamdam79c973
	handler_2	[65565]Iいーさねっとふれーむhandler
}

func (self *Tきょうゆうばいたいあみでんそうわくていきょううつわ) Init(backend Tamdam79c973) {

	self.ねっとわーくかーどげーむ = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var かうんと uint16 = 0

func (self *Tきょうゆうばいたいあみでんそうわくていきょううつわ) Oときrawでーたreceive(でーたぽいんた uintptr, さいず int) bool {

	var buffer_2 *Tいーさねっとふれーむへっだbuffer = (*Tいーさねっとふれーむへっだbuffer)(Pointer(でーたぽいんた))
	var ふれーむ Tきょうゆうばいたいあみでんそうわくせんとうぶ = Tきょうゆうばいたいあみでんそうわくせんとうぶ{}
	ふれーむ.Init(*buffer_2)
	var reply bool = false

	if ふれーむ.てんそうさきmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ふれーむ.てんそうさきmacbe) == self.Getmacaddress() {
		if handler_2[ふれーむ.いーさねっとかたbe] != nil {
			いーさねっとこんそーる.Mいんさつ(([]byte)("provider\n"))

			var ばんちさんしょう uintptr = uintptr(Pointer(でーたぽいんた)) + uintptr(ふれーむへっださいず)
			reply = handler_2[ふれーむ.いーさねっとかたbe].Oいーさねっとふれーむreceivewhen(ばんちさんしょう, さいず-ふれーむへっださいず)

		}
	}

	if reply {
		ふれーむ.てんそうさきmacbe = ふれーむ.てんそうもとmacbe
		ふれーむ.てんそうもとmacbe = Unsignedinteger48r(self.Getmacaddress())
		ふれーむ.Sありbuffer(buffer_2)

	}

	いーさねっとこんそーる.Mいんさつxy(([]byte)("spro["), 0, 1)
	いーさねっとこんそーる.MUnsignedinteger64いんさつ(ふれーむ.てんそうもとmacbe)
	いーさねっとこんそーる.Mいんさつ(([]byte)(":"))
	いーさねっとこんそーる.MUnsignedinteger64いんさつ(ふれーむ.てんそうさきmacbe)
	いーさねっとこんそーる.Mいんさつ(([]byte)(":]["))
	いーさねっとこんそーる.MUnsignedinteger64いんさつ(self.Getmacaddress())
	いーさねっとこんそーる.Mいんさつ(([]byte)(":"))
	いーさねっとこんそーる.MUnsignedinteger16いんさつ(ふれーむ.いーさねっとかたbe)
	いーさねっとこんそーる.Mいんさつ(([]byte)("]"))

	return reply

}
func (self *Tきょうゆうばいたいあみでんそうわくていきょううつわ) Sそうしん(でーたぽいんた uintptr, さいず uint32) {
	self.ねっとわーくかーどげーむ.Sそうしん(でーたぽいんた, さいず)
}
func (self *Tきょうゆうばいたいあみでんそうわくていきょううつわ) Sふれーむそうしん(てんそうさきmacbe uint64, いーさねっとかたbe uint16, でーたぽいんた uintptr, さいず uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *Tいーさねっとふれーむへっだbuffer = (*Tいーさねっとふれーむへっだbuffer)(Pointer(&buffer2_2))

	var ふれーむ Tきょうゆうばいたいあみでんそうわくせんとうぶ = Tきょうゆうばいたいあみでんそうわくせんとうぶ{}
	ふれーむ.Init(*buffer_2)

	ふれーむ.てんそうさきmacbe = Unsignedinteger48r(てんそうさきmacbe)
	ふれーむ.てんそうもとmacbe = Unsignedinteger48r(self.ねっとわーくかーどげーむ.Getmacaddress())
	ふれーむ.いーさねっとかたbe = Unsignedinteger16r(いーさねっとかたbe)

	ふれーむ.Sありbuffer(buffer_2)
	var てんそうもと_2 [4096]byte = *(*([4096]byte))(Pointer(でーたぽいんた))

	var i uint32 = 0
	for i = 0; i < さいず; i++ {
		buffer2_2[uint32(ふれーむへっださいず)+i] = てんそうもと_2[i]

	}

	var ばんちさんしょう uintptr = uintptr(Pointer(&buffer2_2))

	self.ねっとわーくかーどげーむ.Sそうしん(ばんちさんしょう, さいず+uint32(ふれーむへっださいず))

}
func (self *Tきょうゆうばいたいあみでんそうわくていきょううつわ) Getmacaddress() uint64 {
	return self.ねっとわーくかーどげーむ.Getmacaddress()
}
func (self *Tきょうゆうばいたいあみでんそうわくていきょううつわ) Getipaddress() uint64 {
	return self.ねっとわーくかーどげーむ.Getipaddress()
}
