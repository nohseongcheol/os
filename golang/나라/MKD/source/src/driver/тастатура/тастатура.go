package тастатура

import . "unsafe"

import . "порта"
import . "interrupt"

import . "console"
import . "системcall"

type IТастатураeventhandler interface {
	ВклученоkeyДолу(key byte)
	ВклученоkeyГоре(key byte)
}

var iТастатураeventhandler IТастатураeventhandler
var стандардноТастатураeventhandler TСтандардноТастатураeventhandler

type TСтандардноТастатураeventhandler struct {
}

func (само *TСтандардноТастатураeventhandler) ВклученоkeyДолу(key byte) {
	хекса := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = хекса[((key >> 4) & 0xF)]
	buffer[18] = хекса[key&0xF]

	console_2 := TConsole{}
	console_2.MПечати(buffer)

}
func (само *TСтандардноТастатураeventhandler) ВклученоkeyГоре(key byte) {
}

type TТастатураdriver struct {
	TInterrupthandler
}

var активноТастатураdriver *TТастатураdriver
var interrupthandler func(uint32) uint32

var dataПорта_2 uint16 = 0x60
var командаПорта_2 uint16 = 0x64

const ps2Чекајlimit = 100000

func чекајps2ВнесПразно() bool {
	for i := 0; i < ps2Чекајlimit; i++ {
		if (ПортаЧитајbyte(командаПорта_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func чекајps2outputПолно() bool {
	for i := 0; i < ps2Чекајlimit; i++ {
		if (ПортаЧитајbyte(командаПорта_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func запишиps2Команда(вредност uint8) bool {
	if !чекајps2ВнесПразно() {
		return false
	}
	ПортаЗапишиbyte(командаПорта_2, вредност)
	return true
}

func запишиps2data(вредност uint8) bool {
	if !чекајps2ВнесПразно() {
		return false
	}
	ПортаЗапишиbyte(dataПорта_2, вредност)
	return true
}

func читајps2data() (uint8, bool) {
	if !чекајps2outputПолно() {
		return 0, false
	}
	return ПортаЧитајbyte(dataПорта_2), true
}

func (само *TТастатураdriver) Initdriver(manager *TInterruptmanager, тастатураeventhandler IТастатураeventhandler) {

	iТастатураeventhandler = &стандардноТастатураeventhandler
	if тастатураeventhandler != nil {
		iТастатураeventhandler = тастатураeventhandler
	}

	активноТастатураdriver = само
	interrupthandler = handleТастатураinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	само.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортаЧитајbyte(командаПорта_2)&0x01) != 0; i++ {
		ПортаЧитајbyte(dataПорта_2)
	}

	if !запишиps2Команда(0xAE) || !запишиps2Команда(0x20) {
		return
	}
	статус, воред := читајps2data()
	if !воред {
		return
	}
	статус |= 0x01
	статус &^= 0x10
	if !запишиps2Команда(0x60) || !запишиps2data(статус) {
		return
	}

	if !запишиps2data(0xF4) {
		return
	}
	ack, воред := читајps2data()
	if !воред || ack != 0xFA {
		return
	}

}

func handleТастатураinterrupt(esp uint32) uint32 {
	if активноТастатураdriver == nil {
		ПортаЧитајbyte(dataПорта_2)
		return esp
	}
	return активноТастатураdriver.Handleinterrupt(esp)
}

const тастатураqueueГолемина = 64

var тастатураqueue [тастатураqueueГолемина]byte
var тастатураqueueЧитај uint8
var тастатураqueueЗапиши uint8
var левоshift bool
var десноshift bool
var extendedСкенирајcode bool

func queueТастатураbyte(key byte) {
	следна := (тастатураqueueЗапиши + 1) % тастатураqueueГолемина
	if следна == тастатураqueueЧитај {
		return
	}
	тастатураqueue[тастатураqueueЗапиши] = key
	тастатураqueueЗапиши = следна
}

func ПроцесpendingТастатураevents() {
	for тастатураqueueЧитај != тастатураqueueЗапиши {
		key := тастатураqueue[тастатураqueueЧитај]
		тастатураqueueЧитај = (тастатураqueueЧитај + 1) % тастатураqueueГолемина
		Stdinputbyte(key)
		if iТастатураeventhandler != nil {
			iТастатураeventhandler.ВклученоkeyДолу(key)
		}
	}
}

func скенирајcodetobyte(скенирајcode uint8) (byte, bool) {
	shift := левоshift || десноshift

	if скенирајcode >= 0x02 && скенирајcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[скенирајcode-0x02], true
		}
		return "1234567890"[скенирајcode-0x02], true
	}
	if скенирајcode >= 0x10 && скенирајcode <= 0x19 {
		key := "qwertyuiop"[скенирајcode-0x10]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if скенирајcode >= 0x1E && скенирајcode <= 0x26 {
		key := "asdfghjkl"[скенирајcode-0x1E]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if скенирајcode >= 0x2C && скенирајcode <= 0x32 {
		key := "zxcvbnm"[скенирајcode-0x2C]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch скенирајcode {
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

func (само *TТастатураdriver) Handleinterrupt(esp uint32) uint32 {
	статус := ПортаЧитајbyte(командаПорта_2)
	if (статус&0x01) == 0 || (статус&0x20) != 0 {
		return esp
	}

	скенирајcode := ПортаЧитајbyte(dataПорта_2)
	if скенирајcode == 0xE0 {
		extendedСкенирајcode = true
		return esp
	}
	if extendedСкенирајcode {
		extendedСкенирајcode = false
		return esp
	}

	released := (скенирајcode & 0x80) != 0
	basecode := скенирајcode & 0x7F
	if basecode == 0x2A {
		левоshift = !released
		return esp
	}
	if basecode == 0x36 {
		десноshift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, воред := скенирајcodetobyte(basecode); воред {
		queueТастатураbyte(key)
	}

	return esp
}
