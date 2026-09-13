package timer

import . "unsafe"

import . "interrupt"
import . "console"

type ITimereventhandler interface {
	Ontick()
}

var itimereventhandler ITimereventhandler

type TDefaulttimereventhandler struct {
}

func (self *TDefaulttimereventhandler) Ontick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (self *TTimerdriver) Init(manager *TInterruptmanager, keyboardeventhandler ITimereventhandler) {
	itimereventhandler = &TDefaulttimereventhandler{}
	if keyboardeventhandler != nil {
		itimereventhandler = keyboardeventhandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Çapxy(tickcount, 3, 1)
	tickcount++

	return esp
}
