package keyboard

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "systemcall"

type IKeyboardeventhandler interface {
	Onkeydown(key byte)
	Onkeyup(key byte)
}

var ikeyboardeventhandler IKeyboardeventhandler
var defaultkeyboardeventhandler TDefaultkeyboardeventhandler

type TDefaultkeyboardeventhandler struct {
}

func (self *TDefaultkeyboardeventhandler) Onkeydown(key byte) {
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

var activekeyboarddriver *TKeyboarddriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var commandport_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portfaitaubyte(commandport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputfull() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portfaitaubyte(commandport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func tusitusips2command(value uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Porttusitusibyte(commandport_2, value)
	return true
}

func tusitusips2data(value uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Porttusitusibyte(dataport_2, value)
	return true
}

func faitaups2data() (uint8, bool) {
	if !waitps2outputfull() {
		return 0, false
	}
	return Portfaitaubyte(dataport_2), true
}

func (self *TKeyboarddriver) Initdriver(manager *TInterruptmanager, keyboardeventhandler IKeyboardeventhandler) {

	ikeyboardeventhandler = &defaultkeyboardeventhandler
	if keyboardeventhandler != nil {
		ikeyboardeventhandler = keyboardeventhandler
	}

	activekeyboarddriver = self
	interrupthandler = handlekeyboardinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portfaitaubyte(commandport_2)&0x01) != 0; i++ {
		Portfaitaubyte(dataport_2)
	}

	if !tusitusips2command(0xAE) || !tusitusips2command(0x20) {
		return
	}
	status, ok := faitaups2data()
	if !ok {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !tusitusips2command(0x60) || !tusitusips2data(status) {
		return
	}

	if !tusitusips2data(0xF4) {
		return
	}
	ack, ok := faitaups2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handlekeyboardinterrupt(esp uint32) uint32 {
	if activekeyboarddriver == nil {
		Portfaitaubyte(dataport_2)
		return esp
	}
	return activekeyboarddriver.Handleinterrupt(esp)
}

const keyboardqueuesize = 64

var keyboardqueue [keyboardqueuesize]byte
var keyboardqueuefaitau uint8
var keyboardqueuetusitusi uint8
var leftshift bool
var rightshift bool
var extendedscancode bool

func queuekeyboardbyte(key byte) {
	next := (keyboardqueuetusitusi + 1) % keyboardqueuesize
	if next == keyboardqueuefaitau {
		return
	}
	keyboardqueue[keyboardqueuetusitusi] = key
	keyboardqueuetusitusi = next
}

func Processpendingkeyboardevents() {
	for keyboardqueuefaitau != keyboardqueuetusitusi {
		key := keyboardqueue[keyboardqueuefaitau]
		keyboardqueuefaitau = (keyboardqueuefaitau + 1) % keyboardqueuesize
		Stdinputbyte(key)
		if ikeyboardeventhandler != nil {
			ikeyboardeventhandler.Onkeydown(key)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shift := leftshift || rightshift

	if scancode >= 0x02 && scancode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[scancode-0x02], true
		}
		return "1234567890"[scancode-0x02], true
	}
	if scancode >= 0x10 && scancode <= 0x19 {
		key := "qwertyuiop"[scancode-0x10]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scancode >= 0x1E && scancode <= 0x26 {
		key := "asdfghjkl"[scancode-0x1E]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scancode >= 0x2C && scancode <= 0x32 {
		key := "zxcvbnm"[scancode-0x2C]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch scancode {
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
	status := Portfaitaubyte(commandport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	scancode := Portfaitaubyte(dataport_2)
	if scancode == 0xE0 {
		extendedscancode = true
		return esp
	}
	if extendedscancode {
		extendedscancode = false
		return esp
	}

	released := (scancode & 0x80) != 0
	basecode := scancode & 0x7F
	if basecode == 0x2A {
		leftshift = !released
		return esp
	}
	if basecode == 0x36 {
		rightshift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ok := scancodetobyte(basecode); ok {
		queuekeyboardbyte(key)
	}

	return esp
}
