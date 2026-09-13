package minuterie

import . "unsafe"

import . "interruption"
import . "console"

type IMinuterieévénementhandler interface {
	Surtick()
}

var iminuterieévénementhandler IMinuterieévénementhandler

type TPardéfautminuterieévénementhandler struct {
}

func (self *TPardéfautminuterieévénementhandler) Surtick() {
}

type TMinuteriepilote struct {
	TInterruptionhandler
}

var interruptionhandler func(*TMinuteriepilote, uint32) uint32

func (self *TMinuteriepilote) Init(gestionnaire *TInterruptiongestionnaire, clavierévénementhandler IMinuterieévénementhandler) {
	iminuterieévénementhandler = &TPardéfautminuterieévénementhandler{}
	if clavierévénementhandler != nil {
		iminuterieévénementhandler = clavierévénementhandler
	}

	interruptionhandler = (*TMinuteriepilote).Poignéeinterruption
	var address uintptr
	address = uintptr(Pointer(&interruptionhandler))

	self.TInterruptionhandler.Init(0x20, uintptr(Pointer(gestionnaire)), address)

}

var tickNombre uint32 = 0

func (self *TMinuteriepilote) Poignéeinterruption(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Imprimerxy(tickNombre, 3, 1)
	tickNombre++

	return esp
}
