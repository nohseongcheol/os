package timer

import . "unsafe"

import . "interrupt"
import . "console"

type ITimereventhandler interface {
	Вклученоtick()
}

var itimereventhandler ITimereventhandler

type TСтандардноtimereventhandler struct {
}

func (само *TСтандардноtimereventhandler) Вклученоtick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (само *TTimerdriver) Init(manager *TInterruptmanager, тастатураeventhandler ITimereventhandler) {
	itimereventhandler = &TСтандардноtimereventhandler{}
	if тастатураeventhandler != nil {
		itimereventhandler = тастатураeventhandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	само.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (само *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Печатиxy(tickcount, 3, 1)
	tickcount++

	return esp
}
