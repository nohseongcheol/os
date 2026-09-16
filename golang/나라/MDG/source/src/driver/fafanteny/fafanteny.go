/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fafanteny

import . "unsafe"

import . "irika"
import . "interrupt"

import . "konsoly"
import . "rafitracall"

type IFafantenyeventhandler interface {
	Onkeydown(key byte)
	OnkeyAmbony(key byte)
}

var iFafantenyeventhandler IFafantenyeventhandler
var tsotraFafantenyeventhandler TTsotraFafantenyeventhandler

type TTsotraFafantenyeventhandler struct {
}

func (nytena *TTsotraFafantenyeventhandler) Onkeydown(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	konsoly_2 := TKonsoly{}
	konsoly_2.MAtontay(buffer)

}
func (nytena *TTsotraFafantenyeventhandler) OnkeyAmbony(key byte) {
}

type TFafantenydriver struct {
	TInterrupthandler
}

var miasaFafantenydriver *TFafantenydriver
var interrupthandler func(uint32) uint32

var dataIrika_2 uint16 = 0x60
var baikoIrika_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputFoana() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (IrikaMamakybyte(baikoIrika_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputFeno() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (IrikaMamakybyte(baikoIrika_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func manoratraps2Baiko(sanda uint8) bool {
	if !waitps2inputFoana() {
		return false
	}
	IrikaManoratrabyte(baikoIrika_2, sanda)
	return true
}

func manoratraps2data(sanda uint8) bool {
	if !waitps2inputFoana() {
		return false
	}
	IrikaManoratrabyte(dataIrika_2, sanda)
	return true
}

func mamakyps2data() (uint8, bool) {
	if !waitps2outputFeno() {
		return 0, false
	}
	return IrikaMamakybyte(dataIrika_2), true
}

func (nytena *TFafantenydriver) Initdriver(mpandrindra *TInterruptMpandrindra, fafantenyeventhandler IFafantenyeventhandler) {

	iFafantenyeventhandler = &tsotraFafantenyeventhandler
	if fafantenyeventhandler != nil {
		iFafantenyeventhandler = fafantenyeventhandler
	}

	miasaFafantenydriver = nytena
	interrupthandler = handleFafantenyinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	nytena.Init(0x21, uintptr(Pointer(mpandrindra)), address)

	for i := 0; i < 32 && (IrikaMamakybyte(baikoIrika_2)&0x01) != 0; i++ {
		IrikaMamakybyte(dataIrika_2)
	}

	if !manoratraps2Baiko(0xAE) || !manoratraps2Baiko(0x20) {
		return
	}
	fivoarana, ok := mamakyps2data()
	if !ok {
		return
	}
	fivoarana |= 0x01
	fivoarana &^= 0x10
	if !manoratraps2Baiko(0x60) || !manoratraps2data(fivoarana) {
		return
	}

	if !manoratraps2data(0xF4) {
		return
	}
	ack, ok := mamakyps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleFafantenyinterrupt(esp uint32) uint32 {
	if miasaFafantenydriver == nil {
		IrikaMamakybyte(dataIrika_2)
		return esp
	}
	return miasaFafantenydriver.Handleinterrupt(esp)
}

const fafantenyqueueHabe = 64

var fafantenyqueue [fafantenyqueueHabe]byte
var fafantenyqueueMamaky uint8
var fafantenyqueueManoratra uint8
var haviashift bool
var havananashift bool
var extendedZahavocode bool

func queueFafantenybyte(key byte) {
	manaraka := (fafantenyqueueManoratra + 1) % fafantenyqueueHabe
	if manaraka == fafantenyqueueMamaky {
		return
	}
	fafantenyqueue[fafantenyqueueManoratra] = key
	fafantenyqueueManoratra = manaraka
}

func ProcesspendingFafantenyevents() {
	for fafantenyqueueMamaky != fafantenyqueueManoratra {
		key := fafantenyqueue[fafantenyqueueMamaky]
		fafantenyqueueMamaky = (fafantenyqueueMamaky + 1) % fafantenyqueueHabe
		Stdinputbyte(key)
		if iFafantenyeventhandler != nil {
			iFafantenyeventhandler.Onkeydown(key)
		}
	}
}

func zahavocodetobyte(zahavocode uint8) (byte, bool) {
	shift := haviashift || havananashift

	if zahavocode >= 0x02 && zahavocode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[zahavocode-0x02], true
		}
		return "1234567890"[zahavocode-0x02], true
	}
	if zahavocode >= 0x10 && zahavocode <= 0x19 {
		key := "qwertyuiop"[zahavocode-0x10]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if zahavocode >= 0x1E && zahavocode <= 0x26 {
		key := "asdfghjkl"[zahavocode-0x1E]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if zahavocode >= 0x2C && zahavocode <= 0x32 {
		key := "zxcvbnm"[zahavocode-0x2C]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch zahavocode {
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

func (nytena *TFafantenydriver) Handleinterrupt(esp uint32) uint32 {
	fivoarana := IrikaMamakybyte(baikoIrika_2)
	if (fivoarana&0x01) == 0 || (fivoarana&0x20) != 0 {
		return esp
	}

	zahavocode := IrikaMamakybyte(dataIrika_2)
	if zahavocode == 0xE0 {
		extendedZahavocode = true
		return esp
	}
	if extendedZahavocode {
		extendedZahavocode = false
		return esp
	}

	released := (zahavocode & 0x80) != 0
	basecode := zahavocode & 0x7F
	if basecode == 0x2A {
		haviashift = !released
		return esp
	}
	if basecode == 0x36 {
		havananashift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ok := zahavocodetobyte(basecode); ok {
		queueFafantenybyte(key)
	}

	return esp
}
