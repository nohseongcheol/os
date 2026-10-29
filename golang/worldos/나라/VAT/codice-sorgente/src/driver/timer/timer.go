/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package timer

import . "unsafe"

import . "interrupt"
import . "console"

type ITimerEventohandler interface {
	Accesotick()
}

var itimerEventohandler ITimerEventohandler

type TPredefinitotimerEventohandler struct {
}

func (séstesso *TPredefinitotimerEventohandler) Accesotick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (séstesso *TTimerdriver) Init(manager *TInterruptmanager, tastieraEventohandler ITimerEventohandler) {
	itimerEventohandler = &TPredefinitotimerEventohandler{}
	if tastieraEventohandler != nil {
		itimerEventohandler = tastieraEventohandler
	}

	interrupthandler = (*TTimerdriver).Manigliainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	séstesso.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickConteggio uint32 = 0

func (séstesso *TTimerdriver) Manigliainterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Stampaxy(tickConteggio, 3, 1)
	tickConteggio++

	return esp
}
