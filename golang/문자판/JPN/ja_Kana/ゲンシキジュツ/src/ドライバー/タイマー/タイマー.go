package タイマー

import . "unsafe"

import . "ワリコミ"
import . "コンソール"

type Iタイマージショウhandler interface {
	Oトキtick()
}

var iタイマージショウhandler Iタイマージショウhandler

type Tデフォルトタイマージショウhandler struct {
}

func (self *Tデフォルトタイマージショウhandler) Oトキtick() {
}

type Tタイマードライバー struct {
	Tワリコミhandler
}

var ワリコミhandler func(*Tタイマードライバー, uint32) uint32

func (self *Tタイマードライバー) Init(カンリシャ *Tワリコミカンリシャ, キーボードジショウhandler Iタイマージショウhandler) {
	iタイマージショウhandler = &Tデフォルトタイマージショウhandler{}
	if キーボードジショウhandler != nil {
		iタイマージショウhandler = キーボードジショウhandler
	}

	ワリコミhandler = (*Tタイマードライバー).Hトッテワリコミ
	var address uintptr
	address = uintptr(Pointer(&ワリコミhandler))

	self.Tワリコミhandler.Init(0x20, uintptr(Pointer(カンリシャ)), address)

}

var tickカウント uint32 = 0

func (self *Tタイマードライバー) Hトッテワリコミ(esp uint32) uint32 {
	コンソール_2 := Tコンソール{}
	コンソール_2.MUnsignedinteger32インサツxy(tickカウント, 3, 1)
	tickカウント++

	return esp
}
