package taymer

import . "unsafe"

import . "interrupt"
import . "console"

type ITaymereventhandler interface {
	Yoqishtick()
}

var iTaymereventhandler ITaymereventhandler

type TAndozaTaymereventhandler struct {
}

func (self *TAndozaTaymereventhandler) Yoqishtick() {
}

type TTaymerdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TTaymerdriver, uint32) uint32

func (self *TTaymerdriver) Init(manager *TInterruptmanager, klaviaturaeventhandler ITaymereventhandler) {
	iTaymereventhandler = &TAndozaTaymereventhandler{}
	if klaviaturaeventhandler != nil {
		iTaymereventhandler = klaviaturaeventhandler
	}

	interrupthandler = (*TTaymerdriver).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TTaymerdriver) Handleinterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Chopetishxy(tickcount, 3, 1)
	tickcount++

	return esp
}
