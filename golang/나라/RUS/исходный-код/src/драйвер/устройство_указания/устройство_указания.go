package клавиатура

import . "unsafe"

import . "порт"
import . "прерывание"
import . "консоль"

type IМышьсобытиеhandler interface {
	ПримышьВниз(кнопка int8)
	ПримышьВверх(кнопка int8)
	ПримышьПереместить(x int8, y int8)
}

var iмышьсобытиеhandler IМышьсобытиеhandler

type TПоумолчаниюмышьсобытиеhandler struct {
}

var консоль_2 TКонсоль = TКонсоль{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиция int16 = 0
var yПозиция int16 = 0

func (текущий TПоумолчаниюмышьсобытиеhandler) ПримышьВниз(кнопка int8) {
	buffer := []byte("+")
	консоль_2.MПечатьxy(buffer, uint16(previousx), uint16(previousy))
}
func (текущий TПоумолчаниюмышьсобытиеhandler) ПримышьВверх(кнопка int8)	{}
func (текущий TПоумолчаниюмышьсобытиеhandler) ПримышьПереместить(x int8, y int8) {

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
	консоль_2.MПечатьxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	консоль_2.MПечатьxy(buffer, uint16(xПозиция), uint16(yПозиция))

	previousx = xПозиция
	previousy = yПозиция
}

type TМышьдрайвер struct {
	TПрерываниеhandler
}

var активномышьдрайвер *TМышьдрайвер
var прерываниеhandler func(uint32) uint32

var данныепорт_2 uint16 = 0x60
var командапорт_2 uint16 = 0x64

const ps2ПодождатьОграничение = 100000

func подождатьps2ВводПусто() bool {
	for i := 0; i < ps2ПодождатьОграничение; i++ {
		if (Портчитатьбайт(командапорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func подождатьps2ВыводПолный() bool {
	for i := 0; i < ps2ПодождатьОграничение; i++ {
		if (Портчитатьбайт(командапорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func писатьps2Команда(значение uint8) bool {
	if !подождатьps2ВводПусто() {
		return false
	}
	Портписатьбайт(командапорт_2, значение)
	return true
}

func писатьps2данные(значение uint8) bool {
	if !подождатьps2ВводПусто() {
		return false
	}
	Портписатьбайт(данныепорт_2, значение)
	return true
}

func читатьps2данные() (uint8, bool) {
	if !подождатьps2ВыводПолный() {
		return 0, false
	}
	return Портчитатьбайт(данныепорт_2), true
}

func отправитьмышьКоманда(значение uint8) bool {
	if !писатьps2Команда(0xD4) || !писатьps2данные(значение) {
		return false
	}
	ack, оК := читатьps2данные()
	return оК && ack == 0xFA
}

func (текущий *TМышьдрайвер) Initдрайвер(диспетчер *TПрерываниедиспетчер, мышьсобытиеhandler IМышьсобытиеhandler) {

	iмышьсобытиеhandler = TПоумолчаниюмышьсобытиеhandler{}

	if мышьсобытиеhandler != nil {
		iмышьсобытиеhandler = мышьсобытиеhandler
	}

	активномышьдрайвер = текущий
	прерываниеhandler = ручкамышьпрерывание
	var address uintptr
	address = uintptr(Pointer(&прерываниеhandler))
	текущий.Init(0x2C, uintptr(Pointer(диспетчер)), address)

	for i := 0; i < 32 && (Портчитатьбайт(командапорт_2)&0x01) != 0; i++ {
		Портчитатьбайт(данныепорт_2)
	}

	if !писатьps2Команда(0xA8) || !писатьps2Команда(0x20) {
		return
	}
	состояние, оК := читатьps2данные()
	if !оК {
		return
	}
	состояние |= 0x02
	состояние &^= 0x20
	if !писатьps2Команда(0x60) || !писатьps2данные(состояние) {
		return
	}

	if !отправитьмышьКоманда(0xF6) || !отправитьмышьКоманда(0xF4) {
		return
	}
	offset = 0

}

func ручкамышьпрерывание(esp uint32) uint32 {
	if активномышьдрайвер == nil {
		Портчитатьбайт(данныепорт_2)
		return esp
	}
	return активномышьдрайвер.Ручкапрерывание(esp)
}

var количество uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var кнопка_2 int8
var ожидающийx int16
var ожидающийy int16
var ожидающийКнопка int8
var ожидающиймышьсобытие bool

func (текущий *TМышьдрайвер) Ручкапрерывание(esp uint32) uint32 {
	состояние := Портчитатьбайт(командапорт_2)
	if (состояние&0x01) == 0 || (состояние&0x20) == 0 {
		return esp
	}

	данные := Портчитатьбайт(данныепорт_2)

	if offset == 0 && (данные&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(данные)
	offset = (offset + 1) % 3
	if offset == 0 {
		пАКЕТСостояние := uint8(buffer_2[0])

		if (пАКЕТСостояние & 0xC0) == 0 {
			ожидающийx += int16(buffer_2[1])
			ожидающийy += int16(buffer_2[2])
			if ожидающийx > 127 {
				ожидающийx = 127
			} else if ожидающийx < -127 {
				ожидающийx = -127
			}
			if ожидающийy > 127 {
				ожидающийy = 127
			} else if ожидающийy < -127 {
				ожидающийy = -127
			}
		}
		ожидающийКнопка = int8(пАКЕТСостояние & 0x07)
		ожидающиймышьсобытие = true
	}

	return esp

}

func Процессожидающиймышьсобытия() {
	if iмышьсобытиеhandler == nil {
		return
	}

	Прерываниеdeactive()
	if !ожидающиймышьсобытие {
		ПрерываниеАктивно()
		return
	}
	x := int8(ожидающийx)
	y := int8(ожидающийy)
	новыйКнопка := ожидающийКнопка
	oldКнопка := кнопка_2

	ожидающийx = 0
	ожидающийy = 0
	ожидающиймышьсобытие = false
	ПрерываниеАктивно()

	if x != 0 || y != 0 {
		iмышьсобытиеhandler.ПримышьПереместить(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		маска := int8(0x1 << i)
		if (новыйКнопка & маска) != (oldКнопка & маска) {
			if (новыйКнопка & маска) != 0 {
				iмышьсобытиеhandler.ПримышьВниз(int8(i + 1))
			} else {
				iмышьсобытиеhandler.ПримышьВверх(int8(i + 1))
			}
		}
	}
	кнопка_2 = новыйКнопка
}
