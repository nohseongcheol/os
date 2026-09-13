package клавиатура

import . "unsafe"

import . "порт"
import . "прерывание"

import . "консоль"
import . "системавызов"

type IКлавиатурасобытиеhandler interface {
	ПриКлючВниз(ключ byte)
	ПриКлючВверх(ключ byte)
}

var iклавиатурасобытиеhandler IКлавиатурасобытиеhandler
var поумолчаниюклавиатурасобытиеhandler TПоумолчаниюклавиатурасобытиеhandler

type TПоумолчаниюклавиатурасобытиеhandler struct {
}

func (текущий *TПоумолчаниюклавиатурасобытиеhandler) ПриКлючВниз(ключ byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((ключ >> 4) & 0xF)]
	buffer[18] = hex[ключ&0xF]

	консоль_2 := TКонсоль{}
	консоль_2.MПечать(buffer)

}
func (текущий *TПоумолчаниюклавиатурасобытиеhandler) ПриКлючВверх(ключ byte) {
}

type TКлавиатурадрайвер struct {
	TПрерываниеhandler
}

var активноклавиатурадрайвер *TКлавиатурадрайвер
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

func (текущий *TКлавиатурадрайвер) Initдрайвер(диспетчер *TПрерываниедиспетчер, клавиатурасобытиеhandler IКлавиатурасобытиеhandler) {

	iклавиатурасобытиеhandler = &поумолчаниюклавиатурасобытиеhandler
	if клавиатурасобытиеhandler != nil {
		iклавиатурасобытиеhandler = клавиатурасобытиеhandler
	}

	активноклавиатурадрайвер = текущий
	прерываниеhandler = ручкаклавиатурапрерывание
	var address uintptr
	address = uintptr(Pointer(&прерываниеhandler))

	текущий.Init(0x21, uintptr(Pointer(диспетчер)), address)

	for i := 0; i < 32 && (Портчитатьбайт(командапорт_2)&0x01) != 0; i++ {
		Портчитатьбайт(данныепорт_2)
	}

	if !писатьps2Команда(0xAE) || !писатьps2Команда(0x20) {
		return
	}
	состояние, оК := читатьps2данные()
	if !оК {
		return
	}
	состояние |= 0x01
	состояние &^= 0x10
	if !писатьps2Команда(0x60) || !писатьps2данные(состояние) {
		return
	}

	if !писатьps2данные(0xF4) {
		return
	}
	ack, оК := читатьps2данные()
	if !оК || ack != 0xFA {
		return
	}

}

func ручкаклавиатурапрерывание(esp uint32) uint32 {
	if активноклавиатурадрайвер == nil {
		Портчитатьбайт(данныепорт_2)
		return esp
	}
	return активноклавиатурадрайвер.Ручкапрерывание(esp)
}

const клавиатураочередьРазмер = 64

var клавиатураочередь [клавиатураочередьРазмер]byte
var клавиатураочередьчитать uint8
var клавиатураочередьписать uint8
var слеваshift bool
var справаshift bool
var extendedСканироватьcode bool

func очередьклавиатурабайт(ключ byte) {
	далее := (клавиатураочередьписать + 1) % клавиатураочередьРазмер
	if далее == клавиатураочередьчитать {
		return
	}
	клавиатураочередь[клавиатураочередьписать] = ключ
	клавиатураочередьписать = далее
}

func Процессожидающийклавиатурасобытия() {
	for клавиатураочередьчитать != клавиатураочередьписать {
		ключ := клавиатураочередь[клавиатураочередьчитать]
		клавиатураочередьчитать = (клавиатураочередьчитать + 1) % клавиатураочередьРазмер
		Stdinputбайт(ключ)
		if iклавиатурасобытиеhandler != nil {
			iклавиатурасобытиеhandler.ПриКлючВниз(ключ)
		}
	}
}

func сканироватьcodeкбайт(сканироватьcode uint8) (byte, bool) {
	shift := слеваshift || справаshift

	if сканироватьcode >= 0x02 && сканироватьcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[сканироватьcode-0x02], true
		}
		return "1234567890"[сканироватьcode-0x02], true
	}
	if сканироватьcode >= 0x10 && сканироватьcode <= 0x19 {
		ключ := "qwertyuiop"[сканироватьcode-0x10]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if сканироватьcode >= 0x1E && сканироватьcode <= 0x26 {
		ключ := "asdfghjkl"[сканироватьcode-0x1E]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if сканироватьcode >= 0x2C && сканироватьcode <= 0x32 {
		ключ := "zxcvbnm"[сканироватьcode-0x2C]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}

	switch сканироватьcode {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (текущий *TКлавиатурадрайвер) Ручкапрерывание(esp uint32) uint32 {
	состояние := Портчитатьбайт(командапорт_2)
	if (состояние&0x01) == 0 || (состояние&0x20) != 0 {
		return esp
	}

	сканироватьcode := Портчитатьбайт(данныепорт_2)
	if сканироватьcode == 0xE0 {
		extendedСканироватьcode = true
		return esp
	}
	if extendedСканироватьcode {
		extendedСканироватьcode = false
		return esp
	}

	released := (сканироватьcode & 0x80) != 0
	basecode := сканироватьcode & 0x7F
	if basecode == 0x2A {
		слеваshift = !released
		return esp
	}
	if basecode == 0x36 {
		справаshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ключ, оК := сканироватьcodeкбайт(basecode); оК {
		очередьклавиатурабайт(ключ)
	}

	return esp
}
