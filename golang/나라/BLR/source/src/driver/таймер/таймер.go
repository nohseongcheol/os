package таймер

import . "unsafe"

import . "перарыванне"
import . "console"

type IТаймерПадзеяhandler interface {
	Ontick()
}

var iТаймерПадзеяhandler IТаймерПадзеяhandler

type TСтандартнаТаймерПадзеяhandler struct {
}

func (self *TСтандартнаТаймерПадзеяhandler) Ontick() {
}

type TТаймерdriver struct {
	TПерарываннеhandler
}

var перарываннеhandler func(*TТаймерdriver, uint32) uint32

func (self *TТаймерdriver) Init(manager *TПерарываннеmanager, клавіятураПадзеяhandler IТаймерПадзеяhandler) {
	iТаймерПадзеяhandler = &TСтандартнаТаймерПадзеяhandler{}
	if клавіятураПадзеяhandler != nil {
		iТаймерПадзеяhandler = клавіятураПадзеяhandler
	}

	перарываннеhandler = (*TТаймерdriver).HandleПерарыванне
	var address uintptr
	address = uintptr(Pointer(&перарываннеhandler))

	self.TПерарываннеhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TТаймерdriver) HandleПерарыванне(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Друкавацьxy(tickcount, 3, 1)
	tickcount++

	return esp
}
