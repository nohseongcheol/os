package 共有媒体網伝送枠

import . "コンソール"

import . "amdam79c973"
import . "unsafe"
import . "汎用"

var イーサネットコンソール Tコンソール = Tコンソール{}

type Tイーサネットフレームヘッダbuffer struct {
	転送先macbe	[6]byte
	転送元macbe	[6]byte
	イーサネット型be	[2]byte
}

var フレームヘッダサイズ int = 14

type T共有媒体網伝送枠先頭部 struct {
	転送先macbe	uint64
	転送元macbe	uint64
	イーサネット型be	uint16
}

func (self *T共有媒体網伝送枠先頭部) Init(buffer_2 Tイーサネットフレームヘッダbuffer) {
	self.転送先macbe = (A配列tounsignedinteger48(buffer_2.転送先macbe))
	self.転送元macbe = (A配列tounsignedinteger48(buffer_2.転送元macbe))
	self.イーサネット型be = (A配列tounsignedinteger16(buffer_2.イーサネット型be))

}
func (self *T共有媒体網伝送枠先頭部) Sありbuffer(buffer_2 *Tイーサネットフレームヘッダbuffer) {
	buffer_2.転送先macbe = Unsignedinteger48to配列(Unsignedinteger48r(self.転送先macbe))
	buffer_2.転送元macbe = Unsignedinteger48to配列(Unsignedinteger48r(self.転送元macbe))
	buffer_2.イーサネット型be = Unsignedinteger16to配列(Unsignedinteger16r(self.イーサネット型be))
}

type Iイーサネットフレームhandler interface {
	Init(backend T共有媒体網伝送枠提供器)
	Sありhandler(handler Iイーサネットフレームhandler, イーサネット型 uint16)
	Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool
	S送信(転送先macbe uint64, データポインタ uintptr, サイズ uint32)
	Sフレーム送信(転送先macbe uint64, イーサネット型be uint16, データポインタ uintptr, サイズ uint32)
	Providerget() T共有媒体網伝送枠提供器
	Getmacaddress() uint64
	Getipaddress() uint64
}

type Tイーサネットフレームhandler struct {
}

var フレーム T共有媒体網伝送枠先頭部
var Backend T共有媒体網伝送枠提供器
var handler_2 [65535]Iイーサネットフレームhandler
var efhandler *Tイーサネットフレームhandler = nil

func (self *Tイーサネットフレームhandler) Init(backend T共有媒体網伝送枠提供器) {
	Backend = backend
}

func (self *Tイーサネットフレームhandler) Sありhandler(handler Iイーサネットフレームhandler, pイーサネット型 uint16) {
	handler_2[pイーサネット型] = handler
}
func (self *Tイーサネットフレームhandler) Sありbackend(backend T共有媒体網伝送枠提供器) {
	Backend = backend
}
func (self *Tイーサネットフレームhandler) Getbackend() T共有媒体網伝送枠提供器 {
	return Backend
}
func (self *Tイーサネットフレームhandler) Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool {
	イーサネットコンソール.M印刷(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *Tイーサネットフレームhandler) S送信(転送先macbe uint64, データポインタ uintptr, サイズ uint32) {
	Backend.Sフレーム送信(転送先macbe, フレーム.イーサネット型be, データポインタ, サイズ)
}
func (self *Tイーサネットフレームhandler) Sフレーム送信(転送先macbe uint64, イーサネット型be uint16, データポインタ uintptr, サイズ uint32) {
	Backend.Sフレーム送信(転送先macbe, イーサネット型be, データポインタ, サイズ)
}
func (self *Tイーサネットフレームhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *Tイーサネットフレームhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *Tイーサネットフレームhandler) Providerget() T共有媒体網伝送枠提供器 {
	return Backend
}

type Tイーサネットフレームrawデータhandler struct {
	TRawデータhandler
}

var provider T共有媒体網伝送枠提供器

func (self *Tイーサネットフレームrawデータhandler) Init(pprovider T共有媒体網伝送枠提供器, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *Tイーサネットフレームrawデータhandler) O時rawデータreceive(データポインタ uintptr, サイズ int) bool {
	return provider.O時rawデータreceive(データポインタ, サイズ)
}
func (self *Tイーサネットフレームrawデータhandler) S送信(データポインタ uintptr, サイズ uint32) {
	provider.S送信(データポインタ, サイズ)
}
func (self *Tイーサネットフレームrawデータhandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *Tイーサネットフレームrawデータhandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *Tイーサネットフレームrawデータhandler) Providerget() T共有媒体網伝送枠提供器 {
	return provider
}

type T共有媒体網伝送枠提供器 struct {
	ネットワークカードゲーム	Tamdam79c973
	handler_2	[65565]Iイーサネットフレームhandler
}

func (self *T共有媒体網伝送枠提供器) Init(backend Tamdam79c973) {

	self.ネットワークカードゲーム = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var カウント uint16 = 0

func (self *T共有媒体網伝送枠提供器) O時rawデータreceive(データポインタ uintptr, サイズ int) bool {

	var buffer_2 *Tイーサネットフレームヘッダbuffer = (*Tイーサネットフレームヘッダbuffer)(Pointer(データポインタ))
	var フレーム T共有媒体網伝送枠先頭部 = T共有媒体網伝送枠先頭部{}
	フレーム.Init(*buffer_2)
	var reply bool = false

	if フレーム.転送先macbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(フレーム.転送先macbe) == self.Getmacaddress() {
		if handler_2[フレーム.イーサネット型be] != nil {
			イーサネットコンソール.M印刷(([]byte)("provider\n"))

			var 番地参照 uintptr = uintptr(Pointer(データポインタ)) + uintptr(フレームヘッダサイズ)
			reply = handler_2[フレーム.イーサネット型be].Oイーサネットフレームreceivewhen(番地参照, サイズ-フレームヘッダサイズ)

		}
	}

	if reply {
		フレーム.転送先macbe = フレーム.転送元macbe
		フレーム.転送元macbe = Unsignedinteger48r(self.Getmacaddress())
		フレーム.Sありbuffer(buffer_2)

	}

	イーサネットコンソール.M印刷xy(([]byte)("spro["), 0, 1)
	イーサネットコンソール.MUnsignedinteger64印刷(フレーム.転送元macbe)
	イーサネットコンソール.M印刷(([]byte)(":"))
	イーサネットコンソール.MUnsignedinteger64印刷(フレーム.転送先macbe)
	イーサネットコンソール.M印刷(([]byte)(":]["))
	イーサネットコンソール.MUnsignedinteger64印刷(self.Getmacaddress())
	イーサネットコンソール.M印刷(([]byte)(":"))
	イーサネットコンソール.MUnsignedinteger16印刷(フレーム.イーサネット型be)
	イーサネットコンソール.M印刷(([]byte)("]"))

	return reply

}
func (self *T共有媒体網伝送枠提供器) S送信(データポインタ uintptr, サイズ uint32) {
	self.ネットワークカードゲーム.S送信(データポインタ, サイズ)
}
func (self *T共有媒体網伝送枠提供器) Sフレーム送信(転送先macbe uint64, イーサネット型be uint16, データポインタ uintptr, サイズ uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *Tイーサネットフレームヘッダbuffer = (*Tイーサネットフレームヘッダbuffer)(Pointer(&buffer2_2))

	var フレーム T共有媒体網伝送枠先頭部 = T共有媒体網伝送枠先頭部{}
	フレーム.Init(*buffer_2)

	フレーム.転送先macbe = Unsignedinteger48r(転送先macbe)
	フレーム.転送元macbe = Unsignedinteger48r(self.ネットワークカードゲーム.Getmacaddress())
	フレーム.イーサネット型be = Unsignedinteger16r(イーサネット型be)

	フレーム.Sありbuffer(buffer_2)
	var 転送元_2 [4096]byte = *(*([4096]byte))(Pointer(データポインタ))

	var i uint32 = 0
	for i = 0; i < サイズ; i++ {
		buffer2_2[uint32(フレームヘッダサイズ)+i] = 転送元_2[i]

	}

	var 番地参照 uintptr = uintptr(Pointer(&buffer2_2))

	self.ネットワークカードゲーム.S送信(番地参照, サイズ+uint32(フレームヘッダサイズ))

}
func (self *T共有媒体網伝送枠提供器) Getmacaddress() uint64 {
	return self.ネットワークカードゲーム.Getmacaddress()
}
func (self *T共有媒体網伝送枠提供器) Getipaddress() uint64 {
	return self.ネットワークカードゲーム.Getipaddress()
}
