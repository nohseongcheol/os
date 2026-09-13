package keyboard

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type IMouseeventhandler interface {
	Onmouseපහළ(button int8)
	Onmouseඉහළ(button int8)
	Onmousemove(x int8, y int8)
}

var imouseeventhandler IMouseeventhandler

type TDefaultmouseeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self TDefaultmouseeventhandler) Onmouseපහළ(button int8) {
	buffer := []byte("+")
	console_2.MPrintxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TDefaultmouseeventhandler) Onmouseඉහළ(button int8)	{}
func (self TDefaultmouseeventhandler) Onmousemove(x int8, y int8) {

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

type TMousedriver struct {
	TInterrupthandler
}

var activemousedriver *TMousedriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var commandport_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portkiyavimabyte(commandport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputfull() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portkiyavimabyte(commandport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func livimaps2command(අගය uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Portlivimabyte(commandport_2, අගය)
	return true
}

func livimaps2data(අගය uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Portlivimabyte(dataport_2, අගය)
	return true
}

func kiyavimaps2data() (uint8, bool) {
	if !waitps2outputfull() {
		return 0, false
	}
	return Portkiyavimabyte(dataport_2), true
}

func sendmousecommand(අගය uint8) bool {
	if !livimaps2command(0xD4) || !livimaps2data(අගය) {
		return false
	}
	ack, ok := kiyavimaps2data()
	return ok && ack == 0xFA
}

func (self *TMousedriver) Initdriver(manager *TInterruptmanager, mouseeventhandler IMouseeventhandler) {

	imouseeventhandler = TDefaultmouseeventhandler{}

	if mouseeventhandler != nil {
		imouseeventhandler = mouseeventhandler
	}

	activemousedriver = self
	interrupthandler = handlemouseinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portkiyavimabyte(commandport_2)&0x01) != 0; i++ {
		Portkiyavimabyte(dataport_2)
	}

	if !livimaps2command(0xA8) || !livimaps2command(0x20) {
		return
	}
	status, ok := kiyavimaps2data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !livimaps2command(0x60) || !livimaps2data(status) {
		return
	}

	if !sendmousecommand(0xF6) || !sendmousecommand(0xF4) {
		return
	}
	offset = 0

}

func handlemouseinterrupt(esp uint32) uint32 {
	if activemousedriver == nil {
		Portkiyavimabyte(dataport_2)
		return esp
	}
	return activemousedriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingmouseevent bool

func (self *TMousedriver) Handleinterrupt(esp uint32) uint32 {
	status := Portkiyavimabyte(commandport_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := Portkiyavimabyte(dataport_2)

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
		pendingbutton = int8(packetstatus & 0x07)
		pendingmouseevent = true
	}

	return esp

}

func Processpendingmouseevents() {
	if imouseeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingmouseevent {
		Interruptactive()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	නවbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingmouseevent = false
	Interruptactive()

	if x != 0 || y != 0 {
		imouseeventhandler.Onmousemove(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (නවbutton & mask) != (oldbutton & mask) {
			if (නවbutton & mask) != 0 {
				imouseeventhandler.Onmouseපහළ(int8(i + 1))
			} else {
				imouseeventhandler.Onmouseඉහළ(int8(i + 1))
			}
		}
	}
	button_2 = නවbutton
}
