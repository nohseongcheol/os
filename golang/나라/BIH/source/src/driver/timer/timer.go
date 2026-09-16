/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package timer

import . "unsafe"

import . "interrupt"
import . "console"

type ITimereventhandler interface {
	Uključentick()
}

var itimereventhandler ITimereventhandler

type TUobičajenotimereventhandler struct {
}

func (self *TUobičajenotimereventhandler) Uključentick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (self *TTimerdriver) Init(manager *TInterruptmanager, tastaturaeventhandler ITimereventhandler) {
	itimereventhandler = &TUobičajenotimereventhandler{}
	if tastaturaeventhandler != nil {
		itimereventhandler = tastaturaeventhandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Štampajxy(tickcount, 3, 1)
	tickcount++

	return esp
}
