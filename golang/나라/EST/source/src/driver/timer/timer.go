package timer

import . "unsafe"

import . "katkestus"
import . "console"

type ITimerSündmushandler interface {
	Seestick()
}

var itimerSündmushandler ITimerSündmushandler

type TVaikimisitimerSündmushandler struct {
}

func (ise *TVaikimisitimerSündmushandler) Seestick() {
}

type TTimerdriver struct {
	TKatkestushandler
}

var katkestushandler func(*TTimerdriver, uint32) uint32

func (ise *TTimerdriver) Init(manager *TKatkestusmanager, klaviatuurSündmushandler ITimerSündmushandler) {
	itimerSündmushandler = &TVaikimisitimerSündmushandler{}
	if klaviatuurSündmushandler != nil {
		itimerSündmushandler = klaviatuurSündmushandler
	}

	katkestushandler = (*TTimerdriver).HandleKatkestus
	var address uintptr
	address = uintptr(Pointer(&katkestushandler))

	ise.TKatkestushandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (ise *TTimerdriver) HandleKatkestus(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Prindixy(tickcount, 3, 1)
	tickcount++

	return esp
}
