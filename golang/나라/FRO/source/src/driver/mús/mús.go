package knappaborð

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type IMúseventhandler interface {
	OnMúsdown(knappur int8)
	OnMúsup(knappur int8)
	OnMúsmove(x int8, y int8)
}

var iMúseventhandler IMúseventhandler

type TForsettMúseventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self TForsettMúseventhandler) OnMúsdown(knappur int8) {
	buffer := []byte("+")
	console_2.MPrintxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TForsettMúseventhandler) OnMúsup(knappur int8)	{}
func (self TForsettMúseventhandler) OnMúsmove(x int8, y int8) {

	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 80 {
		xposition = 79
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 25 {
		yposition = 24
	}

	buffer := []byte(" ")
	console_2.MPrintxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MPrintxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TMúsdriver struct {
	TInterrupthandler
}

var activeMúsdriver *TMúsdriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var stýriboðport_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portlesabyte(stýriboðport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputfull() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portlesabyte(stýriboðport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skrivaps2Stýriboð(value uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Portskrivabyte(stýriboðport_2, value)
	return true
}

func skrivaps2data(value uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Portskrivabyte(dataport_2, value)
	return true
}

func lesaps2data() (uint8, bool) {
	if !waitps2outputfull() {
		return 0, false
	}
	return Portlesabyte(dataport_2), true
}

func sendMúsStýriboð(value uint8) bool {
	if !skrivaps2Stýriboð(0xD4) || !skrivaps2data(value) {
		return false
	}
	ack, ok := lesaps2data()
	return ok && ack == 0xFA
}

func (self *TMúsdriver) Initdriver(manager *TInterruptmanager, múseventhandler IMúseventhandler) {

	iMúseventhandler = TForsettMúseventhandler{}

	if múseventhandler != nil {
		iMúseventhandler = múseventhandler
	}

	activeMúsdriver = self
	interrupthandler = handleMúsinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portlesabyte(stýriboðport_2)&0x01) != 0; i++ {
		Portlesabyte(dataport_2)
	}

	if !skrivaps2Stýriboð(0xA8) || !skrivaps2Stýriboð(0x20) {
		return
	}
	status, ok := lesaps2data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !skrivaps2Stýriboð(0x60) || !skrivaps2data(status) {
		return
	}

	if !sendMúsStýriboð(0xF6) || !sendMúsStýriboð(0xF4) {
		return
	}
	offset = 0

}

func handleMúsinterrupt(esp uint32) uint32 {
	if activeMúsdriver == nil {
		Portlesabyte(dataport_2)
		return esp
	}
	return activeMúsdriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var knappur_2 int8
var pendingx int16
var pendingy int16
var pendingknappur int8
var pendingMúsevent bool

func (self *TMúsdriver) Handleinterrupt(esp uint32) uint32 {
	status := Portlesabyte(stýriboðport_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := Portlesabyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetstatus := uint8(buffer_2[0])

		if (packetstatus & 0xC0) == 0 {
			pendingx += int16(buffer_2[1])
			pendingy += int16(buffer_2[2])
			if pendingx > 127 {
				pendingx = 127
			} else if pendingx < -127 {
				pendingx = -127
			}
			if pendingy > 127 {
				pendingy = 127
			} else if pendingy < -127 {
				pendingy = -127
			}
		}
		pendingknappur = int8(packetstatus & 0x07)
		pendingMúsevent = true
	}

	return esp

}

func ProcesspendingMúsevents() {
	if iMúseventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingMúsevent {
		Interruptactive()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	newknappur := pendingknappur
	oldknappur := knappur_2

	pendingx = 0
	pendingy = 0
	pendingMúsevent = false
	Interruptactive()

	if x != 0 || y != 0 {
		iMúseventhandler.OnMúsmove(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (newknappur & mask) != (oldknappur & mask) {
			if (newknappur & mask) != 0 {
				iMúseventhandler.OnMúsdown(int8(i + 1))
			} else {
				iMúseventhandler.OnMúsup(int8(i + 1))
			}
		}
	}
	knappur_2 = newknappur
}
