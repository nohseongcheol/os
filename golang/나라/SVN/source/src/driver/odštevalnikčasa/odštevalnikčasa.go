package odštevalnikčasa

import . "unsafe"

import . "prekinitev"
import . "console"

type IOdštevalnikčasaeventhandler interface {
	Vključenotick()
}

var iOdštevalnikčasaeventhandler IOdštevalnikčasaeventhandler

type TPrivzetoOdštevalnikčasaeventhandler struct {
}

func (sam *TPrivzetoOdštevalnikčasaeventhandler) Vključenotick() {
}

type TOdštevalnikčasadriver struct {
	TPrekinitevhandler
}

var prekinitevhandler func(*TOdštevalnikčasadriver, uint32) uint32

func (sam *TOdštevalnikčasadriver) Init(manager *TPrekinitevmanager, tipkovnicaeventhandler IOdštevalnikčasaeventhandler) {
	iOdštevalnikčasaeventhandler = &TPrivzetoOdštevalnikčasaeventhandler{}
	if tipkovnicaeventhandler != nil {
		iOdštevalnikčasaeventhandler = tipkovnicaeventhandler
	}

	prekinitevhandler = (*TOdštevalnikčasadriver).RočicaPrekinitev
	var address uintptr
	address = uintptr(Pointer(&prekinitevhandler))

	sam.TPrekinitevhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (sam *TOdštevalnikčasadriver) RočicaPrekinitev(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Natisnixy(tickcount, 3, 1)
	tickcount++

	return esp
}
