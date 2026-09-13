package timer

import . "unsafe"

import . "interrupt"
import . "konsolë"

type ITimerNgjarjehandler interface {
	Ontick()
}

var itimerNgjarjehandler ITimerNgjarjehandler

type TEprezgjedhurtimerNgjarjehandler struct {
}

func (vetvetja *TEprezgjedhurtimerNgjarjehandler) Ontick() {
}

type TTimerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTimerdriver, uint32) uint32

func (vetvetja *TTimerdriver) Init(manazhuesi *TInterruptManazhuesi, tastieraNgjarjehandler ITimerNgjarjehandler) {
	itimerNgjarjehandler = &TEprezgjedhurtimerNgjarjehandler{}
	if tastieraNgjarjehandler != nil {
		itimerNgjarjehandler = tastieraNgjarjehandler
	}

	interrupthandler = (*TTimerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	vetvetja.TInterrupthandler.Init(0x20, uintptr(Pointer(manazhuesi)), address)

}

var tickcount uint32 = 0

func (vetvetja *TTimerdriver) Handleinterrupt(esp uint32) uint32 {
	konsolë_2 := TKonsolë{}
	konsolë_2.MUnsignedinteger32Printoxy(tickcount, 3, 1)
	tickcount++

	return esp
}
