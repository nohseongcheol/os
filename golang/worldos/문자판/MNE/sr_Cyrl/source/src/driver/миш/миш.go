/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package тастатура

import . "unsafe"

import . "порт"
import . "ометање"
import . "конзола"

type IМишДогађајhandler interface {
	НаМишНиже(дугме int8)
	НаМишГоре(дугме int8)
	НаМишПремести(x int8, y int8)
}

var iМишДогађајhandler IМишДогађајhandler

type TПодразумеваноМишДогађајhandler struct {
}

var конзола_2 TКонзола = TКонзола{}
var previousx int16 = 0
var previousy int16 = 0
var xПоложај int16 = 0
var yПоложај int16 = 0

func (исти TПодразумеваноМишДогађајhandler) НаМишНиже(дугме int8) {
	buffer := []byte("+")
	конзола_2.MШтампајxy(buffer, uint16(previousx), uint16(previousy))
}
func (исти TПодразумеваноМишДогађајhandler) НаМишГоре(дугме int8)	{}
func (исти TПодразумеваноМишДогађајhandler) НаМишПремести(x int8, y int8) {

	xПоложај += int16(x)
	if xПоложај < 0 {
		xПоложај = 0
	}
	if xПоложај >= 80 {
		xПоложај = 79
	}

	yПоложај -= int16(y)

	if yПоложај < 0 {
		yПоложај = 0
	}
	if yПоложај >= 25 {
		yПоложај = 24
	}

	buffer := []byte(" ")
	конзола_2.MШтампајxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	конзола_2.MШтампајxy(buffer, uint16(xПоложај), uint16(yПоложај))

	previousx = xПоложај
	previousy = yПоложај
}

type TМишdriver struct {
	TОметањеhandler
}

var активнаМишdriver *TМишdriver
var ометањеhandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var наредбаПорт_2 uint16 = 0x64

const ps2СачекајОграничи = 100000

func сачекајps2УлазПразно() bool {
	for i := 0; i < ps2СачекајОграничи; i++ {
		if (Портчитањеbyte(наредбаПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func сачекајps2Излазпотпуно() bool {
	for i := 0; i < ps2СачекајОграничи; i++ {
		if (Портчитањеbyte(наредбаПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func пишеps2Наредба(вредност uint8) bool {
	if !сачекајps2УлазПразно() {
		return false
	}
	ПортПишеbyte(наредбаПорт_2, вредност)
	return true
}

func пишеps2data(вредност uint8) bool {
	if !сачекајps2УлазПразно() {
		return false
	}
	ПортПишеbyte(dataПорт_2, вредност)
	return true
}

func читањеps2data() (uint8, bool) {
	if !сачекајps2Излазпотпуно() {
		return 0, false
	}
	return Портчитањеbyte(dataПорт_2), true
}

func пошаљиМишНаредба(вредност uint8) bool {
	if !пишеps2Наредба(0xD4) || !пишеps2data(вредност) {
		return false
	}
	ack, уреду := читањеps2data()
	return уреду && ack == 0xFA
}

func (исти *TМишdriver) Initdriver(manager *TОметањеmanager, мишДогађајhandler IМишДогађајhandler) {

	iМишДогађајhandler = TПодразумеваноМишДогађајhandler{}

	if мишДогађајhandler != nil {
		iМишДогађајhandler = мишДогађајhandler
	}

	активнаМишdriver = исти
	ометањеhandler = ручкаМишОметање
	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))
	исти.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Портчитањеbyte(наредбаПорт_2)&0x01) != 0; i++ {
		Портчитањеbyte(dataПорт_2)
	}

	if !пишеps2Наредба(0xA8) || !пишеps2Наредба(0x20) {
		return
	}
	стање, уреду := читањеps2data()
	if !уреду {
		return
	}
	стање |= 0x02
	стање &^= 0x20
	if !пишеps2Наредба(0x60) || !пишеps2data(стање) {
		return
	}

	if !пошаљиМишНаредба(0xF6) || !пошаљиМишНаредба(0xF4) {
		return
	}
	offset = 0

}

func ручкаМишОметање(esp uint32) uint32 {
	if активнаМишdriver == nil {
		Портчитањеbyte(dataПорт_2)
		return esp
	}
	return активнаМишdriver.РучкаОметање(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var дугме_2 int8
var pendingx int16
var pendingy int16
var pendingДугме int8
var pendingМишДогађај bool

func (исти *TМишdriver) РучкаОметање(esp uint32) uint32 {
	стање := Портчитањеbyte(наредбаПорт_2)
	if (стање&0x01) == 0 || (стање&0x20) == 0 {
		return esp
	}

	data := Портчитањеbyte(dataПорт_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetСтање := uint8(buffer_2[0])

		if (packetСтање & 0xC0) == 0 {
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
		pendingДугме = int8(packetСтање & 0x07)
		pendingМишДогађај = true
	}

	return esp

}

func ПроцесpendingМишДогађаји() {
	if iМишДогађајhandler == nil {
		return
	}

	Ометањеdeactive()
	if !pendingМишДогађај {
		ОметањеАктивна()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	новаДугме := pendingДугме
	oldДугме := дугме_2

	pendingx = 0
	pendingy = 0
	pendingМишДогађај = false
	ОметањеАктивна()

	if x != 0 || y != 0 {
		iМишДогађајhandler.НаМишПремести(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		маска := int8(0x1 << i)
		if (новаДугме & маска) != (oldДугме & маска) {
			if (новаДугме & маска) != 0 {
				iМишДогађајhandler.НаМишНиже(int8(i + 1))
			} else {
				iМишДогађајhandler.НаМишГоре(int8(i + 1))
			}
		}
	}
	дугме_2 = новаДугме
}
