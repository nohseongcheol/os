/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 用户数据报协议

import . "unsafe"
import . "控制台"
import . "工具"
import . "内存管理器"
import . "互联网络协议4"

var udp控制台 = T控制台{}

type T用户datagramprotocol头部buffer struct {
	源端口号	[2]byte
	目标端口号	[2]byte

	长度		[2]byte
	checksum	[2]byte
}

var udp头部大小 uint32 = 8

type T用户数据报头 struct {
	源端口号	uint16
	目标端口号	uint16

	长度		uint16
	checksum	uint16
}

func (self *T用户数据报头) Init(buffer_2 *T用户datagramprotocol头部buffer) {
	self.源端口号 = A数组tounsignedinteger16(buffer_2.源端口号)
	self.目标端口号 = A数组tounsignedinteger16(buffer_2.目标端口号)

	self.长度 = A数组tounsignedinteger16(buffer_2.长度)
	self.checksum = A数组tounsignedinteger16(buffer_2.checksum)
}
func (self *T用户数据报头) S集合buffer(buffer_2 *T用户datagramprotocol头部buffer) {

	buffer_2.源端口号 = Unsignedinteger16to数组(self.源端口号)
	buffer_2.目标端口号 = Unsignedinteger16to数组(self.目标端口号)

	buffer_2.长度 = Unsignedinteger16to数组(self.长度)
	buffer_2.checksum = Unsignedinteger16to数组(self.checksum)

}

type I用户datagramprotocolhandler interface {
	H控制器用户datagramprotocol消息(套接字 *T用户数据报通信端点, 数据 uintptr, 大小 uint16)
}

type T用户datagramprotocolhandler struct {
}

func (self *T用户datagramprotocolhandler) Init(backend T互联网络协议提供器) {
}
func (self *T用户datagramprotocolhandler) H控制器用户datagramprotocol消息(套接字 *T用户数据报通信端点, 数据 uintptr, 大小 uint16) {
}

type I用户datagramprotocol套接字 interface {
	H控制器用户datagramprotocol消息(数据 uintptr, 大小 uint16)
}
type T用户数据报通信端点 struct {
	远程端口数字	uint16
	远程ip	uint32
	本地端口数字	uint16
	本地ip	uint32

	listening	bool
}

var udpprovider T用户datagramprotocolprovider
var udphandler I用户datagramprotocolhandler

func (self *T用户数据报通信端点) T测试() {
}
func (self *T用户数据报通信端点) Init(pudpprovider T用户datagramprotocolprovider, pudphandler I用户datagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *T用户数据报通信端点) H控制器用户datagramprotocol消息(数据 uintptr, 大小 uint16) {
	if udphandler != nil {
		udphandler.H控制器用户datagramprotocol消息(self, 数据, 大小)
	}
}
func (self *T用户数据报通信端点) S发送(p数据 []byte, 大小 uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(大小); i++ {
		buffer_2[i] = p数据[i]
	}
	var 数据 = uintptr(Pointer(&buffer_2))
	udpprovider.S发送(self, 数据, 大小)
}
func (self *T用户数据报通信端点) D断开() {
	udpprovider.D断开(self)
}

type T用户datagramprotocolprovider struct {
}

var iphandler I互联网protocolhandler
var sockets [65535]T用户数据报通信端点
var 数字sockets int
var 空闲端口 uint16

func (self *T用户datagramprotocolprovider) Init(pipprovider T互联网络协议提供器, piphandler I互联网protocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	数字sockets = 0
	空闲端口 = 1024
}
func (self *T用户datagramprotocolprovider) O互联网protocolreceivewhen(源ipaddress网络字节order uint32, 目的ipaddress网络字节order uint32, 互联网protocolpayload uintptr, 大小 uint32) bool {
	if 大小 < udp头部大小 {
		return false
	}

	var buffer_2 *T用户datagramprotocol头部buffer = (*T用户datagramprotocol头部buffer)(Pointer(互联网protocolpayload))
	var msg T用户数据报头
	msg.Init(buffer_2)

	var 套接字 *T用户数据报通信端点 = nil

	for i := 0; i < 数字sockets && 套接字 == nil; i++ {
		if sockets[i].本地端口数字 == msg.目标端口号 && sockets[i].本地ip == 目的ipaddress网络字节order && sockets[i].listening == true {
			套接字 = &sockets[i]
			套接字.listening = false
			套接字.远程端口数字 = msg.源端口号
			套接字.远程ip = 源ipaddress网络字节order
		} else if sockets[i].本地端口数字 == msg.目标端口号 && sockets[i].本地ip == 目的ipaddress网络字节order && sockets[i].远程端口数字 == msg.源端口号 && sockets[i].远程ip == 源ipaddress网络字节order {
			套接字 = &sockets[i]

		}
	}

	msg.S集合buffer(buffer_2)
	if 套接字 != nil {
		套接字.H控制器用户datagramprotocol消息(互联网protocolpayload+uintptr(udp头部大小), uint16(大小-udp头部大小))
	}

	return false
}

func (self *T用户datagramprotocolprovider) C连接(ip uint32, 端口 uint16) *T用户数据报通信端点 {
	var 内存管理器 = &T内存管理器{}
	var 套接字 = (*T用户数据报通信端点)(内存管理器.M分配内存(50))

	if 套接字 != nil {

		套接字.Init(*self, nil)
		套接字.远程端口数字 = 端口
		套接字.远程ip = ip
		套接字.本地端口数字 = 空闲端口
		空闲端口++
		套接字.本地ip = uint32((*iphandler.Providerget()).Getipaddress())

		套接字.远程端口数字 = Unsignedinteger16r(套接字.远程端口数字)
		套接字.本地端口数字 = Unsignedinteger16r(套接字.本地端口数字)

		sockets[数字sockets] = *套接字
		数字sockets++

	}
	return 套接字

}
func (self *T用户datagramprotocolprovider) Listen(端口 uint16) *T用户数据报通信端点 {
	var 套接字 = &T用户数据报通信端点{}
	套接字 = nil
	if 套接字 != nil {
		套接字.Init(*self, nil)
		套接字.listening = true
		套接字.本地端口数字 = 端口
		套接字.本地ip = uint32((*iphandler.Providerget()).Getipaddress())

		套接字.本地端口数字 = Unsignedinteger16r(套接字.本地端口数字)
	}
	return 套接字
}
func (self *T用户datagramprotocolprovider) D断开(套接字 *T用户数据报通信端点) {
	for i := 0; i < 数字sockets && 套接字 == nil; i++ {
		if sockets[i] == *套接字 {
			数字sockets--
			sockets[i] = sockets[数字sockets]
			break
		}
	}
}
func (self *T用户datagramprotocolprovider) S发送(套接字 *T用户数据报通信端点, p数据 uintptr, 大小 uint16) {
	var 总数长度 = uint32(大小) + udp头部大小

	var buffer_2 [4096]byte

	var msgbuffer = (*T用户datagramprotocol头部buffer)(Pointer(&buffer_2))

	var msg = T用户数据报头{}

	msg.源端口号 = 套接字.本地端口数字
	msg.目标端口号 = 套接字.远程端口数字
	msg.长度 = Unsignedinteger16r(uint16(总数长度))

	msg.checksum = 0x0
	msg.S集合buffer(msgbuffer)

	var 数据字节 [4096]byte = *(*[4096]byte)(Pointer(p数据))
	for i := 0; i < int(大小); i++ {
		buffer_2[int(udp头部大小)+i] = 数据字节[i]
	}

	var 数据 uintptr = uintptr(Pointer(&buffer_2))

	iphandler.S发送(套接字.远程ip, 0x11, 数据, 总数长度)

}
func (self *T用户datagramprotocolprovider) B绑定(套接字 *T用户数据报通信端点, handler *T用户datagramprotocolhandler) {
}
