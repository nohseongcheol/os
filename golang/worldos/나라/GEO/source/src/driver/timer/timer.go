/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package timer

import . "unsafe"

import . "interrupt"
import . "console"

type ITimereventhandler interface {
	Ontick()
}

var itimereventhandler ITimereventhandler

type Tნაგულისხმევიtimereventhandler struct {
}

func (self *Tნაგულისხმევიtimereventhandler) Ontick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (self *TTimerdriver) Init(manager *TInterruptmanager, კლავიატურაeventhandler ITimereventhandler) {
	itimereventhandler = &Tნაგულისხმევიtimereventhandler{}
	if კლავიატურაeventhandler != nil {
		itimereventhandler = კლავიატურაeventhandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32ბეჭდვაxy(tickcount, 3, 1)
	tickcount++

	return esp
}
