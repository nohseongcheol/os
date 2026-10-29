/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package клавіатура

import . "unsafe"

import . "порт"
import . "переривання"

import . "консоль"
import . "системаcall"

type IКлавіатураПодіяhandler interface {
	УвімкненоКлючВниз(ключ byte)
	УвімкненоКлючВгору(ключ byte)
}

var iКлавіатураПодіяhandler IКлавіатураПодіяhandler
var типовийКлавіатураПодіяhandler TТиповийКлавіатураПодіяhandler

type TТиповийКлавіатураПодіяhandler struct {
}

func (поточний *TТиповийКлавіатураПодіяhandler) УвімкненоКлючВниз(ключ byte) {
	шістнадцяткова := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = шістнадцяткова[((ключ >> 4) & 0xF)]
	buffer[18] = шістнадцяткова[ключ&0xF]

	консоль_2 := TКонсоль{}
	консоль_2.MДрук(buffer)

}
func (поточний *TТиповийКлавіатураПодіяhandler) УвімкненоКлючВгору(ключ byte) {
}

type TКлавіатураdriver struct {
	TПерериванняhandler
}

var активнийКлавіатураdriver *TКлавіатураdriver
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

func (поточний *TКлавіатураdriver) Initdriver(manager *TПерериванняmanager, клавіатураПодіяhandler IКлавіатураПодіяhandler) {

	iКлавіатураПодіяhandler = &типовийКлавіатураПодіяhandler
	if клавіатураПодіяhandler != nil {
		iКлавіатураПодіяhandler = клавіатураПодіяhandler
	}

	активнийКлавіатураdriver = поточний
	перериванняhandler = елементкеруванняКлавіатураПереривання
	var адреса uintptr
	адреса = uintptr(Pointer(&перериванняhandler))

	поточний.Init(0x21, uintptr(Pointer(manager)), адреса)

	for i := 0; i < 32 && (ПортЧитанняbyte(командаПорт_2)&0x01) != 0; i++ {
		ПортЧитанняbyte(dataПорт_2)
	}

	if !записps2Команда(0xAE) || !записps2Команда(0x20) {
		return
	}
	статус, гаразд := читанняps2data()
	if !гаразд {
		return
	}
	статус |= 0x01
	статус &^= 0x10
	if !записps2Команда(0x60) || !записps2data(статус) {
		return
	}

	if !записps2data(0xF4) {
		return
	}
	ack, гаразд := читанняps2data()
	if !гаразд || ack != 0xFA {
		return
	}

}

func елементкеруванняКлавіатураПереривання(esp uint32) uint32 {
	if активнийКлавіатураdriver == nil {
		ПортЧитанняbyte(dataПорт_2)
		return esp
	}
	return активнийКлавіатураdriver.ЕлементкеруванняПереривання(esp)
}

const клавіатураqueueРозмір = 64

var клавіатураqueue [клавіатураqueueРозмір]byte
var клавіатураqueueЧитання uint8
var клавіатураqueueЗапис uint8
var зліваshift bool
var справаshift bool
var extendedСкануватиcode bool

func queueКлавіатураbyte(ключ byte) {
	наступне := (клавіатураqueueЗапис + 1) % клавіатураqueueРозмір
	if наступне == клавіатураqueueЧитання {
		return
	}
	клавіатураqueue[клавіатураqueueЗапис] = ключ
	клавіатураqueueЗапис = наступне
}

func ПроцесиpendingКлавіатураПодії() {
	for клавіатураqueueЧитання != клавіатураqueueЗапис {
		ключ := клавіатураqueue[клавіатураqueueЧитання]
		клавіатураqueueЧитання = (клавіатураqueueЧитання + 1) % клавіатураqueueРозмір
		Stdinputbyte(ключ)
		if iКлавіатураПодіяhandler != nil {
			iКлавіатураПодіяhandler.УвімкненоКлючВниз(ключ)
		}
	}
}

func скануватиcodeтоbyte(скануватиcode uint8) (byte, bool) {
	shift := зліваshift || справаshift

	if скануватиcode >= 0x02 && скануватиcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[скануватиcode-0x02], true
		}
		return "1234567890"[скануватиcode-0x02], true
	}
	if скануватиcode >= 0x10 && скануватиcode <= 0x19 {
		ключ := "qwertyuiop"[скануватиcode-0x10]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if скануватиcode >= 0x1E && скануватиcode <= 0x26 {
		ключ := "asdfghjkl"[скануватиcode-0x1E]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if скануватиcode >= 0x2C && скануватиcode <= 0x32 {
		ключ := "zxcvbnm"[скануватиcode-0x2C]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}

	switch скануватиcode {
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

func (поточний *TКлавіатураdriver) ЕлементкеруванняПереривання(esp uint32) uint32 {
	статус := ПортЧитанняbyte(командаПорт_2)
	if (статус&0x01) == 0 || (статус&0x20) != 0 {
		return esp
	}

	скануватиcode := ПортЧитанняbyte(dataПорт_2)
	if скануватиcode == 0xE0 {
		extendedСкануватиcode = true
		return esp
	}
	if extendedСкануватиcode {
		extendedСкануватиcode = false
		return esp
	}

	released := (скануватиcode & 0x80) != 0
	basecode := скануватиcode & 0x7F
	if basecode == 0x2A {
		зліваshift = !released
		return esp
	}
	if basecode == 0x36 {
		справаshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ключ, гаразд := скануватиcodeтоbyte(basecode); гаразд {
		queueКлавіатураbyte(ключ)
	}

	return esp
}
