package timer

import . "unsafe"

import . "pārtraukums"
import . "console"

type ITimerNotikumshandler interface {
	Ieslēgtstick()
}

var itimerNotikumshandler ITimerNotikumshandler

type TNoklusētaistimerNotikumshandler struct {
}

func (pats *TNoklusētaistimerNotikumshandler) Ieslēgtstick() {
}

type TTimerdriver struct {
	TPārtraukumshandler
}

var pārtraukumshandler func(*TTimerdriver, uint32) uint32

func (pats *TTimerdriver) Init(manager *TPārtraukumsmanager, klaviatūraNotikumshandler ITimerNotikumshandler) {
	itimerNotikumshandler = &TNoklusētaistimerNotikumshandler{}
	if klaviatūraNotikumshandler != nil {
		itimerNotikumshandler = klaviatūraNotikumshandler
	}

	pārtraukumshandler = (*TTimerdriver).HandlePārtraukums
	var address uintptr
	address = uintptr(Pointer(&pārtraukumshandler))

	pats.TPārtraukumshandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (pats *TTimerdriver) HandlePārtraukums(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Drukātxy(tickcount, 3, 1)
	tickcount++

	return esp
}
