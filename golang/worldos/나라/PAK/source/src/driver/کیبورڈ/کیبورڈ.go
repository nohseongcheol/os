/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package کیبورڈ

import . "unsafe"

import . "پورٹ"
import . "مداخلت"

import . "console"
import . "نظامcall"

type Iکیبورڈواقعہhandler interface {
	Oچالوkeyنیچے(key byte)
	Oچالوkeyاوپر(key byte)
}

var iکیبورڈواقعہhandler Iکیبورڈواقعہhandler
var طےشدہکیبورڈواقعہhandler Tطےشدہکیبورڈواقعہhandler

type Tطےشدہکیبورڈواقعہhandler struct {
}

func (self *Tطےشدہکیبورڈواقعہhandler) Oچالوkeyنیچے(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	console_2 := TConsole{}
	console_2.Mچھاپیں(buffer)

}
func (self *Tطےشدہکیبورڈواقعہhandler) Oچالوkeyاوپر(key byte) {
}

type Tکیبورڈdriver struct {
	Tمداخلتhandler
}

var فعالکیبورڈdriver *Tکیبورڈdriver
var مداخلتhandler func(uint32) uint32

var dataپورٹ_2 uint16 = 0x60
var کمانڈپورٹ_2 uint16 = 0x64

const ps2waitحد = 100000

func waitps2ماداخلخالی() bool {
	for i := 0; i < ps2waitحد; i++ {
		if (Pپورٹپڑھیںbyte(کمانڈپورٹ_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2ماخارجfull() bool {
	for i := 0; i < ps2waitحد; i++ {
		if (Pپورٹپڑھیںbyte(کمانڈپورٹ_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func لکھیںps2کمانڈ(قدر uint8) bool {
	if !waitps2ماداخلخالی() {
		return false
	}
	Pپورٹلکھیںbyte(کمانڈپورٹ_2, قدر)
	return true
}

func لکھیںps2data(قدر uint8) bool {
	if !waitps2ماداخلخالی() {
		return false
	}
	Pپورٹلکھیںbyte(dataپورٹ_2, قدر)
	return true
}

func پڑھیںps2data() (uint8, bool) {
	if !waitps2ماخارجfull() {
		return 0, false
	}
	return Pپورٹپڑھیںbyte(dataپورٹ_2), true
}

func (self *Tکیبورڈdriver) Initdriver(manager *Tمداخلتmanager, کیبورڈواقعہhandler Iکیبورڈواقعہhandler) {

	iکیبورڈواقعہhandler = &طےشدہکیبورڈواقعہhandler
	if کیبورڈواقعہhandler != nil {
		iکیبورڈواقعہhandler = کیبورڈواقعہhandler
	}

	فعالکیبورڈdriver = self
	مداخلتhandler = handleکیبورڈمداخلت
	var address uintptr
	address = uintptr(Pointer(&مداخلتhandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pپورٹپڑھیںbyte(کمانڈپورٹ_2)&0x01) != 0; i++ {
		Pپورٹپڑھیںbyte(dataپورٹ_2)
	}

	if !لکھیںps2کمانڈ(0xAE) || !لکھیںps2کمانڈ(0x20) {
		return
	}
	حالت, ok := پڑھیںps2data()
	if !ok {
		return
	}
	حالت |= 0x01
	حالت &^= 0x10
	if !لکھیںps2کمانڈ(0x60) || !لکھیںps2data(حالت) {
		return
	}

	if !لکھیںps2data(0xF4) {
		return
	}
	ack, ok := پڑھیںps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleکیبورڈمداخلت(esp uint32) uint32 {
	if فعالکیبورڈdriver == nil {
		Pپورٹپڑھیںbyte(dataپورٹ_2)
		return esp
	}
	return فعالکیبورڈdriver.Handleمداخلت(esp)
}

const کیبورڈqueueحجم = 64

var کیبورڈqueue [کیبورڈqueueحجم]byte
var کیبورڈqueueپڑھیں uint8
var کیبورڈqueueلکھیں uint8
var بائیںshift bool
var دائیںshift bool
var توسیعیسکینکریںcode bool

func queueکیبورڈbyte(key byte) {
	اگلا := (کیبورڈqueueلکھیں + 1) % کیبورڈqueueحجم
	if اگلا == کیبورڈqueueپڑھیں {
		return
	}
	کیبورڈqueue[کیبورڈqueueلکھیں] = key
	کیبورڈqueueلکھیں = اگلا
}

func Pعملکاریpendingکیبورڈevents() {
	for کیبورڈqueueپڑھیں != کیبورڈqueueلکھیں {
		key := کیبورڈqueue[کیبورڈqueueپڑھیں]
		کیبورڈqueueپڑھیں = (کیبورڈqueueپڑھیں + 1) % کیبورڈqueueحجم
		Stdinputbyte(key)
		if iکیبورڈواقعہhandler != nil {
			iکیبورڈواقعہhandler.Oچالوkeyنیچے(key)
		}
	}
}

func سکینکریںcodetobyte(سکینکریںcode uint8) (byte, bool) {
	shift := بائیںshift || دائیںshift

	if سکینکریںcode >= 0x02 && سکینکریںcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[سکینکریںcode-0x02], true
		}
		return "1234567890"[سکینکریںcode-0x02], true
	}
	if سکینکریںcode >= 0x10 && سکینکریںcode <= 0x19 {
		key := "qwertyuiop"[سکینکریںcode-0x10]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if سکینکریںcode >= 0x1E && سکینکریںcode <= 0x26 {
		key := "asdfghjkl"[سکینکریںcode-0x1E]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if سکینکریںcode >= 0x2C && سکینکریںcode <= 0x32 {
		key := "zxcvbnm"[سکینکریںcode-0x2C]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch سکینکریںcode {
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

func (self *Tکیبورڈdriver) Handleمداخلت(esp uint32) uint32 {
	حالت := Pپورٹپڑھیںbyte(کمانڈپورٹ_2)
	if (حالت&0x01) == 0 || (حالت&0x20) != 0 {
		return esp
	}

	سکینکریںcode := Pپورٹپڑھیںbyte(dataپورٹ_2)
	if سکینکریںcode == 0xE0 {
		توسیعیسکینکریںcode = true
		return esp
	}
	if توسیعیسکینکریںcode {
		توسیعیسکینکریںcode = false
		return esp
	}

	released := (سکینکریںcode & 0x80) != 0
	basecode := سکینکریںcode & 0x7F
	if basecode == 0x2A {
		بائیںshift = !released
		return esp
	}
	if basecode == 0x36 {
		دائیںshift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ok := سکینکریںcodetobyte(basecode); ok {
		queueکیبورڈbyte(key)
	}

	return esp
}
