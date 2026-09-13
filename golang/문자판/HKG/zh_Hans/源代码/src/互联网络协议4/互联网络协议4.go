package 互联网络协议4

import . "unsafe"
import . "工具"
import . "控制台"
import . "共享介质网络帧"
import . "arp"

var ip控制台 T控制台 = T控制台{}

type T互联网protocolv4消息buffer struct {
	lenver	byte
	tos	byte
	总数长度	[2]byte

	ident	[2]byte
	标志与位移	[2]byte

	时间tolive	byte
	protocol	byte
	checksum	[2]byte

	源ipaddress	[4]byte
	目的ipaddress	[4]byte
}

var ip大小 uint8 = (4 + 4 + 4 + 8)

type T互联网protocolv4消息 struct {
	头部长度	uint8
	版本	uint8
	tos	uint8
	总数长度	uint16

	ident	uint16
	标志与位移	uint16

	时间tolive	uint8
	protocol	uint8
	checksum	uint16

	源ipaddress	uint32
	目的ipaddress	uint32
}

func (self *T互联网protocolv4消息) Init(buffer_2 T互联网protocolv4消息buffer) {

	self.版本 = ((buffer_2.lenver & 0xF0) >> 4)
	self.头部长度 = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.总数长度 = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.总数长度))

	self.ident = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.ident))
	self.标志与位移 = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.标志与位移))

	self.时间tolive = buffer_2.时间tolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(A数组tounsignedinteger16(buffer_2.checksum))

	self.源ipaddress = Unsignedinteger32r(A数组tounsignedinteger32(buffer_2.源ipaddress))
	self.目的ipaddress = Unsignedinteger32r(A数组tounsignedinteger32(buffer_2.目的ipaddress))

}
func (self *T互联网protocolv4消息) S集合buffer(buffer_2 *T互联网protocolv4消息buffer) {

	buffer_2.lenver = byte(((self.版本 & 0x0F) << 4) | (self.头部长度 & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.总数长度 = Unsignedinteger16to数组(self.总数长度)

	buffer_2.ident = Unsignedinteger16to数组(self.ident)
	buffer_2.标志与位移 = Unsignedinteger16to数组(self.标志与位移)

	buffer_2.时间tolive = self.时间tolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16to数组(self.checksum)

	buffer_2.源ipaddress = Unsignedinteger32to数组(self.源ipaddress)
	buffer_2.目的ipaddress = Unsignedinteger32to数组(self.目的ipaddress)

}

type I互联网protocolhandler interface {
	Init(backend T互联网络协议提供器, pihandler I互联网protocolhandler, pprotocol uint8)
	O互联网protocolreceivewhen(源ipaddress网络字节order uint32, 目的ipaddress网络字节order uint32, 数据指针 uintptr, 大小 uint32) bool
	S发送(目的ipaddress网络字节order uint32, pprotocol uint8, 数据指针 uintptr, 大小 uint32)
	Providerget() *T互联网络协议提供器
}

type T互联网protocolhandler struct {
}

var ip以太网帧handler Ip以太网帧handler = Ip以太网帧handler{}
var protocol uint8

func (self *T互联网protocolhandler) Init(backend T互联网络协议提供器, pihandler I互联网protocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *T互联网protocolhandler) O互联网protocolreceivewhen(源ipaddress网络字节order uint32, 目的ipaddress网络字节order uint32, 数据指针 uintptr, 大小 uint32) bool {
	ip控制台.M打印(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *T互联网protocolhandler) S发送(目的ipaddress网络字节order uint32, pprotocol uint8, 数据指针 uintptr, 大小 uint32) {

	互联网络协议提供器.S发送(目的ipaddress网络字节order, pprotocol, 数据指针, 大小)
}
func (self *T互联网protocolhandler) Providerget() *T互联网络协议提供器 {
	return &互联网络协议提供器
}

type Ip以太网帧handler struct {
	T以太网帧handler
}

var 互联网络协议提供器 T互联网络协议提供器

func (self *Ip以太网帧handler) O以太网帧receivewhen(数据指针 uintptr, 大小 int) bool {
	ip控制台.M打印(([]byte)("iphandler:onEtherfameRecv\n"))
	return 互联网络协议提供器.O以太网帧receivewhen(数据指针, uint32(大小))

}

func (self *Ip以太网帧handler) S发送(目的ipaddress网络字节order uint64, 数据指针 uintptr, 大小 uint32) {
	ip控制台.M打印(([]byte)("ipefhandler:send\n"))
	var 以太网类型be = Unsignedinteger16r(0x0800)
	self.T以太网帧handler.S帧发送(目的ipaddress网络字节order, 以太网类型be, 数据指针, 大小)

}

var handler_2 [255]I互联网protocolhandler

type T互联网络协议提供器 struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnet掩码	uint32
}

var efhandler I以太网帧handler

func (self *T互联网络协议提供器) Init(pefprovider T共享介质网络帧提供器, pefhandler I以太网帧handler, arp Arpprovider, gatewayip uint32, subnet掩码 uint32) {

	efhandler = pefhandler
	efhandler.S集合handler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnet掩码 = subnet掩码
	互联网络协议提供器 = *self
}
func (self *T互联网络协议提供器) O以太网帧receivewhen(以太网帧payload uintptr, 大小 uint32) bool {
	if 大小 < uint32(ip大小) {
		return false
	}

	var buffer_2 *T互联网protocolv4消息buffer = (*T互联网protocolv4消息buffer)(Pointer(以太网帧payload))
	var 互联网protocol消息 T互联网protocolv4消息
	互联网protocol消息.Init(*buffer_2)

	var reply bool = false

	if 互联网protocol消息.目的ipaddress == uint32(efhandler.Getipaddress()) {

		var 长度 uint32 = uint32(互联网protocol消息.总数长度)
		if 长度 > 大小 {
			长度 = 大小
		}
		if handler_2[互联网protocol消息.protocol] != nil {
			reply = handler_2[互联网protocol消息.protocol].O互联网protocolreceivewhen(互联网protocol消息.源ipaddress, 互联网protocol消息.目的ipaddress, 以太网帧payload+uintptr(4*互联网protocol消息.头部长度), uint32(长度-uint32(4*互联网protocol消息.头部长度)))

		}
	}

	if reply {

		var temporary = 互联网protocol消息.目的ipaddress
		互联网protocol消息.目的ipaddress = 互联网protocol消息.源ipaddress
		互联网protocol消息.源ipaddress = temporary

		互联网protocol消息.时间tolive = 0x40
		互联网protocol消息.checksum = 0

		互联网protocol消息.S集合buffer(buffer_2)
		互联网protocol消息.checksum = self.Checksum((*([4096]uint16))(Pointer(以太网帧payload)), uint32(4*互联网protocol消息.头部长度))

		互联网protocol消息.S集合buffer(buffer_2)

	}

	ip控制台.M打印(([]byte)("ipmessage"))
	ip控制台.MUnsignedinteger32打印(互联网protocol消息.源ipaddress)
	ip控制台.M打印(([]byte)(":"))
	ip控制台.MUnsignedinteger32打印(互联网protocol消息.目的ipaddress)
	ip控制台.M打印(([]byte)(":"))
	ip控制台.MUnsignedinteger16打印(uint16(互联网protocol消息.头部长度))
	ip控制台.M打印(([]byte)(":"))
	ip控制台.MUnsignedinteger16打印(uint16(互联网protocol消息.版本))
	ip控制台.M打印(([]byte)(":"))
	ip控制台.MUnsignedinteger16打印(互联网protocol消息.总数长度)
	ip控制台.M打印(([]byte)(":"))
	ip控制台.MUnsignedinteger32打印(uint32(efhandler.Getipaddress()))
	ip控制台.M打印(([]byte)(":"))
	ip控制台.M打印(([]byte)("\n"))

	return reply

}
func (self *T互联网络协议提供器) S发送(目的ipaddress网络字节order uint32, protocol uint8, 数据指针 uintptr, 大小 uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *T互联网protocolv4消息buffer = (*T互联网protocolv4消息buffer)(Pointer(&buffer1_2))
	var 消息 T互联网protocolv4消息 = T互联网protocolv4消息{}
	消息.版本 = 4
	消息.头部长度 = ip大小 / 4
	消息.tos = 0
	消息.总数长度 = Unsignedinteger16r(uint16(大小 + uint32(ip大小)))

	消息.ident = 0x0100
	消息.标志与位移 = 0x0040
	消息.时间tolive = 0x40
	消息.protocol = protocol

	消息.目的ipaddress = 目的ipaddress网络字节order

	消息.源ipaddress = uint32(efhandler.Getipaddress())

	消息.checksum = 0

	消息.S集合buffer(buffer_2)
	消息.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ip大小))
	消息.S集合buffer(buffer_2)

	var 数据buffer_2 [4096]byte = *(*([4096]byte))(Pointer(数据指针))

	for i := 0; i < int(大小); i++ {

		buffer1_2[i+int(ip大小)] = 数据buffer_2[i]
	}

	ip控制台.M打印xy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(大小)+int(ip大小); i++ {
		ip控制台.MHexadecimal打印(buffer1_2[i])
	}
	ip控制台.M打印(([]byte)(":"))
	ip控制台.M打印(([]byte)("]\n"))

	var 下一个hopipaddress网络字节order uint32 = 目的ipaddress网络字节order
	if (目的ipaddress网络字节order & self.Subnet掩码) != (消息.源ipaddress & self.Subnet掩码) {
		下一个hopipaddress网络字节order = self.Gatewayip
	}

	var 发送数据指针 = uintptr(Pointer(&buffer1_2))
	ip控制台.MUnsignedinteger32打印(下一个hopipaddress网络字节order)

	var 以太网类型be = Unsignedinteger16r(0x0800)
	efhandler.S帧发送(self.arpprovider.R解决(下一个hopipaddress网络字节order), 以太网类型be, 发送数据指针, uint32(ip大小)+uint32(大小))

}
func (self *T互联网络协议提供器) Checksum(p数据 *[4096]uint16, 长度进字节 uint32) uint16 {
	var 数据 [4096]uint16 = *p数据
	var temporary uint32 = 0
	var 数据字节 [4096]byte = *(*([4096]byte))(Pointer(&数据))
	if (长度进字节 % 2) != 0 {
		temporary += uint32(uint16(数据字节[长度进字节-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *T互联网络协议提供器) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
