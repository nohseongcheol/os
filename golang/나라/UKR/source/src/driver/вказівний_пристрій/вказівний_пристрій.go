package клавіатура

import . "unsafe"

import . "порт"
import . "переривання"
import . "консоль"

type IМишаПодіяhandler interface {
	УвімкненоМишаВниз(кнопка int8)
	УвімкненоМишаВгору(кнопка int8)
	УвімкненоМишаПеремістити(x int8, y int8)
}

var iМишаПодіяhandler IМишаПодіяhandler

type TТиповийМишаПодіяhandler struct {
}

var консоль_2 TКонсоль = TКонсоль{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиція int16 = 0
var yПозиція int16 = 0

func (поточний TТиповийМишаПодіяhandler) УвімкненоМишаВниз(кнопка int8) {
	buffer := []byte("+")
	консоль_2.MДрукxy(buffer, uint16(previousx), uint16(previousy))
}
func (поточний TТиповийМишаПодіяhandler) УвімкненоМишаВгору(кнопка int8)	{}
func (поточний TТиповийМишаПодіяhandler) УвімкненоМишаПеремістити(x int8, y int8) {

	xПозиція += int16(x)
	if xПозиція < 0 {
		xПозиція = 0
	}
	if xПозиція >= 80 {
		xПозиція = 79
	}

	yПозиція -= int16(y)

	if yПозиція < 0 {
		yПозиція = 0
	}
	if yПозиція >= 25 {
		yПозиція = 24
	}

	buffer := []byte(" ")
	консоль_2.MДрукxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	консоль_2.MДрукxy(buffer, uint16(xПозиція), uint16(yПозиція))

	previousx = xПозиція
	previousy = yПозиція
}

type TМишаdriver struct {
	TПерериванняhandler
}

var активнийМишаdriver *TМишаdriver
var перериванняhandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var командаПорт_2 uint16 = 0x64

const ps2ЧекатиОбмеження = 100000

func чекатиps2ВведенняданихПусто() bool {
	for i := 0; i < ps2ЧекатиОбмеження; i++ {
		if (ПортЧитанняbyte(командаПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func чекатиps2ВивідПовністю() bool {
	for i := 0; i < ps2ЧекатиОбмеження; i++ {
		if (ПортЧитанняbyte(командаПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func записps2Команда(значення uint8) bool {
	if !чекатиps2ВведенняданихПусто() {
		return false
	}
	ПортЗаписbyte(командаПорт_2, значення)
	return true
}

func записps2data(значення uint8) bool {
	if !чекатиps2ВведенняданихПусто() {
		return false
	}
	ПортЗаписbyte(dataПорт_2, значення)
	return true
}

func читанняps2data() (uint8, bool) {
	if !чекатиps2ВивідПовністю() {
		return 0, false
	}
	return ПортЧитанняbyte(dataПорт_2), true
}

func надіслатиМишаКоманда(значення uint8) bool {
	if !записps2Команда(0xD4) || !записps2data(значення) {
		return false
	}
	ack, гаразд := читанняps2data()
	return гаразд && ack == 0xFA
}

func (поточний *TМишаdriver) Initdriver(manager *TПерериванняmanager, мишаПодіяhandler IМишаПодіяhandler) {

	iМишаПодіяhandler = TТиповийМишаПодіяhandler{}

	if мишаПодіяhandler != nil {
		iМишаПодіяhandler = мишаПодіяhandler
	}

	активнийМишаdriver = поточний
	перериванняhandler = елементкеруванняМишаПереривання
	var адреса uintptr
	адреса = uintptr(Pointer(&перериванняhandler))
	поточний.Init(0x2C, uintptr(Pointer(manager)), адреса)

	for i := 0; i < 32 && (ПортЧитанняbyte(командаПорт_2)&0x01) != 0; i++ {
		ПортЧитанняbyte(dataПорт_2)
	}

	if !записps2Команда(0xA8) || !записps2Команда(0x20) {
		return
	}
	статус, гаразд := читанняps2data()
	if !гаразд {
		return
	}
	статус |= 0x02
	статус &^= 0x20
	if !записps2Команда(0x60) || !записps2data(статус) {
		return
	}

	if !надіслатиМишаКоманда(0xF6) || !надіслатиМишаКоманда(0xF4) {
		return
	}
	offset = 0

}

func елементкеруванняМишаПереривання(esp uint32) uint32 {
	if активнийМишаdriver == nil {
		ПортЧитанняbyte(dataПорт_2)
		return esp
	}
	return активнийМишаdriver.ЕлементкеруванняПереривання(esp)
}

var відлік uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var кнопка_2 int8
var pendingx int16
var pendingy int16
var pendingКнопка int8
var pendingМишаПодія bool

func (поточний *TМишаdriver) ЕлементкеруванняПереривання(esp uint32) uint32 {
	статус := ПортЧитанняbyte(командаПорт_2)
	if (статус&0x01) == 0 || (статус&0x20) == 0 {
		return esp
	}

	data := ПортЧитанняbyte(dataПорт_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		пАКЕТСтатус := uint8(buffer_2[0])

		if (пАКЕТСтатус & 0xC0) == 0 {
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
		pendingКнопка = int8(пАКЕТСтатус & 0x07)
		pendingМишаПодія = true
	}

	return esp

}

func ПроцесиpendingМишаПодії() {
	if iМишаПодіяhandler == nil {
		return
	}

	Перериванняdeactive()
	if !pendingМишаПодія {
		ПерериванняАктивний()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	новийКнопка := pendingКнопка
	oldКнопка := кнопка_2

	pendingx = 0
	pendingy = 0
	pendingМишаПодія = false
	ПерериванняАктивний()

	if x != 0 || y != 0 {
		iМишаПодіяhandler.УвімкненоМишаПеремістити(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		маска := int8(0x1 << i)
		if (новийКнопка & маска) != (oldКнопка & маска) {
			if (новийКнопка & маска) != 0 {
				iМишаПодіяhandler.УвімкненоМишаВниз(int8(i + 1))
			} else {
				iМишаПодіяhandler.УвімкненоМишаВгору(int8(i + 1))
			}
		}
	}
	кнопка_2 = новийКнопка
}
