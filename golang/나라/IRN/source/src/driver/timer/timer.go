package timer

import . "unsafe"

import . "interrupt"
import . "console"

type ITimereventhandler interface {
	Oروشنtick()
}

var itimereventhandler ITimereventhandler

type TDefaulttimereventhandler struct {
}

func (خود *TDefaulttimereventhandler) Oروشنtick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (خود *TTimerdriver) Init(manager *TInterruptmanager, صفحهکلیدeventhandler ITimereventhandler) {
	itimereventhandler = &TDefaulttimereventhandler{}
	if صفحهکلیدeventhandler != nil {
		itimereventhandler = صفحهکلیدeventhandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	خود.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (خود *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32چاپxy(tickcount, 3, 1)
	tickcount++

	return esp
}
