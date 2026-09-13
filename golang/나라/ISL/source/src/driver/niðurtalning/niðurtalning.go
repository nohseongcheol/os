package niðurtalning

import . "unsafe"

import . "interrupt"
import . "console"

type INiðurtalningeventhandler interface {
	Notatick()
}

var iNiðurtalningeventhandler INiðurtalningeventhandler

type TSjálfgefiðNiðurtalningeventhandler struct {
}

func (sjálft *TSjálfgefiðNiðurtalningeventhandler) Notatick() {
}

type TNiðurtalningdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TNiðurtalningdriver, uint32) uint32

func (sjálft *TNiðurtalningdriver) Init(manager *TInterruptmanager, lyklaborðeventhandler INiðurtalningeventhandler) {
	iNiðurtalningeventhandler = &TSjálfgefiðNiðurtalningeventhandler{}
	if lyklaborðeventhandler != nil {
		iNiðurtalningeventhandler = lyklaborðeventhandler
	}

	interrupthandler = (*TNiðurtalningdriver).Haldfanginterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	sjálft.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (sjálft *TNiðurtalningdriver) Haldfanginterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Prentaxy(tickcount, 3, 1)
	tickcount++

	return esp
}
