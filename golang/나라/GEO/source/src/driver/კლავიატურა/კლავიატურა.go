package კლავიატურა

import . "unsafe"

import . "პორტი"
import . "interrupt"

import . "console"
import . "სისტემაcall"

type Iკლავიატურაeventhandler interface {
	Onkeydown(key byte)
	Onkeyზემოთ(key byte)
}

var iკლავიატურაeventhandler Iკლავიატურაeventhandler
var ნაგულისხმევიკლავიატურაeventhandler Tნაგულისხმევიკლავიატურაeventhandler

type Tნაგულისხმევიკლავიატურაeventhandler struct {
}

func (self *Tნაგულისხმევიკლავიატურაeventhandler) Onkeydown(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	console_2 := TConsole{}
	console_2.Mბეჭდვა(buffer)

}
func (self *Tნაგულისხმევიკლავიატურაeventhandler) Onkeyზემოთ(key byte) {
}

type Tკლავიატურაdriver struct {
	TInterrupthandler
}

var აქტიურიკლავიატურაdriver *Tკლავიატურაdriver
var interrupthandler func(uint32) uint32

var dataპორტი_2 uint16 = 0x60
var ბრძანებაპორტი_2 uint16 = 0x64

const ps2ლოდინიlimit = 100000

func ლოდინიps2inputცარიელი() bool {
	for i := 0; i < ps2ლოდინიlimit; i++ {
		if (Pპორტიკითხვაbyte(ბრძანებაპორტი_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ლოდინიps2outputსრული() bool {
	for i := 0; i < ps2ლოდინიlimit; i++ {
		if (Pპორტიკითხვაbyte(ბრძანებაპორტი_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func ჩაწერაps2ბრძანება(მნიშვნელობა uint8) bool {
	if !ლოდინიps2inputცარიელი() {
		return false
	}
	Pპორტიჩაწერაbyte(ბრძანებაპორტი_2, მნიშვნელობა)
	return true
}

func ჩაწერაps2data(მნიშვნელობა uint8) bool {
	if !ლოდინიps2inputცარიელი() {
		return false
	}
	Pპორტიჩაწერაbyte(dataპორტი_2, მნიშვნელობა)
	return true
}

func კითხვაps2data() (uint8, bool) {
	if !ლოდინიps2outputსრული() {
		return 0, false
	}
	return Pპორტიკითხვაbyte(dataპორტი_2), true
}

func (self *Tკლავიატურაdriver) Initdriver(manager *TInterruptmanager, კლავიატურაeventhandler Iკლავიატურაeventhandler) {

	iკლავიატურაeventhandler = &ნაგულისხმევიკლავიატურაeventhandler
	if კლავიატურაeventhandler != nil {
		iკლავიატურაeventhandler = კლავიატურაeventhandler
	}

	აქტიურიკლავიატურაdriver = self
	interrupthandler = handleკლავიატურაinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pპორტიკითხვაbyte(ბრძანებაპორტი_2)&0x01) != 0; i++ {
		Pპორტიკითხვაbyte(dataპორტი_2)
	}

	if !ჩაწერაps2ბრძანება(0xAE) || !ჩაწერაps2ბრძანება(0x20) {
		return
	}
	სტატუსი, ok := კითხვაps2data()
	if !ok {
		return
	}
	სტატუსი |= 0x01
	სტატუსი &^= 0x10
	if !ჩაწერაps2ბრძანება(0x60) || !ჩაწერაps2data(სტატუსი) {
		return
	}

	if !ჩაწერაps2data(0xF4) {
		return
	}
	ack, ok := კითხვაps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleკლავიატურაinterrupt(esp uint32) uint32 {
	if აქტიურიკლავიატურაdriver == nil {
		Pპორტიკითხვაbyte(dataპორტი_2)
		return esp
	}
	return აქტიურიკლავიატურაdriver.Handleinterrupt(esp)
}

const კლავიატურაqueueზომა = 64

var კლავიატურაqueue [კლავიატურაqueueზომა]byte
var კლავიატურაqueueკითხვა uint8
var კლავიატურაqueueჩაწერა uint8
var მარცხნივshift bool
var მარჯვნივshift bool
var extendedscancode bool

func queueკლავიატურაbyte(key byte) {
	შემდეგი := (კლავიატურაqueueჩაწერა + 1) % კლავიატურაqueueზომა
	if შემდეგი == კლავიატურაqueueკითხვა {
		return
	}
	კლავიატურაqueue[კლავიატურაqueueჩაწერა] = key
	კლავიატურაqueueჩაწერა = შემდეგი
}

func Pპროცესიpendingკლავიატურაevents() {
	for კლავიატურაqueueკითხვა != კლავიატურაqueueჩაწერა {
		key := კლავიატურაqueue[კლავიატურაqueueკითხვა]
		კლავიატურაqueueკითხვა = (კლავიატურაqueueკითხვა + 1) % კლავიატურაqueueზომა
		Stdinputbyte(key)
		if iკლავიატურაeventhandler != nil {
			iკლავიატურაeventhandler.Onkeydown(key)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shift := მარცხნივshift || მარჯვნივshift

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

func (self *Tკლავიატურაdriver) Handleinterrupt(esp uint32) uint32 {
	სტატუსი := Pპორტიკითხვაbyte(ბრძანებაპორტი_2)
	if (სტატუსი&0x01) == 0 || (სტატუსი&0x20) != 0 {
		return esp
	}

	scancode := Pპორტიკითხვაbyte(dataპორტი_2)
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
		მარცხნივshift = !released
		return esp
	}
	if basecode == 0x36 {
		მარჯვნივshift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, ok := scancodetobyte(basecode); ok {
		queueკლავიატურაbyte(key)
	}

	return esp
}
