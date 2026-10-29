/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 互聯網路控制訊息協定

import . "unsafe"
import . "控制台"
import . "記憶體管理器"
import . "共享媒介網路框"
import . "互聯網路協定4"
import . "工具"

var icmp控制台 = T控制台{}

type T互聯網控制訊息protocol訊息buffer struct {
	T類型	byte
	code	byte

	checksum	[2]byte
	資料		[4]byte
}

var icmp大小 int = 64

type T互聯網控制訊息protocol訊息 struct {
	T類型	uint8
	code	uint8

	checksum	uint16
	資料		uint32
}

func (self *T互聯網控制訊息protocol訊息) Init(buffer_2 T互聯網控制訊息protocol訊息buffer) {
	self.T類型 = buffer_2.T類型
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(A陣列tounsignedinteger16(buffer_2.checksum))
	self.資料 = Unsignedinteger32r(A陣列tounsignedinteger32(buffer_2.資料))
}

func (self *T互聯網控制訊息protocol訊息) S設定buffer(buffer_2 *T互聯網控制訊息protocol訊息buffer) {
	buffer_2.T類型 = self.T類型
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16to陣列(self.checksum)
	buffer_2.資料 = Unsignedinteger32to陣列(self.資料)
}

type Icmphandler struct {
	T互聯網protocolhandler
}

var 互聯網路控制訊息協定 *T互聯網路控制訊息協定

func (self *Icmphandler) O互聯網protocolreceivewhen(來源ipaddress網路位元組order uint32, 目的地ipaddress網路位元組order uint32, 資料指標 uintptr, 大小 uint32) bool {
	return 互聯網路控制訊息協定.O互聯網protocolreceivewhen(來源ipaddress網路位元組order, 目的地ipaddress網路位元組order, 資料指標, 大小)
}

var iphandler I互聯網protocolhandler

type T互聯網路控制訊息協定 struct {
}

func (self *T互聯網路控制訊息協定) Init(backend T互聯網路協定提供器, handler I互聯網protocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	互聯網路控制訊息協定 = self
}
func (self *T互聯網路控制訊息協定) O互聯網protocolreceivewhen(來源ipaddress網路位元組order uint32, 目的地ipaddress網路位元組order uint32, 資料指標 uintptr, 大小 uint32) bool {
	if 大小 < uint32(icmp大小) {
		return false
	}

	var buffer_2 *T互聯網控制訊息protocol訊息buffer = (*T互聯網控制訊息protocol訊息buffer)(Pointer(資料指標))
	var msg T互聯網控制訊息protocol訊息 = T互聯網控制訊息protocol訊息{}
	msg.Init(*buffer_2)

	icmp控制台.M列印(([]byte)("icmp:OnInternet"))
	icmp控制台.MUnsignedinteger16列印(uint16(msg.T類型))
	icmp控制台.M列印(([]byte)(":"))

	switch msg.T類型 {
	case 0:
		icmp控制台.M列印(([]byte)("ping response from "))
		break

	case 8:
		icmp控制台.M列印(([]byte)("ping send "))
		msg.T類型 = 0

		msg.checksum = 0
		msg.S設定buffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(資料指標)), uint32(icmp大小))

		msg.S設定buffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *T互聯網路控制訊息協定) Echorequest送出(ip網路位元組order uint32) bool {
	var 互聯網路控制訊息協定 T互聯網控制訊息protocol訊息 = T互聯網控制訊息protocol訊息{}

	var 記憶體管理器 = &T記憶體管理器{}
	var buffer_2 = (*T互聯網控制訊息protocol訊息buffer)(記憶體管理器.M配置記憶體(1024))

	互聯網路控制訊息協定.T類型 = 8
	互聯網路控制訊息協定.code = 0
	互聯網路控制訊息協定.資料 = 0x3713
	互聯網路控制訊息協定.checksum = 0
	互聯網路控制訊息協定.S設定buffer(buffer_2)
	互聯網路控制訊息協定.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmp大小))
	互聯網路控制訊息協定.S設定buffer(buffer_2)

	var 資料指標 uintptr = uintptr(Pointer(buffer_2))
	iphandler.S送出(ip網路位元組order, 0x01, 資料指標, uint32(icmp大小))

	return false

}
