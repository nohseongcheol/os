package ソウゴセツゾクアミセイギョデンブンキヤク

import . "unsafe"
import . "コンソール"
import . "メモリカンリシャ"
import . "キョウユウバイタイモウデンソウワク"
import . "ソウゴセツゾクアミキヤク4"
import . "ハンヨウ"

var icmpコンソール = Tコンソール{}

type Tインターネットセイギョメッセージprotocolメッセージbuffer struct {
	Tカタ	byte
	code	byte

	checksum	[2]byte
	データ		[4]byte
}

var icmpサイズ int = 64

type Tインターネットセイギョメッセージprotocolメッセージ struct {
	Tカタ	uint8
	code	uint8

	checksum	uint16
	データ		uint32
}

func (self *Tインターネットセイギョメッセージprotocolメッセージ) Init(buffer_2 Tインターネットセイギョメッセージprotocolメッセージbuffer) {
	self.Tカタ = buffer_2.Tカタ
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer_2.checksum))
	self.データ = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer_2.データ))
}

func (self *Tインターネットセイギョメッセージprotocolメッセージ) Sアリbuffer(buffer_2 *Tインターネットセイギョメッセージprotocolメッセージbuffer) {
	buffer_2.Tカタ = self.Tカタ
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toハイレツ(self.checksum)
	buffer_2.データ = Unsignedinteger32toハイレツ(self.データ)
}

type Icmphandler struct {
	Tインターネットprotocolhandler
}

var ソウゴセツゾクアミセイギョデンブンキヤク *Tソウゴセツゾクアミセイギョデンブンキヤク

func (self *Icmphandler) Oインターネットprotocolreceivewhen(テンソウモトipaddressネットワークバイトorder uint32, テンソウサキipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool {
	return ソウゴセツゾクアミセイギョデンブンキヤク.Oインターネットprotocolreceivewhen(テンソウモトipaddressネットワークバイトorder, テンソウサキipaddressネットワークバイトorder, データポインタ, サイズ)
}

var iphandler Iインターネットprotocolhandler

type Tソウゴセツゾクアミセイギョデンブンキヤク struct {
}

func (self *Tソウゴセツゾクアミセイギョデンブンキヤク) Init(backend Tソウゴセツゾクアミキヤクテイキョウウツワ, handler Iインターネットprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	ソウゴセツゾクアミセイギョデンブンキヤク = self
}
func (self *Tソウゴセツゾクアミセイギョデンブンキヤク) Oインターネットprotocolreceivewhen(テンソウモトipaddressネットワークバイトorder uint32, テンソウサキipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool {
	if サイズ < uint32(icmpサイズ) {
		return false
	}

	var buffer_2 *Tインターネットセイギョメッセージprotocolメッセージbuffer = (*Tインターネットセイギョメッセージprotocolメッセージbuffer)(Pointer(データポインタ))
	var msg Tインターネットセイギョメッセージprotocolメッセージ = Tインターネットセイギョメッセージprotocolメッセージ{}
	msg.Init(*buffer_2)

	icmpコンソール.Mインサツ(([]byte)("icmp:OnInternet"))
	icmpコンソール.MUnsignedinteger16インサツ(uint16(msg.Tカタ))
	icmpコンソール.Mインサツ(([]byte)(":"))

	switch msg.Tカタ {
	case 0:
		icmpコンソール.Mインサツ(([]byte)("ping response from "))
		break

	case 8:
		icmpコンソール.Mインサツ(([]byte)("ping send "))
		msg.Tカタ = 0

		msg.checksum = 0
		msg.Sアリbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(データポインタ)), uint32(icmpサイズ))

		msg.Sアリbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *Tソウゴセツゾクアミセイギョデンブンキヤク) Echorequestソウシン(ipネットワークバイトorder uint32) bool {
	var ソウゴセツゾクアミセイギョデンブンキヤク Tインターネットセイギョメッセージprotocolメッセージ = Tインターネットセイギョメッセージprotocolメッセージ{}

	var メモリカンリシャ = &Tメモリカンリシャ{}
	var buffer_2 = (*Tインターネットセイギョメッセージprotocolメッセージbuffer)(メモリカンリシャ.Mキオクリョウイキヲカクホ(1024))

	ソウゴセツゾクアミセイギョデンブンキヤク.Tカタ = 8
	ソウゴセツゾクアミセイギョデンブンキヤク.code = 0
	ソウゴセツゾクアミセイギョデンブンキヤク.データ = 0x3713
	ソウゴセツゾクアミセイギョデンブンキヤク.checksum = 0
	ソウゴセツゾクアミセイギョデンブンキヤク.Sアリbuffer(buffer_2)
	ソウゴセツゾクアミセイギョデンブンキヤク.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpサイズ))
	ソウゴセツゾクアミセイギョデンブンキヤク.Sアリbuffer(buffer_2)

	var データポインタ uintptr = uintptr(Pointer(buffer_2))
	iphandler.Sソウシン(ipネットワークバイトorder, 0x01, データポインタ, uint32(icmpサイズ))

	return false

}
