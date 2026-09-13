package timer

import . "unsafe"

import . "interrupt"
import . "консол"

type ITimereventhandler interface {
	Ontick()
}

var itimereventhandler ITimereventhandler

type TСтандартtimereventhandler struct {
}

func (self *TСтандартtimereventhandler) Ontick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (self *TTimerdriver) Init(зохицуулагч *TInterruptЗохицуулагч, гарeventhandler ITimereventhandler) {
	itimereventhandler = &TСтандартtimereventhandler{}
	if гарeventhandler != nil {
		itimereventhandler = гарeventhandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x20, uintptr(Pointer(зохицуулагч)), address)

}

var tickcount uint32 = 0

func (self *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	консол_2 := TКонсол{}
	консол_2.MUnsignedinteger32Хэвлэхxy(tickcount, 3, 1)
	tickcount++

	return esp
}
