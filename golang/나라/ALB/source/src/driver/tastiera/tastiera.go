package tastiera

import . "unsafe"

import . "porta"
import . "interrupt"

import . "konsolë"
import . "sistemicall"

type ITastieraNgjarjehandler interface {
	OnÇelesPoshtë(çeles byte)
	OnÇelesSipër(çeles byte)
}

var iTastieraNgjarjehandler ITastieraNgjarjehandler
var eprezgjedhurTastieraNgjarjehandler TEprezgjedhurTastieraNgjarjehandler

type TEprezgjedhurTastieraNgjarjehandler struct {
}

func (vetvetja *TEprezgjedhurTastieraNgjarjehandler) OnÇelesPoshtë(çeles byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((çeles >> 4) & 0xF)]
	buffer[18] = hex[çeles&0xF]

	konsolë_2 := TKonsolë{}
	konsolë_2.MPrinto(buffer)

}
func (vetvetja *TEprezgjedhurTastieraNgjarjehandler) OnÇelesSipër(çeles byte) {
}

type TTastieradriver struct {
	TInterrupthandler
}

var aktivTastieradriver *TTastieradriver
var interrupthandler func(uint32) uint32

var dataPorta_2 uint16 = 0x60
var urdhërPorta_2 uint16 = 0x64

const ps2PritKufi = 100000

func pritps2HyrjaBosh() bool {
	for i := 0; i < ps2PritKufi; i++ {
		if (PortaLeximibyte(urdhërPorta_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func pritps2outputIplotë() bool {
	for i := 0; i < ps2PritKufi; i++ {
		if (PortaLeximibyte(urdhërPorta_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func shkrimips2Urdhër(vlera uint8) bool {
	if !pritps2HyrjaBosh() {
		return false
	}
	PortaShkrimibyte(urdhërPorta_2, vlera)
	return true
}

func shkrimips2data(vlera uint8) bool {
	if !pritps2HyrjaBosh() {
		return false
	}
	PortaShkrimibyte(dataPorta_2, vlera)
	return true
}

func leximips2data() (uint8, bool) {
	if !pritps2outputIplotë() {
		return 0, false
	}
	return PortaLeximibyte(dataPorta_2), true
}

func (vetvetja *TTastieradriver) Initdriver(manazhuesi *TInterruptManazhuesi, tastieraNgjarjehandler ITastieraNgjarjehandler) {

	iTastieraNgjarjehandler = &eprezgjedhurTastieraNgjarjehandler
	if tastieraNgjarjehandler != nil {
		iTastieraNgjarjehandler = tastieraNgjarjehandler
	}

	aktivTastieradriver = vetvetja
	interrupthandler = handleTastierainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	vetvetja.Init(0x21, uintptr(Pointer(manazhuesi)), address)

	for i := 0; i < 32 && (PortaLeximibyte(urdhërPorta_2)&0x01) != 0; i++ {
		PortaLeximibyte(dataPorta_2)
	}

	if !shkrimips2Urdhër(0xAE) || !shkrimips2Urdhër(0x20) {
		return
	}
	gjendja, ok := leximips2data()
	if !ok {
		return
	}
	gjendja |= 0x01
	gjendja &^= 0x10
	if !shkrimips2Urdhër(0x60) || !shkrimips2data(gjendja) {
		return
	}

	if !shkrimips2data(0xF4) {
		return
	}
	ack, ok := leximips2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleTastierainterrupt(esp uint32) uint32 {
	if aktivTastieradriver == nil {
		PortaLeximibyte(dataPorta_2)
		return esp
	}
	return aktivTastieradriver.Handleinterrupt(esp)
}

const tastieraqueueMadhësia = 64

var tastieraqueue [tastieraqueueMadhësia]byte
var tastieraqueueLeximi uint8
var tastieraqueueShkrimi uint8
var majtasshift bool
var djathtasshift bool
var extendedscancode bool

func queueTastierabyte(çeles byte) {
	pasuesen := (tastieraqueueShkrimi + 1) % tastieraqueueMadhësia
	if pasuesen == tastieraqueueLeximi {
		return
	}
	tastieraqueue[tastieraqueueShkrimi] = çeles
	tastieraqueueShkrimi = pasuesen
}

func ProçespendingTastieraevents() {
	for tastieraqueueLeximi != tastieraqueueShkrimi {
		çeles := tastieraqueue[tastieraqueueLeximi]
		tastieraqueueLeximi = (tastieraqueueLeximi + 1) % tastieraqueueMadhësia
		Stdinputbyte(çeles)
		if iTastieraNgjarjehandler != nil {
			iTastieraNgjarjehandler.OnÇelesPoshtë(çeles)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shift := majtasshift || djathtasshift

	if scancode >= 0x02 && scancode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[scancode-0x02], true
		}
		return "1234567890"[scancode-0x02], true
	}
	if scancode >= 0x10 && scancode <= 0x19 {
		çeles := "qwertyuiop"[scancode-0x10]
		if shift {
			çeles -= 'a' - 'A'
		}
		return çeles, true
	}
	if scancode >= 0x1E && scancode <= 0x26 {
		çeles := "asdfghjkl"[scancode-0x1E]
		if shift {
			çeles -= 'a' - 'A'
		}
		return çeles, true
	}
	if scancode >= 0x2C && scancode <= 0x32 {
		çeles := "zxcvbnm"[scancode-0x2C]
		if shift {
			çeles -= 'a' - 'A'
		}
		return çeles, true
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

func (vetvetja *TTastieradriver) Handleinterrupt(esp uint32) uint32 {
	gjendja := PortaLeximibyte(urdhërPorta_2)
	if (gjendja&0x01) == 0 || (gjendja&0x20) != 0 {
		return esp
	}

	scancode := PortaLeximibyte(dataPorta_2)
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
		majtasshift = !released
		return esp
	}
	if basecode == 0x36 {
		djathtasshift = !released
		return esp
	}
	if released {
		return esp
	}

	if çeles, ok := scancodetobyte(basecode); ok {
		queueTastierabyte(çeles)
	}

	return esp
}
