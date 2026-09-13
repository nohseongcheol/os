package timer

import . "unsafe"

import . "giánđoạn"
import . "console"

type ITimerSựkiệnhandler interface {
	Bậttick()
}

var itimerSựkiệnhandler ITimerSựkiệnhandler

type TMặcđịnhtimerSựkiệnhandler struct {
}

func (mình *TMặcđịnhtimerSựkiệnhandler) Bậttick() {
}

type TTimerdriver struct {
	TGiánđoạnhandler
}

var giánđoạnhandler func(*TTimerdriver, uint32) uint32

func (mình *TTimerdriver) Init(manager *TGiánđoạnmanager, bànphímSựkiệnhandler ITimerSựkiệnhandler) {
	itimerSựkiệnhandler = &TMặcđịnhtimerSựkiệnhandler{}
	if bànphímSựkiệnhandler != nil {
		itimerSựkiệnhandler = bànphímSựkiệnhandler
	}

	giánđoạnhandler = (*TTimerdriver).HandleGiánđoạn
	var address uintptr
	address = uintptr(Pointer(&giánđoạnhandler))

	mình.TGiánđoạnhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickSốlượng uint32 = 0

func (mình *TTimerdriver) HandleGiánđoạn(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Inxy(tickSốlượng, 3, 1)
	tickSốlượng++

	return esp
}
