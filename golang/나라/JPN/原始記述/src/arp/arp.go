/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "コンソール"
import . "共有媒体網伝送枠"
import . "汎用"

var arpコンソール Tコンソール = Tコンソール{}

type Arpメッセージbuffer struct {
	ハードウェア型			[2]byte
	protocol		[2]byte
	ハードウェアaddressサイズ	byte
	protocoladdressサイズ	byte
	コマンド			[2]byte

	転送元macaddress	[6]byte
	転送元ipaddress	[4]byte
	転送先macaddress	[6]byte
	転送先ipaddress	[4]byte
}

var arpmesgサイズ uint32 = (64+92+64)/8 + 2

type Arpメッセージ struct {
	ハードウェア型			uint16
	protocol		uint16
	ハードウェアaddressサイズ	uint8
	protocoladdressサイズ	uint8
	コマンド			uint16

	転送元macaddress	uint64
	転送元ipaddress	uint32
	転送先macaddress	uint64
	転送先ipaddress	uint32
}

func (self *Arpメッセージ) Init(buffer_2 *Arpメッセージbuffer) {

	self.ハードウェア型 = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.ハードウェア型))
	self.protocol = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.protocol))
	self.ハードウェアaddressサイズ = byte(buffer_2.ハードウェアaddressサイズ)
	self.protocoladdressサイズ = byte(buffer_2.protocoladdressサイズ)
	self.コマンド = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.コマンド))

	self.転送元macaddress = Unsignedinteger48r(A配列tounsignedinteger48(buffer_2.転送元macaddress))
	self.転送元ipaddress = Unsignedinteger32r(A配列tounsignedinteger32(buffer_2.転送元ipaddress))
	self.転送先macaddress = Unsignedinteger48r(A配列tounsignedinteger48(buffer_2.転送先macaddress))
	self.転送先ipaddress = Unsignedinteger32r(A配列tounsignedinteger32(buffer_2.転送先ipaddress))
}
func (self *Arpメッセージ) Sありbuffer(buffer_2 *Arpメッセージbuffer) {
	buffer_2.ハードウェア型 = Unsignedinteger16to配列(self.ハードウェア型)
	buffer_2.protocol = Unsignedinteger16to配列(self.protocol)
	buffer_2.ハードウェアaddressサイズ = uint8(self.ハードウェアaddressサイズ)
	buffer_2.protocoladdressサイズ = uint8(self.protocoladdressサイズ)

	buffer_2.コマンド = Unsignedinteger16to配列(self.コマンド)
	buffer_2.転送元macaddress = Unsignedinteger48to配列(self.転送元macaddress)
	buffer_2.転送元ipaddress = Unsignedinteger32to配列(self.転送元ipaddress)
	buffer_2.転送先macaddress = Unsignedinteger48to配列(self.転送先macaddress)
	buffer_2.転送先ipaddress = Unsignedinteger32to配列(self.転送先ipaddress)
}

type Arpイーサネットフレームhandler struct {
	Tイーサネットフレームhandler
}

var arpprovider Arpprovider
var 共有媒体網伝送枠提供器 T共有媒体網伝送枠提供器

func (self *Arpイーサネットフレームhandler) Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool {
	arpコンソール.M印刷xy([]byte("arp recv:"), 0, 23)
	return arpprovider.Oイーサネットフレームreceivewhen(データポインタ, uint32(サイズ))

}
func (self *Arpイーサネットフレームhandler) S送信(転送先macbe uint64, データポインタ uintptr, サイズ uint32) {
	arpコンソール.M印刷xy([]byte("arp send:"), 0, 24)
	var イーサネット型be = Unsignedinteger16r(0x0806)
	self.Tイーサネットフレームhandler.Sフレーム送信(転送先macbe, イーサネット型be, データポインタ, サイズ)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	Iイーサネットフレームhandler
}

var handler Iイーサネットフレームhandler

func (self *Arpprovider) Init(backend T共有媒体網伝送枠提供器, userhandler Iイーサネットフレームhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sありhandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ uint32) bool {

	if サイズ < arpmesgサイズ {
		return false
	}
	var arpbuffer *Arpメッセージbuffer = (*Arpメッセージbuffer)(Pointer(データポインタ))
	var arp Arpメッセージ = Arpメッセージ{}
	arp.Init(arpbuffer)

	if arp.ハードウェア型 == 0x0100 {

		if arp.protocol == 0x0008 && arp.ハードウェアaddressサイズ == 6 && arp.protocoladdressサイズ == 4 && uint64(arp.転送先ipaddress) == handler.Getipaddress() {

			arpコンソール.M印刷([]byte("arp onetherframe"))
			arpコンソール.MUnsignedinteger16印刷(arp.protocol)
			arpコンソール.M印刷([]byte(":"))
			arpコンソール.MUnsignedinteger64印刷(uint64(arp.転送先macaddress))
			arpコンソール.M印刷([]byte(":"))
			arpコンソール.MUnsignedinteger16印刷(arp.コマンド)
			arpコンソール.M印刷([]byte(":"))
			arpコンソール.MUnsignedinteger64印刷(handler.Getmacaddress())

			switch arp.コマンド {
			case 0x0100:

				if self.Getmacからcache(arp.転送元ipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.転送元ipaddress
						self.Maccache[self.numbercacheentry] = arp.転送元macaddress
						self.numbercacheentry++
					}
				}
				arp.コマンド = 0x0200
				arp.転送先ipaddress = arp.転送元ipaddress
				arp.転送先macaddress = arp.転送元macaddress
				arp.転送元ipaddress = uint32(handler.Getipaddress())
				arp.転送元macaddress = handler.Getmacaddress()
				arp.Sありbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpコンソール.M印刷(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.転送元ipaddress
					self.Maccache[self.numbercacheentry] = arp.転送元macaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipネットワークバイトorder uint32) {

	var arp Arpメッセージ = Arpメッセージ{}
	arp.ハードウェア型 = 0x0100
	arp.protocol = 0x0008
	arp.ハードウェアaddressサイズ = 6
	arp.protocoladdressサイズ = 4
	arp.コマンド = 0x0200

	arp.転送元ipaddress = uint32(handler.Getipaddress())

	arp.転送先macaddress = self.R解決(Ipネットワークバイトorder)
	arp.転送先ipaddress = Ipネットワークバイトorder
	arpコンソール.M印刷xy([]byte("broad mac"), 0, 15)

	arp.転送元macaddress = handler.Getmacaddress()

	var arpbuffer Arpメッセージbuffer = Arpメッセージbuffer{}
	arp.Sありbuffer(&arpbuffer)

	var 番地参照 uintptr = uintptr(Pointer(&arpbuffer))
	handler.S送信(arp.転送先macaddress, 番地参照, arpmesgサイズ)
}
func (self *Arpprovider) Requestmacaddress(Ipネットワークバイトorder uint32) {

	var arp Arpメッセージ = Arpメッセージ{}
	arp.ハードウェア型 = 0x0100

	arp.protocol = 0x0008
	arp.ハードウェアaddressサイズ = 6
	arp.protocoladdressサイズ = 4
	arp.コマンド = 0x0100

	arp.転送元macaddress = handler.Getmacaddress()
	arp.転送元ipaddress = uint32(handler.Getipaddress())

	arp.転送先macaddress = 0xFFFFFFFFFFFF
	arp.転送先ipaddress = Ipネットワークバイトorder

	var arpbuffer Arpメッセージbuffer = Arpメッセージbuffer{}
	arp.Sありbuffer(&arpbuffer)

	var 番地参照 uintptr = uintptr(Pointer(&arpbuffer))
	handler.S送信(arp.転送先macaddress, 番地参照, arpmesgサイズ)
}
func (self *Arpprovider) Tテスト印刷(データ *[]byte, サイズ uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(データ))
	arpコンソール.M印刷xy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpコンソール.MHexadecimal印刷(buffer_2[i])
		arpコンソール.M印刷([]byte(":"))
	}
	arpコンソール.M印刷([]byte("]"))
}

func (self *Arpprovider) Getmacからcache(Ipネットワークバイトorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpコンソール.M印刷(([]byte)("["))
		arpコンソール.MUnsignedinteger32印刷(self.Ipcache[i])
		arpコンソール.M印刷(([]byte)(":"))
		arpコンソール.MUnsignedinteger32印刷(Ipネットワークバイトorder)
		arpコンソール.M印刷(([]byte)(":"))
		arpコンソール.M印刷(([]byte)(":"))
		arpコンソール.MUnsignedinteger64印刷(self.Maccache[i])
		arpコンソール.M印刷(([]byte)("]\n"))

		if self.Ipcache[i] == Ipネットワークバイトorder {
			arpコンソール.M印刷([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) R解決(Ipネットワークバイトorder uint32) uint64 {
	var 生成先 uint64 = self.Getmacからcache(Ipネットワークバイトorder)
	if 生成先 == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipネットワークバイトorder)
	}
	for i := 0; i < 128 && 生成先 == 0xFFFFFFFFFFFF; i++ {
		生成先 = self.Getmacからcache(Ipネットワークバイトorder)

	}

	return 生成先
}
