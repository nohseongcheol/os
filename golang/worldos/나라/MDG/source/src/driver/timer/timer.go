/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package timer

import . "unsafe"

import . "interrupt"
import . "konsoly"

type ITimereventhandler interface {
	Ontick()
}

var itimereventhandler ITimereventhandler

type TTsotratimereventhandler struct {
}

func (nytena *TTsotratimereventhandler) Ontick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (nytena *TTimerdriver) Init(mpandrindra *TInterruptMpandrindra, fafantenyeventhandler ITimereventhandler) {
	itimereventhandler = &TTsotratimereventhandler{}
	if fafantenyeventhandler != nil {
		itimereventhandler = fafantenyeventhandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	nytena.TInterrupthandler.Init(0x20, uintptr(Pointer(mpandrindra)), address)

}

var tickcount uint32 = 0

func (nytena *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	konsoly_2 := TKonsoly{}
	konsoly_2.MUnsignedinteger32Atontayxy(tickcount, 3, 1)
	tickcount++

	return esp
}
