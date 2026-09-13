package timer

import . "unsafe"

import . "مداخلت"
import . "console"

type ITimerواقعہhandler interface {
	Oچالوtick()
}

var itimerواقعہhandler ITimerواقعہhandler

type Tطےشدہtimerواقعہhandler struct {
}

func (self *Tطےشدہtimerواقعہhandler) Oچالوtick() {
}

type TTimerdriver struct {
	Tمداخلتhandler
}

var مداخلتhandler func(*TTimerdriver, uint32) uint32

func (self *TTimerdriver) Init(manager *Tمداخلتmanager, کیبورڈواقعہhandler ITimerواقعہhandler) {
	itimerواقعہhandler = &Tطےشدہtimerواقعہhandler{}
	if کیبورڈواقعہhandler != nil {
		itimerواقعہhandler = کیبورڈواقعہhandler
	}

	مداخلتhandler = (*TTimerdriver).Handleمداخلت
	var address uintptr
	address = uintptr(Pointer(&مداخلتhandler))

	self.Tمداخلتhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TTimerdriver) Handleمداخلت(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32چھاپیںxy(tickcount, 3, 1)
	tickcount++

	return esp
}
