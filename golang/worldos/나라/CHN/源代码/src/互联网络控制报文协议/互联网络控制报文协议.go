/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 互联网络控制报文协议

import . "unsafe"
import . "控制台"
import . "内存管理器"
import . "共享介质网络帧"
import . "互联网络协议4"
import . "工具"

var icmp控制台 = T控制台{}

type T互联网Ctrl消息protocol消息buffer struct {
	T类型	byte
	code	byte

	checksum	[2]byte
	数据		[4]byte
}

var icmp大小 int = 64

type T互联网Ctrl消息protocol消息 struct {
	T类型	uint8
	code	uint8

	checksum	uint16
	数据		uint32
}

func (self *T互联网Ctrl消息protocol消息) Init(buffer_2 T互联网Ctrl消息protocol消息buffer) {
	self.T类型 = buffer_2.T类型
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.checksum))
	self.数据 = Unsignedinteger32r(A数组tounsignedinteger32(buffer_2.数据))
}

func (self *T互联网Ctrl消息protocol消息) S集合buffer(buffer_2 *T互联网Ctrl消息protocol消息buffer) {
	buffer_2.T类型 = self.T类型
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16to数组(self.checksum)
	buffer_2.数据 = Unsignedinteger32to数组(self.数据)
}

type Icmphandler struct {
	T互联网protocolhandler
}

var 互联网络控制报文协议 *T互联网络控制报文协议

func (self *Icmphandler) O互联网protocolreceivewhen(源ipaddress网络字节order uint32, 目的ipaddress网络字节order uint32, 数据指针 uintptr, 大小 uint32) bool {
	return 互联网络控制报文协议.O互联网protocolreceivewhen(源ipaddress网络字节order, 目的ipaddress网络字节order, 数据指针, 大小)
}

var iphandler I互联网protocolhandler

type T互联网络控制报文协议 struct {
}

func (self *T互联网络控制报文协议) Init(backend T互联网络协议提供器, handler I互联网protocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	互联网络控制报文协议 = self
}
func (self *T互联网络控制报文协议) O互联网protocolreceivewhen(源ipaddress网络字节order uint32, 目的ipaddress网络字节order uint32, 数据指针 uintptr, 大小 uint32) bool {
	if 大小 < uint32(icmp大小) {
		return false
	}

	var buffer_2 *T互联网Ctrl消息protocol消息buffer = (*T互联网Ctrl消息protocol消息buffer)(Pointer(数据指针))
	var msg T互联网Ctrl消息protocol消息 = T互联网Ctrl消息protocol消息{}
	msg.Init(*buffer_2)

	icmp控制台.M打印(([]byte)("icmp:OnInternet"))
	icmp控制台.MUnsignedinteger16打印(uint16(msg.T类型))
	icmp控制台.M打印(([]byte)(":"))

	switch msg.T类型 {
	case 0:
		icmp控制台.M打印(([]byte)("ping response from "))
		break

	case 8:
		icmp控制台.M打印(([]byte)("ping send "))
		msg.T类型 = 0

		msg.checksum = 0
		msg.S集合buffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(数据指针)), uint32(icmp大小))

		msg.S集合buffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *T互联网络控制报文协议) Echorequest发送(ip网络字节order uint32) bool {
	var 互联网络控制报文协议 T互联网Ctrl消息protocol消息 = T互联网Ctrl消息protocol消息{}

	var 内存管理器 = &T内存管理器{}
	var buffer_2 = (*T互联网Ctrl消息protocol消息buffer)(内存管理器.M分配内存(1024))

	互联网络控制报文协议.T类型 = 8
	互联网络控制报文协议.code = 0
	互联网络控制报文协议.数据 = 0x3713
	互联网络控制报文协议.checksum = 0
	互联网络控制报文协议.S集合buffer(buffer_2)
	互联网络控制报文协议.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmp大小))
	互联网络控制报文协议.S集合buffer(buffer_2)

	var 数据指针 uintptr = uintptr(Pointer(buffer_2))
	iphandler.S发送(ip网络字节order, 0x01, 数据指针, uint32(icmp大小))

	return false

}
