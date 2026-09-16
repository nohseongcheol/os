/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package тастатура

import . "unsafe"

import . "порт"
import . "ометање"

import . "конзола"
import . "системcall"

type IТастатураДогађајhandler interface {
	NaКључНиже(кључ byte)
	NaКључGore(кључ byte)
}

var iТастатураДогађајhandler IТастатураДогађајhandler
var подразумеваноТастатураДогађајhandler TПодразумеваноТастатураДогађајhandler

type TПодразумеваноТастатураДогађајhandler struct {
}

func (isti *TПодразумеваноТастатураДогађајhandler) NaКључНиже(кључ byte) {
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heksadecimalno[((кључ >> 4) & 0xF)]
	buffer[18] = heksadecimalno[кључ&0xF]

	конзола_2 := TКонзола{}
	конзола_2.MŠtampaj(buffer)

}
func (isti *TПодразумеваноТастатураДогађајhandler) NaКључGore(кључ byte) {
}

type TТастатураdriver struct {
	TОметањеhandler
}

var aktivnaТастатураdriver *TТастатураdriver
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

func (isti *TТастатураdriver) Initdriver(manager *TОметањеmanager, тастатураДогађајhandler IТастатураДогађајhandler) {

	iТастатураДогађајhandler = &подразумеваноТастатураДогађајhandler
	if тастатураДогађајhandler != nil {
		iТастатураДогађајhandler = тастатураДогађајhandler
	}

	aktivnaТастатураdriver = isti
	ометањеhandler = ручкаТастатураОметање
	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))

	isti.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Портчитањеbyte(наредбаПорт_2)&0x01) != 0; i++ {
		Портчитањеbyte(dataПорт_2)
	}

	if !upisps2Наредба(0xAE) || !upisps2Наредба(0x20) {
		return
	}
	стање, уреду := читањеps2data()
	if !уреду {
		return
	}
	стање |= 0x01
	стање &^= 0x10
	if !upisps2Наредба(0x60) || !upisps2data(стање) {
		return
	}

	if !upisps2data(0xF4) {
		return
	}
	ack, уреду := читањеps2data()
	if !уреду || ack != 0xFA {
		return
	}

}

func ручкаТастатураОметање(esp uint32) uint32 {
	if aktivnaТастатураdriver == nil {
		Портчитањеbyte(dataПорт_2)
		return esp
	}
	return aktivnaТастатураdriver.РучкаОметање(esp)
}

const тастатураqueueВеличина = 64

var тастатураqueue [тастатураqueueВеличина]byte
var тастатураqueueчитање uint8
var тастатураqueueupis uint8
var левоШифт bool
var десноШифт bool
var extendedПрегледајcode bool

func queueТастатураbyte(кључ byte) {
	следеће := (тастатураqueueupis + 1) % тастатураqueueВеличина
	if следеће == тастатураqueueчитање {
		return
	}
	тастатураqueue[тастатураqueueupis] = кључ
	тастатураqueueupis = следеће
}

func ПроцесpendingТастатураDogađaji() {
	for тастатураqueueчитање != тастатураqueueupis {
		кључ := тастатураqueue[тастатураqueueчитање]
		тастатураqueueчитање = (тастатураqueueчитање + 1) % тастатураqueueВеличина
		Stdinputbyte(кључ)
		if iТастатураДогађајhandler != nil {
			iТастатураДогађајhandler.NaКључНиже(кључ)
		}
	}
}

func прегледајcodetobyte(прегледајcode uint8) (byte, bool) {
	шифт := левоШифт || десноШифт

	if прегледајcode >= 0x02 && прегледајcode <= 0x0B {
		if шифт {
			return "!@#$%^&*()"[прегледајcode-0x02], true
		}
		return "1234567890"[прегледајcode-0x02], true
	}
	if прегледајcode >= 0x10 && прегледајcode <= 0x19 {
		кључ := "qwertyuiop"[прегледајcode-0x10]
		if шифт {
			кључ -= 'a' - 'A'
		}
		return кључ, true
	}
	if прегледајcode >= 0x1E && прегледајcode <= 0x26 {
		кључ := "asdfghjkl"[прегледајcode-0x1E]
		if шифт {
			кључ -= 'a' - 'A'
		}
		return кључ, true
	}
	if прегледајcode >= 0x2C && прегледајcode <= 0x32 {
		кључ := "zxcvbnm"[прегледајcode-0x2C]
		if шифт {
			кључ -= 'a' - 'A'
		}
		return кључ, true
	}

	switch прегледајcode {
	case 0x0C:
		if шифт {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if шифт {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if шифт {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if шифт {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if шифт {
			return ':', true
		}
		return ';', true
	case 0x28:
		if шифт {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if шифт {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if шифт {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if шифт {
			return '<', true
		}
		return ',', true
	case 0x34:
		if шифт {
			return '>', true
		}
		return '.', true
	case 0x35:
		if шифт {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (isti *TТастатураdriver) РучкаОметање(esp uint32) uint32 {
	стање := Портчитањеbyte(наредбаПорт_2)
	if (стање&0x01) == 0 || (стање&0x20) != 0 {
		return esp
	}

	прегледајcode := Портчитањеbyte(dataПорт_2)
	if прегледајcode == 0xE0 {
		extendedПрегледајcode = true
		return esp
	}
	if extendedПрегледајcode {
		extendedПрегледајcode = false
		return esp
	}

	released := (прегледајcode & 0x80) != 0
	basecode := прегледајcode & 0x7F
	if basecode == 0x2A {
		левоШифт = !released
		return esp
	}
	if basecode == 0x36 {
		десноШифт = !released
		return esp
	}
	if released {
		return esp
	}

	if кључ, уреду := прегледајcodetobyte(basecode); уреду {
		queueТастатураbyte(кључ)
	}

	return esp
}
