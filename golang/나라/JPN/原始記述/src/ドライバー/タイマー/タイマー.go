package タイマー

import . "unsafe"

import . "割込み"
import . "コンソール"

type Iタイマー事象handler interface {
	O時tick()
}

var iタイマー事象handler Iタイマー事象handler

type Tデフォルトタイマー事象handler struct {
}

func (self *Tデフォルトタイマー事象handler) O時tick() {
}

type Tタイマードライバー struct {
	T割込みhandler
}

var 割込みhandler func(*Tタイマードライバー, uint32) uint32

func (self *Tタイマードライバー) Init(管理者 *T割込み管理者, キーボード事象handler Iタイマー事象handler) {
	iタイマー事象handler = &Tデフォルトタイマー事象handler{}
	if キーボード事象handler != nil {
		iタイマー事象handler = キーボード事象handler
	}

	割込みhandler = (*Tタイマードライバー).H取っ手割込み
	var address uintptr
	address = uintptr(Pointer(&割込みhandler))

	self.T割込みhandler.Init(0x20, uintptr(Pointer(管理者)), address)

}

var tickカウント uint32 = 0

func (self *Tタイマードライバー) H取っ手割込み(esp uint32) uint32 {
	コンソール_2 := Tコンソール{}
	コンソール_2.MUnsignedinteger32印刷xy(tickカウント, 3, 1)
	tickカウント++

	return esp
}
