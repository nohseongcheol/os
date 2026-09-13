package arp

import . "unsafe"
import . "控制台"
import . "共享媒介網路框"
import . "工具"

var arp控制台 T控制台 = T控制台{}

type Arp訊息buffer struct {
	硬體類型			[2]byte
	protocol		[2]byte
	硬體address大小		byte
	protocoladdress大小	byte
	指令			[2]byte

	來源macaddress	[6]byte
	來源ipaddress	[4]byte
	目的地macaddress	[6]byte
	目的地ipaddress	[4]byte
}

var arpmesg大小 uint32 = (64+92+64)/8 + 2

type Arp訊息 struct {
	硬體類型			uint16
	protocol		uint16
	硬體address大小		uint8
	protocoladdress大小	uint8
	指令			uint16

	來源macaddress	uint64
	來源ipaddress	uint32
	目的地macaddress	uint64
	目的地ipaddress	uint32
}

func (self *Arp訊息) Init(buffer_2 *Arp訊息buffer) {

	self.硬體類型 = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.硬體類型))
	self.protocol = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.protocol))
	self.硬體address大小 = byte(buffer_2.硬體address大小)
	self.protocoladdress大小 = byte(buffer_2.protocoladdress大小)
	self.指令 = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.指令))

	self.來源macaddress = Unsignedinteger48r(A陣列tounsignedinteger48(buffer_2.來源macaddress))
	self.來源ipaddress = Unsignedinteger32r(A陣列tounsignedinteger32(buffer_2.來源ipaddress))
	self.目的地macaddress = Unsignedinteger48r(A陣列tounsignedinteger48(buffer_2.目的地macaddress))
	self.目的地ipaddress = Unsignedinteger32r(A陣列tounsignedinteger32(buffer_2.目的地ipaddress))
}
func (self *Arp訊息) S設定buffer(buffer_2 *Arp訊息buffer) {
	buffer_2.硬體類型 = Unsignedinteger16to陣列(self.硬體類型)
	buffer_2.protocol = Unsignedinteger16to陣列(self.protocol)
	buffer_2.硬體address大小 = uint8(self.硬體address大小)
	buffer_2.protocoladdress大小 = uint8(self.protocoladdress大小)

	buffer_2.指令 = Unsignedinteger16to陣列(self.指令)
	buffer_2.來源macaddress = Unsignedinteger48to陣列(self.來源macaddress)
	buffer_2.來源ipaddress = Unsignedinteger32to陣列(self.來源ipaddress)
	buffer_2.目的地macaddress = Unsignedinteger48to陣列(self.目的地macaddress)
	buffer_2.目的地ipaddress = Unsignedinteger32to陣列(self.目的地ipaddress)
}

type Arp乙太網路框架handler struct {
	T乙太網路框架handler
}

var arpprovider Arpprovider
var 共享媒介網路框提供器 T共享媒介網路框提供器

func (self *Arp乙太網路框架handler) O乙太網路框架receivewhen(資料指標 uintptr, 大小 int) bool {
	arp控制台.M列印xy([]byte("arp recv:"), 0, 23)
	return arpprovider.O乙太網路框架receivewhen(資料指標, uint32(大小))

}
func (self *Arp乙太網路框架handler) S送出(目的地macbe uint64, 資料指標 uintptr, 大小 uint32) {
	arp控制台.M列印xy([]byte("arp send:"), 0, 24)
	var 乙太網路類型be = Unsignedinteger16r(0x0806)
	self.T乙太網路框架handler.S框架送出(目的地macbe, 乙太網路類型be, 資料指標, 大小)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	數字cache項目	int

	handler	I乙太網路框架handler
}

var handler I乙太網路框架handler

func (self *Arpprovider) Init(backend T共享媒介網路框提供器, userhandler I乙太網路框架handler) {

	handler = userhandler
	handler.Init(backend)
	handler.S設定handler(userhandler, 0x0806)
	self.數字cache項目 = 0
	arpprovider = *self

}

func (self *Arpprovider) O乙太網路框架receivewhen(資料指標 uintptr, 大小 uint32) bool {

	if 大小 < arpmesg大小 {
		return false
	}
	var arpbuffer *Arp訊息buffer = (*Arp訊息buffer)(Pointer(資料指標))
	var arp Arp訊息 = Arp訊息{}
	arp.Init(arpbuffer)

	if arp.硬體類型 == 0x0100 {

		if arp.protocol == 0x0008 && arp.硬體address大小 == 6 && arp.protocoladdress大小 == 4 && uint64(arp.目的地ipaddress) == handler.Getipaddress() {

			arp控制台.M列印([]byte("arp onetherframe"))
			arp控制台.MUnsignedinteger16列印(arp.protocol)
			arp控制台.M列印([]byte(":"))
			arp控制台.MUnsignedinteger64列印(uint64(arp.目的地macaddress))
			arp控制台.M列印([]byte(":"))
			arp控制台.MUnsignedinteger16列印(arp.指令)
			arp控制台.M列印([]byte(":"))
			arp控制台.MUnsignedinteger64列印(handler.Getmacaddress())

			switch arp.指令 {
			case 0x0100:

				if self.Getmacfromcache(arp.來源ipaddress) == 0xFFFFFFFFFFFF {
					if self.數字cache項目 < 128 {
						self.Ipcache[self.數字cache項目] = arp.來源ipaddress
						self.Maccache[self.數字cache項目] = arp.來源macaddress
						self.數字cache項目++
					}
				}
				arp.指令 = 0x0200
				arp.目的地ipaddress = arp.來源ipaddress
				arp.目的地macaddress = arp.來源macaddress
				arp.來源ipaddress = uint32(handler.Getipaddress())
				arp.來源macaddress = handler.Getmacaddress()
				arp.S設定buffer(arpbuffer)

				return true
				break

			case 0x0200:
				arp控制台.M列印(([]byte)("self.numCacheEntries"))

				if self.數字cache項目 < 128 {
					self.Ipcache[self.數字cache項目] = arp.來源ipaddress
					self.Maccache[self.數字cache項目] = arp.來源macaddress
					self.數字cache項目++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ip網路位元組order uint32) {

	var arp Arp訊息 = Arp訊息{}
	arp.硬體類型 = 0x0100
	arp.protocol = 0x0008
	arp.硬體address大小 = 6
	arp.protocoladdress大小 = 4
	arp.指令 = 0x0200

	arp.來源ipaddress = uint32(handler.Getipaddress())

	arp.目的地macaddress = self.R解決(Ip網路位元組order)
	arp.目的地ipaddress = Ip網路位元組order
	arp控制台.M列印xy([]byte("broad mac"), 0, 15)

	arp.來源macaddress = handler.Getmacaddress()

	var arpbuffer Arp訊息buffer = Arp訊息buffer{}
	arp.S設定buffer(&arpbuffer)

	var 位址參照 uintptr = uintptr(Pointer(&arpbuffer))
	handler.S送出(arp.目的地macaddress, 位址參照, arpmesg大小)
}
func (self *Arpprovider) Requestmacaddress(Ip網路位元組order uint32) {

	var arp Arp訊息 = Arp訊息{}
	arp.硬體類型 = 0x0100

	arp.protocol = 0x0008
	arp.硬體address大小 = 6
	arp.protocoladdress大小 = 4
	arp.指令 = 0x0100

	arp.來源macaddress = handler.Getmacaddress()
	arp.來源ipaddress = uint32(handler.Getipaddress())

	arp.目的地macaddress = 0xFFFFFFFFFFFF
	arp.目的地ipaddress = Ip網路位元組order

	var arpbuffer Arp訊息buffer = Arp訊息buffer{}
	arp.S設定buffer(&arpbuffer)

	var 位址參照 uintptr = uintptr(Pointer(&arpbuffer))
	handler.S送出(arp.目的地macaddress, 位址參照, arpmesg大小)
}
func (self *Arpprovider) T測試列印(資料 *[]byte, 大小 uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(資料))
	arp控制台.M列印xy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arp控制台.MHexadecimal列印(buffer_2[i])
		arp控制台.M列印([]byte(":"))
	}
	arp控制台.M列印([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ip網路位元組order uint32) uint64 {
	for i := 0; i < self.數字cache項目; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arp控制台.M列印(([]byte)("["))
		arp控制台.MUnsignedinteger32列印(self.Ipcache[i])
		arp控制台.M列印(([]byte)(":"))
		arp控制台.MUnsignedinteger32列印(Ip網路位元組order)
		arp控制台.M列印(([]byte)(":"))
		arp控制台.M列印(([]byte)(":"))
		arp控制台.MUnsignedinteger64列印(self.Maccache[i])
		arp控制台.M列印(([]byte)("]\n"))

		if self.Ipcache[i] == Ip網路位元組order {
			arp控制台.M列印([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) R解決(Ip網路位元組order uint32) uint64 {
	var 結果 uint64 = self.Getmacfromcache(Ip網路位元組order)
	if 結果 == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ip網路位元組order)
	}
	for i := 0; i < 128 && 結果 == 0xFFFFFFFFFFFF; i++ {
		結果 = self.Getmacfromcache(Ip網路位元組order)

	}

	return 結果
}
