/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 相互接続網規約4

import . "unsafe"
import . "汎用"
import . "コンソール"
import . "共有媒体網伝送枠"
import . "arp"

var ipコンソール Tコンソール = Tコンソール{}

type Tインターネットprotocolv4メッセージbuffer struct {
	lenver	byte
	tos	byte
	合計長さ	[2]byte

	ident		[2]byte
	フラグとoffset	[2]byte

	時間tolive	byte
	protocol	byte
	checksum	[2]byte

	転送元ipaddress	[4]byte
	転送先ipaddress	[4]byte
}

var ipサイズ uint8 = (4 + 4 + 4 + 8)

type Tインターネットprotocolv4メッセージ struct {
	ヘッダ長さ	uint8
	バージョン	uint8
	tos	uint8
	合計長さ	uint16

	ident		uint16
	フラグとoffset	uint16

	時間tolive	uint8
	protocol	uint8
	checksum	uint16

	転送元ipaddress	uint32
	転送先ipaddress	uint32
}

func (self *Tインターネットprotocolv4メッセージ) Init(buffer_2 Tインターネットprotocolv4メッセージbuffer) {

	self.バージョン = ((buffer_2.lenver & 0xF0) >> 4)
	self.ヘッダ長さ = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.合計長さ = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.合計長さ))

	self.ident = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.ident))
	self.フラグとoffset = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.フラグとoffset))

	self.時間tolive = buffer_2.時間tolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.checksum))

	self.転送元ipaddress = Unsignedinteger32r(A配列tounsignedinteger32(buffer_2.転送元ipaddress))
	self.転送先ipaddress = Unsignedinteger32r(A配列tounsignedinteger32(buffer_2.転送先ipaddress))

}
func (self *Tインターネットprotocolv4メッセージ) Sありbuffer(buffer_2 *Tインターネットprotocolv4メッセージbuffer) {

	buffer_2.lenver = byte(((self.バージョン & 0x0F) << 4) | (self.ヘッダ長さ & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.合計長さ = Unsignedinteger16to配列(self.合計長さ)

	buffer_2.ident = Unsignedinteger16to配列(self.ident)
	buffer_2.フラグとoffset = Unsignedinteger16to配列(self.フラグとoffset)

	buffer_2.時間tolive = self.時間tolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16to配列(self.checksum)

	buffer_2.転送元ipaddress = Unsignedinteger32to配列(self.転送元ipaddress)
	buffer_2.転送先ipaddress = Unsignedinteger32to配列(self.転送先ipaddress)

}

type Iインターネットprotocolhandler interface {
	Init(backend T相互接続網規約提供器, pihandler Iインターネットprotocolhandler, pprotocol uint8)
	Oインターネットprotocolreceivewhen(転送元ipaddressネットワークバイトorder uint32, 転送先ipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool
	S送信(転送先ipaddressネットワークバイトorder uint32, pprotocol uint8, データポインタ uintptr, サイズ uint32)
	Providerget() *T相互接続網規約提供器
}

type Tインターネットprotocolhandler struct {
}

var ipイーサネットフレームhandler Ipイーサネットフレームhandler = Ipイーサネットフレームhandler{}
var protocol uint8

func (self *Tインターネットprotocolhandler) Init(backend T相互接続網規約提供器, pihandler Iインターネットprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tインターネットprotocolhandler) Oインターネットprotocolreceivewhen(転送元ipaddressネットワークバイトorder uint32, 転送先ipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool {
	ipコンソール.M印刷(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tインターネットprotocolhandler) S送信(転送先ipaddressネットワークバイトorder uint32, pprotocol uint8, データポインタ uintptr, サイズ uint32) {

	相互接続網規約提供器.S送信(転送先ipaddressネットワークバイトorder, pprotocol, データポインタ, サイズ)
}
func (self *Tインターネットprotocolhandler) Providerget() *T相互接続網規約提供器 {
	return &相互接続網規約提供器
}

type Ipイーサネットフレームhandler struct {
	Tイーサネットフレームhandler
}

var 相互接続網規約提供器 T相互接続網規約提供器

func (self *Ipイーサネットフレームhandler) Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool {
	ipコンソール.M印刷(([]byte)("iphandler:onEtherfameRecv\n"))
	return 相互接続網規約提供器.Oイーサネットフレームreceivewhen(データポインタ, uint32(サイズ))

}

func (self *Ipイーサネットフレームhandler) S送信(転送先ipaddressネットワークバイトorder uint64, データポインタ uintptr, サイズ uint32) {
	ipコンソール.M印刷(([]byte)("ipefhandler:send\n"))
	var イーサネット型be = Unsignedinteger16r(0x0800)
	self.Tイーサネットフレームhandler.Sフレーム送信(転送先ipaddressネットワークバイトorder, イーサネット型be, データポインタ, サイズ)

}

var handler_2 [255]Iインターネットprotocolhandler

type T相互接続網規約提供器 struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetマスク	uint32
}

var efhandler Iイーサネットフレームhandler

func (self *T相互接続網規約提供器) Init(pefprovider T共有媒体網伝送枠提供器, pefhandler Iイーサネットフレームhandler, arp Arpprovider, gatewayip uint32, subnetマスク uint32) {

	efhandler = pefhandler
	efhandler.Sありhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetマスク = subnetマスク
	相互接続網規約提供器 = *self
}
func (self *T相互接続網規約提供器) Oイーサネットフレームreceivewhen(イーサネットフレームpayload uintptr, サイズ uint32) bool {
	if サイズ < uint32(ipサイズ) {
		return false
	}

	var buffer_2 *Tインターネットprotocolv4メッセージbuffer = (*Tインターネットprotocolv4メッセージbuffer)(Pointer(イーサネットフレームpayload))
	var インターネットprotocolメッセージ Tインターネットprotocolv4メッセージ
	インターネットprotocolメッセージ.Init(*buffer_2)

	var reply bool = false

	if インターネットprotocolメッセージ.転送先ipaddress == uint32(efhandler.Getipaddress()) {

		var 長さ uint32 = uint32(インターネットprotocolメッセージ.合計長さ)
		if 長さ > サイズ {
			長さ = サイズ
		}
		if handler_2[インターネットprotocolメッセージ.protocol] != nil {
			reply = handler_2[インターネットprotocolメッセージ.protocol].Oインターネットprotocolreceivewhen(インターネットprotocolメッセージ.転送元ipaddress, インターネットprotocolメッセージ.転送先ipaddress, イーサネットフレームpayload+uintptr(4*インターネットprotocolメッセージ.ヘッダ長さ), uint32(長さ-uint32(4*インターネットprotocolメッセージ.ヘッダ長さ)))

		}
	}

	if reply {

		var temporary = インターネットprotocolメッセージ.転送先ipaddress
		インターネットprotocolメッセージ.転送先ipaddress = インターネットprotocolメッセージ.転送元ipaddress
		インターネットprotocolメッセージ.転送元ipaddress = temporary

		インターネットprotocolメッセージ.時間tolive = 0x40
		インターネットprotocolメッセージ.checksum = 0

		インターネットprotocolメッセージ.Sありbuffer(buffer_2)
		インターネットprotocolメッセージ.checksum = self.Checksum((*([4096]uint16))(Pointer(イーサネットフレームpayload)), uint32(4*インターネットprotocolメッセージ.ヘッダ長さ))

		インターネットprotocolメッセージ.Sありbuffer(buffer_2)

	}

	ipコンソール.M印刷(([]byte)("ipmessage"))
	ipコンソール.MUnsignedinteger32印刷(インターネットprotocolメッセージ.転送元ipaddress)
	ipコンソール.M印刷(([]byte)(":"))
	ipコンソール.MUnsignedinteger32印刷(インターネットprotocolメッセージ.転送先ipaddress)
	ipコンソール.M印刷(([]byte)(":"))
	ipコンソール.MUnsignedinteger16印刷(uint16(インターネットprotocolメッセージ.ヘッダ長さ))
	ipコンソール.M印刷(([]byte)(":"))
	ipコンソール.MUnsignedinteger16印刷(uint16(インターネットprotocolメッセージ.バージョン))
	ipコンソール.M印刷(([]byte)(":"))
	ipコンソール.MUnsignedinteger16印刷(インターネットprotocolメッセージ.合計長さ)
	ipコンソール.M印刷(([]byte)(":"))
	ipコンソール.MUnsignedinteger32印刷(uint32(efhandler.Getipaddress()))
	ipコンソール.M印刷(([]byte)(":"))
	ipコンソール.M印刷(([]byte)("\n"))

	return reply

}
func (self *T相互接続網規約提供器) S送信(転送先ipaddressネットワークバイトorder uint32, protocol uint8, データポインタ uintptr, サイズ uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tインターネットprotocolv4メッセージbuffer = (*Tインターネットprotocolv4メッセージbuffer)(Pointer(&buffer1_2))
	var メッセージ Tインターネットprotocolv4メッセージ = Tインターネットprotocolv4メッセージ{}
	メッセージ.バージョン = 4
	メッセージ.ヘッダ長さ = ipサイズ / 4
	メッセージ.tos = 0
	メッセージ.合計長さ = Unsignedinteger16r(uint16(サイズ + uint32(ipサイズ)))

	メッセージ.ident = 0x0100
	メッセージ.フラグとoffset = 0x0040
	メッセージ.時間tolive = 0x40
	メッセージ.protocol = protocol

	メッセージ.転送先ipaddress = 転送先ipaddressネットワークバイトorder

	メッセージ.転送元ipaddress = uint32(efhandler.Getipaddress())

	メッセージ.checksum = 0

	メッセージ.Sありbuffer(buffer_2)
	メッセージ.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipサイズ))
	メッセージ.Sありbuffer(buffer_2)

	var データbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(データポインタ))

	for i := 0; i < int(サイズ); i++ {

		buffer1_2[i+int(ipサイズ)] = データbuffer_2[i]
	}

	ipコンソール.M印刷xy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(サイズ)+int(ipサイズ); i++ {
		ipコンソール.MHexadecimal印刷(buffer1_2[i])
	}
	ipコンソール.M印刷(([]byte)(":"))
	ipコンソール.M印刷(([]byte)("]\n"))

	var 次hopipaddressネットワークバイトorder uint32 = 転送先ipaddressネットワークバイトorder
	if (転送先ipaddressネットワークバイトorder & self.Subnetマスク) != (メッセージ.転送元ipaddress & self.Subnetマスク) {
		次hopipaddressネットワークバイトorder = self.Gatewayip
	}

	var 送信データポインタ = uintptr(Pointer(&buffer1_2))
	ipコンソール.MUnsignedinteger32印刷(次hopipaddressネットワークバイトorder)

	var イーサネット型be = Unsignedinteger16r(0x0800)
	efhandler.Sフレーム送信(self.arpprovider.R解決(次hopipaddressネットワークバイトorder), イーサネット型be, 送信データポインタ, uint32(ipサイズ)+uint32(サイズ))

}
func (self *T相互接続網規約提供器) Checksum(pデータ *[4096]uint16, 長さ受信バイト uint32) uint16 {
	var データ [4096]uint16 = *pデータ
	var temporary uint32 = 0
	var データバイト [4096]byte = *(*([4096]byte))(Pointer(&データ))
	if (長さ受信バイト % 2) != 0 {
		temporary += uint32(uint16(データバイト[長さ受信バイト-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *T相互接続網規約提供器) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
