/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "中断"
import . "控制台"
import . "端口"
import . "pci"

var 网络纸牌类控制台 T控制台 = T控制台{}

type TInitialization块 struct {
	模式		uint16
	数字发送buffer	uint8
	数字recvbuffer	uint8

	物理address	uint64

	逻辑address		uint64
	recvbuffer描述address	uintptr
	发送buffer描述address	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	标志		uint32
	标志2		uint32
	可用		uint32
}

type IRaw数据handler interface {
	O时raw数据receive(数据指针 uintptr, 大小 int) bool
	S发送(数据指针 uintptr, 大小 uint32)
}

var raw数据backend Tamdam79c973

type TRaw数据handler struct {
}

func (self *TRaw数据handler) S集合backend(backend Tamdam79c973) {

	raw数据backend = backend
}
func (self *TRaw数据handler) Getbackend() Tamdam79c973 {
	return raw数据backend
}
func (self *TRaw数据handler) O时raw数据receive(数据指针 uintptr, 大小 int) bool {
	网络纸牌类控制台.M打印xy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRaw数据handler) S发送(数据指针 uintptr, 大小 uint32) {
	网络纸牌类控制台.M打印xy(([]byte)("TRawDataSend"), 10, 10)
	raw数据backend.S发送(数据指针, 大小)
}

var Macaddress0端口 uint16
var Macaddress2端口 uint16
var Macaddress4端口 uint16
var 寄存器数据端口 uint16
var 寄存器address端口 uint16
var 重置端口 uint16
var busCtrl寄存器数据端口 uint16

var init块 TInitialization块

var 发送buffer描述 [8]TBufferdescriptor
var 发送buffer描述内存 [2048 + 15]byte
var 发送buffer [2*1024 + 15][8]uint8
var 当前发送buffer uint8

var recvbuffer描述 [8]TBufferdescriptor
var recvbuffer描述内存 [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var 当前recvbuffer uint8
var func值 func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	T中断handler
	设备descriptor	TPeripheralcomponentinterconnect设备descriptor
	中断		*T中断管理器
	handler		*TRaw数据handler
}

var 控制台_2 T控制台 = T控制台{}
var iraw数据handler IRaw数据handler

func (self *Tamdam79c973) Init驱动程序(中断 *T中断管理器, 设备descriptor TPeripheralcomponentinterconnect设备descriptor, handler IRaw数据handler) {

	self.设备descriptor = 设备descriptor

	func值 = (*Tamdam79c973).H控制器中断
	var address uintptr
	address = uintptr(Pointer(&func值))

	self.Init(uint8(0x20+设备descriptor.I中断), uintptr(Pointer(中断)), address)

	Macaddress0端口 = uint16(设备descriptor.P端口base)
	Macaddress2端口 = uint16(设备descriptor.P端口base) + 0x02
	Macaddress4端口 = uint16(设备descriptor.P端口base) + 0x04
	寄存器数据端口 = uint16(设备descriptor.P端口base) + 0x10
	寄存器address端口 = uint16(设备descriptor.P端口base) + 0x12
	重置端口 = uint16(设备descriptor.P端口base) + 0x14
	busCtrl寄存器数据端口 = uint16(设备descriptor.P端口base) + 0x16

	iraw数据handler = &TRaw数据handler{}
	if handler != nil {
		iraw数据handler = handler
	}

	当前发送buffer = 0
	当前recvbuffer = 0

	var Mac0 uint64 = uint64(P端口读取字(Macaddress0端口) % 256)
	var Mac1 uint64 = uint64(P端口读取字(Macaddress0端口) / 256)
	var Mac2 uint64 = uint64(P端口读取字(Macaddress2端口) % 256)
	var Mac3 uint64 = uint64(P端口读取字(Macaddress2端口) / 256)
	var Mac4 uint64 = uint64(P端口读取字(Macaddress4端口) % 256)
	var Mac5 uint64 = uint64(P端口读取字(Macaddress4端口) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	控制台_2.M打印xy(([]byte)("[interrupt num : "), 0, 13)
	控制台_2.MHexadecimal打印(uint8(设备descriptor.I中断))
	控制台_2.M打印(([]byte)("]"))
	控制台_2.M打印(([]byte)("[mac address : "))
	控制台_2.MUnsignedinteger16打印(uint16(macaddress >> 32))
	控制台_2.MUnsignedinteger32打印(uint32(macaddress & 0x00000000FFFFFFFF))
	控制台_2.M打印(([]byte)("]"))

	P端口写入字(寄存器address端口, 20)
	P端口写入字(busCtrl寄存器数据端口, 0x102)

	P端口写入字(寄存器address端口, 0)
	P端口写入字(寄存器数据端口, 0x04)

	init块.模式 = 0x0000
	init块.数字发送buffer = 3
	init块.数字recvbuffer = 3

	init块.物理address = Mac

	init块.逻辑address = 0

	发送buffer描述 = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&发送buffer描述内存)) + 15) & ^(uintptr)(0xF)))
	init块.发送buffer描述address = uintptr(Pointer(&发送buffer描述))
	recvbuffer描述 = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbuffer描述内存)) + 15) & ^(uintptr)(0xF)))
	init块.recvbuffer描述address = uintptr(Pointer(&recvbuffer描述))

	for i := 0; i < 8; i++ {
		发送buffer描述[i].address_2 = uint32((uintptr(Pointer(&发送buffer[i])) + 15) & ^(uintptr(0xF)))
		发送buffer描述[i].标志 = 0x7FF | 0xF000
		发送buffer描述[i].标志2 = 0
		发送buffer描述[i].可用 = 0

		recvbuffer描述[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbuffer描述[i].标志 = 0xF7FF | 0x80000000

	}

	P端口写入字(寄存器address端口, 1)
	P端口写入字(寄存器数据端口, uint16(uintptr(Pointer(&init块))&0xFFFF))

	P端口写入字(寄存器address端口, 2)
	P端口写入字(寄存器数据端口, uint16((uintptr(Pointer(&init块))>>16)&0xFFFF))

}
func (self *Tamdam79c973) A激活() {
	P端口写入字(寄存器address端口, 0)
	P端口写入字(寄存器数据端口, 0x41)

	P端口写入字(寄存器address端口, 4)
	temporary := P端口读取字(寄存器数据端口)
	P端口写入字(寄存器address端口, 4)
	P端口写入字(寄存器数据端口, temporary|0xC00)

	P端口写入字(寄存器address端口, 0)
	P端口写入字(寄存器数据端口, 0x42)

}
func (self *Tamdam79c973) R重置() int {
	P端口读取字(重置端口)
	P端口写入字(重置端口, 0)
	return 10
}

var 计数 uint16 = 0

func (self *Tamdam79c973) H控制器中断(esp uint32) uint32 {

	P端口写入字(寄存器address端口, 0)
	temporary := uint32(P端口读取字(寄存器数据端口))
	控制台_2.M打印(([]byte)("interrupt("))
	控制台_2.MUnsignedinteger32打印(esp)
	控制台_2.M打印(([]byte)(":"))
	控制台_2.MUnsignedinteger32打印(temporary)
	控制台_2.M打印(([]byte)(":"))
	控制台_2.MUnsignedinteger16打印(计数)
	计数++
	控制台_2.M打印(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		控制台_2.M打印(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		控制台_2.M打印(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		控制台_2.M打印(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		控制台_2.M打印(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		控制台_2.M打印(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		控制台_2.M打印(([]byte)("am79c973 data sent"))
	}

	P端口写入字(寄存器address端口, 0)
	P端口写入字(寄存器数据端口, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		控制台_2.M打印(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) S发送(数据指针 uintptr, 大小 uint32) {
	var 发送descriptor uint16 = uint16(当前发送buffer)
	当前发送buffer = 0

	if 大小 > 1518 {
		大小 = 1518
	}

	var 源_2 [4096]byte = *(*([4096]byte))(Pointer(数据指针))
	var 目的_2 uint32 = 发送buffer描述[发送descriptor].address_2 + 大小 - 1

	for i := 0; i < int(大小); i++ {

		*(*byte)(Pointer(uintptr(目的_2))) = 源_2[int(大小)-i-1]

		目的_2--
	}

	var 数据 [4096]byte = *(*([4096]byte))(Pointer(数据指针))
	控制台_2.M打印xy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		控制台_2.MHexadecimal打印(数据[i])
		控制台_2.M打印(([]byte)(":"))
	}
	控制台_2.M打印(([]byte)("\n"))

	发送buffer描述[发送descriptor].可用 = 0
	发送buffer描述[发送descriptor].标志2 = 0
	发送buffer描述[发送descriptor].标志 = 0x8300F000 | uint32((-大小)&0xFFF)

	P端口写入字(寄存器address端口, 0)
	P端口写入字(寄存器数据端口, 0x48)

}
func (self *Tamdam79c973) Receive() {
	控制台_2.M打印(([]byte)(":"))
	控制台_2.MUnsignedinteger32打印(uint32(uintptr(Pointer(&发送buffer))))
	控制台_2.M打印(([]byte)(":"))
	控制台_2.MHexadecimal打印(发送buffer[0][0])
	控制台_2.MHexadecimal打印(发送buffer[0][1])
	控制台_2.M打印(([]byte)(":"))
	当前recvbuffer = 0

	for ; (recvbuffer描述[当前recvbuffer].标志 & 0x80000000) == 0; 当前recvbuffer = (当前recvbuffer + 1) % 8 {

		if !(recvbuffer描述[当前recvbuffer].标志&0x40000000 != 0) && ((recvbuffer描述[当前recvbuffer].标志 & 0x03000000) == 0x03000000) {
			var 大小 uint32 = recvbuffer描述[当前recvbuffer].标志 & 0xFFF
			if 大小 > 64 {
				大小 -= 4
			}

			控制台_2.M打印([]byte(" size : ["))
			控制台_2.MUnsignedinteger32打印(大小)
			控制台_2.M打印([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbuffer描述[当前recvbuffer].address_2)))
			var 地址引用 uintptr = uintptr(Pointer(&buffer_2))
			if iraw数据handler != nil {
				if iraw数据handler.O时raw数据receive(地址引用, int(大小)) {

					控制台_2.M打印xy(([]byte)("self.Send"), 0, 22)

					self.S发送(地址引用, 大小)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				控制台_2.MHexadecimal打印(buffer_2[i])
				控制台_2.M打印([]byte(":"))
			}

		}
		recvbuffer描述[当前recvbuffer].标志2 = 0
		recvbuffer描述[当前recvbuffer].标志 = 0x8000F7FF
	}
}
func (self *Tamdam79c973) S集合handler(handler *TRaw数据handler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return init块.物理address
}
func (self *Tamdam79c973) S集合ipaddress(ip uint64) {
	init块.逻辑address = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return init块.逻辑address
}
