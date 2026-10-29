/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "こんそーる"
import . "きょうゆうばいたいもうでんそうわく"
import . "はんよう"

var arpこんそーる Tこんそーる = Tこんそーる{}

type Arpめっせーじbuffer struct {
	はーどうぇあかた			[2]byte
	protocol		[2]byte
	はーどうぇあaddressさいず	byte
	protocoladdressさいず	byte
	こまんど			[2]byte

	てんそうもとmacaddress	[6]byte
	てんそうもとipaddress	[4]byte
	てんそうさきmacaddress	[6]byte
	てんそうさきipaddress	[4]byte
}

var arpmesgさいず uint32 = (64+92+64)/8 + 2

type Arpめっせーじ struct {
	はーどうぇあかた			uint16
	protocol		uint16
	はーどうぇあaddressさいず	uint8
	protocoladdressさいず	uint8
	こまんど			uint16

	てんそうもとmacaddress	uint64
	てんそうもとipaddress	uint32
	てんそうさきmacaddress	uint64
	てんそうさきipaddress	uint32
}

func (self *Arpめっせーじ) Init(buffer_2 *Arpめっせーじbuffer) {

	self.はーどうぇあかた = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.はーどうぇあかた))
	self.protocol = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.protocol))
	self.はーどうぇあaddressさいず = byte(buffer_2.はーどうぇあaddressさいず)
	self.protocoladdressさいず = byte(buffer_2.protocoladdressさいず)
	self.こまんど = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.こまんど))

	self.てんそうもとmacaddress = Unsignedinteger48r(Aはいれつtounsignedinteger48(buffer_2.てんそうもとmacaddress))
	self.てんそうもとipaddress = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer_2.てんそうもとipaddress))
	self.てんそうさきmacaddress = Unsignedinteger48r(Aはいれつtounsignedinteger48(buffer_2.てんそうさきmacaddress))
	self.てんそうさきipaddress = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer_2.てんそうさきipaddress))
}
func (self *Arpめっせーじ) Sありbuffer(buffer_2 *Arpめっせーじbuffer) {
	buffer_2.はーどうぇあかた = Unsignedinteger16toはいれつ(self.はーどうぇあかた)
	buffer_2.protocol = Unsignedinteger16toはいれつ(self.protocol)
	buffer_2.はーどうぇあaddressさいず = uint8(self.はーどうぇあaddressさいず)
	buffer_2.protocoladdressさいず = uint8(self.protocoladdressさいず)

	buffer_2.こまんど = Unsignedinteger16toはいれつ(self.こまんど)
	buffer_2.てんそうもとmacaddress = Unsignedinteger48toはいれつ(self.てんそうもとmacaddress)
	buffer_2.てんそうもとipaddress = Unsignedinteger32toはいれつ(self.てんそうもとipaddress)
	buffer_2.てんそうさきmacaddress = Unsignedinteger48toはいれつ(self.てんそうさきmacaddress)
	buffer_2.てんそうさきipaddress = Unsignedinteger32toはいれつ(self.てんそうさきipaddress)
}

type Arpいーさねっとふれーむhandler struct {
	Tいーさねっとふれーむhandler
}

var arpprovider Arpprovider
var きょうゆうばいたいあみでんそうわくていきょううつわ Tきょうゆうばいたいあみでんそうわくていきょううつわ

func (self *Arpいーさねっとふれーむhandler) Oいーさねっとふれーむreceivewhen(でーたぽいんた uintptr, さいず int) bool {
	arpこんそーる.Mいんさつxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Oいーさねっとふれーむreceivewhen(でーたぽいんた, uint32(さいず))

}
func (self *Arpいーさねっとふれーむhandler) Sそうしん(てんそうさきmacbe uint64, でーたぽいんた uintptr, さいず uint32) {
	arpこんそーる.Mいんさつxy([]byte("arp send:"), 0, 24)
	var いーさねっとかたbe = Unsignedinteger16r(0x0806)
	self.Tいーさねっとふれーむhandler.Sふれーむそうしん(てんそうさきmacbe, いーさねっとかたbe, でーたぽいんた, さいず)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	Iいーさねっとふれーむhandler
}

var handler Iいーさねっとふれーむhandler

func (self *Arpprovider) Init(backend Tきょうゆうばいたいあみでんそうわくていきょううつわ, userhandler Iいーさねっとふれーむhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sありhandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Oいーさねっとふれーむreceivewhen(でーたぽいんた uintptr, さいず uint32) bool {

	if さいず < arpmesgさいず {
		return false
	}
	var arpbuffer *Arpめっせーじbuffer = (*Arpめっせーじbuffer)(Pointer(でーたぽいんた))
	var arp Arpめっせーじ = Arpめっせーじ{}
	arp.Init(arpbuffer)

	if arp.はーどうぇあかた == 0x0100 {

		if arp.protocol == 0x0008 && arp.はーどうぇあaddressさいず == 6 && arp.protocoladdressさいず == 4 && uint64(arp.てんそうさきipaddress) == handler.Getipaddress() {

			arpこんそーる.Mいんさつ([]byte("arp onetherframe"))
			arpこんそーる.MUnsignedinteger16いんさつ(arp.protocol)
			arpこんそーる.Mいんさつ([]byte(":"))
			arpこんそーる.MUnsignedinteger64いんさつ(uint64(arp.てんそうさきmacaddress))
			arpこんそーる.Mいんさつ([]byte(":"))
			arpこんそーる.MUnsignedinteger16いんさつ(arp.こまんど)
			arpこんそーる.Mいんさつ([]byte(":"))
			arpこんそーる.MUnsignedinteger64いんさつ(handler.Getmacaddress())

			switch arp.こまんど {
			case 0x0100:

				if self.Getmacからcache(arp.てんそうもとipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.てんそうもとipaddress
						self.Maccache[self.numbercacheentry] = arp.てんそうもとmacaddress
						self.numbercacheentry++
					}
				}
				arp.こまんど = 0x0200
				arp.てんそうさきipaddress = arp.てんそうもとipaddress
				arp.てんそうさきmacaddress = arp.てんそうもとmacaddress
				arp.てんそうもとipaddress = uint32(handler.Getipaddress())
				arp.てんそうもとmacaddress = handler.Getmacaddress()
				arp.Sありbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpこんそーる.Mいんさつ(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.てんそうもとipaddress
					self.Maccache[self.numbercacheentry] = arp.てんそうもとmacaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipねっとわーくばいとorder uint32) {

	var arp Arpめっせーじ = Arpめっせーじ{}
	arp.はーどうぇあかた = 0x0100
	arp.protocol = 0x0008
	arp.はーどうぇあaddressさいず = 6
	arp.protocoladdressさいず = 4
	arp.こまんど = 0x0200

	arp.てんそうもとipaddress = uint32(handler.Getipaddress())

	arp.てんそうさきmacaddress = self.Rかいけつ(Ipねっとわーくばいとorder)
	arp.てんそうさきipaddress = Ipねっとわーくばいとorder
	arpこんそーる.Mいんさつxy([]byte("broad mac"), 0, 15)

	arp.てんそうもとmacaddress = handler.Getmacaddress()

	var arpbuffer Arpめっせーじbuffer = Arpめっせーじbuffer{}
	arp.Sありbuffer(&arpbuffer)

	var ばんちさんしょう uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sそうしん(arp.てんそうさきmacaddress, ばんちさんしょう, arpmesgさいず)
}
func (self *Arpprovider) Requestmacaddress(Ipねっとわーくばいとorder uint32) {

	var arp Arpめっせーじ = Arpめっせーじ{}
	arp.はーどうぇあかた = 0x0100

	arp.protocol = 0x0008
	arp.はーどうぇあaddressさいず = 6
	arp.protocoladdressさいず = 4
	arp.こまんど = 0x0100

	arp.てんそうもとmacaddress = handler.Getmacaddress()
	arp.てんそうもとipaddress = uint32(handler.Getipaddress())

	arp.てんそうさきmacaddress = 0xFFFFFFFFFFFF
	arp.てんそうさきipaddress = Ipねっとわーくばいとorder

	var arpbuffer Arpめっせーじbuffer = Arpめっせーじbuffer{}
	arp.Sありbuffer(&arpbuffer)

	var ばんちさんしょう uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sそうしん(arp.てんそうさきmacaddress, ばんちさんしょう, arpmesgさいず)
}
func (self *Arpprovider) Tてすといんさつ(でーた *[]byte, さいず uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(でーた))
	arpこんそーる.Mいんさつxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpこんそーる.MHexadecimalいんさつ(buffer_2[i])
		arpこんそーる.Mいんさつ([]byte(":"))
	}
	arpこんそーる.Mいんさつ([]byte("]"))
}

func (self *Arpprovider) Getmacからcache(Ipねっとわーくばいとorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpこんそーる.Mいんさつ(([]byte)("["))
		arpこんそーる.MUnsignedinteger32いんさつ(self.Ipcache[i])
		arpこんそーる.Mいんさつ(([]byte)(":"))
		arpこんそーる.MUnsignedinteger32いんさつ(Ipねっとわーくばいとorder)
		arpこんそーる.Mいんさつ(([]byte)(":"))
		arpこんそーる.Mいんさつ(([]byte)(":"))
		arpこんそーる.MUnsignedinteger64いんさつ(self.Maccache[i])
		arpこんそーる.Mいんさつ(([]byte)("]\n"))

		if self.Ipcache[i] == Ipねっとわーくばいとorder {
			arpこんそーる.Mいんさつ([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Rかいけつ(Ipねっとわーくばいとorder uint32) uint64 {
	var せいせいさき uint64 = self.Getmacからcache(Ipねっとわーくばいとorder)
	if せいせいさき == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipねっとわーくばいとorder)
	}
	for i := 0; i < 128 && せいせいさき == 0xFFFFFFFFFFFF; i++ {
		せいせいさき = self.Getmacからcache(Ipねっとわーくばいとorder)

	}

	return せいせいさき
}
