package 利用者資料電文規約

import . "unsafe"
import . "コンソール"
import . "汎用"
import . "メモリ管理者"
import . "相互接続網規約4"

var udpコンソール = Tコンソール{}

type T利用者datagramprotocolヘッダbuffer struct {
	送信元接続番号	[2]byte
	宛先接続番号	[2]byte

	長さ		[2]byte
	checksum	[2]byte
}

var udpヘッダサイズ uint32 = 8

type T利用者資料電文先頭部 struct {
	送信元接続番号	uint16
	宛先接続番号	uint16

	長さ		uint16
	checksum	uint16
}

func (self *T利用者資料電文先頭部) Init(buffer_2 *T利用者datagramprotocolヘッダbuffer) {
	self.送信元接続番号 = A配列tounsignedinteger16(buffer_2.送信元接続番号)
	self.宛先接続番号 = A配列tounsignedinteger16(buffer_2.宛先接続番号)

	self.長さ = A配列tounsignedinteger16(buffer_2.長さ)
	self.checksum = A配列tounsignedinteger16(buffer_2.checksum)
}
func (self *T利用者資料電文先頭部) Sありbuffer(buffer_2 *T利用者datagramprotocolヘッダbuffer) {

	buffer_2.送信元接続番号 = Unsignedinteger16to配列(self.送信元接続番号)
	buffer_2.宛先接続番号 = Unsignedinteger16to配列(self.宛先接続番号)

	buffer_2.長さ = Unsignedinteger16to配列(self.長さ)
	buffer_2.checksum = Unsignedinteger16to配列(self.checksum)

}

type I利用者datagramprotocolhandler interface {
	H取っ手利用者datagramprotocolメッセージ(ソケット *T利用者資料電文通信端点, データ uintptr, サイズ uint16)
}

type T利用者datagramprotocolhandler struct {
}

func (self *T利用者datagramprotocolhandler) Init(backend T相互接続網規約提供器) {
}
func (self *T利用者datagramprotocolhandler) H取っ手利用者datagramprotocolメッセージ(ソケット *T利用者資料電文通信端点, データ uintptr, サイズ uint16) {
}

type I利用者datagramprotocolソケット interface {
	H取っ手利用者datagramprotocolメッセージ(データ uintptr, サイズ uint16)
}
type T利用者資料電文通信端点 struct {
	リモートポートnumber	uint16
	リモートip		uint32
	ローカルポートnumber	uint16
	ローカルip		uint32

	listening	bool
}

var udpprovider T利用者datagramprotocolprovider
var udphandler I利用者datagramprotocolhandler

func (self *T利用者資料電文通信端点) Tテスト() {
}
func (self *T利用者資料電文通信端点) Init(pudpprovider T利用者datagramprotocolprovider, pudphandler I利用者datagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *T利用者資料電文通信端点) H取っ手利用者datagramprotocolメッセージ(データ uintptr, サイズ uint16) {
	if udphandler != nil {
		udphandler.H取っ手利用者datagramprotocolメッセージ(self, データ, サイズ)
	}
}
func (self *T利用者資料電文通信端点) S送信(pデータ []byte, サイズ uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(サイズ); i++ {
		buffer_2[i] = pデータ[i]
	}
	var データ = uintptr(Pointer(&buffer_2))
	udpprovider.S送信(self, データ, サイズ)
}
func (self *T利用者資料電文通信端点) D切断する() {
	udpprovider.D切断する(self)
}

type T利用者datagramprotocolprovider struct {
}

var iphandler Iインターネットprotocolhandler
var sockets [65535]T利用者資料電文通信端点
var numbersockets int
var 空きポート uint16

func (self *T利用者datagramprotocolprovider) Init(pipprovider T相互接続網規約提供器, piphandler Iインターネットprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	空きポート = 1024
}
func (self *T利用者datagramprotocolprovider) Oインターネットprotocolreceivewhen(転送元ipaddressネットワークバイトorder uint32, 転送先ipaddressネットワークバイトorder uint32, インターネットprotocolpayload uintptr, サイズ uint32) bool {
	if サイズ < udpヘッダサイズ {
		return false
	}

	var buffer_2 *T利用者datagramprotocolヘッダbuffer = (*T利用者datagramprotocolヘッダbuffer)(Pointer(インターネットprotocolpayload))
	var msg T利用者資料電文先頭部
	msg.Init(buffer_2)

	var ソケット *T利用者資料電文通信端点 = nil

	for i := 0; i < numbersockets && ソケット == nil; i++ {
		if sockets[i].ローカルポートnumber == msg.宛先接続番号 && sockets[i].ローカルip == 転送先ipaddressネットワークバイトorder && sockets[i].listening == true {
			ソケット = &sockets[i]
			ソケット.listening = false
			ソケット.リモートポートnumber = msg.送信元接続番号
			ソケット.リモートip = 転送元ipaddressネットワークバイトorder
		} else if sockets[i].ローカルポートnumber == msg.宛先接続番号 && sockets[i].ローカルip == 転送先ipaddressネットワークバイトorder && sockets[i].リモートポートnumber == msg.送信元接続番号 && sockets[i].リモートip == 転送元ipaddressネットワークバイトorder {
			ソケット = &sockets[i]

		}
	}

	msg.Sありbuffer(buffer_2)
	if ソケット != nil {
		ソケット.H取っ手利用者datagramprotocolメッセージ(インターネットprotocolpayload+uintptr(udpヘッダサイズ), uint16(サイズ-udpヘッダサイズ))
	}

	return false
}

func (self *T利用者datagramprotocolprovider) C接続(ip uint32, ポート uint16) *T利用者資料電文通信端点 {
	var メモリ管理者 = &Tメモリ管理者{}
	var ソケット = (*T利用者資料電文通信端点)(メモリ管理者.M記憶領域を確保(50))

	if ソケット != nil {

		ソケット.Init(*self, nil)
		ソケット.リモートポートnumber = ポート
		ソケット.リモートip = ip
		ソケット.ローカルポートnumber = 空きポート
		空きポート++
		ソケット.ローカルip = uint32((*iphandler.Providerget()).Getipaddress())

		ソケット.リモートポートnumber = Unsignedinteger16r(ソケット.リモートポートnumber)
		ソケット.ローカルポートnumber = Unsignedinteger16r(ソケット.ローカルポートnumber)

		sockets[numbersockets] = *ソケット
		numbersockets++

	}
	return ソケット

}
func (self *T利用者datagramprotocolprovider) Listen(ポート uint16) *T利用者資料電文通信端点 {
	var ソケット = &T利用者資料電文通信端点{}
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
func (self *T利用者datagramprotocolprovider) D切断する(ソケット *T利用者資料電文通信端点) {
	for i := 0; i < numbersockets && ソケット == nil; i++ {
		if sockets[i] == *ソケット {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *T利用者datagramprotocolprovider) S送信(ソケット *T利用者資料電文通信端点, pデータ uintptr, サイズ uint16) {
	var 合計長さ = uint32(サイズ) + udpヘッダサイズ

	var buffer_2 [4096]byte

	var msgbuffer = (*T利用者datagramprotocolヘッダbuffer)(Pointer(&buffer_2))

	var msg = T利用者資料電文先頭部{}

	msg.送信元接続番号 = ソケット.ローカルポートnumber
	msg.宛先接続番号 = ソケット.リモートポートnumber
	msg.長さ = Unsignedinteger16r(uint16(合計長さ))

	msg.checksum = 0x0
	msg.Sありbuffer(msgbuffer)

	var データバイト [4096]byte = *(*[4096]byte)(Pointer(pデータ))
	for i := 0; i < int(サイズ); i++ {
		buffer_2[int(udpヘッダサイズ)+i] = データバイト[i]
	}

	var データ uintptr = uintptr(Pointer(&buffer_2))

	iphandler.S送信(ソケット.リモートip, 0x11, データ, 合計長さ)

}
func (self *T利用者datagramprotocolprovider) Bバインド(ソケット *T利用者資料電文通信端点, handler *T利用者datagramprotocolhandler) {
}
