/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klaviatura

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "tizimcall"

type IKlaviaturaeventhandler interface {
	YoqishKalitPastga(kalit byte)
	YoqishKalitYuqoriga(kalit byte)
}

var iKlaviaturaeventhandler IKlaviaturaeventhandler
var andozaKlaviaturaeventhandler TAndozaKlaviaturaeventhandler

type TAndozaKlaviaturaeventhandler struct {
}

func (self *TAndozaKlaviaturaeventhandler) YoqishKalitPastga(kalit byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((kalit >> 4) & 0xF)]
	buffer[18] = hex[kalit&0xF]

	console_2 := TConsole{}
	console_2.MChopetish(buffer)

}
func (self *TAndozaKlaviaturaeventhandler) YoqishKalitYuqoriga(kalit byte) {
}

type TKlaviaturadriver struct {
	TInterrupthandler
}

var faolKlaviaturadriver *TKlaviaturadriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var buyruqport_2 uint16 = 0x64

const ps2Kutishlimit = 100000

func kutishps2inputBosh() bool {
	for i := 0; i < ps2Kutishlimit; i++ {
		if (PortOʻqishbyte(buyruqport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func kutishps2outputTola() bool {
	for i := 0; i < ps2Kutishlimit; i++ {
		if (PortOʻqishbyte(buyruqport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func yozishps2Buyruq(qiymat uint8) bool {
	if !kutishps2inputBosh() {
		return false
	}
	PortYozishbyte(buyruqport_2, qiymat)
	return true
}

func yozishps2data(qiymat uint8) bool {
	if !kutishps2inputBosh() {
		return false
	}
	PortYozishbyte(dataport_2, qiymat)
	return true
}

func oʻqishps2data() (uint8, bool) {
	if !kutishps2outputTola() {
		return 0, false
	}
	return PortOʻqishbyte(dataport_2), true
}

func (self *TKlaviaturadriver) Initdriver(manager *TInterruptmanager, klaviaturaeventhandler IKlaviaturaeventhandler) {

	iKlaviaturaeventhandler = &andozaKlaviaturaeventhandler
	if klaviaturaeventhandler != nil {
		iKlaviaturaeventhandler = klaviaturaeventhandler
	}

	faolKlaviaturadriver = self
	interrupthandler = handleKlaviaturainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortOʻqishbyte(buyruqport_2)&0x01) != 0; i++ {
		PortOʻqishbyte(dataport_2)
	}

	if !yozishps2Buyruq(0xAE) || !yozishps2Buyruq(0x20) {
		return
	}
	holat, ok := oʻqishps2data()
	if !ok {
		return
	}
	holat |= 0x01
	holat &^= 0x10
	if !yozishps2Buyruq(0x60) || !yozishps2data(holat) {
		return
	}

	if !yozishps2data(0xF4) {
		return
	}
	ack, ok := oʻqishps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleKlaviaturainterrupt(esp uint32) uint32 {
	if faolKlaviaturadriver == nil {
		PortOʻqishbyte(dataport_2)
		return esp
	}
	return faolKlaviaturadriver.Handleinterrupt(esp)
}

const klaviaturaqueueHajmi = 64

var klaviaturaqueue [klaviaturaqueueHajmi]byte
var klaviaturaqueueOʻqish uint8
var klaviaturaqueueYozish uint8
var chapshift bool
var oʻngshift bool
var extendedTekshirishcode bool

func queueKlaviaturabyte(kalit byte) {
	keyingi := (klaviaturaqueueYozish + 1) % klaviaturaqueueHajmi
	if keyingi == klaviaturaqueueOʻqish {
		return
	}
	klaviaturaqueue[klaviaturaqueueYozish] = kalit
	klaviaturaqueueYozish = keyingi
}

func JarayonpendingKlaviaturaevents() {
	for klaviaturaqueueOʻqish != klaviaturaqueueYozish {
		kalit := klaviaturaqueue[klaviaturaqueueOʻqish]
		klaviaturaqueueOʻqish = (klaviaturaqueueOʻqish + 1) % klaviaturaqueueHajmi
		Stdinputbyte(kalit)
		if iKlaviaturaeventhandler != nil {
			iKlaviaturaeventhandler.YoqishKalitPastga(kalit)
		}
	}
}

func tekshirishcodetobyte(tekshirishcode uint8) (byte, bool) {
	shift := chapshift || oʻngshift

	if tekshirishcode >= 0x02 && tekshirishcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[tekshirishcode-0x02], true
		}
		return "1234567890"[tekshirishcode-0x02], true
	}
	if tekshirishcode >= 0x10 && tekshirishcode <= 0x19 {
		kalit := "qwertyuiop"[tekshirishcode-0x10]
		if shift {
			kalit -= 'a' - 'A'
		}
		return kalit, true
	}
	if tekshirishcode >= 0x1E && tekshirishcode <= 0x26 {
		kalit := "asdfghjkl"[tekshirishcode-0x1E]
		if shift {
			kalit -= 'a' - 'A'
		}
		return kalit, true
	}
	if tekshirishcode >= 0x2C && tekshirishcode <= 0x32 {
		kalit := "zxcvbnm"[tekshirishcode-0x2C]
		if shift {
			kalit -= 'a' - 'A'
		}
		return kalit, true
	}

	switch tekshirishcode {
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

func (self *TKlaviaturadriver) Handleinterrupt(esp uint32) uint32 {
	holat := PortOʻqishbyte(buyruqport_2)
	if (holat&0x01) == 0 || (holat&0x20) != 0 {
		return esp
	}

	tekshirishcode := PortOʻqishbyte(dataport_2)
	if tekshirishcode == 0xE0 {
		extendedTekshirishcode = true
		return esp
	}
	if extendedTekshirishcode {
		extendedTekshirishcode = false
		return esp
	}

	released := (tekshirishcode & 0x80) != 0
	basecode := tekshirishcode & 0x7F
	if basecode == 0x2A {
		chapshift = !released
		return esp
	}
	if basecode == 0x36 {
		oʻngshift = !released
		return esp
	}
	if released {
		return esp
	}

	if kalit, ok := tekshirishcodetobyte(basecode); ok {
		queueKlaviaturabyte(kalit)
	}

	return esp
}
