package keyboard

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "نظامی_طلب"

type IKeyboardEventHandler interface {
	OnKeyDown(key byte)
	OnKeyUp(key byte)
}

var iKeyboardEventHandler IKeyboardEventHandler
var defaultKeyboardEventHandler TDefaultKeyboardEventHandler

type TDefaultKeyboardEventHandler struct {
}

func (self *TDefaultKeyboardEventHandler) OnKeyDown(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buf := []byte("\n\n\n\n\n\nkeyboard :    ")

	buf[17] = hex[((key >> 4) & 0xF)]
	buf[18] = hex[key&0xF]

	콘솔 := T콘솔{}
	콘솔.M출력(buf)

}
func (self *TDefaultKeyboardEventHandler) OnKeyUp(key byte) {
}

type TKeyboardDriver struct {
	TInterruptHandler
}

var activeKeyboardDriver *TKeyboardDriver
var interruptHandler func(uint32) uint32

var dataport uint16 = 0x60
var commandport uint16 = 0x64

const ps2WaitLimit = 100000

func waitPS2InputEmpty() bool {
	for i := 0; i < ps2WaitLimit; i++ {
		if (PortReadByte(commandport) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitPS2OutputFull() bool {
	for i := 0; i < ps2WaitLimit; i++ {
		if (PortReadByte(commandport) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func writePS2Command(value uint8) bool {
	if !waitPS2InputEmpty() {
		return false
	}
	PortWriteByte(commandport, value)
	return true
}

func writePS2Data(value uint8) bool {
	if !waitPS2InputEmpty() {
		return false
	}
	PortWriteByte(dataport, value)
	return true
}

func readPS2Data() (uint8, bool) {
	if !waitPS2OutputFull() {
		return 0, false
	}
	return PortReadByte(dataport), true
}

func (self *TKeyboardDriver) InitDriver(manager *TInterruptManager, keyboardEventHandler IKeyboardEventHandler) {

	iKeyboardEventHandler = &defaultKeyboardEventHandler
	if keyboardEventHandler != nil {
		iKeyboardEventHandler = keyboardEventHandler
	}

	activeKeyboardDriver = self
	interruptHandler = handleKeyboardInterrupt
	var addr uintptr
	addr = uintptr(Pointer(&interruptHandler))

	self.Vآغاز_کرنا(0x21, uintptr(Pointer(manager)), addr)

	for i := 0; i < 32 && (PortReadByte(commandport)&0x01) != 0; i++ {
		PortReadByte(dataport)
	}

	if !writePS2Command(0xAE) || !writePS2Command(0x20) {
		return
	}
	status, ok := readPS2Data()
	if !ok {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !writePS2Command(0x60) || !writePS2Data(status) {
		return
	}

	if !writePS2Data(0xF4) {
		return
	}
	ack, ok := readPS2Data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleKeyboardInterrupt(esp uint32) uint32 {
	if activeKeyboardDriver == nil {
		PortReadByte(dataport)
		return esp
	}
	return activeKeyboardDriver.HandleInterrupt(esp)
}

const keyboardQueueSize = 64

var keyboardQueue [keyboardQueueSize]byte
var keyboardQueueRead uint8
var keyboardQueueWrite uint8
var leftShift bool
var rightShift bool
var extendedScanCode bool

func queueKeyboardByte(key byte) {
	next := (keyboardQueueWrite + 1) % keyboardQueueSize
	if next == keyboardQueueRead {
		return
	}
	keyboardQueue[keyboardQueueWrite] = key
	keyboardQueueWrite = next
}

func ProcessPendingKeyboardEvents() {
	for keyboardQueueRead != keyboardQueueWrite {
		key := keyboardQueue[keyboardQueueRead]
		keyboardQueueRead = (keyboardQueueRead + 1) % keyboardQueueSize
		StdinPutByte(key)
		if iKeyboardEventHandler != nil {
			iKeyboardEventHandler.OnKeyDown(key)
		}
	}
}

func scanCodeToByte(scanCode uint8) (byte, bool) {
	shift := leftShift || rightShift

	if scanCode >= 0x02 && scanCode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[scanCode-0x02], true
		}
		return "1234567890"[scanCode-0x02], true
	}
	if scanCode >= 0x10 && scanCode <= 0x19 {
		key := "qwertyuiop"[scanCode-0x10]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scanCode >= 0x1E && scanCode <= 0x26 {
		key := "asdfghjkl"[scanCode-0x1E]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scanCode >= 0x2C && scanCode <= 0x32 {
		key := "zxcvbnm"[scanCode-0x2C]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch scanCode {
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

func (self *TKeyboardDriver) HandleInterrupt(esp uint32) uint32 {
	status := PortReadByte(commandport)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	scanCode := PortReadByte(dataport)
	if scanCode == 0xE0 {
		extendedScanCode = true
		return esp
	}
	if extendedScanCode {
		extendedScanCode = false
		return esp
	}

	released := (scanCode & 0x80) != 0
	baseCode := scanCode & 0x7F
	if baseCode == 0x2A {
		leftShift = !released
		return esp
	}
	if baseCode == 0x36 {
		rightShift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ok := scanCodeToByte(baseCode); ok {
		queueKeyboardByte(key)
	}

	return esp
}
