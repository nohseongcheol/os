package amdam79c973

import . "unsafe"
import . "割込み"
import . "コンソール"
import . "ポート"
import . "pci"

var ネットワークカードゲームコンソール Tコンソール = Tコンソール{}

type TInitializationブロック struct {
	モード			uint16
	number送信buffer		uint8
	numberrecvbuffer	uint8

	物理address	uint64

	論理演算address		uint64
	recvbuffer説明address	uintptr
	送信buffer説明address	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	フラグ		uint32
	フラグ2		uint32
	使用可能		uint32
}

type IRawデータhandler interface {
	O時rawデータreceive(データポインタ uintptr, サイズ int) bool
	S送信(データポインタ uintptr, サイズ uint32)
}

var rawデータbackend Tamdam79c973

type TRawデータhandler struct {
}

func (self *TRawデータhandler) Sありbackend(backend Tamdam79c973) {

	rawデータbackend = backend
}
func (self *TRawデータhandler) Getbackend() Tamdam79c973 {
	return rawデータbackend
}
func (self *TRawデータhandler) O時rawデータreceive(データポインタ uintptr, サイズ int) bool {
	ネットワークカードゲームコンソール.M印刷xy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawデータhandler) S送信(データポインタ uintptr, サイズ uint32) {
	ネットワークカードゲームコンソール.M印刷xy(([]byte)("TRawDataSend"), 10, 10)
	rawデータbackend.S送信(データポインタ, サイズ)
}

var Macaddress0ポート uint16
var Macaddress2ポート uint16
var Macaddress4ポート uint16
var レジスタデータポート uint16
var レジスタaddressポート uint16
var リセットポート uint16
var bus制御レジスタデータポート uint16

var initブロック TInitializationブロック

var 送信buffer説明 [8]TBufferdescriptor
var 送信buffer説明メモリ [2048 + 15]byte
var 送信buffer [2*1024 + 15][8]uint8
var 現在の日時送信buffer uint8

var recvbuffer説明 [8]TBufferdescriptor
var recvbuffer説明メモリ [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var 現在の日時recvbuffer uint8
var func値 func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	T割込みhandler
	デバイスdescriptor	TPeripheralcomponentinterconnectデバイスdescriptor
	割込み		*T割込み管理者
	handler		*TRawデータhandler
}

var コンソール_2 Tコンソール = Tコンソール{}
var irawデータhandler IRawデータhandler

func (self *Tamdam79c973) Initドライバー(割込み *T割込み管理者, デバイスdescriptor TPeripheralcomponentinterconnectデバイスdescriptor, handler IRawデータhandler) {

	self.デバイスdescriptor = デバイスdescriptor

	func値 = (*Tamdam79c973).H取っ手割込み
	var address uintptr
	address = uintptr(Pointer(&func値))

	self.Init(uint8(0x20+デバイスdescriptor.I割込み), uintptr(Pointer(割込み)), address)

	Macaddress0ポート = uint16(デバイスdescriptor.Pポートbase)
	Macaddress2ポート = uint16(デバイスdescriptor.Pポートbase) + 0x02
	Macaddress4ポート = uint16(デバイスdescriptor.Pポートbase) + 0x04
	レジスタデータポート = uint16(デバイスdescriptor.Pポートbase) + 0x10
	レジスタaddressポート = uint16(デバイスdescriptor.Pポートbase) + 0x12
	リセットポート = uint16(デバイスdescriptor.Pポートbase) + 0x14
	bus制御レジスタデータポート = uint16(デバイスdescriptor.Pポートbase) + 0x16

	irawデータhandler = &TRawデータhandler{}
	if handler != nil {
		irawデータhandler = handler
	}

	現在の日時送信buffer = 0
	現在の日時recvbuffer = 0

	var Mac0 uint64 = uint64(Pポート読込み語(Macaddress0ポート) % 256)
	var Mac1 uint64 = uint64(Pポート読込み語(Macaddress0ポート) / 256)
	var Mac2 uint64 = uint64(Pポート読込み語(Macaddress2ポート) % 256)
	var Mac3 uint64 = uint64(Pポート読込み語(Macaddress2ポート) / 256)
	var Mac4 uint64 = uint64(Pポート読込み語(Macaddress4ポート) % 256)
	var Mac5 uint64 = uint64(Pポート読込み語(Macaddress4ポート) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	コンソール_2.M印刷xy(([]byte)("[interrupt num : "), 0, 13)
	コンソール_2.MHexadecimal印刷(uint8(デバイスdescriptor.I割込み))
	コンソール_2.M印刷(([]byte)("]"))
	コンソール_2.M印刷(([]byte)("[mac address : "))
	コンソール_2.MUnsignedinteger16印刷(uint16(macaddress >> 32))
	コンソール_2.MUnsignedinteger32印刷(uint32(macaddress & 0x00000000FFFFFFFF))
	コンソール_2.M印刷(([]byte)("]"))

	Pポート書込み語(レジスタaddressポート, 20)
	Pポート書込み語(bus制御レジスタデータポート, 0x102)

	Pポート書込み語(レジスタaddressポート, 0)
	Pポート書込み語(レジスタデータポート, 0x04)

	initブロック.モード = 0x0000
	initブロック.number送信buffer = 3
	initブロック.numberrecvbuffer = 3

	initブロック.物理address = Mac

	initブロック.論理演算address = 0

	送信buffer説明 = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&送信buffer説明メモリ)) + 15) & ^(uintptr)(0xF)))
	initブロック.送信buffer説明address = uintptr(Pointer(&送信buffer説明))
	recvbuffer説明 = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbuffer説明メモリ)) + 15) & ^(uintptr)(0xF)))
	initブロック.recvbuffer説明address = uintptr(Pointer(&recvbuffer説明))

	for i := 0; i < 8; i++ {
		送信buffer説明[i].address_2 = uint32((uintptr(Pointer(&送信buffer[i])) + 15) & ^(uintptr(0xF)))
		送信buffer説明[i].フラグ = 0x7FF | 0xF000
		送信buffer説明[i].フラグ2 = 0
		送信buffer説明[i].使用可能 = 0

		recvbuffer説明[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbuffer説明[i].フラグ = 0xF7FF | 0x80000000

	}

	Pポート書込み語(レジスタaddressポート, 1)
	Pポート書込み語(レジスタデータポート, uint16(uintptr(Pointer(&initブロック))&0xFFFF))

	Pポート書込み語(レジスタaddressポート, 2)
	Pポート書込み語(レジスタデータポート, uint16((uintptr(Pointer(&initブロック))>>16)&0xFFFF))

}
func (self *Tamdam79c973) A有効にする() {
	Pポート書込み語(レジスタaddressポート, 0)
	Pポート書込み語(レジスタデータポート, 0x41)

	Pポート書込み語(レジスタaddressポート, 4)
	temporary := Pポート読込み語(レジスタデータポート)
	Pポート書込み語(レジスタaddressポート, 4)
	Pポート書込み語(レジスタデータポート, temporary|0xC00)

	Pポート書込み語(レジスタaddressポート, 0)
	Pポート書込み語(レジスタデータポート, 0x42)

}
func (self *Tamdam79c973) Rリセット() int {
	Pポート読込み語(リセットポート)
	Pポート書込み語(リセットポート, 0)
	return 10
}

var カウント uint16 = 0

func (self *Tamdam79c973) H取っ手割込み(esp uint32) uint32 {

	Pポート書込み語(レジスタaddressポート, 0)
	temporary := uint32(Pポート読込み語(レジスタデータポート))
	コンソール_2.M印刷(([]byte)("interrupt("))
	コンソール_2.MUnsignedinteger32印刷(esp)
	コンソール_2.M印刷(([]byte)(":"))
	コンソール_2.MUnsignedinteger32印刷(temporary)
	コンソール_2.M印刷(([]byte)(":"))
	コンソール_2.MUnsignedinteger16印刷(カウント)
	カウント++
	コンソール_2.M印刷(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		コンソール_2.M印刷(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		コンソール_2.M印刷(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		コンソール_2.M印刷(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		コンソール_2.M印刷(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		コンソール_2.M印刷(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		コンソール_2.M印刷(([]byte)("am79c973 data sent"))
	}

	Pポート書込み語(レジスタaddressポート, 0)
	Pポート書込み語(レジスタデータポート, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		コンソール_2.M印刷(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) S送信(データポインタ uintptr, サイズ uint32) {
	var 送信descriptor uint16 = uint16(現在の日時送信buffer)
	現在の日時送信buffer = 0

	if サイズ > 1518 {
		サイズ = 1518
	}

	var 転送元_2 [4096]byte = *(*([4096]byte))(Pointer(データポインタ))
	var 転送先_2 uint32 = 送信buffer説明[送信descriptor].address_2 + サイズ - 1

	for i := 0; i < int(サイズ); i++ {

		*(*byte)(Pointer(uintptr(転送先_2))) = 転送元_2[int(サイズ)-i-1]

		転送先_2--
	}

	var データ [4096]byte = *(*([4096]byte))(Pointer(データポインタ))
	コンソール_2.M印刷xy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		コンソール_2.MHexadecimal印刷(データ[i])
		コンソール_2.M印刷(([]byte)(":"))
	}
	コンソール_2.M印刷(([]byte)("\n"))

	送信buffer説明[送信descriptor].使用可能 = 0
	送信buffer説明[送信descriptor].フラグ2 = 0
	送信buffer説明[送信descriptor].フラグ = 0x8300F000 | uint32((-サイズ)&0xFFF)

	Pポート書込み語(レジスタaddressポート, 0)
	Pポート書込み語(レジスタデータポート, 0x48)

}
func (self *Tamdam79c973) Receive() {
	コンソール_2.M印刷(([]byte)(":"))
	コンソール_2.MUnsignedinteger32印刷(uint32(uintptr(Pointer(&送信buffer))))
	コンソール_2.M印刷(([]byte)(":"))
	コンソール_2.MHexadecimal印刷(送信buffer[0][0])
	コンソール_2.MHexadecimal印刷(送信buffer[0][1])
	コンソール_2.M印刷(([]byte)(":"))
	現在の日時recvbuffer = 0

	for ; (recvbuffer説明[現在の日時recvbuffer].フラグ & 0x80000000) == 0; 現在の日時recvbuffer = (現在の日時recvbuffer + 1) % 8 {

		if !(recvbuffer説明[現在の日時recvbuffer].フラグ&0x40000000 != 0) && ((recvbuffer説明[現在の日時recvbuffer].フラグ & 0x03000000) == 0x03000000) {
			var サイズ uint32 = recvbuffer説明[現在の日時recvbuffer].フラグ & 0xFFF
			if サイズ > 64 {
				サイズ -= 4
			}

			コンソール_2.M印刷([]byte(" size : ["))
			コンソール_2.MUnsignedinteger32印刷(サイズ)
			コンソール_2.M印刷([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbuffer説明[現在の日時recvbuffer].address_2)))
			var 番地参照 uintptr = uintptr(Pointer(&buffer_2))
			if irawデータhandler != nil {
				if irawデータhandler.O時rawデータreceive(番地参照, int(サイズ)) {

					コンソール_2.M印刷xy(([]byte)("self.Send"), 0, 22)

					self.S送信(番地参照, サイズ)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				コンソール_2.MHexadecimal印刷(buffer_2[i])
				コンソール_2.M印刷([]byte(":"))
			}

		}
		recvbuffer説明[現在の日時recvbuffer].フラグ2 = 0
		recvbuffer説明[現在の日時recvbuffer].フラグ = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sありhandler(handler *TRawデータhandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initブロック.物理address
}
func (self *Tamdam79c973) Sありipaddress(ip uint64) {
	initブロック.論理演算address = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initブロック.論理演算address
}
