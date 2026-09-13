package pewaktu

import . "unsafe"

import . "interupsi"
import . "console"

type IPewaktuEvenhandler interface {
	Hiduptick()
}

var iPewaktuEvenhandler IPewaktuEvenhandler

type TBakuPewaktuEvenhandler struct {
}

func (dirisendiri *TBakuPewaktuEvenhandler) Hiduptick() {
}

type TPewaktudriver struct {
	TInterupsihandler
}

var interupsihandler func(*TPewaktudriver, uint32) uint32

func (dirisendiri *TPewaktudriver) Init(manager *TInterupsimanager, papanketikEvenhandler IPewaktuEvenhandler) {
	iPewaktuEvenhandler = &TBakuPewaktuEvenhandler{}
	if papanketikEvenhandler != nil {
		iPewaktuEvenhandler = papanketikEvenhandler
	}

	interupsihandler = (*TPewaktudriver).PenangananInterupsi
	var address uintptr
	address = uintptr(Pointer(&interupsihandler))

	dirisendiri.TInterupsihandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (dirisendiri *TPewaktudriver) PenangananInterupsi(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Cetakxy(tickcount, 3, 1)
	tickcount++

	return esp
}
