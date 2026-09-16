/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "ワリコミ"
import . "コンソール"
import . "ポート"
import . "pci"

var ネットワークカードゲームコンソール Tコンソール = Tコンソール{}

type TInitializationブロック struct {
	モード			uint16
	numberソウシンbuffer		uint8
	numberrecvbuffer	uint8

	ブツリaddress	uint64

	ロンリエンザンaddress		uint64
	recvbufferセツメイaddress	uintptr
	ソウシンbufferセツメイaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	フラグ		uint32
	フラグ2		uint32
	シヨウカノウ		uint32
}

type IRawデータhandler interface {
	Oトキrawデータreceive(データポインタ uintptr, サイズ int) bool
	Sソウシン(データポインタ uintptr, サイズ uint32)
}

var rawデータbackend Tamdam79c973

type TRawデータhandler struct {
}

func (self *TRawデータhandler) Sアリbackend(backend Tamdam79c973) {

	rawデータbackend = backend
}
func (self *TRawデータhandler) Getbackend() Tamdam79c973 {
	return rawデータbackend
}
func (self *TRawデータhandler) Oトキrawデータreceive(データポインタ uintptr, サイズ int) bool {
	ネットワークカードゲームコンソール.Mインサツxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawデータhandler) Sソウシン(データポインタ uintptr, サイズ uint32) {
	ネットワークカードゲームコンソール.Mインサツxy(([]byte)("TRawDataSend"), 10, 10)
	rawデータbackend.Sソウシン(データポインタ, サイズ)
}

var Macaddress0ポート uint16
var Macaddress2ポート uint16
var Macaddress4ポート uint16
var レジスタデータポート uint16
var レジスタaddressポート uint16
var リセットポート uint16
var busセイギョレジスタデータポート uint16

var initブロック TInitializationブロック

var ソウシンbufferセツメイ [8]TBufferdescriptor
var ソウシンbufferセツメイメモリ [2048 + 15]byte
var ソウシンbuffer [2*1024 + 15][8]uint8
var ゲンザイノニチジソウシンbuffer uint8

var recvbufferセツメイ [8]TBufferdescriptor
var recvbufferセツメイメモリ [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var ゲンザイノニチジrecvbuffer uint8
var funcアタイ func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	Tワリコミhandler
	デバイスdescriptor	TPeripheralcomponentinterconnectデバイスdescriptor
	ワリコミ		*Tワリコミカンリシャ
	handler		*TRawデータhandler
}

var コンソール_2 Tコンソール = Tコンソール{}
var irawデータhandler IRawデータhandler

func (self *Tamdam79c973) Initドライバー(ワリコミ *Tワリコミカンリシャ, デバイスdescriptor TPeripheralcomponentinterconnectデバイスdescriptor, handler IRawデータhandler) {

	self.デバイスdescriptor = デバイスdescriptor

	funcアタイ = (*Tamdam79c973).Hトッテワリコミ
	var address uintptr
	address = uintptr(Pointer(&funcアタイ))

	self.Init(uint8(0x20+デバイスdescriptor.Iワリコミ), uintptr(Pointer(ワリコミ)), address)

	Macaddress0ポート = uint16(デバイスdescriptor.Pポートbase)
	Macaddress2ポート = uint16(デバイスdescriptor.Pポートbase) + 0x02
	Macaddress4ポート = uint16(デバイスdescriptor.Pポートbase) + 0x04
	レジスタデータポート = uint16(デバイスdescriptor.Pポートbase) + 0x10
	レジスタaddressポート = uint16(デバイスdescriptor.Pポートbase) + 0x12
	リセットポート = uint16(デバイスdescriptor.Pポートbase) + 0x14
	busセイギョレジスタデータポート = uint16(デバイスdescriptor.Pポートbase) + 0x16

	irawデータhandler = &TRawデータhandler{}
	if handler != nil {
		irawデータhandler = handler
	}

	ゲンザイノニチジソウシンbuffer = 0
	ゲンザイノニチジrecvbuffer = 0

	var Mac0 uint64 = uint64(Pポートヨミコミゴ(Macaddress0ポート) % 256)
	var Mac1 uint64 = uint64(Pポートヨミコミゴ(Macaddress0ポート) / 256)
	var Mac2 uint64 = uint64(Pポートヨミコミゴ(Macaddress2ポート) % 256)
	var Mac3 uint64 = uint64(Pポートヨミコミゴ(Macaddress2ポート) / 256)
	var Mac4 uint64 = uint64(Pポートヨミコミゴ(Macaddress4ポート) % 256)
	var Mac5 uint64 = uint64(Pポートヨミコミゴ(Macaddress4ポート) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	コンソール_2.Mインサツxy(([]byte)("[interrupt num : "), 0, 13)
	コンソール_2.MHexadecimalインサツ(uint8(デバイスdescriptor.Iワリコミ))
	コンソール_2.Mインサツ(([]byte)("]"))
	コンソール_2.Mインサツ(([]byte)("[mac address : "))
	コンソール_2.MUnsignedinteger16インサツ(uint16(macaddress >> 32))
	コンソール_2.MUnsignedinteger32インサツ(uint32(macaddress & 0x00000000FFFFFFFF))
	コンソール_2.Mインサツ(([]byte)("]"))

	Pポートカキコミゴ(レジスタaddressポート, 20)
	Pポートカキコミゴ(busセイギョレジスタデータポート, 0x102)

	Pポートカキコミゴ(レジスタaddressポート, 0)
	Pポートカキコミゴ(レジスタデータポート, 0x04)

	initブロック.モード = 0x0000
	initブロック.numberソウシンbuffer = 3
	initブロック.numberrecvbuffer = 3

	initブロック.ブツリaddress = Mac

	initブロック.ロンリエンザンaddress = 0

	ソウシンbufferセツメイ = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&ソウシンbufferセツメイメモリ)) + 15) & ^(uintptr)(0xF)))
	initブロック.ソウシンbufferセツメイaddress = uintptr(Pointer(&ソウシンbufferセツメイ))
	recvbufferセツメイ = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferセツメイメモリ)) + 15) & ^(uintptr)(0xF)))
	initブロック.recvbufferセツメイaddress = uintptr(Pointer(&recvbufferセツメイ))

	for i := 0; i < 8; i++ {
		ソウシンbufferセツメイ[i].address_2 = uint32((uintptr(Pointer(&ソウシンbuffer[i])) + 15) & ^(uintptr(0xF)))
		ソウシンbufferセツメイ[i].フラグ = 0x7FF | 0xF000
		ソウシンbufferセツメイ[i].フラグ2 = 0
		ソウシンbufferセツメイ[i].シヨウカノウ = 0

		recvbufferセツメイ[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferセツメイ[i].フラグ = 0xF7FF | 0x80000000

	}

	Pポートカキコミゴ(レジスタaddressポート, 1)
	Pポートカキコミゴ(レジスタデータポート, uint16(uintptr(Pointer(&initブロック))&0xFFFF))

	Pポートカキコミゴ(レジスタaddressポート, 2)
	Pポートカキコミゴ(レジスタデータポート, uint16((uintptr(Pointer(&initブロック))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aユウコウニスル() {
	Pポートカキコミゴ(レジスタaddressポート, 0)
	Pポートカキコミゴ(レジスタデータポート, 0x41)

	Pポートカキコミゴ(レジスタaddressポート, 4)
	temporary := Pポートヨミコミゴ(レジスタデータポート)
	Pポートカキコミゴ(レジスタaddressポート, 4)
	Pポートカキコミゴ(レジスタデータポート, temporary|0xC00)

	Pポートカキコミゴ(レジスタaddressポート, 0)
	Pポートカキコミゴ(レジスタデータポート, 0x42)

}
func (self *Tamdam79c973) Rリセット() int {
	Pポートヨミコミゴ(リセットポート)
	Pポートカキコミゴ(リセットポート, 0)
	return 10
}

var カウント uint16 = 0

func (self *Tamdam79c973) Hトッテワリコミ(esp uint32) uint32 {

	Pポートカキコミゴ(レジスタaddressポート, 0)
	temporary := uint32(Pポートヨミコミゴ(レジスタデータポート))
	コンソール_2.Mインサツ(([]byte)("interrupt("))
	コンソール_2.MUnsignedinteger32インサツ(esp)
	コンソール_2.Mインサツ(([]byte)(":"))
	コンソール_2.MUnsignedinteger32インサツ(temporary)
	コンソール_2.Mインサツ(([]byte)(":"))
	コンソール_2.MUnsignedinteger16インサツ(カウント)
	カウント++
	コンソール_2.Mインサツ(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		コンソール_2.Mインサツ(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		コンソール_2.Mインサツ(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		コンソール_2.Mインサツ(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		コンソール_2.Mインサツ(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		コンソール_2.Mインサツ(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		コンソール_2.Mインサツ(([]byte)("am79c973 data sent"))
	}

	Pポートカキコミゴ(レジスタaddressポート, 0)
	Pポートカキコミゴ(レジスタデータポート, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		コンソール_2.Mインサツ(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Sソウシン(データポインタ uintptr, サイズ uint32) {
	var ソウシンdescriptor uint16 = uint16(ゲンザイノニチジソウシンbuffer)
	ゲンザイノニチジソウシンbuffer = 0

	if サイズ > 1518 {
		サイズ = 1518
	}

	var テンソウモト_2 [4096]byte = *(*([4096]byte))(Pointer(データポインタ))
	var テンソウサキ_2 uint32 = ソウシンbufferセツメイ[ソウシンdescriptor].address_2 + サイズ - 1

	for i := 0; i < int(サイズ); i++ {

		*(*byte)(Pointer(uintptr(テンソウサキ_2))) = テンソウモト_2[int(サイズ)-i-1]

		テンソウサキ_2--
	}

	var データ [4096]byte = *(*([4096]byte))(Pointer(データポインタ))
	コンソール_2.Mインサツxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		コンソール_2.MHexadecimalインサツ(データ[i])
		コンソール_2.Mインサツ(([]byte)(":"))
	}
	コンソール_2.Mインサツ(([]byte)("\n"))

	ソウシンbufferセツメイ[ソウシンdescriptor].シヨウカノウ = 0
	ソウシンbufferセツメイ[ソウシンdescriptor].フラグ2 = 0
	ソウシンbufferセツメイ[ソウシンdescriptor].フラグ = 0x8300F000 | uint32((-サイズ)&0xFFF)

	Pポートカキコミゴ(レジスタaddressポート, 0)
	Pポートカキコミゴ(レジスタデータポート, 0x48)

}
func (self *Tamdam79c973) Receive() {
	コンソール_2.Mインサツ(([]byte)(":"))
	コンソール_2.MUnsignedinteger32インサツ(uint32(uintptr(Pointer(&ソウシンbuffer))))
	コンソール_2.Mインサツ(([]byte)(":"))
	コンソール_2.MHexadecimalインサツ(ソウシンbuffer[0][0])
	コンソール_2.MHexadecimalインサツ(ソウシンbuffer[0][1])
	コンソール_2.Mインサツ(([]byte)(":"))
	ゲンザイノニチジrecvbuffer = 0

	for ; (recvbufferセツメイ[ゲンザイノニチジrecvbuffer].フラグ & 0x80000000) == 0; ゲンザイノニチジrecvbuffer = (ゲンザイノニチジrecvbuffer + 1) % 8 {

		if !(recvbufferセツメイ[ゲンザイノニチジrecvbuffer].フラグ&0x40000000 != 0) && ((recvbufferセツメイ[ゲンザイノニチジrecvbuffer].フラグ & 0x03000000) == 0x03000000) {
			var サイズ uint32 = recvbufferセツメイ[ゲンザイノニチジrecvbuffer].フラグ & 0xFFF
			if サイズ > 64 {
				サイズ -= 4
			}

			コンソール_2.Mインサツ([]byte(" size : ["))
			コンソール_2.MUnsignedinteger32インサツ(サイズ)
			コンソール_2.Mインサツ([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferセツメイ[ゲンザイノニチジrecvbuffer].address_2)))
			var バンチサンショウ uintptr = uintptr(Pointer(&buffer_2))
			if irawデータhandler != nil {
				if irawデータhandler.Oトキrawデータreceive(バンチサンショウ, int(サイズ)) {

					コンソール_2.Mインサツxy(([]byte)("self.Send"), 0, 22)

					self.Sソウシン(バンチサンショウ, サイズ)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				コンソール_2.MHexadecimalインサツ(buffer_2[i])
				コンソール_2.Mインサツ([]byte(":"))
			}

		}
		recvbufferセツメイ[ゲンザイノニチジrecvbuffer].フラグ2 = 0
		recvbufferセツメイ[ゲンザイノニチジrecvbuffer].フラグ = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Sアリhandler(handler *TRawデータhandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initブロック.ブツリaddress
}
func (self *Tamdam79c973) Sアリipaddress(ip uint64) {
	initブロック.ロンリエンザンaddress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initブロック.ロンリエンザンaddress
}
