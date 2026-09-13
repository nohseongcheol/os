package клавіятура

import . "unsafe"

import . "порт"
import . "перарыванне"

import . "console"
import . "сістэмаcall"

type IКлавіятураПадзеяhandler interface {
	OnКлючУніз(ключ byte)
	OnКлючВышэй(ключ byte)
}

var iКлавіятураПадзеяhandler IКлавіятураПадзеяhandler
var стандартнаКлавіятураПадзеяhandler TСтандартнаКлавіятураПадзеяhandler

type TСтандартнаКлавіятураПадзеяhandler struct {
}

func (self *TСтандартнаКлавіятураПадзеяhandler) OnКлючУніз(ключ byte) {
	шаснаццатковы := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = шаснаццатковы[((ключ >> 4) & 0xF)]
	buffer[18] = шаснаццатковы[ключ&0xF]

	console_2 := TConsole{}
	console_2.MДрукаваць(buffer)

}
func (self *TСтандартнаКлавіятураПадзеяhandler) OnКлючВышэй(ключ byte) {
}

type TКлавіятураdriver struct {
	TПерарываннеhandler
}

var актыўнаКлавіятураdriver *TКлавіятураdriver
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

func (self *TКлавіятураdriver) Initdriver(manager *TПерарываннеmanager, клавіятураПадзеяhandler IКлавіятураПадзеяhandler) {

	iКлавіятураПадзеяhandler = &стандартнаКлавіятураПадзеяhandler
	if клавіятураПадзеяhandler != nil {
		iКлавіятураПадзеяhandler = клавіятураПадзеяhandler
	}

	актыўнаКлавіятураdriver = self
	перарываннеhandler = handleКлавіятураПерарыванне
	var address uintptr
	address = uintptr(Pointer(&перарываннеhandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортЧытаннеbyte(загадПорт_2)&0x01) != 0; i++ {
		ПортЧытаннеbyte(dataПорт_2)
	}

	if !запісps2Загад(0xAE) || !запісps2Загад(0x20) {
		return
	}
	стан, добра := чытаннеps2data()
	if !добра {
		return
	}
	стан |= 0x01
	стан &^= 0x10
	if !запісps2Загад(0x60) || !запісps2data(стан) {
		return
	}

	if !запісps2data(0xF4) {
		return
	}
	ack, добра := чытаннеps2data()
	if !добра || ack != 0xFA {
		return
	}

}

func handleКлавіятураПерарыванне(esp uint32) uint32 {
	if актыўнаКлавіятураdriver == nil {
		ПортЧытаннеbyte(dataПорт_2)
		return esp
	}
	return актыўнаКлавіятураdriver.HandleПерарыванне(esp)
}

const клавіятураqueueПамер = 64

var клавіятураqueue [клавіятураqueueПамер]byte
var клавіятураqueueЧытанне uint8
var клавіятураqueueЗапіс uint8
var злеваshift bool
var справаshift bool
var extendedАналізcode bool

func queueКлавіятураbyte(ключ byte) {
	наступны := (клавіятураqueueЗапіс + 1) % клавіятураqueueПамер
	if наступны == клавіятураqueueЧытанне {
		return
	}
	клавіятураqueue[клавіятураqueueЗапіс] = ключ
	клавіятураqueueЗапіс = наступны
}

func ПрацэсpendingКлавіятураevents() {
	for клавіятураqueueЧытанне != клавіятураqueueЗапіс {
		ключ := клавіятураqueue[клавіятураqueueЧытанне]
		клавіятураqueueЧытанне = (клавіятураqueueЧытанне + 1) % клавіятураqueueПамер
		Stdinputbyte(ключ)
		if iКлавіятураПадзеяhandler != nil {
			iКлавіятураПадзеяhandler.OnКлючУніз(ключ)
		}
	}
}

func аналізcodetobyte(аналізcode uint8) (byte, bool) {
	shift := злеваshift || справаshift

	if аналізcode >= 0x02 && аналізcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[аналізcode-0x02], true
		}
		return "1234567890"[аналізcode-0x02], true
	}
	if аналізcode >= 0x10 && аналізcode <= 0x19 {
		ключ := "qwertyuiop"[аналізcode-0x10]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if аналізcode >= 0x1E && аналізcode <= 0x26 {
		ключ := "asdfghjkl"[аналізcode-0x1E]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}
	if аналізcode >= 0x2C && аналізcode <= 0x32 {
		ключ := "zxcvbnm"[аналізcode-0x2C]
		if shift {
			ключ -= 'a' - 'A'
		}
		return ключ, true
	}

	switch аналізcode {
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

func (self *TКлавіятураdriver) HandleПерарыванне(esp uint32) uint32 {
	стан := ПортЧытаннеbyte(загадПорт_2)
	if (стан&0x01) == 0 || (стан&0x20) != 0 {
		return esp
	}

	аналізcode := ПортЧытаннеbyte(dataПорт_2)
	if аналізcode == 0xE0 {
		extendedАналізcode = true
		return esp
	}
	if extendedАналізcode {
		extendedАналізcode = false
		return esp
	}

	released := (аналізcode & 0x80) != 0
	basecode := аналізcode & 0x7F
	if basecode == 0x2A {
		злеваshift = !released
		return esp
	}
	if basecode == 0x36 {
		справаshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ключ, добра := аналізcodetobyte(basecode); добра {
		queueКлавіятураbyte(ключ)
	}

	return esp
}
