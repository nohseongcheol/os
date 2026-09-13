package keyboard

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "ระบบcall"

type IKeyboardeventhandler interface {
	Onkeyลง(key byte)
	Onkeyup(key byte)
}

var ikeyboardeventhandler IKeyboardeventhandler
var defaultkeyboardeventhandler TDefaultkeyboardeventhandler

type TDefaultkeyboardeventhandler struct {
}

func (self *TDefaultkeyboardeventhandler) Onkeyลง(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	console_2 := TConsole{}
	console_2.MPrint(buffer)

}
func (self *TDefaultkeyboardeventhandler) Onkeyup(key byte) {
}

type TKeyboarddriver struct {
	TInterrupthandler
}

var ทำงานkeyboarddriver *TKeyboarddriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var commandport_2 uint16 = 0x64

const ps2รอlimit = 100000

func รอps2inputempty() bool {
	for i := 0; i < ps2รอlimit; i++ {
		if (Portanbyte(commandport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func รอps2outputfull() bool {
	for i := 0; i < ps2รอlimit; i++ {
		if (Portanbyte(commandport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func khianps2command(value uint8) bool {
	if !รอps2inputempty() {
		return false
	}
	Portkhianbyte(commandport_2, value)
	return true
}

func khianps2data(value uint8) bool {
	if !รอps2inputempty() {
		return false
	}
	Portkhianbyte(dataport_2, value)
	return true
}

func anps2data() (uint8, bool) {
	if !รอps2outputfull() {
		return 0, false
	}
	return Portanbyte(dataport_2), true
}

func (self *TKeyboarddriver) Initdriver(manager *TInterruptmanager, keyboardeventhandler IKeyboardeventhandler) {

	ikeyboardeventhandler = &defaultkeyboardeventhandler
	if keyboardeventhandler != nil {
		ikeyboardeventhandler = keyboardeventhandler
	}

	ทำงานkeyboarddriver = self
	interrupthandler = handlekeyboardinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portanbyte(commandport_2)&0x01) != 0; i++ {
		Portanbyte(dataport_2)
	}

	if !khianps2command(0xAE) || !khianps2command(0x20) {
		return
	}
	สถานะ, ตกลง := anps2data()
	if !ตกลง {
		return
	}
	สถานะ |= 0x01
	สถานะ &^= 0x10
	if !khianps2command(0x60) || !khianps2data(สถานะ) {
		return
	}

	if !khianps2data(0xF4) {
		return
	}
	ack, ตกลง := anps2data()
	if !ตกลง || ack != 0xFA {
		return
	}

}

func handlekeyboardinterrupt(esp uint32) uint32 {
	if ทำงานkeyboarddriver == nil {
		Portanbyte(dataport_2)
		return esp
	}
	return ทำงานkeyboarddriver.Handleinterrupt(esp)
}

const keyboardqueueขนาด = 64

var keyboardqueue [keyboardqueueขนาด]byte
var keyboardqueuean uint8
var keyboardqueuekhian uint8
var leftshift bool
var ขวาshift bool
var extendedตรวจcode bool

func queuekeyboardbyte(key byte) {
	next := (keyboardqueuekhian + 1) % keyboardqueueขนาด
	if next == keyboardqueuean {
		return
	}
	keyboardqueue[keyboardqueuekhian] = key
	keyboardqueuekhian = next
}

func Pโพรเซสpendingkeyboardevents() {
	for keyboardqueuean != keyboardqueuekhian {
		key := keyboardqueue[keyboardqueuean]
		keyboardqueuean = (keyboardqueuean + 1) % keyboardqueueขนาด
		Stdinputbyte(key)
		if ikeyboardeventhandler != nil {
			ikeyboardeventhandler.Onkeyลง(key)
		}
	}
}

func ตรวจcodetobyte(ตรวจcode uint8) (byte, bool) {
	shift := leftshift || ขวาshift

	if ตรวจcode >= 0x02 && ตรวจcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[ตรวจcode-0x02], true
		}
		return "1234567890"[ตรวจcode-0x02], true
	}
	if ตรวจcode >= 0x10 && ตรวจcode <= 0x19 {
		key := "qwertyuiop"[ตรวจcode-0x10]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if ตรวจcode >= 0x1E && ตรวจcode <= 0x26 {
		key := "asdfghjkl"[ตรวจcode-0x1E]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if ตรวจcode >= 0x2C && ตรวจcode <= 0x32 {
		key := "zxcvbnm"[ตรวจcode-0x2C]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch ตรวจcode {
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

func (self *TKeyboarddriver) Handleinterrupt(esp uint32) uint32 {
	สถานะ := Portanbyte(commandport_2)
	if (สถานะ&0x01) == 0 || (สถานะ&0x20) != 0 {
		return esp
	}

	ตรวจcode := Portanbyte(dataport_2)
	if ตรวจcode == 0xE0 {
		extendedตรวจcode = true
		return esp
	}
	if extendedตรวจcode {
		extendedตรวจcode = false
		return esp
	}

	released := (ตรวจcode & 0x80) != 0
	basecode := ตรวจcode & 0x7F
	if basecode == 0x2A {
		leftshift = !released
		return esp
	}
	if basecode == 0x36 {
		ขวาshift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ตกลง := ตรวจcodetobyte(basecode); ตกลง {
		queuekeyboardbyte(key)
	}

	return esp
}
