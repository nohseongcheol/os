/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 互聯網路協定4

import . "unsafe"
import . "工具"
import . "控制台"
import . "共享媒介網路框"
import . "arp"

var ip控制台 T控制台 = T控制台{}

type T互聯網protocolv4訊息buffer struct {
	lenver	byte
	tos	byte
	總數長度	[2]byte

	ident	[2]byte
	旗標和位移	[2]byte

	時間tolive	byte
	protocol	byte
	checksum	[2]byte

	來源ipaddress	[4]byte
	目的地ipaddress	[4]byte
}

var ip大小 uint8 = (4 + 4 + 4 + 8)

type T互聯網protocolv4訊息 struct {
	標頭長度	uint8
	版本	uint8
	tos	uint8
	總數長度	uint16

	ident	uint16
	旗標和位移	uint16

	時間tolive	uint8
	protocol	uint8
	checksum	uint16

	來源ipaddress	uint32
	目的地ipaddress	uint32
}

func (self *T互聯網protocolv4訊息) Init(buffer_2 T互聯網protocolv4訊息buffer) {

	self.版本 = ((buffer_2.lenver & 0xF0) >> 4)
	self.標頭長度 = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.總數長度 = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.總數長度))

	self.ident = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.ident))
	self.旗標和位移 = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.旗標和位移))

	self.時間tolive = buffer_2.時間tolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.checksum))

	self.來源ipaddress = Unsignedinteger32r(A陣列tounsignedinteger32(buffer_2.來源ipaddress))
	self.目的地ipaddress = Unsignedinteger32r(A陣列tounsignedinteger32(buffer_2.目的地ipaddress))

}
func (self *T互聯網protocolv4訊息) S設定buffer(buffer_2 *T互聯網protocolv4訊息buffer) {

	buffer_2.lenver = byte(((self.版本 & 0x0F) << 4) | (self.標頭長度 & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.總數長度 = Unsignedinteger16to陣列(self.總數長度)

	buffer_2.ident = Unsignedinteger16to陣列(self.ident)
	buffer_2.旗標和位移 = Unsignedinteger16to陣列(self.旗標和位移)

	buffer_2.時間tolive = self.時間tolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16to陣列(self.checksum)

	buffer_2.來源ipaddress = Unsignedinteger32to陣列(self.來源ipaddress)
	buffer_2.目的地ipaddress = Unsignedinteger32to陣列(self.目的地ipaddress)

}

type I互聯網protocolhandler interface {
	Init(backend T互聯網路協定提供器, pihandler I互聯網protocolhandler, pprotocol uint8)
	O互聯網protocolreceivewhen(來源ipaddress網路位元組order uint32, 目的地ipaddress網路位元組order uint32, 資料指標 uintptr, 大小 uint32) bool
	S送出(目的地ipaddress網路位元組order uint32, pprotocol uint8, 資料指標 uintptr, 大小 uint32)
	Providerget() *T互聯網路協定提供器
}

type T互聯網protocolhandler struct {
}

var ip乙太網路框架handler Ip乙太網路框架handler = Ip乙太網路框架handler{}
var protocol uint8

func (self *T互聯網protocolhandler) Init(backend T互聯網路協定提供器, pihandler I互聯網protocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *T互聯網protocolhandler) O互聯網protocolreceivewhen(來源ipaddress網路位元組order uint32, 目的地ipaddress網路位元組order uint32, 資料指標 uintptr, 大小 uint32) bool {
	ip控制台.M列印(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *T互聯網protocolhandler) S送出(目的地ipaddress網路位元組order uint32, pprotocol uint8, 資料指標 uintptr, 大小 uint32) {

	互聯網路協定提供器.S送出(目的地ipaddress網路位元組order, pprotocol, 資料指標, 大小)
}
func (self *T互聯網protocolhandler) Providerget() *T互聯網路協定提供器 {
	return &互聯網路協定提供器
}

type Ip乙太網路框架handler struct {
	T乙太網路框架handler
}

var 互聯網路協定提供器 T互聯網路協定提供器

func (self *Ip乙太網路框架handler) O乙太網路框架receivewhen(資料指標 uintptr, 大小 int) bool {
	ip控制台.M列印(([]byte)("iphandler:onEtherfameRecv\n"))
	return 互聯網路協定提供器.O乙太網路框架receivewhen(資料指標, uint32(大小))

}

func (self *Ip乙太網路框架handler) S送出(目的地ipaddress網路位元組order uint64, 資料指標 uintptr, 大小 uint32) {
	ip控制台.M列印(([]byte)("ipefhandler:send\n"))
	var 乙太網路類型be = Unsignedinteger16r(0x0800)
	self.T乙太網路框架handler.S框架送出(目的地ipaddress網路位元組order, 乙太網路類型be, 資料指標, 大小)

}

var handler_2 [255]I互聯網protocolhandler

type T互聯網路協定提供器 struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnet遮罩	uint32
}

var efhandler I乙太網路框架handler

func (self *T互聯網路協定提供器) Init(pefprovider T共享媒介網路框提供器, pefhandler I乙太網路框架handler, arp Arpprovider, gatewayip uint32, subnet遮罩 uint32) {

	efhandler = pefhandler
	efhandler.S設定handler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnet遮罩 = subnet遮罩
	互聯網路協定提供器 = *self
}
func (self *T互聯網路協定提供器) O乙太網路框架receivewhen(乙太網路框架payload uintptr, 大小 uint32) bool {
	if 大小 < uint32(ip大小) {
		return false
	}

	var buffer_2 *T互聯網protocolv4訊息buffer = (*T互聯網protocolv4訊息buffer)(Pointer(乙太網路框架payload))
	var 互聯網protocol訊息 T互聯網protocolv4訊息
	互聯網protocol訊息.Init(*buffer_2)

	var reply bool = false

	if 互聯網protocol訊息.目的地ipaddress == uint32(efhandler.Getipaddress()) {

		var 長度 uint32 = uint32(互聯網protocol訊息.總數長度)
		if 長度 > 大小 {
			長度 = 大小
		}
		if handler_2[互聯網protocol訊息.protocol] != nil {
			reply = handler_2[互聯網protocol訊息.protocol].O互聯網protocolreceivewhen(互聯網protocol訊息.來源ipaddress, 互聯網protocol訊息.目的地ipaddress, 乙太網路框架payload+uintptr(4*互聯網protocol訊息.標頭長度), uint32(長度-uint32(4*互聯網protocol訊息.標頭長度)))

		}
	}

	if reply {

		var temporary = 互聯網protocol訊息.目的地ipaddress
		互聯網protocol訊息.目的地ipaddress = 互聯網protocol訊息.來源ipaddress
		互聯網protocol訊息.來源ipaddress = temporary

		互聯網protocol訊息.時間tolive = 0x40
		互聯網protocol訊息.checksum = 0

		互聯網protocol訊息.S設定buffer(buffer_2)
		互聯網protocol訊息.checksum = self.Checksum((*([4096]uint16))(Pointer(乙太網路框架payload)), uint32(4*互聯網protocol訊息.標頭長度))

		互聯網protocol訊息.S設定buffer(buffer_2)

	}

	ip控制台.M列印(([]byte)("ipmessage"))
	ip控制台.MUnsignedinteger32列印(互聯網protocol訊息.來源ipaddress)
	ip控制台.M列印(([]byte)(":"))
	ip控制台.MUnsignedinteger32列印(互聯網protocol訊息.目的地ipaddress)
	ip控制台.M列印(([]byte)(":"))
	ip控制台.MUnsignedinteger16列印(uint16(互聯網protocol訊息.標頭長度))
	ip控制台.M列印(([]byte)(":"))
	ip控制台.MUnsignedinteger16列印(uint16(互聯網protocol訊息.版本))
	ip控制台.M列印(([]byte)(":"))
	ip控制台.MUnsignedinteger16列印(互聯網protocol訊息.總數長度)
	ip控制台.M列印(([]byte)(":"))
	ip控制台.MUnsignedinteger32列印(uint32(efhandler.Getipaddress()))
	ip控制台.M列印(([]byte)(":"))
	ip控制台.M列印(([]byte)("\n"))

	return reply

}
func (self *T互聯網路協定提供器) S送出(目的地ipaddress網路位元組order uint32, protocol uint8, 資料指標 uintptr, 大小 uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *T互聯網protocolv4訊息buffer = (*T互聯網protocolv4訊息buffer)(Pointer(&buffer1_2))
	var 訊息 T互聯網protocolv4訊息 = T互聯網protocolv4訊息{}
	訊息.版本 = 4
	訊息.標頭長度 = ip大小 / 4
	訊息.tos = 0
	訊息.總數長度 = Unsignedinteger16r(uint16(大小 + uint32(ip大小)))

	訊息.ident = 0x0100
	訊息.旗標和位移 = 0x0040
	訊息.時間tolive = 0x40
	訊息.protocol = protocol

	訊息.目的地ipaddress = 目的地ipaddress網路位元組order

	訊息.來源ipaddress = uint32(efhandler.Getipaddress())

	訊息.checksum = 0

	訊息.S設定buffer(buffer_2)
	訊息.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ip大小))
	訊息.S設定buffer(buffer_2)

	var 資料buffer_2 [4096]byte = *(*([4096]byte))(Pointer(資料指標))

	for i := 0; i < int(大小); i++ {

		buffer1_2[i+int(ip大小)] = 資料buffer_2[i]
	}

	ip控制台.M列印xy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(大小)+int(ip大小); i++ {
		ip控制台.MHexadecimal列印(buffer1_2[i])
	}
	ip控制台.M列印(([]byte)(":"))
	ip控制台.M列印(([]byte)("]\n"))

	var 下一個hopipaddress網路位元組order uint32 = 目的地ipaddress網路位元組order
	if (目的地ipaddress網路位元組order & self.Subnet遮罩) != (訊息.來源ipaddress & self.Subnet遮罩) {
		下一個hopipaddress網路位元組order = self.Gatewayip
	}

	var 送出資料指標 = uintptr(Pointer(&buffer1_2))
	ip控制台.MUnsignedinteger32列印(下一個hopipaddress網路位元組order)

	var 乙太網路類型be = Unsignedinteger16r(0x0800)
	efhandler.S框架送出(self.arpprovider.R解決(下一個hopipaddress網路位元組order), 乙太網路類型be, 送出資料指標, uint32(ip大小)+uint32(大小))

}
func (self *T互聯網路協定提供器) Checksum(p資料 *[4096]uint16, 長度進位元組 uint32) uint16 {
	var 資料 [4096]uint16 = *p資料
	var temporary uint32 = 0
	var 資料位元組 [4096]byte = *(*([4096]byte))(Pointer(&資料))
	if (長度進位元組 % 2) != 0 {
		temporary += uint32(uint16(資料位元組[長度進位元組-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *T互聯網路協定提供器) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
