/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ソウゴセツゾクアミキヤク4

import . "unsafe"
import . "ハンヨウ"
import . "コンソール"
import . "キョウユウバイタイモウデンソウワク"
import . "arp"

var ipコンソール Tコンソール = Tコンソール{}

type Tインターネットprotocolv4メッセージbuffer struct {
	lenver	byte
	tos	byte
	ゴウケイナガサ	[2]byte

	ident		[2]byte
	フラグトoffset	[2]byte

	ジカンtolive	byte
	protocol	byte
	checksum	[2]byte

	テンソウモトipaddress	[4]byte
	テンソウサキipaddress	[4]byte
}

var ipサイズ uint8 = (4 + 4 + 4 + 8)

type Tインターネットprotocolv4メッセージ struct {
	ヘッダナガサ	uint8
	バージョン	uint8
	tos	uint8
	ゴウケイナガサ	uint16

	ident		uint16
	フラグトoffset	uint16

	ジカンtolive	uint8
	protocol	uint8
	checksum	uint16

	テンソウモトipaddress	uint32
	テンソウサキipaddress	uint32
}

func (self *Tインターネットprotocolv4メッセージ) Init(buffer_2 Tインターネットprotocolv4メッセージbuffer) {

	self.バージョン = ((buffer_2.lenver & 0xF0) >> 4)
	self.ヘッダナガサ = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.ゴウケイナガサ = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.ゴウケイナガサ))

	self.ident = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.ident))
	self.フラグトoffset = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.フラグトoffset))

	self.ジカンtolive = buffer_2.ジカンtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.checksum))

	self.テンソウモトipaddress = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer_2.テンソウモトipaddress))
	self.テンソウサキipaddress = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer_2.テンソウサキipaddress))

}
func (self *Tインターネットprotocolv4メッセージ) Sアリbuffer(buffer_2 *Tインターネットprotocolv4メッセージbuffer) {

	buffer_2.lenver = byte(((self.バージョン & 0x0F) << 4) | (self.ヘッダナガサ & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.ゴウケイナガサ = Unsignedinteger16toハイレツ(self.ゴウケイナガサ)

	buffer_2.ident = Unsignedinteger16toハイレツ(self.ident)
	buffer_2.フラグトoffset = Unsignedinteger16toハイレツ(self.フラグトoffset)

	buffer_2.ジカンtolive = self.ジカンtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toハイレツ(self.checksum)

	buffer_2.テンソウモトipaddress = Unsignedinteger32toハイレツ(self.テンソウモトipaddress)
	buffer_2.テンソウサキipaddress = Unsignedinteger32toハイレツ(self.テンソウサキipaddress)

}

type Iインターネットprotocolhandler interface {
	Init(backend Tソウゴセツゾクアミキヤクテイキョウウツワ, pihandler Iインターネットprotocolhandler, pprotocol uint8)
	Oインターネットprotocolreceivewhen(テンソウモトipaddressネットワークバイトorder uint32, テンソウサキipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool
	Sソウシン(テンソウサキipaddressネットワークバイトorder uint32, pprotocol uint8, データポインタ uintptr, サイズ uint32)
	Providerget() *Tソウゴセツゾクアミキヤクテイキョウウツワ
}

type Tインターネットprotocolhandler struct {
}

var ipイーサネットフレームhandler Ipイーサネットフレームhandler = Ipイーサネットフレームhandler{}
var protocol uint8

func (self *Tインターネットprotocolhandler) Init(backend Tソウゴセツゾクアミキヤクテイキョウウツワ, pihandler Iインターネットprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tインターネットprotocolhandler) Oインターネットprotocolreceivewhen(テンソウモトipaddressネットワークバイトorder uint32, テンソウサキipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool {
	ipコンソール.Mインサツ(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tインターネットprotocolhandler) Sソウシン(テンソウサキipaddressネットワークバイトorder uint32, pprotocol uint8, データポインタ uintptr, サイズ uint32) {

	ソウゴセツゾクアミキヤクテイキョウウツワ.Sソウシン(テンソウサキipaddressネットワークバイトorder, pprotocol, データポインタ, サイズ)
}
func (self *Tインターネットprotocolhandler) Providerget() *Tソウゴセツゾクアミキヤクテイキョウウツワ {
	return &ソウゴセツゾクアミキヤクテイキョウウツワ
}

type Ipイーサネットフレームhandler struct {
	Tイーサネットフレームhandler
}

var ソウゴセツゾクアミキヤクテイキョウウツワ Tソウゴセツゾクアミキヤクテイキョウウツワ

func (self *Ipイーサネットフレームhandler) Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool {
	ipコンソール.Mインサツ(([]byte)("iphandler:onEtherfameRecv\n"))
	return ソウゴセツゾクアミキヤクテイキョウウツワ.Oイーサネットフレームreceivewhen(データポインタ, uint32(サイズ))

}

func (self *Ipイーサネットフレームhandler) Sソウシン(テンソウサキipaddressネットワークバイトorder uint64, データポインタ uintptr, サイズ uint32) {
	ipコンソール.Mインサツ(([]byte)("ipefhandler:send\n"))
	var イーサネットカタbe = Unsignedinteger16r(0x0800)
	self.Tイーサネットフレームhandler.Sフレームソウシン(テンソウサキipaddressネットワークバイトorder, イーサネットカタbe, データポインタ, サイズ)

}

var handler_2 [255]Iインターネットprotocolhandler

type Tソウゴセツゾクアミキヤクテイキョウウツワ struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetマスク	uint32
}

var efhandler Iイーサネットフレームhandler

func (self *Tソウゴセツゾクアミキヤクテイキョウウツワ) Init(pefprovider Tキョウユウバイタイアミデンソウワクテイキョウウツワ, pefhandler Iイーサネットフレームhandler, arp Arpprovider, gatewayip uint32, subnetマスク uint32) {

	efhandler = pefhandler
	efhandler.Sアリhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetマスク = subnetマスク
	ソウゴセツゾクアミキヤクテイキョウウツワ = *self
}
func (self *Tソウゴセツゾクアミキヤクテイキョウウツワ) Oイーサネットフレームreceivewhen(イーサネットフレームpayload uintptr, サイズ uint32) bool {
	if サイズ < uint32(ipサイズ) {
		return false
	}

	var buffer_2 *Tインターネットprotocolv4メッセージbuffer = (*Tインターネットprotocolv4メッセージbuffer)(Pointer(イーサネットフレームpayload))
	var インターネットprotocolメッセージ Tインターネットprotocolv4メッセージ
	インターネットprotocolメッセージ.Init(*buffer_2)

	var reply bool = false

	if インターネットprotocolメッセージ.テンソウサキipaddress == uint32(efhandler.Getipaddress()) {

		var ナガサ uint32 = uint32(インターネットprotocolメッセージ.ゴウケイナガサ)
		if ナガサ > サイズ {
			ナガサ = サイズ
		}
		if handler_2[インターネットprotocolメッセージ.protocol] != nil {
			reply = handler_2[インターネットprotocolメッセージ.protocol].Oインターネットprotocolreceivewhen(インターネットprotocolメッセージ.テンソウモトipaddress, インターネットprotocolメッセージ.テンソウサキipaddress, イーサネットフレームpayload+uintptr(4*インターネットprotocolメッセージ.ヘッダナガサ), uint32(ナガサ-uint32(4*インターネットprotocolメッセージ.ヘッダナガサ)))

		}
	}

	if reply {

		var temporary = インターネットprotocolメッセージ.テンソウサキipaddress
		インターネットprotocolメッセージ.テンソウサキipaddress = インターネットprotocolメッセージ.テンソウモトipaddress
		インターネットprotocolメッセージ.テンソウモトipaddress = temporary

		インターネットprotocolメッセージ.ジカンtolive = 0x40
		インターネットprotocolメッセージ.checksum = 0

		インターネットprotocolメッセージ.Sアリbuffer(buffer_2)
		インターネットprotocolメッセージ.checksum = self.Checksum((*([4096]uint16))(Pointer(イーサネットフレームpayload)), uint32(4*インターネットprotocolメッセージ.ヘッダナガサ))

		インターネットprotocolメッセージ.Sアリbuffer(buffer_2)

	}

	ipコンソール.Mインサツ(([]byte)("ipmessage"))
	ipコンソール.MUnsignedinteger32インサツ(インターネットprotocolメッセージ.テンソウモトipaddress)
	ipコンソール.Mインサツ(([]byte)(":"))
	ipコンソール.MUnsignedinteger32インサツ(インターネットprotocolメッセージ.テンソウサキipaddress)
	ipコンソール.Mインサツ(([]byte)(":"))
	ipコンソール.MUnsignedinteger16インサツ(uint16(インターネットprotocolメッセージ.ヘッダナガサ))
	ipコンソール.Mインサツ(([]byte)(":"))
	ipコンソール.MUnsignedinteger16インサツ(uint16(インターネットprotocolメッセージ.バージョン))
	ipコンソール.Mインサツ(([]byte)(":"))
	ipコンソール.MUnsignedinteger16インサツ(インターネットprotocolメッセージ.ゴウケイナガサ)
	ipコンソール.Mインサツ(([]byte)(":"))
	ipコンソール.MUnsignedinteger32インサツ(uint32(efhandler.Getipaddress()))
	ipコンソール.Mインサツ(([]byte)(":"))
	ipコンソール.Mインサツ(([]byte)("\n"))

	return reply

}
func (self *Tソウゴセツゾクアミキヤクテイキョウウツワ) Sソウシン(テンソウサキipaddressネットワークバイトorder uint32, protocol uint8, データポインタ uintptr, サイズ uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tインターネットprotocolv4メッセージbuffer = (*Tインターネットprotocolv4メッセージbuffer)(Pointer(&buffer1_2))
	var メッセージ Tインターネットprotocolv4メッセージ = Tインターネットprotocolv4メッセージ{}
	メッセージ.バージョン = 4
	メッセージ.ヘッダナガサ = ipサイズ / 4
	メッセージ.tos = 0
	メッセージ.ゴウケイナガサ = Unsignedinteger16r(uint16(サイズ + uint32(ipサイズ)))

	メッセージ.ident = 0x0100
	メッセージ.フラグトoffset = 0x0040
	メッセージ.ジカンtolive = 0x40
	メッセージ.protocol = protocol

	メッセージ.テンソウサキipaddress = テンソウサキipaddressネットワークバイトorder

	メッセージ.テンソウモトipaddress = uint32(efhandler.Getipaddress())

	メッセージ.checksum = 0

	メッセージ.Sアリbuffer(buffer_2)
	メッセージ.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipサイズ))
	メッセージ.Sアリbuffer(buffer_2)

	var データbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(データポインタ))

	for i := 0; i < int(サイズ); i++ {

		buffer1_2[i+int(ipサイズ)] = データbuffer_2[i]
	}

	ipコンソール.Mインサツxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(サイズ)+int(ipサイズ); i++ {
		ipコンソール.MHexadecimalインサツ(buffer1_2[i])
	}
	ipコンソール.Mインサツ(([]byte)(":"))
	ipコンソール.Mインサツ(([]byte)("]\n"))

	var ツギhopipaddressネットワークバイトorder uint32 = テンソウサキipaddressネットワークバイトorder
	if (テンソウサキipaddressネットワークバイトorder & self.Subnetマスク) != (メッセージ.テンソウモトipaddress & self.Subnetマスク) {
		ツギhopipaddressネットワークバイトorder = self.Gatewayip
	}

	var ソウシンデータポインタ = uintptr(Pointer(&buffer1_2))
	ipコンソール.MUnsignedinteger32インサツ(ツギhopipaddressネットワークバイトorder)

	var イーサネットカタbe = Unsignedinteger16r(0x0800)
	efhandler.Sフレームソウシン(self.arpprovider.Rカイケツ(ツギhopipaddressネットワークバイトorder), イーサネットカタbe, ソウシンデータポインタ, uint32(ipサイズ)+uint32(サイズ))

}
func (self *Tソウゴセツゾクアミキヤクテイキョウウツワ) Checksum(pデータ *[4096]uint16, ナガサジュシンバイト uint32) uint16 {
	var データ [4096]uint16 = *pデータ
	var temporary uint32 = 0
	var データバイト [4096]byte = *(*([4096]byte))(Pointer(&データ))
	if (ナガサジュシンバイト % 2) != 0 {
		temporary += uint32(uint16(データバイト[ナガサジュシンバイト-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *Tソウゴセツゾクアミキヤクテイキョウウツワ) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
