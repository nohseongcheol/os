/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package リヨウシャシリョウデンブンキヤク

import . "unsafe"
import . "コンソール"
import . "ハンヨウ"
import . "メモリカンリシャ"
import . "ソウゴセツゾクアミキヤク4"

var udpコンソール = Tコンソール{}

type Tリヨウシャdatagramprotocolヘッダbuffer struct {
	ソウシンモトセツゾクバンゴウ	[2]byte
	アテサキセツゾクバンゴウ	[2]byte

	ナガサ		[2]byte
	checksum	[2]byte
}

var udpヘッダサイズ uint32 = 8

type Tリヨウシャシリョウデンブンセントウブ struct {
	ソウシンモトセツゾクバンゴウ	uint16
	アテサキセツゾクバンゴウ	uint16

	ナガサ		uint16
	checksum	uint16
}

func (self *Tリヨウシャシリョウデンブンセントウブ) Init(buffer_2 *Tリヨウシャdatagramprotocolヘッダbuffer) {
	self.ソウシンモトセツゾクバンゴウ = Aハイレツtounsignedinteger16(buffer_2.ソウシンモトセツゾクバンゴウ)
	self.アテサキセツゾクバンゴウ = Aハイレツtounsignedinteger16(buffer_2.アテサキセツゾクバンゴウ)

	self.ナガサ = Aハイレツtounsignedinteger16(buffer_2.ナガサ)
	self.checksum = Aハイレツtounsignedinteger16(buffer_2.checksum)
}
func (self *Tリヨウシャシリョウデンブンセントウブ) Sアリbuffer(buffer_2 *Tリヨウシャdatagramprotocolヘッダbuffer) {

	buffer_2.ソウシンモトセツゾクバンゴウ = Unsignedinteger16toハイレツ(self.ソウシンモトセツゾクバンゴウ)
	buffer_2.アテサキセツゾクバンゴウ = Unsignedinteger16toハイレツ(self.アテサキセツゾクバンゴウ)

	buffer_2.ナガサ = Unsignedinteger16toハイレツ(self.ナガサ)
	buffer_2.checksum = Unsignedinteger16toハイレツ(self.checksum)

}

type Iリヨウシャdatagramprotocolhandler interface {
	Hトッテリヨウシャdatagramprotocolメッセージ(ソケット *Tリヨウシャシリョウデンブンツウシンタンテン, データ uintptr, サイズ uint16)
}

type Tリヨウシャdatagramprotocolhandler struct {
}

func (self *Tリヨウシャdatagramprotocolhandler) Init(backend Tソウゴセツゾクアミキヤクテイキョウウツワ) {
}
func (self *Tリヨウシャdatagramprotocolhandler) Hトッテリヨウシャdatagramprotocolメッセージ(ソケット *Tリヨウシャシリョウデンブンツウシンタンテン, データ uintptr, サイズ uint16) {
}

type Iリヨウシャdatagramprotocolソケット interface {
	Hトッテリヨウシャdatagramprotocolメッセージ(データ uintptr, サイズ uint16)
}
type Tリヨウシャシリョウデンブンツウシンタンテン struct {
	リモートポートnumber	uint16
	リモートip		uint32
	ローカルポートnumber	uint16
	ローカルip		uint32

	listening	bool
}

var udpprovider Tリヨウシャdatagramprotocolprovider
var udphandler Iリヨウシャdatagramprotocolhandler

func (self *Tリヨウシャシリョウデンブンツウシンタンテン) Tテスト() {
}
func (self *Tリヨウシャシリョウデンブンツウシンタンテン) Init(pudpprovider Tリヨウシャdatagramprotocolprovider, pudphandler Iリヨウシャdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *Tリヨウシャシリョウデンブンツウシンタンテン) Hトッテリヨウシャdatagramprotocolメッセージ(データ uintptr, サイズ uint16) {
	if udphandler != nil {
		udphandler.Hトッテリヨウシャdatagramprotocolメッセージ(self, データ, サイズ)
	}
}
func (self *Tリヨウシャシリョウデンブンツウシンタンテン) Sソウシン(pデータ []byte, サイズ uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(サイズ); i++ {
		buffer_2[i] = pデータ[i]
	}
	var データ = uintptr(Pointer(&buffer_2))
	udpprovider.Sソウシン(self, データ, サイズ)
}
func (self *Tリヨウシャシリョウデンブンツウシンタンテン) Dセツダンスル() {
	udpprovider.Dセツダンスル(self)
}

type Tリヨウシャdatagramprotocolprovider struct {
}

var iphandler Iインターネットprotocolhandler
var sockets [65535]Tリヨウシャシリョウデンブンツウシンタンテン
var numbersockets int
var アキポート uint16

func (self *Tリヨウシャdatagramprotocolprovider) Init(pipprovider Tソウゴセツゾクアミキヤクテイキョウウツワ, piphandler Iインターネットprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	アキポート = 1024
}
func (self *Tリヨウシャdatagramprotocolprovider) Oインターネットprotocolreceivewhen(テンソウモトipaddressネットワークバイトorder uint32, テンソウサキipaddressネットワークバイトorder uint32, インターネットprotocolpayload uintptr, サイズ uint32) bool {
	if サイズ < udpヘッダサイズ {
		return false
	}

	var buffer_2 *Tリヨウシャdatagramprotocolヘッダbuffer = (*Tリヨウシャdatagramprotocolヘッダbuffer)(Pointer(インターネットprotocolpayload))
	var msg Tリヨウシャシリョウデンブンセントウブ
	msg.Init(buffer_2)

	var ソケット *Tリヨウシャシリョウデンブンツウシンタンテン = nil

	for i := 0; i < numbersockets && ソケット == nil; i++ {
		if sockets[i].ローカルポートnumber == msg.アテサキセツゾクバンゴウ && sockets[i].ローカルip == テンソウサキipaddressネットワークバイトorder && sockets[i].listening == true {
			ソケット = &sockets[i]
			ソケット.listening = false
			ソケット.リモートポートnumber = msg.ソウシンモトセツゾクバンゴウ
			ソケット.リモートip = テンソウモトipaddressネットワークバイトorder
		} else if sockets[i].ローカルポートnumber == msg.アテサキセツゾクバンゴウ && sockets[i].ローカルip == テンソウサキipaddressネットワークバイトorder && sockets[i].リモートポートnumber == msg.ソウシンモトセツゾクバンゴウ && sockets[i].リモートip == テンソウモトipaddressネットワークバイトorder {
			ソケット = &sockets[i]

		}
	}

	msg.Sアリbuffer(buffer_2)
	if ソケット != nil {
		ソケット.Hトッテリヨウシャdatagramprotocolメッセージ(インターネットprotocolpayload+uintptr(udpヘッダサイズ), uint16(サイズ-udpヘッダサイズ))
	}

	return false
}

func (self *Tリヨウシャdatagramprotocolprovider) Cセツゾク(ip uint32, ポート uint16) *Tリヨウシャシリョウデンブンツウシンタンテン {
	var メモリカンリシャ = &Tメモリカンリシャ{}
	var ソケット = (*Tリヨウシャシリョウデンブンツウシンタンテン)(メモリカンリシャ.Mキオクリョウイキヲカクホ(50))

	if ソケット != nil {

		ソケット.Init(*self, nil)
		ソケット.リモートポートnumber = ポート
		ソケット.リモートip = ip
		ソケット.ローカルポートnumber = アキポート
		アキポート++
		ソケット.ローカルip = uint32((*iphandler.Providerget()).Getipaddress())

		ソケット.リモートポートnumber = Unsignedinteger16r(ソケット.リモートポートnumber)
		ソケット.ローカルポートnumber = Unsignedinteger16r(ソケット.ローカルポートnumber)

		sockets[numbersockets] = *ソケット
		numbersockets++

	}
	return ソケット

}
func (self *Tリヨウシャdatagramprotocolprovider) Listen(ポート uint16) *Tリヨウシャシリョウデンブンツウシンタンテン {
	var ソケット = &Tリヨウシャシリョウデンブンツウシンタンテン{}
	ソケット = nil
	if ソケット != nil {
		ソケット.Init(*self, nil)
		ソケット.listening = true
		ソケット.ローカルポートnumber = ポート
		ソケット.ローカルip = uint32((*iphandler.Providerget()).Getipaddress())

		ソケット.ローカルポートnumber = Unsignedinteger16r(ソケット.ローカルポートnumber)
	}
	return ソケット
}
func (self *Tリヨウシャdatagramprotocolprovider) Dセツダンスル(ソケット *Tリヨウシャシリョウデンブンツウシンタンテン) {
	for i := 0; i < numbersockets && ソケット == nil; i++ {
		if sockets[i] == *ソケット {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *Tリヨウシャdatagramprotocolprovider) Sソウシン(ソケット *Tリヨウシャシリョウデンブンツウシンタンテン, pデータ uintptr, サイズ uint16) {
	var ゴウケイナガサ = uint32(サイズ) + udpヘッダサイズ

	var buffer_2 [4096]byte

	var msgbuffer = (*Tリヨウシャdatagramprotocolヘッダbuffer)(Pointer(&buffer_2))

	var msg = Tリヨウシャシリョウデンブンセントウブ{}

	msg.ソウシンモトセツゾクバンゴウ = ソケット.ローカルポートnumber
	msg.アテサキセツゾクバンゴウ = ソケット.リモートポートnumber
	msg.ナガサ = Unsignedinteger16r(uint16(ゴウケイナガサ))

	msg.checksum = 0x0
	msg.Sアリbuffer(msgbuffer)

	var データバイト [4096]byte = *(*[4096]byte)(Pointer(pデータ))
	for i := 0; i < int(サイズ); i++ {
		buffer_2[int(udpヘッダサイズ)+i] = データバイト[i]
	}

	var データ uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Sソウシン(ソケット.リモートip, 0x11, データ, ゴウケイナガサ)

}
func (self *Tリヨウシャdatagramprotocolprovider) Bバインド(ソケット *Tリヨウシャシリョウデンブンツウシンタンテン, handler *Tリヨウシャdatagramprotocolhandler) {
}
