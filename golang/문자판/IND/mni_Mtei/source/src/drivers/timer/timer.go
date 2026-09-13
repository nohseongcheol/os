package timer

import . "unsafe"

import . "interrupt"
import . "console"

type ITimerEventHandler interface {
	OnTick()
}

var iTimerEventHandler ITimerEventHandler

type TDefaultTimerEventHandler struct {
}

func (self *TDefaultTimerEventHandler) OnTick() {
}

type TTimerDriver struct {
	TInterruptHandler
}

var interruptHandler func(*TTimerDriver, uint32) uint32

func (self *TTimerDriver) Init(manager *TInterruptManager, keyboardEventHandler ITimerEventHandler) {
	iTimerEventHandler = &TDefaultTimerEventHandler{}
	if keyboardEventHandler != nil {
		iTimerEventHandler = keyboardEventHandler
	}

	interruptHandler = (*TTimerDriver).HandleInterrupt
	var addr uintptr
	addr = uintptr(Pointer(&interruptHandler))

	self.TInterruptHandler.Init(0x20, uintptr(Pointer(manager)), addr)

}

var tickCount uint32 = 0

func (self *TTimerDriver) HandleInterrupt(esp uint32) uint32 {
	콘솔 := T콘솔{}
	콘솔.MUint32출력XY(tickCount, 3, 1)
	tickCount++

	return esp
}
