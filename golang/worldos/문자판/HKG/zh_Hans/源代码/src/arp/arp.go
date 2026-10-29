/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "控制台"
import . "共享介质网络帧"
import . "工具"

var arp控制台 T控制台 = T控制台{}

type Arp消息buffer struct {
	硬件类型			[2]byte
	protocol		[2]byte
	硬件address大小		byte
	protocoladdress大小	byte
	命令			[2]byte

	源macaddress	[6]byte
	源ipaddress	[4]byte
	目的macaddress	[6]byte
	目的ipaddress	[4]byte
}

var arpmesg大小 uint32 = (64+92+64)/8 + 2

type Arp消息 struct {
	硬件类型			uint16
	protocol		uint16
	硬件address大小		uint8
	protocoladdress大小	uint8
	命令			uint16

	源macaddress	uint64
	源ipaddress	uint32
	目的macaddress	uint64
	目的ipaddress	uint32
}

func (self *Arp消息) Init(buffer_2 *Arp消息buffer) {

	self.硬件类型 = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.硬件类型))
	self.protocol = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.protocol))
	self.硬件address大小 = byte(buffer_2.硬件address大小)
	self.protocoladdress大小 = byte(buffer_2.protocoladdress大小)
	self.命令 = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.命令))

	self.源macaddress = Unsignedinteger48r(A数组tounsignedinteger48(buffer_2.源macaddress))
	self.源ipaddress = Unsignedinteger32r(A数组tounsignedinteger32(buffer_2.源ipaddress))
	self.目的macaddress = Unsignedinteger48r(A数组tounsignedinteger48(buffer_2.目的macaddress))
	self.目的ipaddress = Unsignedinteger32r(A数组tounsignedinteger32(buffer_2.目的ipaddress))
}
func (self *Arp消息) S集合buffer(buffer_2 *Arp消息buffer) {
	buffer_2.硬件类型 = Unsignedinteger16to数组(self.硬件类型)
	buffer_2.protocol = Unsignedinteger16to数组(self.protocol)
	buffer_2.硬件address大小 = uint8(self.硬件address大小)
	buffer_2.protocoladdress大小 = uint8(self.protocoladdress大小)

	buffer_2.命令 = Unsignedinteger16to数组(self.命令)
	buffer_2.源macaddress = Unsignedinteger48to数组(self.源macaddress)
	buffer_2.源ipaddress = Unsignedinteger32to数组(self.源ipaddress)
	buffer_2.目的macaddress = Unsignedinteger48to数组(self.目的macaddress)
	buffer_2.目的ipaddress = Unsignedinteger32to数组(self.目的ipaddress)
}

type Arp以太网帧handler struct {
	T以太网帧handler
}

var arpprovider Arpprovider
var 共享介质网络帧提供器 T共享介质网络帧提供器

func (self *Arp以太网帧handler) O以太网帧receivewhen(数据指针 uintptr, 大小 int) bool {
	arp控制台.M打印xy([]byte("arp recv:"), 0, 23)
	return arpprovider.O以太网帧receivewhen(数据指针, uint32(大小))

}
func (self *Arp以太网帧handler) S发送(目的macbe uint64, 数据指针 uintptr, 大小 uint32) {
	arp控制台.M打印xy([]byte("arp send:"), 0, 24)
	var 以太网类型be = Unsignedinteger16r(0x0806)
	self.T以太网帧handler.S帧发送(目的macbe, 以太网类型be, 数据指针, 大小)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	数字cache条目	int

	handler	I以太网帧handler
}

var handler I以太网帧handler

func (self *Arpprovider) Init(backend T共享介质网络帧提供器, userhandler I以太网帧handler) {

	handler = userhandler
	handler.Init(backend)
	handler.S集合handler(userhandler, 0x0806)
	self.数字cache条目 = 0
	arpprovider = *self

}

func (self *Arpprovider) O以太网帧receivewhen(数据指针 uintptr, 大小 uint32) bool {

	if 大小 < arpmesg大小 {
		return false
	}
	var arpbuffer *Arp消息buffer = (*Arp消息buffer)(Pointer(数据指针))
	var arp Arp消息 = Arp消息{}
	arp.Init(arpbuffer)

	if arp.硬件类型 == 0x0100 {

		if arp.protocol == 0x0008 && arp.硬件address大小 == 6 && arp.protocoladdress大小 == 4 && uint64(arp.目的ipaddress) == handler.Getipaddress() {

			arp控制台.M打印([]byte("arp onetherframe"))
			arp控制台.MUnsignedinteger16打印(arp.protocol)
			arp控制台.M打印([]byte(":"))
			arp控制台.MUnsignedinteger64打印(uint64(arp.目的macaddress))
			arp控制台.M打印([]byte(":"))
			arp控制台.MUnsignedinteger16打印(arp.命令)
			arp控制台.M打印([]byte(":"))
			arp控制台.MUnsignedinteger64打印(handler.Getmacaddress())

			switch arp.命令 {
			case 0x0100:

				if self.Getmacfromcache(arp.源ipaddress) == 0xFFFFFFFFFFFF {
					if self.数字cache条目 < 128 {
						self.Ipcache[self.数字cache条目] = arp.源ipaddress
						self.Maccache[self.数字cache条目] = arp.源macaddress
						self.数字cache条目++
					}
				}
				arp.命令 = 0x0200
				arp.目的ipaddress = arp.源ipaddress
				arp.目的macaddress = arp.源macaddress
				arp.源ipaddress = uint32(handler.Getipaddress())
				arp.源macaddress = handler.Getmacaddress()
				arp.S集合buffer(arpbuffer)

				return true
				break

			case 0x0200:
				arp控制台.M打印(([]byte)("self.numCacheEntries"))

				if self.数字cache条目 < 128 {
					self.Ipcache[self.数字cache条目] = arp.源ipaddress
					self.Maccache[self.数字cache条目] = arp.源macaddress
					self.数字cache条目++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ip网络字节order uint32) {

	var arp Arp消息 = Arp消息{}
	arp.硬件类型 = 0x0100
	arp.protocol = 0x0008
	arp.硬件address大小 = 6
	arp.protocoladdress大小 = 4
	arp.命令 = 0x0200

	arp.源ipaddress = uint32(handler.Getipaddress())

	arp.目的macaddress = self.R解决(Ip网络字节order)
	arp.目的ipaddress = Ip网络字节order
	arp控制台.M打印xy([]byte("broad mac"), 0, 15)

	arp.源macaddress = handler.Getmacaddress()

	var arpbuffer Arp消息buffer = Arp消息buffer{}
	arp.S集合buffer(&arpbuffer)

	var 地址引用 uintptr = uintptr(Pointer(&arpbuffer))
	handler.S发送(arp.目的macaddress, 地址引用, arpmesg大小)
}
func (self *Arpprovider) Requestmacaddress(Ip网络字节order uint32) {

	var arp Arp消息 = Arp消息{}
	arp.硬件类型 = 0x0100

	arp.protocol = 0x0008
	arp.硬件address大小 = 6
	arp.protocoladdress大小 = 4
	arp.命令 = 0x0100

	arp.源macaddress = handler.Getmacaddress()
	arp.源ipaddress = uint32(handler.Getipaddress())

	arp.目的macaddress = 0xFFFFFFFFFFFF
	arp.目的ipaddress = Ip网络字节order

	var arpbuffer Arp消息buffer = Arp消息buffer{}
	arp.S集合buffer(&arpbuffer)

	var 地址引用 uintptr = uintptr(Pointer(&arpbuffer))
	handler.S发送(arp.目的macaddress, 地址引用, arpmesg大小)
}
func (self *Arpprovider) T测试打印(数据 *[]byte, 大小 uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(数据))
	arp控制台.M打印xy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arp控制台.MHexadecimal打印(buffer_2[i])
		arp控制台.M打印([]byte(":"))
	}
	arp控制台.M打印([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ip网络字节order uint32) uint64 {
	for i := 0; i < self.数字cache条目; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arp控制台.M打印(([]byte)("["))
		arp控制台.MUnsignedinteger32打印(self.Ipcache[i])
		arp控制台.M打印(([]byte)(":"))
		arp控制台.MUnsignedinteger32打印(Ip网络字节order)
		arp控制台.M打印(([]byte)(":"))
		arp控制台.M打印(([]byte)(":"))
		arp控制台.MUnsignedinteger64打印(self.Maccache[i])
		arp控制台.M打印(([]byte)("]\n"))

		if self.Ipcache[i] == Ip网络字节order {
			arp控制台.M打印([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) R解决(Ip网络字节order uint32) uint64 {
	var 结果 uint64 = self.Getmacfromcache(Ip网络字节order)
	if 结果 == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ip网络字节order)
	}
	for i := 0; i < 128 && 结果 == 0xFFFFFFFFFFFF; i++ {
		结果 = self.Getmacfromcache(Ip网络字节order)

	}

	return 结果
}
