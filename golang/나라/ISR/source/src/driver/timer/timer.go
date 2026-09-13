package timer

import . "unsafe"

import . "פסק"
import . "console"

type ITimereventhandler interface {
	Oפעילtick()
}

var itimereventhandler ITimereventhandler

type Tברירתמחדלtimereventhandler struct {
}

func (self *Tברירתמחדלtimereventhandler) Oפעילtick() {
}

type TTimerdriver struct {
	Tפסקhandler
}

var פסקhandler func(*TTimerdriver, uint32) uint32

func (self *TTimerdriver) Init(manager *Tפסקmanager, מקלדתeventhandler ITimereventhandler) {
	itimereventhandler = &Tברירתמחדלtimereventhandler{}
	if מקלדתeventhandler != nil {
		itimereventhandler = מקלדתeventhandler
	}

	פסקhandler = (*TTimerdriver).Hידיתפסק
	var address uintptr
	address = uintptr(Pointer(&פסקhandler))

	self.Tפסקhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TTimerdriver) Hידיתפסק(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32הדפסהxy(tickcount, 3, 1)
	tickcount++

	return esp
}
