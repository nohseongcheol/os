package たいまー

import . "unsafe"

import . "わりこみ"
import . "こんそーる"

type Iたいまーじしょうhandler interface {
	Oときtick()
}

var iたいまーじしょうhandler Iたいまーじしょうhandler

type Tでふぉるとたいまーじしょうhandler struct {
}

func (self *Tでふぉるとたいまーじしょうhandler) Oときtick() {
}

type Tたいまーどらいばー struct {
	Tわりこみhandler
}

var わりこみhandler func(*Tたいまーどらいばー, uint32) uint32

func (self *Tたいまーどらいばー) Init(かんりしゃ *Tわりこみかんりしゃ, きーぼーどじしょうhandler Iたいまーじしょうhandler) {
	iたいまーじしょうhandler = &Tでふぉるとたいまーじしょうhandler{}
	if きーぼーどじしょうhandler != nil {
		iたいまーじしょうhandler = きーぼーどじしょうhandler
	}

	わりこみhandler = (*Tたいまーどらいばー).Hとってわりこみ
	var address uintptr
	address = uintptr(Pointer(&わりこみhandler))

	self.Tわりこみhandler.Init(0x20, uintptr(Pointer(かんりしゃ)), address)

}

var tickかうんと uint32 = 0

func (self *Tたいまーどらいばー) Hとってわりこみ(esp uint32) uint32 {
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.MUnsignedinteger32いんさつxy(tickかうんと, 3, 1)
	tickかうんと++

	return esp
}
