package клавиатура

import . "unsafe"

import . "порт"
import . "interrupt"

import . "console"
import . "системаcall"

type IКлавиатураeventhandler interface {
	OnАчкычdown(ачкыч byte)
	OnАчкычӨйдө(ачкыч byte)
}

var iКлавиатураeventhandler IКлавиатураeventhandler
var жарыяланбасКлавиатураeventhandler TЖарыяланбасКлавиатураeventhandler

type TЖарыяланбасКлавиатураeventhandler struct {
}

func (self *TЖарыяланбасКлавиатураeventhandler) OnАчкычdown(ачкыч byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((ачкыч >> 4) & 0xF)]
	buffer[18] = hex[ачкыч&0xF]

	console_2 := TConsole{}
	console_2.MБасма(buffer)

}
func (self *TЖарыяланбасКлавиатураeventhandler) OnАчкычӨйдө(ачкыч byte) {
}

type TКлавиатураdriver struct {
	TInterrupthandler
}

var активдүүКлавиатураdriver *TКлавиатураdriver
var interrupthandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var командаПорт_2 uint16 = 0x64

const ps2Күтүүlimit = 100000

func күтүүps2КиришБош() bool {
	for i := 0; i < ps2Күтүүlimit; i++ {
		if (ПортОкууbyte(командаПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func күтүүps2ЧыгышТолук() bool {
	for i := 0; i < ps2Күтүүlimit; i++ {
		if (ПортОкууbyte(командаПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func жазууps2Команда(мааниси uint8) bool {
	if !күтүүps2КиришБош() {
		return false
	}
	ПортЖазууbyte(командаПорт_2, мааниси)
	return true
}

func жазууps2data(мааниси uint8) bool {
	if !күтүүps2КиришБош() {
		return false
	}
	ПортЖазууbyte(dataПорт_2, мааниси)
	return true
}

func окууps2data() (uint8, bool) {
	if !күтүүps2ЧыгышТолук() {
		return 0, false
	}
	return ПортОкууbyte(dataПорт_2), true
}

func (self *TКлавиатураdriver) Initdriver(manager *TInterruptmanager, клавиатураeventhandler IКлавиатураeventhandler) {

	iКлавиатураeventhandler = &жарыяланбасКлавиатураeventhandler
	if клавиатураeventhandler != nil {
		iКлавиатураeventhandler = клавиатураeventhandler
	}

	активдүүКлавиатураdriver = self
	interrupthandler = handleКлавиатураinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ПортОкууbyte(командаПорт_2)&0x01) != 0; i++ {
		ПортОкууbyte(dataПорт_2)
	}

	if !жазууps2Команда(0xAE) || !жазууps2Команда(0x20) {
		return
	}
	абалы, ok := окууps2data()
	if !ok {
		return
	}
	абалы |= 0x01
	абалы &^= 0x10
	if !жазууps2Команда(0x60) || !жазууps2data(абалы) {
		return
	}

	if !жазууps2data(0xF4) {
		return
	}
	ack, ok := окууps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleКлавиатураinterrupt(esp uint32) uint32 {
	if активдүүКлавиатураdriver == nil {
		ПортОкууbyte(dataПорт_2)
		return esp
	}
	return активдүүКлавиатураdriver.Handleinterrupt(esp)
}

const клавиатураqueueӨлчөм = 64

var клавиатураqueue [клавиатураqueueӨлчөм]byte
var клавиатураqueueОкуу uint8
var клавиатураqueueЖазуу uint8
var солshift bool
var оңshift bool
var extendedСкандооcode bool

func queueКлавиатураbyte(ачкыч byte) {
	кийинки := (клавиатураqueueЖазуу + 1) % клавиатураqueueӨлчөм
	if кийинки == клавиатураqueueОкуу {
		return
	}
	клавиатураqueue[клавиатураqueueЖазуу] = ачкыч
	клавиатураqueueЖазуу = кийинки
}

func ПроцессиpendingКлавиатураevents() {
	for клавиатураqueueОкуу != клавиатураqueueЖазуу {
		ачкыч := клавиатураqueue[клавиатураqueueОкуу]
		клавиатураqueueОкуу = (клавиатураqueueОкуу + 1) % клавиатураqueueӨлчөм
		Stdinputbyte(ачкыч)
		if iКлавиатураeventhandler != nil {
			iКлавиатураeventhandler.OnАчкычdown(ачкыч)
		}
	}
}

func скандооcodetobyte(скандооcode uint8) (byte, bool) {
	shift := солshift || оңshift

	if скандооcode >= 0x02 && скандооcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[скандооcode-0x02], true
		}
		return "1234567890"[скандооcode-0x02], true
	}
	if скандооcode >= 0x10 && скандооcode <= 0x19 {
		ачкыч := "qwertyuiop"[скандооcode-0x10]
		if shift {
			ачкыч -= 'a' - 'A'
		}
		return ачкыч, true
	}
	if скандооcode >= 0x1E && скандооcode <= 0x26 {
		ачкыч := "asdfghjkl"[скандооcode-0x1E]
		if shift {
			ачкыч -= 'a' - 'A'
		}
		return ачкыч, true
	}
	if скандооcode >= 0x2C && скандооcode <= 0x32 {
		ачкыч := "zxcvbnm"[скандооcode-0x2C]
		if shift {
			ачкыч -= 'a' - 'A'
		}
		return ачкыч, true
	}

	switch скандооcode {
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

func (self *TКлавиатураdriver) Handleinterrupt(esp uint32) uint32 {
	абалы := ПортОкууbyte(командаПорт_2)
	if (абалы&0x01) == 0 || (абалы&0x20) != 0 {
		return esp
	}

	скандооcode := ПортОкууbyte(dataПорт_2)
	if скандооcode == 0xE0 {
		extendedСкандооcode = true
		return esp
	}
	if extendedСкандооcode {
		extendedСкандооcode = false
		return esp
	}

	released := (скандооcode & 0x80) != 0
	basecode := скандооcode & 0x7F
	if basecode == 0x2A {
		солshift = !released
		return esp
	}
	if basecode == 0x36 {
		оңshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ачкыч, ok := скандооcodetobyte(basecode); ok {
		queueКлавиатураbyte(ачкыч)
	}

	return esp
}
