/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package гар

import . "unsafe"

import . "порт"
import . "interrupt"

import . "консол"
import . "системcall"

type IГарeventhandler interface {
	Onkeydown(key byte)
	OnkeyДээш(key byte)
}

var iГарeventhandler IГарeventhandler
var стандартГарeventhandler TСтандартГарeventhandler

type TСтандартГарeventhandler struct {
}

func (self *TСтандартГарeventhandler) Onkeydown(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	консол_2 := TКонсол{}
	консол_2.MХэвлэх(buffer)

}
func (self *TСтандартГарeventhandler) OnkeyДээш(key byte) {
}

type TГарdriver struct {
	TInterrupthandler
}

var идэвхтэйГарdriver *TГарdriver
var interrupthandler func(uint32) uint32

var dataПорт_2 uint16 = 0x60
var тушаалПорт_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (ПортУншихbyte(тушаалПорт_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputДүүрэн() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (ПортУншихbyte(тушаалПорт_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func бичихps2Тушаал(утга uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	ПортБичихbyte(тушаалПорт_2, утга)
	return true
}

func бичихps2data(утга uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	ПортБичихbyte(dataПорт_2, утга)
	return true
}

func уншихps2data() (uint8, bool) {
	if !waitps2outputДүүрэн() {
		return 0, false
	}
	return ПортУншихbyte(dataПорт_2), true
}

func (self *TГарdriver) Initdriver(зохицуулагч *TInterruptЗохицуулагч, гарeventhandler IГарeventhandler) {

	iГарeventhandler = &стандартГарeventhandler
	if гарeventhandler != nil {
		iГарeventhandler = гарeventhandler
	}

	идэвхтэйГарdriver = self
	interrupthandler = handleГарinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(зохицуулагч)), address)

	for i := 0; i < 32 && (ПортУншихbyte(тушаалПорт_2)&0x01) != 0; i++ {
		ПортУншихbyte(dataПорт_2)
	}

	if !бичихps2Тушаал(0xAE) || !бичихps2Тушаал(0x20) {
		return
	}
	төлөв, ok := уншихps2data()
	if !ok {
		return
	}
	төлөв |= 0x01
	төлөв &^= 0x10
	if !бичихps2Тушаал(0x60) || !бичихps2data(төлөв) {
		return
	}

	if !бичихps2data(0xF4) {
		return
	}
	ack, ok := уншихps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleГарinterrupt(esp uint32) uint32 {
	if идэвхтэйГарdriver == nil {
		ПортУншихbyte(dataПорт_2)
		return esp
	}
	return идэвхтэйГарdriver.Handleinterrupt(esp)
}

const гарqueueХэмжээ = 64

var гарqueue [гарqueueХэмжээ]byte
var гарqueueУнших uint8
var гарqueueБичих uint8
var зүүнshift bool
var баруунshift bool
var extendedscancode bool

func queueГарbyte(key byte) {
	дараах := (гарqueueБичих + 1) % гарqueueХэмжээ
	if дараах == гарqueueУнших {
		return
	}
	гарqueue[гарqueueБичих] = key
	гарqueueБичих = дараах
}

func ProcesspendingГарevents() {
	for гарqueueУнших != гарqueueБичих {
		key := гарqueue[гарqueueУнших]
		гарqueueУнших = (гарqueueУнших + 1) % гарqueueХэмжээ
		Stdinputbyte(key)
		if iГарeventhandler != nil {
			iГарeventhandler.Onkeydown(key)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shift := зүүнshift || баруунshift

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

func (self *TГарdriver) Handleinterrupt(esp uint32) uint32 {
	төлөв := ПортУншихbyte(тушаалПорт_2)
	if (төлөв&0x01) == 0 || (төлөв&0x20) != 0 {
		return esp
	}

	scancode := ПортУншихbyte(dataПорт_2)
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
		зүүнshift = !released
		return esp
	}
	if basecode == 0x36 {
		баруунshift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ok := scancodetobyte(basecode); ok {
		queueГарbyte(key)
	}

	return esp
}
