package timer

import . "unsafe"

import . "prekid"
import . "console"

type ITimerDogađajhandler interface {
	Uključenotick()
}

var itimerDogađajhandler ITimerDogađajhandler

type TZadanotimerDogađajhandler struct {
}

func (sam *TZadanotimerDogađajhandler) Uključenotick() {
}

type TTimerdriver struct {
	TPrekidhandler
}

var prekidhandler func(*TTimerdriver, uint32) uint32

func (sam *TTimerdriver) Init(manager *TPrekidmanager, tipkovnicaDogađajhandler ITimerDogađajhandler) {
	itimerDogađajhandler = &TZadanotimerDogađajhandler{}
	if tipkovnicaDogađajhandler != nil {
		itimerDogađajhandler = tipkovnicaDogađajhandler
	}

	prekidhandler = (*TTimerdriver).RučkaPrekid
	var address uintptr
	address = uintptr(Pointer(&prekidhandler))

	sam.TPrekidhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (sam *TTimerdriver) RučkaPrekid(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Ispisxy(tickcount, 3, 1)
	tickcount++

	return esp
}
