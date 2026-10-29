/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package клавиатура

import . "unsafe"

import . "порт"
import . "interrupt"
import . "console"

type IЧычканeventhandler interface {
	OnЧычканdown(button int8)
	OnЧычканӨйдө(button int8)
	OnЧычканТашуу(x int8, y int8)
}

var iЧычканeventhandler IЧычканeventhandler

type TЖарыяланбасЧычканeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xТурганжери int16 = 0
var yТурганжери int16 = 0

func (self TЖарыяланбасЧычканeventhandler) OnЧычканdown(button int8) {
	buffer := []byte("+")
	console_2.MБасмаxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TЖарыяланбасЧычканeventhandler) OnЧычканӨйдө(button int8)	{}
func (self TЖарыяланбасЧычканeventhandler) OnЧычканТашуу(x int8, y int8) {

	xТурганжери += int16(x)
	if xТурганжери < 0 {
		xТурганжери = 0
	}
	if xТурганжери >= 80 {
		xТурганжери = 79
	}

	yТурганжери -= int16(y)

	if yТурганжери < 0 {
		yТурганжери = 0
	}
	if yТурганжери >= 25 {
		yТурганжери = 24
	}

	buffer := []byte(" ")
	console_2.MБасмаxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MБасмаxy(buffer, uint16(xТурганжери), uint16(yТурганжери))

	previousx = xТурганжери
	previousy = yТурганжери
}

type TЧычканdriver struct {
	TInterrupthandler
}

var активдүүЧычканdriver *TЧычканdriver
var interrupthandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var командаПорт_2 uint16 = 0x64

const ps2Күтүүlimit = 100000

func күтүүps2КиришБош() bool {
	for i := 0; i < ps2Күтүүlimit; i++ {
		if (ПортОкууbyte(командаПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func күтүүps2ЧыгышТолук() bool {
	for i := 0; i < ps2Күтүүlimit; i++ {
		if (ПортОкууbyte(командаПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func жазууps2Команда(мааниси uint8) bool {
	if !күтүүps2КиришБош() {
		return false
	}
	ПортЖазууbyte(командаПорт_2, мааниси)
	return true
}

func жазууps2data(мааниси uint8) bool {
	if !күтүүps2КиришБош() {
		return false
	}
	ПортЖазууbyte(dataПорт_2, мааниси)
	return true
}

func окууps2data() (uint8, bool) {
	if !күтүүps2ЧыгышТолук() {
		return 0, false
	}
	return ПортОкууbyte(dataПорт_2), true
}

func sendЧычканКоманда(мааниси uint8) bool {
	if !жазууps2Команда(0xD4) || !жазууps2data(мааниси) {
		return false
	}
	ack, ok := окууps2data()
	return ok && ack == 0xFA
}

func (self *TЧычканdriver) Initdriver(manager *TInterruptmanager, чычканeventhandler IЧычканeventhandler) {

	iЧычканeventhandler = TЖарыяланбасЧычканeventhandler{}

	if чычканeventhandler != nil {
		iЧычканeventhandler = чычканeventhandler
	}

	активдүүЧычканdriver = self
	interrupthandler = handleЧычканinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортОкууbyte(командаПорт_2)&0x01) != 0; i++ {
		ПортОкууbyte(dataПорт_2)
	}

	if !жазууps2Команда(0xA8) || !жазууps2Команда(0x20) {
		return
	}
	абалы, ok := окууps2data()
	if !ok {
		return
	}
	абалы |= 0x02
	абалы &^= 0x20
	if !жазууps2Команда(0x60) || !жазууps2data(абалы) {
		return
	}

	if !sendЧычканКоманда(0xF6) || !sendЧычканКоманда(0xF4) {
		return
	}
	offset = 0

}

func handleЧычканinterrupt(esp uint32) uint32 {
	if активдүүЧычканdriver == nil {
		ПортОкууbyte(dataПорт_2)
		return esp
	}
	return активдүүЧычканdriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingЧычканevent bool

func (self *TЧычканdriver) Handleinterrupt(esp uint32) uint32 {
	абалы := ПортОкууbyte(командаПорт_2)
	if (абалы&0x01) == 0 || (абалы&0x20) == 0 {
		return esp
	}

	data := ПортОкууbyte(dataПорт_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetАбалы := uint8(buffer_2[0])

		if (packetАбалы & 0xC0) == 0 {
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
		pendingbutton = int8(packetАбалы & 0x07)
		pendingЧычканevent = true
	}

	return esp

}

func ПроцессиpendingЧычканevents() {
	if iЧычканeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingЧычканevent {
		Interruptактивдүү()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	жаңыbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingЧычканevent = false
	Interruptактивдүү()

	if x != 0 || y != 0 {
		iЧычканeventhandler.OnЧычканТашуу(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (жаңыbutton & mask) != (oldbutton & mask) {
			if (жаңыbutton & mask) != 0 {
				iЧычканeventhandler.OnЧычканdown(int8(i + 1))
			} else {
				iЧычканeventhandler.OnЧычканӨйдө(int8(i + 1))
			}
		}
	}
	button_2 = жаңыbutton
}
