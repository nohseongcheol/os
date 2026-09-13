package lyklaborð

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "kerfiscall"

type ILyklaborðeventhandler interface {
	NotakeyNiður(key byte)
	NotakeyUpp(key byte)
}

var iLyklaborðeventhandler ILyklaborðeventhandler
var sjálfgefiðLyklaborðeventhandler TSjálfgefiðLyklaborðeventhandler

type TSjálfgefiðLyklaborðeventhandler struct {
}

func (sjálft *TSjálfgefiðLyklaborðeventhandler) NotakeyNiður(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	console_2 := TConsole{}
	console_2.MPrenta(buffer)

}
func (sjálft *TSjálfgefiðLyklaborðeventhandler) NotakeyUpp(key byte) {
}

type TLyklaborðdriver struct {
	TInterrupthandler
}

var virktLyklaborðdriver *TLyklaborðdriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var skipunport_2 uint16 = 0x64

const ps2Bíðalimit = 100000

func bíðaps2InntakTómt() bool {
	for i := 0; i < ps2Bíðalimit; i++ {
		if (PortLesturbyte(skipunport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func bíðaps2outputMikið() bool {
	for i := 0; i < ps2Bíðalimit; i++ {
		if (PortLesturbyte(skipunport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skriftps2Skipun(gildi uint8) bool {
	if !bíðaps2InntakTómt() {
		return false
	}
	PortSkriftbyte(skipunport_2, gildi)
	return true
}

func skriftps2data(gildi uint8) bool {
	if !bíðaps2InntakTómt() {
		return false
	}
	PortSkriftbyte(dataport_2, gildi)
	return true
}

func lesturps2data() (uint8, bool) {
	if !bíðaps2outputMikið() {
		return 0, false
	}
	return PortLesturbyte(dataport_2), true
}

func (sjálft *TLyklaborðdriver) Initdriver(manager *TInterruptmanager, lyklaborðeventhandler ILyklaborðeventhandler) {

	iLyklaborðeventhandler = &sjálfgefiðLyklaborðeventhandler
	if lyklaborðeventhandler != nil {
		iLyklaborðeventhandler = lyklaborðeventhandler
	}

	virktLyklaborðdriver = sjálft
	interrupthandler = haldfangLyklaborðinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	sjálft.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLesturbyte(skipunport_2)&0x01) != 0; i++ {
		PortLesturbyte(dataport_2)
	}

	if !skriftps2Skipun(0xAE) || !skriftps2Skipun(0x20) {
		return
	}
	staða_3, ílagi := lesturps2data()
	if !ílagi {
		return
	}
	staða_3 |= 0x01
	staða_3 &^= 0x10
	if !skriftps2Skipun(0x60) || !skriftps2data(staða_3) {
		return
	}

	if !skriftps2data(0xF4) {
		return
	}
	ack, ílagi := lesturps2data()
	if !ílagi || ack != 0xFA {
		return
	}

}

func haldfangLyklaborðinterrupt(esp uint32) uint32 {
	if virktLyklaborðdriver == nil {
		PortLesturbyte(dataport_2)
		return esp
	}
	return virktLyklaborðdriver.Haldfanginterrupt(esp)
}

const lyklaborðqueueStærð = 64

var lyklaborðqueue [lyklaborðqueueStærð]byte
var lyklaborðqueueLestur uint8
var lyklaborðqueueSkrift uint8
var vinstriShiftlykill bool
var hægriShiftlykill bool
var extendedscancode bool

func queueLyklaborðbyte(key byte) {
	næsta := (lyklaborðqueueSkrift + 1) % lyklaborðqueueStærð
	if næsta == lyklaborðqueueLestur {
		return
	}
	lyklaborðqueue[lyklaborðqueueSkrift] = key
	lyklaborðqueueSkrift = næsta
}

func ProcesspendingLyklaborðevents() {
	for lyklaborðqueueLestur != lyklaborðqueueSkrift {
		key := lyklaborðqueue[lyklaborðqueueLestur]
		lyklaborðqueueLestur = (lyklaborðqueueLestur + 1) % lyklaborðqueueStærð
		Stdinputbyte(key)
		if iLyklaborðeventhandler != nil {
			iLyklaborðeventhandler.NotakeyNiður(key)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shiftlykill := vinstriShiftlykill || hægriShiftlykill

	if scancode >= 0x02 && scancode <= 0x0B {
		if shiftlykill {
			return "!@#$%^&*()"[scancode-0x02], true
		}
		return "1234567890"[scancode-0x02], true
	}
	if scancode >= 0x10 && scancode <= 0x19 {
		key := "qwertyuiop"[scancode-0x10]
		if shiftlykill {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scancode >= 0x1E && scancode <= 0x26 {
		key := "asdfghjkl"[scancode-0x1E]
		if shiftlykill {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scancode >= 0x2C && scancode <= 0x32 {
		key := "zxcvbnm"[scancode-0x2C]
		if shiftlykill {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch scancode {
	case 0x0C:
		if shiftlykill {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shiftlykill {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shiftlykill {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shiftlykill {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shiftlykill {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shiftlykill {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shiftlykill {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shiftlykill {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shiftlykill {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shiftlykill {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shiftlykill {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (sjálft *TLyklaborðdriver) Haldfanginterrupt(esp uint32) uint32 {
	staða_3 := PortLesturbyte(skipunport_2)
	if (staða_3&0x01) == 0 || (staða_3&0x20) != 0 {
		return esp
	}

	scancode := PortLesturbyte(dataport_2)
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
		vinstriShiftlykill = !released
		return esp
	}
	if basecode == 0x36 {
		hægriShiftlykill = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ílagi := scancodetobyte(basecode); ílagi {
		queueLyklaborðbyte(key)
	}

	return esp
}
