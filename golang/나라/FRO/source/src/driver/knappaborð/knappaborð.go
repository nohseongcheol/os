/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package knappaborð

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "systemcall"

type IKnappaborðeventhandler interface {
	Onkeydown(key byte)
	Onkeyup(key byte)
}

var iKnappaborðeventhandler IKnappaborðeventhandler
var forsettKnappaborðeventhandler TForsettKnappaborðeventhandler

type TForsettKnappaborðeventhandler struct {
}

func (self *TForsettKnappaborðeventhandler) Onkeydown(key byte) {
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
func (self *TForsettKnappaborðeventhandler) Onkeyup(key byte) {
}

type TKnappaborðdriver struct {
	TInterrupthandler
}

var activeKnappaborðdriver *TKnappaborðdriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var stýriboðport_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portlesabyte(stýriboðport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputfull() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Portlesabyte(stýriboðport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skrivaps2Stýriboð(value uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Portskrivabyte(stýriboðport_2, value)
	return true
}

func skrivaps2data(value uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Portskrivabyte(dataport_2, value)
	return true
}

func lesaps2data() (uint8, bool) {
	if !waitps2outputfull() {
		return 0, false
	}
	return Portlesabyte(dataport_2), true
}

func (self *TKnappaborðdriver) Initdriver(manager *TInterruptmanager, knappaborðeventhandler IKnappaborðeventhandler) {

	iKnappaborðeventhandler = &forsettKnappaborðeventhandler
	if knappaborðeventhandler != nil {
		iKnappaborðeventhandler = knappaborðeventhandler
	}

	activeKnappaborðdriver = self
	interrupthandler = handleKnappaborðinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portlesabyte(stýriboðport_2)&0x01) != 0; i++ {
		Portlesabyte(dataport_2)
	}

	if !skrivaps2Stýriboð(0xAE) || !skrivaps2Stýriboð(0x20) {
		return
	}
	status, ok := lesaps2data()
	if !ok {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !skrivaps2Stýriboð(0x60) || !skrivaps2data(status) {
		return
	}

	if !skrivaps2data(0xF4) {
		return
	}
	ack, ok := lesaps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleKnappaborðinterrupt(esp uint32) uint32 {
	if activeKnappaborðdriver == nil {
		Portlesabyte(dataport_2)
		return esp
	}
	return activeKnappaborðdriver.Handleinterrupt(esp)
}

const knappaborðqueueStødd = 64

var knappaborðqueue [knappaborðqueueStødd]byte
var knappaborðqueuelesa uint8
var knappaborðqueueskriva uint8
var vinstrushift bool
var høgrushift bool
var extendedscancode bool

func queueKnappaborðbyte(key byte) {
	næsta := (knappaborðqueueskriva + 1) % knappaborðqueueStødd
	if næsta == knappaborðqueuelesa {
		return
	}
	knappaborðqueue[knappaborðqueueskriva] = key
	knappaborðqueueskriva = næsta
}

func ProcesspendingKnappaborðevents() {
	for knappaborðqueuelesa != knappaborðqueueskriva {
		key := knappaborðqueue[knappaborðqueuelesa]
		knappaborðqueuelesa = (knappaborðqueuelesa + 1) % knappaborðqueueStødd
		Stdinputbyte(key)
		if iKnappaborðeventhandler != nil {
			iKnappaborðeventhandler.Onkeydown(key)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shift := vinstrushift || høgrushift

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

func (self *TKnappaborðdriver) Handleinterrupt(esp uint32) uint32 {
	status := Portlesabyte(stýriboðport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	scancode := Portlesabyte(dataport_2)
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
		vinstrushift = !released
		return esp
	}
	if basecode == 0x36 {
		høgrushift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ok := scancodetobyte(basecode); ok {
		queueKnappaborðbyte(key)
	}

	return esp
}
