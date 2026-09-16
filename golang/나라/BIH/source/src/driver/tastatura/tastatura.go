/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tastatura

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "sistemcall"

type ITastaturaeventhandler interface {
	UključenKljučdown(ključ byte)
	UključenKljučGore(ključ byte)
}

var iTastaturaeventhandler ITastaturaeventhandler
var uobičajenoTastaturaeventhandler TUobičajenoTastaturaeventhandler

type TUobičajenoTastaturaeventhandler struct {
}

func (self *TUobičajenoTastaturaeventhandler) UključenKljučdown(ključ byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((ključ >> 4) & 0xF)]
	buffer[18] = hex[ključ&0xF]

	console_2 := TConsole{}
	console_2.MŠtampaj(buffer)

}
func (self *TUobičajenoTastaturaeventhandler) UključenKljučGore(ključ byte) {
}

type TTastaturadriver struct {
	TInterrupthandler
}

var activeTastaturadriver *TTastaturadriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var naredbaport_2 uint16 = 0x64

const ps2Sačekajlimit = 100000

func sačekajps2Ulazempty() bool {
	for i := 0; i < ps2Sačekajlimit; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func sačekajps2IzlazPotpuno() bool {
	for i := 0; i < ps2Sačekajlimit; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func pišips2Naredba(vrijednost uint8) bool {
	if !sačekajps2Ulazempty() {
		return false
	}
	PortPišibyte(naredbaport_2, vrijednost)
	return true
}

func pišips2data(vrijednost uint8) bool {
	if !sačekajps2Ulazempty() {
		return false
	}
	PortPišibyte(dataport_2, vrijednost)
	return true
}

func čitajps2data() (uint8, bool) {
	if !sačekajps2IzlazPotpuno() {
		return 0, false
	}
	return PortČitajbyte(dataport_2), true
}

func (self *TTastaturadriver) Initdriver(manager *TInterruptmanager, tastaturaeventhandler ITastaturaeventhandler) {

	iTastaturaeventhandler = &uobičajenoTastaturaeventhandler
	if tastaturaeventhandler != nil {
		iTastaturaeventhandler = tastaturaeventhandler
	}

	activeTastaturadriver = self
	interrupthandler = handleTastaturainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortČitajbyte(naredbaport_2)&0x01) != 0; i++ {
		PortČitajbyte(dataport_2)
	}

	if !pišips2Naredba(0xAE) || !pišips2Naredba(0x20) {
		return
	}
	status, uredu := čitajps2data()
	if !uredu {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !pišips2Naredba(0x60) || !pišips2data(status) {
		return
	}

	if !pišips2data(0xF4) {
		return
	}
	ack, uredu := čitajps2data()
	if !uredu || ack != 0xFA {
		return
	}

}

func handleTastaturainterrupt(esp uint32) uint32 {
	if activeTastaturadriver == nil {
		PortČitajbyte(dataport_2)
		return esp
	}
	return activeTastaturadriver.Handleinterrupt(esp)
}

const tastaturaqueueVeličina = 64

var tastaturaqueue [tastaturaqueueVeličina]byte
var tastaturaqueueČitaj uint8
var tastaturaqueuePiši uint8
var lijevoshift bool
var desnoshift bool
var extendedscancode bool

func queueTastaturabyte(ključ byte) {
	sljedeće := (tastaturaqueuePiši + 1) % tastaturaqueueVeličina
	if sljedeće == tastaturaqueueČitaj {
		return
	}
	tastaturaqueue[tastaturaqueuePiši] = ključ
	tastaturaqueuePiši = sljedeće
}

func ProcesspendingTastaturaevents() {
	for tastaturaqueueČitaj != tastaturaqueuePiši {
		ključ := tastaturaqueue[tastaturaqueueČitaj]
		tastaturaqueueČitaj = (tastaturaqueueČitaj + 1) % tastaturaqueueVeličina
		Stdinputbyte(ključ)
		if iTastaturaeventhandler != nil {
			iTastaturaeventhandler.UključenKljučdown(ključ)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shift := lijevoshift || desnoshift

	if scancode >= 0x02 && scancode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[scancode-0x02], true
		}
		return "1234567890"[scancode-0x02], true
	}
	if scancode >= 0x10 && scancode <= 0x19 {
		ključ := "qwertyuiop"[scancode-0x10]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if scancode >= 0x1E && scancode <= 0x26 {
		ključ := "asdfghjkl"[scancode-0x1E]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if scancode >= 0x2C && scancode <= 0x32 {
		ključ := "zxcvbnm"[scancode-0x2C]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
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

func (self *TTastaturadriver) Handleinterrupt(esp uint32) uint32 {
	status := PortČitajbyte(naredbaport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	scancode := PortČitajbyte(dataport_2)
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
		lijevoshift = !released
		return esp
	}
	if basecode == 0x36 {
		desnoshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ključ, uredu := scancodetobyte(basecode); uredu {
		queueTastaturabyte(ključ)
	}

	return esp
}
