package keyboard

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type IMouseeventhandler interface {
	Onmouseลง(button int8)
	Onmouseup(button int8)
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

func (self TDefaultmouseeventhandler) Onmouseลง(button int8) {
	buffer := []byte("+")
	console_2.MPrintxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TDefaultmouseeventhandler) Onmouseup(button int8)	{}
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

var ทำงานmousedriver *TMousedriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var commandport_2 uint16 = 0x64

const ps2รอlimit = 100000

func รอps2inputempty() bool {
	for i := 0; i < ps2รอlimit; i++ {
		if (Portanbyte(commandport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func รอps2outputfull() bool {
	for i := 0; i < ps2รอlimit; i++ {
		if (Portanbyte(commandport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func khianps2command(value uint8) bool {
	if !รอps2inputempty() {
		return false
	}
	Portkhianbyte(commandport_2, value)
	return true
}

func khianps2data(value uint8) bool {
	if !รอps2inputempty() {
		return false
	}
	Portkhianbyte(dataport_2, value)
	return true
}

func anps2data() (uint8, bool) {
	if !รอps2outputfull() {
		return 0, false
	}
	return Portanbyte(dataport_2), true
}

func sendmousecommand(value uint8) bool {
	if !khianps2command(0xD4) || !khianps2data(value) {
		return false
	}
	ack, ตกลง := anps2data()
	return ตกลง && ack == 0xFA
}

func (self *TMousedriver) Initdriver(manager *TInterruptmanager, mouseeventhandler IMouseeventhandler) {

	imouseeventhandler = TDefaultmouseeventhandler{}

	if mouseeventhandler != nil {
		imouseeventhandler = mouseeventhandler
	}

	ทำงานmousedriver = self
	interrupthandler = handlemouseinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portanbyte(commandport_2)&0x01) != 0; i++ {
		Portanbyte(dataport_2)
	}

	if !khianps2command(0xA8) || !khianps2command(0x20) {
		return
	}
	สถานะ, ตกลง := anps2data()
	if !ตกลง {
		return
	}
	สถานะ |= 0x02
	สถานะ &^= 0x20
	if !khianps2command(0x60) || !khianps2data(สถานะ) {
		return
	}

	if !sendmousecommand(0xF6) || !sendmousecommand(0xF4) {
		return
	}
	offset = 0

}

func handlemouseinterrupt(esp uint32) uint32 {
	if ทำงานmousedriver == nil {
		Portanbyte(dataport_2)
		return esp
	}
	return ทำงานmousedriver.Handleinterrupt(esp)
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
	สถานะ := Portanbyte(commandport_2)
	if (สถานะ&0x01) == 0 || (สถานะ&0x20) == 0 {
		return esp
	}

	data := Portanbyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetสถานะ := uint8(buffer_2[0])

		if (packetสถานะ & 0xC0) == 0 {
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
		pendingbutton = int8(packetสถานะ & 0x07)
		pendingmouseevent = true
	}

	return esp

}

func Pโพรเซสpendingmouseevents() {
	if imouseeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingmouseevent {
		Interruptทำงาน()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	newbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingmouseevent = false
	Interruptทำงาน()

	if x != 0 || y != 0 {
		imouseeventhandler.Onmousemove(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (newbutton & mask) != (oldbutton & mask) {
			if (newbutton & mask) != 0 {
				imouseeventhandler.Onmouseลง(int8(i + 1))
			} else {
				imouseeventhandler.Onmouseup(int8(i + 1))
			}
		}
	}
	button_2 = newbutton
}
