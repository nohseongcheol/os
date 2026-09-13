package тастатура

import . "unsafe"

import . "порта"
import . "interrupt"
import . "console"

type IГлушецeventhandler interface {
	ВклученоГлушецДолу(button int8)
	ВклученоГлушецГоре(button int8)
	ВклученоГлушецПомести(x int8, y int8)
}

var iГлушецeventhandler IГлушецeventhandler

type TСтандардноГлушецeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиција int16 = 0
var yПозиција int16 = 0

func (само TСтандардноГлушецeventhandler) ВклученоГлушецДолу(button int8) {
	buffer := []byte("+")
	console_2.MПечатиxy(buffer, uint16(previousx), uint16(previousy))
}
func (само TСтандардноГлушецeventhandler) ВклученоГлушецГоре(button int8)	{}
func (само TСтандардноГлушецeventhandler) ВклученоГлушецПомести(x int8, y int8) {

	xПозиција += int16(x)
	if xПозиција < 0 {
		xПозиција = 0
	}
	if xПозиција >= 80 {
		xПозиција = 79
	}

	yПозиција -= int16(y)

	if yПозиција < 0 {
		yПозиција = 0
	}
	if yПозиција >= 25 {
		yПозиција = 24
	}

	buffer := []byte(" ")
	console_2.MПечатиxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MПечатиxy(buffer, uint16(xПозиција), uint16(yПозиција))

	previousx = xПозиција
	previousy = yПозиција
}

type TГлушецdriver struct {
	TInterrupthandler
}

var активноГлушецdriver *TГлушецdriver
var interrupthandler func(uint32) uint32

var dataПорта_2 uint16 = 0x60
var командаПорта_2 uint16 = 0x64

const ps2Чекајlimit = 100000

func чекајps2ВнесПразно() bool {
	for i := 0; i < ps2Чекајlimit; i++ {
		if (ПортаЧитајbyte(командаПорта_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func чекајps2outputПолно() bool {
	for i := 0; i < ps2Чекајlimit; i++ {
		if (ПортаЧитајbyte(командаПорта_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func запишиps2Команда(вредност uint8) bool {
	if !чекајps2ВнесПразно() {
		return false
	}
	ПортаЗапишиbyte(командаПорта_2, вредност)
	return true
}

func запишиps2data(вредност uint8) bool {
	if !чекајps2ВнесПразно() {
		return false
	}
	ПортаЗапишиbyte(dataПорта_2, вредност)
	return true
}

func читајps2data() (uint8, bool) {
	if !чекајps2outputПолно() {
		return 0, false
	}
	return ПортаЧитајbyte(dataПорта_2), true
}

func испратиГлушецКоманда(вредност uint8) bool {
	if !запишиps2Команда(0xD4) || !запишиps2data(вредност) {
		return false
	}
	ack, воред := читајps2data()
	return воред && ack == 0xFA
}

func (само *TГлушецdriver) Initdriver(manager *TInterruptmanager, глушецeventhandler IГлушецeventhandler) {

	iГлушецeventhandler = TСтандардноГлушецeventhandler{}

	if глушецeventhandler != nil {
		iГлушецeventhandler = глушецeventhandler
	}

	активноГлушецdriver = само
	interrupthandler = handleГлушецinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	само.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортаЧитајbyte(командаПорта_2)&0x01) != 0; i++ {
		ПортаЧитајbyte(dataПорта_2)
	}

	if !запишиps2Команда(0xA8) || !запишиps2Команда(0x20) {
		return
	}
	статус, воред := читајps2data()
	if !воред {
		return
	}
	статус |= 0x02
	статус &^= 0x20
	if !запишиps2Команда(0x60) || !запишиps2data(статус) {
		return
	}

	if !испратиГлушецКоманда(0xF6) || !испратиГлушецКоманда(0xF4) {
		return
	}
	offset = 0

}

func handleГлушецinterrupt(esp uint32) uint32 {
	if активноГлушецdriver == nil {
		ПортаЧитајbyte(dataПорта_2)
		return esp
	}
	return активноГлушецdriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingГлушецevent bool

func (само *TГлушецdriver) Handleinterrupt(esp uint32) uint32 {
	статус := ПортаЧитајbyte(командаПорта_2)
	if (статус&0x01) == 0 || (статус&0x20) == 0 {
		return esp
	}

	data := ПортаЧитајbyte(dataПорта_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetСтатус := uint8(buffer_2[0])

		if (packetСтатус & 0xC0) == 0 {
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
		pendingbutton = int8(packetСтатус & 0x07)
		pendingГлушецevent = true
	}

	return esp

}

func ПроцесpendingГлушецevents() {
	if iГлушецeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingГлушецevent {
		Interruptактивно()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	новbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingГлушецevent = false
	Interruptактивно()

	if x != 0 || y != 0 {
		iГлушецeventhandler.ВклученоГлушецПомести(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		маска := int8(0x1 << i)
		if (новbutton & маска) != (oldbutton & маска) {
			if (новbutton & маска) != 0 {
				iГлушецeventhandler.ВклученоГлушецДолу(int8(i + 1))
			} else {
				iГлушецeventhandler.ВклученоГлушецГоре(int8(i + 1))
			}
		}
	}
	button_2 = новbutton
}
