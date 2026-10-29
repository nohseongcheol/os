/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package клавиатура

import . "unsafe"

import . "порт"
import . "прекъсване"
import . "console"

type IМишкаСъбитиеhandler interface {
	ВклМишкаНадолу(бутон int8)
	ВклМишкаНагоре(бутон int8)
	ВклМишкаПреместване(x int8, y int8)
}

var iМишкаСъбитиеhandler IМишкаСъбитиеhandler

type TПоподразбиранеМишкаСъбитиеhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиция int16 = 0
var yПозиция int16 = 0

func (себеси TПоподразбиранеМишкаСъбитиеhandler) ВклМишкаНадолу(бутон int8) {
	buffer := []byte("+")
	console_2.MПечатxy(buffer, uint16(previousx), uint16(previousy))
}
func (себеси TПоподразбиранеМишкаСъбитиеhandler) ВклМишкаНагоре(бутон int8)	{}
func (себеси TПоподразбиранеМишкаСъбитиеhandler) ВклМишкаПреместване(x int8, y int8) {

	xПозиция += int16(x)
	if xПозиция < 0 {
		xПозиция = 0
	}
	if xПозиция >= 80 {
		xПозиция = 79
	}

	yПозиция -= int16(y)

	if yПозиция < 0 {
		yПозиция = 0
	}
	if yПозиция >= 25 {
		yПозиция = 24
	}

	buffer := []byte(" ")
	console_2.MПечатxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MПечатxy(buffer, uint16(xПозиция), uint16(yПозиция))

	previousx = xПозиция
	previousy = yПозиция
}

type TМишкаdriver struct {
	TПрекъсванеhandler
}

var активнаМишкаdriver *TМишкаdriver
var прекъсванеhandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var командаПорт_2 uint16 = 0x64

const ps2ИзчакванеОграничение = 100000

func изчакванеps2ВходПразен() bool {
	for i := 0; i < ps2ИзчакванеОграничение; i++ {
		if (ПортЧетенеbyte(командаПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func изчакванеps2ИзходПълен() bool {
	for i := 0; i < ps2ИзчакванеОграничение; i++ {
		if (ПортЧетенеbyte(командаПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func писанеps2Команда(стойност uint8) bool {
	if !изчакванеps2ВходПразен() {
		return false
	}
	ПортПисанеbyte(командаПорт_2, стойност)
	return true
}

func писанеps2data(стойност uint8) bool {
	if !изчакванеps2ВходПразен() {
		return false
	}
	ПортПисанеbyte(dataПорт_2, стойност)
	return true
}

func четенеps2data() (uint8, bool) {
	if !изчакванеps2ИзходПълен() {
		return 0, false
	}
	return ПортЧетенеbyte(dataПорт_2), true
}

func изпращанеМишкаКоманда(стойност uint8) bool {
	if !писанеps2Команда(0xD4) || !писанеps2data(стойност) {
		return false
	}
	ack, приеми := четенеps2data()
	return приеми && ack == 0xFA
}

func (себеси *TМишкаdriver) Initdriver(manager *TПрекъсванеmanager, мишкаСъбитиеhandler IМишкаСъбитиеhandler) {

	iМишкаСъбитиеhandler = TПоподразбиранеМишкаСъбитиеhandler{}

	if мишкаСъбитиеhandler != nil {
		iМишкаСъбитиеhandler = мишкаСъбитиеhandler
	}

	активнаМишкаdriver = себеси
	прекъсванеhandler = ръкохваткаМишкаПрекъсване
	var address uintptr
	address = uintptr(Pointer(&прекъсванеhandler))
	себеси.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортЧетенеbyte(командаПорт_2)&0x01) != 0; i++ {
		ПортЧетенеbyte(dataПорт_2)
	}

	if !писанеps2Команда(0xA8) || !писанеps2Команда(0x20) {
		return
	}
	състояние, приеми := четенеps2data()
	if !приеми {
		return
	}
	състояние |= 0x02
	състояние &^= 0x20
	if !писанеps2Команда(0x60) || !писанеps2data(състояние) {
		return
	}

	if !изпращанеМишкаКоманда(0xF6) || !изпращанеМишкаКоманда(0xF4) {
		return
	}
	offset = 0

}

func ръкохваткаМишкаПрекъсване(esp uint32) uint32 {
	if активнаМишкаdriver == nil {
		ПортЧетенеbyte(dataПорт_2)
		return esp
	}
	return активнаМишкаdriver.РъкохваткаПрекъсване(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var бутон_2 int8
var pendingx int16
var pendingy int16
var pendingБутон int8
var pendingМишкаСъбитие bool

func (себеси *TМишкаdriver) РъкохваткаПрекъсване(esp uint32) uint32 {
	състояние := ПортЧетенеbyte(командаПорт_2)
	if (състояние&0x01) == 0 || (състояние&0x20) == 0 {
		return esp
	}

	data := ПортЧетенеbyte(dataПорт_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetСъстояние := uint8(buffer_2[0])

		if (packetСъстояние & 0xC0) == 0 {
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
		pendingБутон = int8(packetСъстояние & 0x07)
		pendingМишкаСъбитие = true
	}

	return esp

}

func ПроцесpendingМишкаevents() {
	if iМишкаСъбитиеhandler == nil {
		return
	}

	Прекъсванеdeactive()
	if !pendingМишкаСъбитие {
		ПрекъсванеАктивна()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	новБутон := pendingБутон
	oldБутон := бутон_2

	pendingx = 0
	pendingy = 0
	pendingМишкаСъбитие = false
	ПрекъсванеАктивна()

	if x != 0 || y != 0 {
		iМишкаСъбитиеhandler.ВклМишкаПреместване(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		маска := int8(0x1 << i)
		if (новБутон & маска) != (oldБутон & маска) {
			if (новБутон & маска) != 0 {
				iМишкаСъбитиеhandler.ВклМишкаНадолу(int8(i + 1))
			} else {
				iМишкаСъбитиеhandler.ВклМишкаНагоре(int8(i + 1))
			}
		}
	}
	бутон_2 = новБутон
}
