package arp

import . "unsafe"
import . "コンソール"
import . "キョウユウバイタイモウデンソウワク"
import . "ハンヨウ"

var arpコンソール Tコンソール = Tコンソール{}

type Arpメッセージbuffer struct {
	ハードウェアカタ			[2]byte
	protocol		[2]byte
	ハードウェアaddressサイズ	byte
	protocoladdressサイズ	byte
	コマンド			[2]byte

	テンソウモトmacaddress	[6]byte
	テンソウモトipaddress	[4]byte
	テンソウサキmacaddress	[6]byte
	テンソウサキipaddress	[4]byte
}

var arpmesgサイズ uint32 = (64+92+64)/8 + 2

type Arpメッセージ struct {
	ハードウェアカタ			uint16
	protocol		uint16
	ハードウェアaddressサイズ	uint8
	protocoladdressサイズ	uint8
	コマンド			uint16

	テンソウモトmacaddress	uint64
	テンソウモトipaddress	uint32
	テンソウサキmacaddress	uint64
	テンソウサキipaddress	uint32
}

func (self *Arpメッセージ) Init(buffer_2 *Arpメッセージbuffer) {

	self.ハードウェアカタ = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.ハードウェアカタ))
	self.protocol = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.protocol))
	self.ハードウェアaddressサイズ = byte(buffer_2.ハードウェアaddressサイズ)
	self.protocoladdressサイズ = byte(buffer_2.protocoladdressサイズ)
	self.コマンド = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.コマンド))

	self.テンソウモトmacaddress = Unsignedinteger48r(Aハイレツtounsignedinteger48(buffer_2.テンソウモトmacaddress))
	self.テンソウモトipaddress = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer_2.テンソウモトipaddress))
	self.テンソウサキmacaddress = Unsignedinteger48r(Aハイレツtounsignedinteger48(buffer_2.テンソウサキmacaddress))
	self.テンソウサキipaddress = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer_2.テンソウサキipaddress))
}
func (self *Arpメッセージ) Sアリbuffer(buffer_2 *Arpメッセージbuffer) {
	buffer_2.ハードウェアカタ = Unsignedinteger16toハイレツ(self.ハードウェアカタ)
	buffer_2.protocol = Unsignedinteger16toハイレツ(self.protocol)
	buffer_2.ハードウェアaddressサイズ = uint8(self.ハードウェアaddressサイズ)
	buffer_2.protocoladdressサイズ = uint8(self.protocoladdressサイズ)

	buffer_2.コマンド = Unsignedinteger16toハイレツ(self.コマンド)
	buffer_2.テンソウモトmacaddress = Unsignedinteger48toハイレツ(self.テンソウモトmacaddress)
	buffer_2.テンソウモトipaddress = Unsignedinteger32toハイレツ(self.テンソウモトipaddress)
	buffer_2.テンソウサキmacaddress = Unsignedinteger48toハイレツ(self.テンソウサキmacaddress)
	buffer_2.テンソウサキipaddress = Unsignedinteger32toハイレツ(self.テンソウサキipaddress)
}

type Arpイーサネットフレームhandler struct {
	Tイーサネットフレームhandler
}

var arpprovider Arpprovider
var キョウユウバイタイアミデンソウワクテイキョウウツワ Tキョウユウバイタイアミデンソウワクテイキョウウツワ

func (self *Arpイーサネットフレームhandler) Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool {
	arpコンソール.Mインサツxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Oイーサネットフレームreceivewhen(データポインタ, uint32(サイズ))

}
func (self *Arpイーサネットフレームhandler) Sソウシン(テンソウサキmacbe uint64, データポインタ uintptr, サイズ uint32) {
	arpコンソール.Mインサツxy([]byte("arp send:"), 0, 24)
	var イーサネットカタbe = Unsignedinteger16r(0x0806)
	self.Tイーサネットフレームhandler.Sフレームソウシン(テンソウサキmacbe, イーサネットカタbe, データポインタ, サイズ)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	Iイーサネットフレームhandler
}

var handler Iイーサネットフレームhandler

func (self *Arpprovider) Init(backend Tキョウユウバイタイアミデンソウワクテイキョウウツワ, userhandler Iイーサネットフレームhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sアリhandler(userhandler, 0x0806)
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

	if arp.ハードウェアカタ == 0x0100 {

		if arp.protocol == 0x0008 && arp.ハードウェアaddressサイズ == 6 && arp.protocoladdressサイズ == 4 && uint64(arp.テンソウサキipaddress) == handler.Getipaddress() {

			arpコンソール.Mインサツ([]byte("arp onetherframe"))
			arpコンソール.MUnsignedinteger16インサツ(arp.protocol)
			arpコンソール.Mインサツ([]byte(":"))
			arpコンソール.MUnsignedinteger64インサツ(uint64(arp.テンソウサキmacaddress))
			arpコンソール.Mインサツ([]byte(":"))
			arpコンソール.MUnsignedinteger16インサツ(arp.コマンド)
			arpコンソール.Mインサツ([]byte(":"))
			arpコンソール.MUnsignedinteger64インサツ(handler.Getmacaddress())

			switch arp.コマンド {
			case 0x0100:

				if self.Getmacカラcache(arp.テンソウモトipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.テンソウモトipaddress
						self.Maccache[self.numbercacheentry] = arp.テンソウモトmacaddress
						self.numbercacheentry++
					}
				}
				arp.コマンド = 0x0200
				arp.テンソウサキipaddress = arp.テンソウモトipaddress
				arp.テンソウサキmacaddress = arp.テンソウモトmacaddress
				arp.テンソウモトipaddress = uint32(handler.Getipaddress())
				arp.テンソウモトmacaddress = handler.Getmacaddress()
				arp.Sアリbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpコンソール.Mインサツ(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.テンソウモトipaddress
					self.Maccache[self.numbercacheentry] = arp.テンソウモトmacaddress
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
	arp.ハードウェアカタ = 0x0100
	arp.protocol = 0x0008
	arp.ハードウェアaddressサイズ = 6
	arp.protocoladdressサイズ = 4
	arp.コマンド = 0x0200

	arp.テンソウモトipaddress = uint32(handler.Getipaddress())

	arp.テンソウサキmacaddress = self.Rカイケツ(Ipネットワークバイトorder)
	arp.テンソウサキipaddress = Ipネットワークバイトorder
	arpコンソール.Mインサツxy([]byte("broad mac"), 0, 15)

	arp.テンソウモトmacaddress = handler.Getmacaddress()

	var arpbuffer Arpメッセージbuffer = Arpメッセージbuffer{}
	arp.Sアリbuffer(&arpbuffer)

	var バンチサンショウ uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sソウシン(arp.テンソウサキmacaddress, バンチサンショウ, arpmesgサイズ)
}
func (self *Arpprovider) Requestmacaddress(Ipネットワークバイトorder uint32) {

	var arp Arpメッセージ = Arpメッセージ{}
	arp.ハードウェアカタ = 0x0100

	arp.protocol = 0x0008
	arp.ハードウェアaddressサイズ = 6
	arp.protocoladdressサイズ = 4
	arp.コマンド = 0x0100

	arp.テンソウモトmacaddress = handler.Getmacaddress()
	arp.テンソウモトipaddress = uint32(handler.Getipaddress())

	arp.テンソウサキmacaddress = 0xFFFFFFFFFFFF
	arp.テンソウサキipaddress = Ipネットワークバイトorder

	var arpbuffer Arpメッセージbuffer = Arpメッセージbuffer{}
	arp.Sアリbuffer(&arpbuffer)

	var バンチサンショウ uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sソウシン(arp.テンソウサキmacaddress, バンチサンショウ, arpmesgサイズ)
}
func (self *Arpprovider) Tテストインサツ(データ *[]byte, サイズ uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(データ))
	arpコンソール.Mインサツxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpコンソール.MHexadecimalインサツ(buffer_2[i])
		arpコンソール.Mインサツ([]byte(":"))
	}
	arpコンソール.Mインサツ([]byte("]"))
}

func (self *Arpprovider) Getmacカラcache(Ipネットワークバイトorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpコンソール.Mインサツ(([]byte)("["))
		arpコンソール.MUnsignedinteger32インサツ(self.Ipcache[i])
		arpコンソール.Mインサツ(([]byte)(":"))
		arpコンソール.MUnsignedinteger32インサツ(Ipネットワークバイトorder)
		arpコンソール.Mインサツ(([]byte)(":"))
		arpコンソール.Mインサツ(([]byte)(":"))
		arpコンソール.MUnsignedinteger64インサツ(self.Maccache[i])
		arpコンソール.Mインサツ(([]byte)("]\n"))

		if self.Ipcache[i] == Ipネットワークバイトorder {
			arpコンソール.Mインサツ([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Rカイケツ(Ipネットワークバイトorder uint32) uint64 {
	var セイセイサキ uint64 = self.Getmacカラcache(Ipネットワークバイトorder)
	if セイセイサキ == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipネットワークバイトorder)
	}
	for i := 0; i < 128 && セイセイサキ == 0xFFFFFFFFFFFF; i++ {
		セイセイサキ = self.Getmacカラcache(Ipネットワークバイトorder)

	}

	return セイセイサキ
}
