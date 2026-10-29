/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package клавіятура

import . "unsafe"

import . "порт"
import . "перарыванне"
import . "console"

type IМышПадзеяhandler interface {
	OnМышУніз(кнопка int8)
	OnМышВышэй(кнопка int8)
	OnМышПеранесці(x int8, y int8)
}

var iМышПадзеяhandler IМышПадзеяhandler

type TСтандартнаМышПадзеяhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xПазіцыя int16 = 0
var yПазіцыя int16 = 0

func (self TСтандартнаМышПадзеяhandler) OnМышУніз(кнопка int8) {
	buffer := []byte("+")
	console_2.MДрукавацьxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TСтандартнаМышПадзеяhandler) OnМышВышэй(кнопка int8)	{}
func (self TСтандартнаМышПадзеяhandler) OnМышПеранесці(x int8, y int8) {

	xПазіцыя += int16(x)
	if xПазіцыя < 0 {
		xПазіцыя = 0
	}
	if xПазіцыя >= 80 {
		xПазіцыя = 79
	}

	yПазіцыя -= int16(y)

	if yПазіцыя < 0 {
		yПазіцыя = 0
	}
	if yПазіцыя >= 25 {
		yПазіцыя = 24
	}

	buffer := []byte(" ")
	console_2.MДрукавацьxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MДрукавацьxy(buffer, uint16(xПазіцыя), uint16(yПазіцыя))

	previousx = xПазіцыя
	previousy = yПазіцыя
}

type TМышdriver struct {
	TПерарываннеhandler
}

var актыўнаМышdriver *TМышdriver
var перарываннеhandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var загадПорт_2 uint16 = 0x64

const ps2ЧакацьАбмежаваць = 100000

func чакацьps2УводПуста() bool {
	for i := 0; i < ps2ЧакацьАбмежаваць; i++ {
		if (ПортЧытаннеbyte(загадПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func чакацьps2ВыхадЦалкам() bool {
	for i := 0; i < ps2ЧакацьАбмежаваць; i++ {
		if (ПортЧытаннеbyte(загадПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func запісps2Загад(значэнне uint8) bool {
	if !чакацьps2УводПуста() {
		return false
	}
	ПортЗапісbyte(загадПорт_2, значэнне)
	return true
}

func запісps2data(значэнне uint8) bool {
	if !чакацьps2УводПуста() {
		return false
	}
	ПортЗапісbyte(dataПорт_2, значэнне)
	return true
}

func чытаннеps2data() (uint8, bool) {
	if !чакацьps2ВыхадЦалкам() {
		return 0, false
	}
	return ПортЧытаннеbyte(dataПорт_2), true
}

func даслацьМышЗагад(значэнне uint8) bool {
	if !запісps2Загад(0xD4) || !запісps2data(значэнне) {
		return false
	}
	ack, добра := чытаннеps2data()
	return добра && ack == 0xFA
}

func (self *TМышdriver) Initdriver(manager *TПерарываннеmanager, мышПадзеяhandler IМышПадзеяhandler) {

	iМышПадзеяhandler = TСтандартнаМышПадзеяhandler{}

	if мышПадзеяhandler != nil {
		iМышПадзеяhandler = мышПадзеяhandler
	}

	актыўнаМышdriver = self
	перарываннеhandler = handleМышПерарыванне
	var address uintptr
	address = uintptr(Pointer(&перарываннеhandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортЧытаннеbyte(загадПорт_2)&0x01) != 0; i++ {
		ПортЧытаннеbyte(dataПорт_2)
	}

	if !запісps2Загад(0xA8) || !запісps2Загад(0x20) {
		return
	}
	стан, добра := чытаннеps2data()
	if !добра {
		return
	}
	стан |= 0x02
	стан &^= 0x20
	if !запісps2Загад(0x60) || !запісps2data(стан) {
		return
	}

	if !даслацьМышЗагад(0xF6) || !даслацьМышЗагад(0xF4) {
		return
	}
	offset = 0

}

func handleМышПерарыванне(esp uint32) uint32 {
	if актыўнаМышdriver == nil {
		ПортЧытаннеbyte(dataПорт_2)
		return esp
	}
	return актыўнаМышdriver.HandleПерарыванне(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var кнопка_2 int8
var pendingx int16
var pendingy int16
var pendingКнопка int8
var pendingМышПадзея bool

func (self *TМышdriver) HandleПерарыванне(esp uint32) uint32 {
	стан := ПортЧытаннеbyte(загадПорт_2)
	if (стан&0x01) == 0 || (стан&0x20) == 0 {
		return esp
	}

	data := ПортЧытаннеbyte(dataПорт_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetСтан := uint8(buffer_2[0])

		if (packetСтан & 0xC0) == 0 {
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
		pendingКнопка = int8(packetСтан & 0x07)
		pendingМышПадзея = true
	}

	return esp

}

func ПрацэсpendingМышevents() {
	if iМышПадзеяhandler == nil {
		return
	}

	Перарываннеdeactive()
	if !pendingМышПадзея {
		ПерарываннеАктыўна()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	новыКнопка := pendingКнопка
	oldКнопка := кнопка_2

	pendingx = 0
	pendingy = 0
	pendingМышПадзея = false
	ПерарываннеАктыўна()

	if x != 0 || y != 0 {
		iМышПадзеяhandler.OnМышПеранесці(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		маска := int8(0x1 << i)
		if (новыКнопка & маска) != (oldКнопка & маска) {
			if (новыКнопка & маска) != 0 {
				iМышПадзеяhandler.OnМышУніз(int8(i + 1))
			} else {
				iМышПадзеяhandler.OnМышВышэй(int8(i + 1))
			}
		}
	}
	кнопка_2 = новыКнопка
}
