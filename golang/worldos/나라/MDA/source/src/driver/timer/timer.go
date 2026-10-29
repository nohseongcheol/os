/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package timer

import . "unsafe"

import . "intrerupere"
import . "console"

type ITimerEvenimenthandler interface {
	Pornittick()
}

var itimerEvenimenthandler ITimerEvenimenthandler

type TImplicitătimerEvenimenthandler struct {
}

func (sine *TImplicitătimerEvenimenthandler) Pornittick() {
}

type TTimerdriver struct {
	TIntreruperehandler
}

var intreruperehandler func(*TTimerdriver, uint32) uint32

func (sine *TTimerdriver) Init(manager *TIntreruperemanager, tastaturăEvenimenthandler ITimerEvenimenthandler) {
	itimerEvenimenthandler = &TImplicitătimerEvenimenthandler{}
	if tastaturăEvenimenthandler != nil {
		itimerEvenimenthandler = tastaturăEvenimenthandler
	}

	intreruperehandler = (*TTimerdriver).MânerIntrerupere
	var address uintptr
	address = uintptr(Pointer(&intreruperehandler))

	sine.TIntreruperehandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (sine *TTimerdriver) MânerIntrerupere(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Tipăreștexy(tickcount, 3, 1)
	tickcount++

	return esp
}
