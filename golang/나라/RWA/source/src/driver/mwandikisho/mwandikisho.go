/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package mwandikisho

import . "unsafe"

import . "umuyoboro"
import . "interrupt"

import . "console"
import . "systemcall"

type IMwandikishoeventhandler interface {
	Kurikeydown(key byte)
	Kurikeyup(key byte)
}

var iMwandikishoeventhandler IMwandikishoeventhandler
var mburabuziMwandikishoeventhandler TMburabuziMwandikishoeventhandler

type TMburabuziMwandikishoeventhandler struct {
}

func (self *TMburabuziMwandikishoeventhandler) Kurikeydown(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	console_2 := TConsole{}
	console_2.MGucapa(buffer)

}
func (self *TMburabuziMwandikishoeventhandler) Kurikeyup(key byte) {
}

type TMwandikishodriver struct {
	TInterrupthandler
}

var gikoraMwandikishodriver *TMwandikishodriver
var interrupthandler func(uint32) uint32

var dataUmuyoboro_2 uint16 = 0x60
var icyowifuzaUmuyoboro_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Umuyoborogusomabyte(icyowifuzaUmuyoboro_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputfull() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Umuyoborogusomabyte(icyowifuzaUmuyoboro_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func kwandikaps2Icyowifuza(agaciro uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Umuyoborokwandikabyte(icyowifuzaUmuyoboro_2, agaciro)
	return true
}

func kwandikaps2data(agaciro uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Umuyoborokwandikabyte(dataUmuyoboro_2, agaciro)
	return true
}

func gusomaps2data() (uint8, bool) {
	if !waitps2outputfull() {
		return 0, false
	}
	return Umuyoborogusomabyte(dataUmuyoboro_2), true
}

func (self *TMwandikishodriver) Initdriver(manager *TInterruptmanager, mwandikishoeventhandler IMwandikishoeventhandler) {

	iMwandikishoeventhandler = &mburabuziMwandikishoeventhandler
	if mwandikishoeventhandler != nil {
		iMwandikishoeventhandler = mwandikishoeventhandler
	}

	gikoraMwandikishodriver = self
	interrupthandler = handleMwandikishointerrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Umuyoborogusomabyte(icyowifuzaUmuyoboro_2)&0x01) != 0; i++ {
		Umuyoborogusomabyte(dataUmuyoboro_2)
	}

	if !kwandikaps2Icyowifuza(0xAE) || !kwandikaps2Icyowifuza(0x20) {
		return
	}
	imimerere, yEGO := gusomaps2data()
	if !yEGO {
		return
	}
	imimerere |= 0x01
	imimerere &^= 0x10
	if !kwandikaps2Icyowifuza(0x60) || !kwandikaps2data(imimerere) {
		return
	}

	if !kwandikaps2data(0xF4) {
		return
	}
	ack, yEGO := gusomaps2data()
	if !yEGO || ack != 0xFA {
		return
	}

}

func handleMwandikishointerrupt(esp uint32) uint32 {
	if gikoraMwandikishodriver == nil {
		Umuyoborogusomabyte(dataUmuyoboro_2)
		return esp
	}
	return gikoraMwandikishodriver.Handleinterrupt(esp)
}

const mwandikishoqueueIngano = 64

var mwandikishoqueue [mwandikishoqueueIngano]byte
var mwandikishoqueuegusoma uint8
var mwandikishoqueuekwandika uint8
var ibumosoGusunika bool
var iburyoGusunika bool
var extendedscancode bool

func queueMwandikishobyte(key byte) {
	ikurikira := (mwandikishoqueuekwandika + 1) % mwandikishoqueueIngano
	if ikurikira == mwandikishoqueuegusoma {
		return
	}
	mwandikishoqueue[mwandikishoqueuekwandika] = key
	mwandikishoqueuekwandika = ikurikira
}

func ProcesspendingMwandikishoevents() {
	for mwandikishoqueuegusoma != mwandikishoqueuekwandika {
		key := mwandikishoqueue[mwandikishoqueuegusoma]
		mwandikishoqueuegusoma = (mwandikishoqueuegusoma + 1) % mwandikishoqueueIngano
		Stdinputbyte(key)
		if iMwandikishoeventhandler != nil {
			iMwandikishoeventhandler.Kurikeydown(key)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	gusunika := ibumosoGusunika || iburyoGusunika

	if scancode >= 0x02 && scancode <= 0x0B {
		if gusunika {
			return "!@#$%^&*()"[scancode-0x02], true
		}
		return "1234567890"[scancode-0x02], true
	}
	if scancode >= 0x10 && scancode <= 0x19 {
		key := "qwertyuiop"[scancode-0x10]
		if gusunika {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scancode >= 0x1E && scancode <= 0x26 {
		key := "asdfghjkl"[scancode-0x1E]
		if gusunika {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if scancode >= 0x2C && scancode <= 0x32 {
		key := "zxcvbnm"[scancode-0x2C]
		if gusunika {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch scancode {
	case 0x0C:
		if gusunika {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if gusunika {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if gusunika {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if gusunika {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if gusunika {
			return ':', true
		}
		return ';', true
	case 0x28:
		if gusunika {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if gusunika {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if gusunika {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if gusunika {
			return '<', true
		}
		return ',', true
	case 0x34:
		if gusunika {
			return '>', true
		}
		return '.', true
	case 0x35:
		if gusunika {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (self *TMwandikishodriver) Handleinterrupt(esp uint32) uint32 {
	imimerere := Umuyoborogusomabyte(icyowifuzaUmuyoboro_2)
	if (imimerere&0x01) == 0 || (imimerere&0x20) != 0 {
		return esp
	}

	scancode := Umuyoborogusomabyte(dataUmuyoboro_2)
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
		ibumosoGusunika = !released
		return esp
	}
	if basecode == 0x36 {
		iburyoGusunika = !released
		return esp
	}
	if released {
		return esp
	}

	if key, yEGO := scancodetobyte(basecode); yEGO {
		queueMwandikishobyte(key)
	}

	return esp
}
