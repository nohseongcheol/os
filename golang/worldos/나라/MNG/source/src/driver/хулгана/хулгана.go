/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package гар

import . "unsafe"

import . "порт"
import . "interrupt"
import . "консол"

type IХулганаeventhandler interface {
	OnХулганаdown(button int8)
	OnХулганаДээш(button int8)
	OnХулганаЗөөх(x int8, y int8)
}

var iХулганаeventhandler IХулганаeventhandler

type TСтандартХулганаeventhandler struct {
}

var консол_2 TКонсол = TКонсол{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self TСтандартХулганаeventhandler) OnХулганаdown(button int8) {
	buffer := []byte("+")
	консол_2.MХэвлэхxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TСтандартХулганаeventhandler) OnХулганаДээш(button int8)	{}
func (self TСтандартХулганаeventhandler) OnХулганаЗөөх(x int8, y int8) {

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
	консол_2.MХэвлэхxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	консол_2.MХэвлэхxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TХулганаdriver struct {
	TInterrupthandler
}

var идэвхтэйХулганаdriver *TХулганаdriver
var interrupthandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var тушаалПорт_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (ПортУншихbyte(тушаалПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputДүүрэн() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (ПортУншихbyte(тушаалПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func бичихps2Тушаал(утга uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	ПортБичихbyte(тушаалПорт_2, утга)
	return true
}

func бичихps2data(утга uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	ПортБичихbyte(dataПорт_2, утга)
	return true
}

func уншихps2data() (uint8, bool) {
	if !waitps2outputДүүрэн() {
		return 0, false
	}
	return ПортУншихbyte(dataПорт_2), true
}

func sendХулганаТушаал(утга uint8) bool {
	if !бичихps2Тушаал(0xD4) || !бичихps2data(утга) {
		return false
	}
	ack, ok := уншихps2data()
	return ok && ack == 0xFA
}

func (self *TХулганаdriver) Initdriver(зохицуулагч *TInterruptЗохицуулагч, хулганаeventhandler IХулганаeventhandler) {

	iХулганаeventhandler = TСтандартХулганаeventhandler{}

	if хулганаeventhandler != nil {
		iХулганаeventhandler = хулганаeventhandler
	}

	идэвхтэйХулганаdriver = self
	interrupthandler = handleХулганаinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(зохицуулагч)), address)

	for i := 0; i < 32 && (ПортУншихbyte(тушаалПорт_2)&0x01) != 0; i++ {
		ПортУншихbyte(dataПорт_2)
	}

	if !бичихps2Тушаал(0xA8) || !бичихps2Тушаал(0x20) {
		return
	}
	төлөв, ok := уншихps2data()
	if !ok {
		return
	}
	төлөв |= 0x02
	төлөв &^= 0x20
	if !бичихps2Тушаал(0x60) || !бичихps2data(төлөв) {
		return
	}

	if !sendХулганаТушаал(0xF6) || !sendХулганаТушаал(0xF4) {
		return
	}
	offset = 0

}

func handleХулганаinterrupt(esp uint32) uint32 {
	if идэвхтэйХулганаdriver == nil {
		ПортУншихbyte(dataПорт_2)
		return esp
	}
	return идэвхтэйХулганаdriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingХулганаevent bool

func (self *TХулганаdriver) Handleinterrupt(esp uint32) uint32 {
	төлөв := ПортУншихbyte(тушаалПорт_2)
	if (төлөв&0x01) == 0 || (төлөв&0x20) == 0 {
		return esp
	}

	data := ПортУншихbyte(dataПорт_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetТөлөв := uint8(buffer_2[0])

		if (packetТөлөв & 0xC0) == 0 {
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
		pendingbutton = int8(packetТөлөв & 0x07)
		pendingХулганаevent = true
	}

	return esp

}

func ProcesspendingХулганаevents() {
	if iХулганаeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingХулганаevent {
		InterruptИдэвхтэй()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	шинэbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingХулганаevent = false
	InterruptИдэвхтэй()

	if x != 0 || y != 0 {
		iХулганаeventhandler.OnХулганаЗөөх(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (шинэbutton & mask) != (oldbutton & mask) {
			if (шинэbutton & mask) != 0 {
				iХулганаeventhandler.OnХулганаdown(int8(i + 1))
			} else {
				iХулганаeventhandler.OnХулганаДээш(int8(i + 1))
			}
		}
	}
	button_2 = шинэbutton
}
