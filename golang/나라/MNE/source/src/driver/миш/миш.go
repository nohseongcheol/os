package тастатура

import . "unsafe"

import . "порт"
import . "ометање"
import . "конзола"

type IМишДогађајhandler interface {
	NaМишНиже(дугме int8)
	NaМишGore(дугме int8)
	NaМишПремести(x int8, y int8)
}

var iМишДогађајhandler IМишДогађајhandler

type TПодразумеваноМишДогађајhandler struct {
}

var конзола_2 TКонзола = TКонзола{}
var previousx int16 = 0
var previousy int16 = 0
var xПоложај int16 = 0
var yПоложај int16 = 0

func (isti TПодразумеваноМишДогађајhandler) NaМишНиже(дугме int8) {
	buffer := []byte("+")
	конзола_2.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))
}
func (isti TПодразумеваноМишДогађајhandler) NaМишGore(дугме int8)	{}
func (isti TПодразумеваноМишДогађајhandler) NaМишПремести(x int8, y int8) {

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
	конзола_2.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	конзола_2.MŠtampajxy(buffer, uint16(xПоложај), uint16(yПоложај))

	previousx = xПоложај
	previousy = yПоложај
}

type TМишdriver struct {
	TОметањеhandler
}

var aktivnaМишdriver *TМишdriver
var ометањеhandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var наредбаПорт_2 uint16 = 0x64

const ps2SačekajОграничи = 100000

func sačekajps2УлазПразно() bool {
	for i := 0; i < ps2SačekajОграничи; i++ {
		if (Портчитањеbyte(наредбаПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func sačekajps2Излазпотпуно() bool {
	for i := 0; i < ps2SačekajОграничи; i++ {
		if (Портчитањеbyte(наредбаПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func upisps2Наредба(вредност uint8) bool {
	if !sačekajps2УлазПразно() {
		return false
	}
	Портupisbyte(наредбаПорт_2, вредност)
	return true
}

func upisps2data(вредност uint8) bool {
	if !sačekajps2УлазПразно() {
		return false
	}
	Портupisbyte(dataПорт_2, вредност)
	return true
}

func читањеps2data() (uint8, bool) {
	if !sačekajps2Излазпотпуно() {
		return 0, false
	}
	return Портчитањеbyte(dataПорт_2), true
}

func пошаљиМишНаредба(вредност uint8) bool {
	if !upisps2Наредба(0xD4) || !upisps2data(вредност) {
		return false
	}
	ack, уреду := читањеps2data()
	return уреду && ack == 0xFA
}

func (isti *TМишdriver) Initdriver(manager *TОметањеmanager, мишДогађајhandler IМишДогађајhandler) {

	iМишДогађајhandler = TПодразумеваноМишДогађајhandler{}

	if мишДогађајhandler != nil {
		iМишДогађајhandler = мишДогађајhandler
	}

	aktivnaМишdriver = isti
	ометањеhandler = ручкаМишОметање
	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))
	isti.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Портчитањеbyte(наредбаПорт_2)&0x01) != 0; i++ {
		Портчитањеbyte(dataПорт_2)
	}

	if !upisps2Наредба(0xA8) || !upisps2Наредба(0x20) {
		return
	}
	стање, уреду := читањеps2data()
	if !уреду {
		return
	}
	стање |= 0x02
	стање &^= 0x20
	if !upisps2Наредба(0x60) || !upisps2data(стање) {
		return
	}

	if !пошаљиМишНаредба(0xF6) || !пошаљиМишНаредба(0xF4) {
		return
	}
	offset = 0

}

func ручкаМишОметање(esp uint32) uint32 {
	if aktivnaМишdriver == nil {
		Портчитањеbyte(dataПорт_2)
		return esp
	}
	return aktivnaМишdriver.РучкаОметање(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var дугме_2 int8
var pendingx int16
var pendingy int16
var pendingДугме int8
var pendingМишДогађај bool

func (isti *TМишdriver) РучкаОметање(esp uint32) uint32 {
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

func ПроцесpendingМишDogađaji() {
	if iМишДогађајhandler == nil {
		return
	}

	Ометањеdeactive()
	if !pendingМишДогађај {
		ОметањеAktivna()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	новаДугме := pendingДугме
	oldДугме := дугме_2

	pendingx = 0
	pendingy = 0
	pendingМишДогађај = false
	ОметањеAktivna()

	if x != 0 || y != 0 {
		iМишДогађајhandler.NaМишПремести(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (новаДугме & maska) != (oldДугме & maska) {
			if (новаДугме & maska) != 0 {
				iМишДогађајhandler.NaМишНиже(int8(i + 1))
			} else {
				iМишДогађајhandler.NaМишGore(int8(i + 1))
			}
		}
	}
	дугме_2 = новаДугме
}
