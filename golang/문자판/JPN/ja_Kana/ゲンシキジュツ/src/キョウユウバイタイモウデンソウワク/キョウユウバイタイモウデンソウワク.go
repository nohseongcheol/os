package キョウユウバイタイモウデンソウワク

import . "コンソール"

import . "amdam79c973"
import . "unsafe"
import . "ハンヨウ"

var イーサネットコンソール Tコンソール = Tコンソール{}

type Tイーサネットフレームヘッダbuffer struct {
	テンソウサキmacbe	[6]byte
	テンソウモトmacbe	[6]byte
	イーサネットカタbe	[2]byte
}

var フレームヘッダサイズ int = 14

type Tキョウユウバイタイアミデンソウワクセントウブ struct {
	テンソウサキmacbe	uint64
	テンソウモトmacbe	uint64
	イーサネットカタbe	uint16
}

func (self *Tキョウユウバイタイアミデンソウワクセントウブ) Init(buffer_2 Tイーサネットフレームヘッダbuffer) {
	self.テンソウサキmacbe = (Aハイレツtounsignedinteger48(buffer_2.テンソウサキmacbe))
	self.テンソウモトmacbe = (Aハイレツtounsignedinteger48(buffer_2.テンソウモトmacbe))
	self.イーサネットカタbe = (Aハイレツtounsignedinteger16(buffer_2.イーサネットカタbe))

}
func (self *Tキョウユウバイタイアミデンソウワクセントウブ) Sアリbuffer(buffer_2 *Tイーサネットフレームヘッダbuffer) {
	buffer_2.テンソウサキmacbe = Unsignedinteger48toハイレツ(Unsignedinteger48r(self.テンソウサキmacbe))
	buffer_2.テンソウモトmacbe = Unsignedinteger48toハイレツ(Unsignedinteger48r(self.テンソウモトmacbe))
	buffer_2.イーサネットカタbe = Unsignedinteger16toハイレツ(Unsignedinteger16r(self.イーサネットカタbe))
}

type Iイーサネットフレームhandler interface {
	Init(backend Tキョウユウバイタイアミデンソウワクテイキョウウツワ)
	Sアリhandler(handler Iイーサネットフレームhandler, イーサネットカタ uint16)
	Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool
	Sソウシン(テンソウサキmacbe uint64, データポインタ uintptr, サイズ uint32)
	Sフレームソウシン(テンソウサキmacbe uint64, イーサネットカタbe uint16, データポインタ uintptr, サイズ uint32)
	Providerget() Tキョウユウバイタイアミデンソウワクテイキョウウツワ
	Getmacaddress() uint64
	Getipaddress() uint64
}

type Tイーサネットフレームhandler struct {
}

var フレーム Tキョウユウバイタイアミデンソウワクセントウブ
var Backend Tキョウユウバイタイアミデンソウワクテイキョウウツワ
var handler_2 [65535]Iイーサネットフレームhandler
var efhandler *Tイーサネットフレームhandler = nil

func (self *Tイーサネットフレームhandler) Init(backend Tキョウユウバイタイアミデンソウワクテイキョウウツワ) {
	Backend = backend
}

func (self *Tイーサネットフレームhandler) Sアリhandler(handler Iイーサネットフレームhandler, pイーサネットカタ uint16) {
	handler_2[pイーサネットカタ] = handler
}
func (self *Tイーサネットフレームhandler) Sアリbackend(backend Tキョウユウバイタイアミデンソウワクテイキョウウツワ) {
	Backend = backend
}
func (self *Tイーサネットフレームhandler) Getbackend() Tキョウユウバイタイアミデンソウワクテイキョウウツワ {
	return Backend
}
func (self *Tイーサネットフレームhandler) Oイーサネットフレームreceivewhen(データポインタ uintptr, サイズ int) bool {
	イーサネットコンソール.Mインサツ(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *Tイーサネットフレームhandler) Sソウシン(テンソウサキmacbe uint64, データポインタ uintptr, サイズ uint32) {
	Backend.Sフレームソウシン(テンソウサキmacbe, フレーム.イーサネットカタbe, データポインタ, サイズ)
}
func (self *Tイーサネットフレームhandler) Sフレームソウシン(テンソウサキmacbe uint64, イーサネットカタbe uint16, データポインタ uintptr, サイズ uint32) {
	Backend.Sフレームソウシン(テンソウサキmacbe, イーサネットカタbe, データポインタ, サイズ)
}
func (self *Tイーサネットフレームhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *Tイーサネットフレームhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *Tイーサネットフレームhandler) Providerget() Tキョウユウバイタイアミデンソウワクテイキョウウツワ {
	return Backend
}

type Tイーサネットフレームrawデータhandler struct {
	TRawデータhandler
}

var provider Tキョウユウバイタイアミデンソウワクテイキョウウツワ

func (self *Tイーサネットフレームrawデータhandler) Init(pprovider Tキョウユウバイタイアミデンソウワクテイキョウウツワ, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *Tイーサネットフレームrawデータhandler) Oトキrawデータreceive(データポインタ uintptr, サイズ int) bool {
	return provider.Oトキrawデータreceive(データポインタ, サイズ)
}
func (self *Tイーサネットフレームrawデータhandler) Sソウシン(データポインタ uintptr, サイズ uint32) {
	provider.Sソウシン(データポインタ, サイズ)
}
func (self *Tイーサネットフレームrawデータhandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *Tイーサネットフレームrawデータhandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *Tイーサネットフレームrawデータhandler) Providerget() Tキョウユウバイタイアミデンソウワクテイキョウウツワ {
	return provider
}

type Tキョウユウバイタイアミデンソウワクテイキョウウツワ struct {
	ネットワークカードゲーム	Tamdam79c973
	handler_2	[65565]Iイーサネットフレームhandler
}

func (self *Tキョウユウバイタイアミデンソウワクテイキョウウツワ) Init(backend Tamdam79c973) {

	self.ネットワークカードゲーム = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var カウント uint16 = 0

func (self *Tキョウユウバイタイアミデンソウワクテイキョウウツワ) Oトキrawデータreceive(データポインタ uintptr, サイズ int) bool {

	var buffer_2 *Tイーサネットフレームヘッダbuffer = (*Tイーサネットフレームヘッダbuffer)(Pointer(データポインタ))
	var フレーム Tキョウユウバイタイアミデンソウワクセントウブ = Tキョウユウバイタイアミデンソウワクセントウブ{}
	フレーム.Init(*buffer_2)
	var reply bool = false

	if フレーム.テンソウサキmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(フレーム.テンソウサキmacbe) == self.Getmacaddress() {
		if handler_2[フレーム.イーサネットカタbe] != nil {
			イーサネットコンソール.Mインサツ(([]byte)("provider\n"))

			var バンチサンショウ uintptr = uintptr(Pointer(データポインタ)) + uintptr(フレームヘッダサイズ)
			reply = handler_2[フレーム.イーサネットカタbe].Oイーサネットフレームreceivewhen(バンチサンショウ, サイズ-フレームヘッダサイズ)

		}
	}

	if reply {
		フレーム.テンソウサキmacbe = フレーム.テンソウモトmacbe
		フレーム.テンソウモトmacbe = Unsignedinteger48r(self.Getmacaddress())
		フレーム.Sアリbuffer(buffer_2)

	}

	イーサネットコンソール.Mインサツxy(([]byte)("spro["), 0, 1)
	イーサネットコンソール.MUnsignedinteger64インサツ(フレーム.テンソウモトmacbe)
	イーサネットコンソール.Mインサツ(([]byte)(":"))
	イーサネットコンソール.MUnsignedinteger64インサツ(フレーム.テンソウサキmacbe)
	イーサネットコンソール.Mインサツ(([]byte)(":]["))
	イーサネットコンソール.MUnsignedinteger64インサツ(self.Getmacaddress())
	イーサネットコンソール.Mインサツ(([]byte)(":"))
	イーサネットコンソール.MUnsignedinteger16インサツ(フレーム.イーサネットカタbe)
	イーサネットコンソール.Mインサツ(([]byte)("]"))

	return reply

}
func (self *Tキョウユウバイタイアミデンソウワクテイキョウウツワ) Sソウシン(データポインタ uintptr, サイズ uint32) {
	self.ネットワークカードゲーム.Sソウシン(データポインタ, サイズ)
}
func (self *Tキョウユウバイタイアミデンソウワクテイキョウウツワ) Sフレームソウシン(テンソウサキmacbe uint64, イーサネットカタbe uint16, データポインタ uintptr, サイズ uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *Tイーサネットフレームヘッダbuffer = (*Tイーサネットフレームヘッダbuffer)(Pointer(&buffer2_2))

	var フレーム Tキョウユウバイタイアミデンソウワクセントウブ = Tキョウユウバイタイアミデンソウワクセントウブ{}
	フレーム.Init(*buffer_2)

	フレーム.テンソウサキmacbe = Unsignedinteger48r(テンソウサキmacbe)
	フレーム.テンソウモトmacbe = Unsignedinteger48r(self.ネットワークカードゲーム.Getmacaddress())
	フレーム.イーサネットカタbe = Unsignedinteger16r(イーサネットカタbe)

	フレーム.Sアリbuffer(buffer_2)
	var テンソウモト_2 [4096]byte = *(*([4096]byte))(Pointer(データポインタ))

	var i uint32 = 0
	for i = 0; i < サイズ; i++ {
		buffer2_2[uint32(フレームヘッダサイズ)+i] = テンソウモト_2[i]

	}

	var バンチサンショウ uintptr = uintptr(Pointer(&buffer2_2))

	self.ネットワークカードゲーム.Sソウシン(バンチサンショウ, サイズ+uint32(フレームヘッダサイズ))

}
func (self *Tキョウユウバイタイアミデンソウワクテイキョウウツワ) Getmacaddress() uint64 {
	return self.ネットワークカードゲーム.Getmacaddress()
}
func (self *Tキョウユウバイタイアミデンソウワクテイキョウウツワ) Getipaddress() uint64 {
	return self.ネットワークカードゲーム.Getipaddress()
}
