/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package клавиатура

import . "unsafe"

import . "порт"
import . "прекъсване"

import . "console"
import . "системаcall"

type IКлавиатураСъбитиеhandler interface {
	ВклКлючНадолу(ключ byte)
	ВклКлючНагоре(ключ byte)
}

var iКлавиатураСъбитиеhandler IКлавиатураСъбитиеhandler
var поподразбиранеКлавиатураСъбитиеhandler TПоподразбиранеКлавиатураСъбитиеhandler

type TПоподразбиранеКлавиатураСъбитиеhandler struct {
}

func (себеси *TПоподразбиранеКлавиатураСъбитиеhandler) ВклКлючНадолу(ключ byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((ключ >> 4) & 0xF)]
	buffer[18] = hex[ключ&0xF]

	console_2 := TConsole{}
	console_2.MПечат(buffer)

}
func (себеси *TПоподразбиранеКлавиатураСъбитиеhandler) ВклКлючНагоре(ключ byte) {
}

type TКлавиатураdriver struct {
	TПрекъсванеhandler
}

var активнаКлавиатураdriver *TКлавиатураdriver
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

func (себеси *TКлавиатураdriver) Initdriver(manager *TПрекъсванеmanager, клавиатураСъбитиеhandler IКлавиатураСъбитиеhandler) {

	iКлавиатураСъбитиеhandler = &поподразбиранеКлавиатураСъбитиеhandler
	if клавиатураСъбитиеhandler != nil {
		iКлавиатураСъбитиеhandler = клавиатураСъбитиеhandler
	}

	активнаКлавиатураdriver = себеси
	прекъсванеhandler = ръкохваткаКлавиатураПрекъсване
	var address uintptr
	address = uintptr(Pointer(&прекъсванеhandler))

	себеси.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортЧетенеbyte(командаПорт_2)&0x01) != 0; i++ {
		ПортЧетенеbyte(dataПорт_2)
	}

	if !писанеps2Команда(0xAE) || !писанеps2Команда(0x20) {
		return
	}
	състояние, приеми := четенеps2data()
	if !приеми {
		return
	}
	състояние |= 0x01
	състояние &^= 0x10
	if !писанеps2Команда(0x60) || !писанеps2data(състояние) {
		return
	}

	if !писанеps2data(0xF4) {
		return
	}
	ack, приеми := четенеps2data()
	if !приеми || ack != 0xFA {
		return
	}

}

func ръкохваткаКлавиатураПрекъсване(esp uint32) uint32 {
	if активнаКлавиатураdriver == nil {
		ПортЧетенеbyte(dataПорт_2)
		return esp
	}
	return активнаКлавиатураdriver.РъкохваткаПрекъсване(esp)
}

const клавиатураqueueРазмер = 64

var клавиатураqueue [клавиатураqueueРазмер]byte
var клавиатураqueueЧетене uint8
var клавиатураqueueПисане uint8
var лявоshift bool
var дясноshift bool
var extendedТърсенеcode bool

func queueКлавиатураbyte(ключ byte) {
	следващо := (клавиатураqueueПисане + 1) % клавиатураqueueРазмер
	if следващо == клавиатураqueueЧетене {
		return
	}
	клавиатураqueue[клавиатураqueueПисане] = ключ
	клавиатураqueueПисане = следващо
}

func ПроцесpendingКлавиатураevents() {
	for клавиатураqueueЧетене != клавиатураqueueПисане {
		ключ := клавиатураqueue[клавиатураqueueЧетене]
		клавиатураqueueЧетене = (клавиатураqueueЧетене + 1) % клавиатураqueueРазмер
		Stdinputbyte(ключ)
		if iКлавиатураСъбитиеhandler != nil {
			iКлавиатураСъбитиеhandler.ВклКлючНадолу(ключ)
		}
	}
}

func търсенеcodetobyte(търсенеcode uint8) (byte, bool) {
	shift := лявоshift || дясноshift

	if търсенеcode >= 0x02 && търсенеcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[търсенеcode-0x02], true
		}
		return "1234567890"[търсенеcode-0x02], true
	}
	if търсенеcode >= 0x10 && търсенеcode <= 0x19 {
		ключ := "qwertyuiop"[търсенеcode-0x10]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if търсенеcode >= 0x1E && търсенеcode <= 0x26 {
		ключ := "asdfghjkl"[търсенеcode-0x1E]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if търсенеcode >= 0x2C && търсенеcode <= 0x32 {
		ключ := "zxcvbnm"[търсенеcode-0x2C]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}

	switch търсенеcode {
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

func (себеси *TКлавиатураdriver) РъкохваткаПрекъсване(esp uint32) uint32 {
	състояние := ПортЧетенеbyte(командаПорт_2)
	if (състояние&0x01) == 0 || (състояние&0x20) != 0 {
		return esp
	}

	търсенеcode := ПортЧетенеbyte(dataПорт_2)
	if търсенеcode == 0xE0 {
		extendedТърсенеcode = true
		return esp
	}
	if extendedТърсенеcode {
		extendedТърсенеcode = false
		return esp
	}

	released := (търсенеcode & 0x80) != 0
	basecode := търсенеcode & 0x7F
	if basecode == 0x2A {
		лявоshift = !released
		return esp
	}
	if basecode == 0x36 {
		дясноshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ключ, приеми := търсенеcodetobyte(basecode); приеми {
		queueКлавиатураbyte(ключ)
	}

	return esp
}
