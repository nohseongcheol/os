package stopur

import . "unsafe"

import . "interrupt"
import . "console"

type IStopureventhandler interface {
	Tændttick()
}

var iStopureventhandler IStopureventhandler

type TStandardStopureventhandler struct {
}

func (selv *TStandardStopureventhandler) Tændttick() {
}

type TStopurdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TStopurdriver, uint32) uint32

func (selv *TStopurdriver) Init(manager *TInterruptmanager, tastatureventhandler IStopureventhandler) {
	iStopureventhandler = &TStandardStopureventhandler{}
	if tastatureventhandler != nil {
		iStopureventhandler = tastatureventhandler
	}

	interrupthandler = (*TStopurdriver).Håndtaginterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	selv.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickAntal uint32 = 0

func (selv *TStopurdriver) Håndtaginterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Udskrivxy(tickAntal, 3, 1)
	tickAntal++

	return esp
}
