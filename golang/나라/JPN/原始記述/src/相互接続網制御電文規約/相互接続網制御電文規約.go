package 相互接続網制御電文規約

import . "unsafe"
import . "コンソール"
import . "メモリ管理者"
import . "共有媒体網伝送枠"
import . "相互接続網規約4"
import . "汎用"

var icmpコンソール = Tコンソール{}

type Tインターネット制御メッセージprotocolメッセージbuffer struct {
	T型	byte
	code	byte

	checksum	[2]byte
	データ		[4]byte
}

var icmpサイズ int = 64

type Tインターネット制御メッセージprotocolメッセージ struct {
	T型	uint8
	code	uint8

	checksum	uint16
	データ		uint32
}

func (self *Tインターネット制御メッセージprotocolメッセージ) Init(buffer_2 Tインターネット制御メッセージprotocolメッセージbuffer) {
	self.T型 = buffer_2.T型
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(A配列tounsignedinteger16(buffer_2.checksum))
	self.データ = Unsignedinteger32r(A配列tounsignedinteger32(buffer_2.データ))
}

func (self *Tインターネット制御メッセージprotocolメッセージ) Sありbuffer(buffer_2 *Tインターネット制御メッセージprotocolメッセージbuffer) {
	buffer_2.T型 = self.T型
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16to配列(self.checksum)
	buffer_2.データ = Unsignedinteger32to配列(self.データ)
}

type Icmphandler struct {
	Tインターネットprotocolhandler
}

var 相互接続網制御電文規約 *T相互接続網制御電文規約

func (self *Icmphandler) Oインターネットprotocolreceivewhen(転送元ipaddressネットワークバイトorder uint32, 転送先ipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool {
	return 相互接続網制御電文規約.Oインターネットprotocolreceivewhen(転送元ipaddressネットワークバイトorder, 転送先ipaddressネットワークバイトorder, データポインタ, サイズ)
}

var iphandler Iインターネットprotocolhandler

type T相互接続網制御電文規約 struct {
}

func (self *T相互接続網制御電文規約) Init(backend T相互接続網規約提供器, handler Iインターネットprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	相互接続網制御電文規約 = self
}
func (self *T相互接続網制御電文規約) Oインターネットprotocolreceivewhen(転送元ipaddressネットワークバイトorder uint32, 転送先ipaddressネットワークバイトorder uint32, データポインタ uintptr, サイズ uint32) bool {
	if サイズ < uint32(icmpサイズ) {
		return false
	}

	var buffer_2 *Tインターネット制御メッセージprotocolメッセージbuffer = (*Tインターネット制御メッセージprotocolメッセージbuffer)(Pointer(データポインタ))
	var msg Tインターネット制御メッセージprotocolメッセージ = Tインターネット制御メッセージprotocolメッセージ{}
	msg.Init(*buffer_2)

	icmpコンソール.M印刷(([]byte)("icmp:OnInternet"))
	icmpコンソール.MUnsignedinteger16印刷(uint16(msg.T型))
	icmpコンソール.M印刷(([]byte)(":"))

	switch msg.T型 {
	case 0:
		icmpコンソール.M印刷(([]byte)("ping response from "))
		break

	case 8:
		icmpコンソール.M印刷(([]byte)("ping send "))
		msg.T型 = 0

		msg.checksum = 0
		msg.Sありbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(データポインタ)), uint32(icmpサイズ))

		msg.Sありbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *T相互接続網制御電文規約) Echorequest送信(ipネットワークバイトorder uint32) bool {
	var 相互接続網制御電文規約 Tインターネット制御メッセージprotocolメッセージ = Tインターネット制御メッセージprotocolメッセージ{}

	var メモリ管理者 = &Tメモリ管理者{}
	var buffer_2 = (*Tインターネット制御メッセージprotocolメッセージbuffer)(メモリ管理者.M記憶領域を確保(1024))

	相互接続網制御電文規約.T型 = 8
	相互接続網制御電文規約.code = 0
	相互接続網制御電文規約.データ = 0x3713
	相互接続網制御電文規約.checksum = 0
	相互接続網制御電文規約.Sありbuffer(buffer_2)
	相互接続網制御電文規約.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpサイズ))
	相互接続網制御電文規約.Sありbuffer(buffer_2)

	var データポインタ uintptr = uintptr(Pointer(buffer_2))
	iphandler.S送信(ipネットワークバイトorder, 0x01, データポインタ, uint32(icmpサイズ))

	return false

}
