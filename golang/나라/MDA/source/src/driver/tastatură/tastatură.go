package tastatură

import . "unsafe"

import . "port"
import . "intrerupere"

import . "console"
import . "sistemcall"

type ITastaturăEvenimenthandler interface {
	PornitCheieÎnjos(cheie byte)
	PornitCheieSus(cheie byte)
}

var iTastaturăEvenimenthandler ITastaturăEvenimenthandler
var implicităTastaturăEvenimenthandler TImplicităTastaturăEvenimenthandler

type TImplicităTastaturăEvenimenthandler struct {
}

func (sine *TImplicităTastaturăEvenimenthandler) PornitCheieÎnjos(cheie byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((cheie >> 4) & 0xF)]
	buffer[18] = hex[cheie&0xF]

	console_2 := TConsole{}
	console_2.MTipărește(buffer)

}
func (sine *TImplicităTastaturăEvenimenthandler) PornitCheieSus(cheie byte) {
}

type TTastaturădriver struct {
	TIntreruperehandler
}

var activTastaturădriver *TTastaturădriver
var intreruperehandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var comandăport_2 uint16 = 0x64

const ps2AșteaptăLimită = 100000

func așteaptăps2IntroducețiGol() bool {
	for i := 0; i < ps2AșteaptăLimită; i++ {
		if (PortCitirebyte(comandăport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func așteaptăps2RezultatComplet() bool {
	for i := 0; i < ps2AșteaptăLimită; i++ {
		if (PortCitirebyte(comandăport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func scriereps2Comandă(valoare uint8) bool {
	if !așteaptăps2IntroducețiGol() {
		return false
	}
	PortScrierebyte(comandăport_2, valoare)
	return true
}

func scriereps2data(valoare uint8) bool {
	if !așteaptăps2IntroducețiGol() {
		return false
	}
	PortScrierebyte(dataport_2, valoare)
	return true
}

func citireps2data() (uint8, bool) {
	if !așteaptăps2RezultatComplet() {
		return 0, false
	}
	return PortCitirebyte(dataport_2), true
}

func (sine *TTastaturădriver) Initdriver(manager *TIntreruperemanager, tastaturăEvenimenthandler ITastaturăEvenimenthandler) {

	iTastaturăEvenimenthandler = &implicităTastaturăEvenimenthandler
	if tastaturăEvenimenthandler != nil {
		iTastaturăEvenimenthandler = tastaturăEvenimenthandler
	}

	activTastaturădriver = sine
	intreruperehandler = mânerTastaturăIntrerupere
	var address uintptr
	address = uintptr(Pointer(&intreruperehandler))

	sine.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortCitirebyte(comandăport_2)&0x01) != 0; i++ {
		PortCitirebyte(dataport_2)
	}

	if !scriereps2Comandă(0xAE) || !scriereps2Comandă(0x20) {
		return
	}
	stare, ok := citireps2data()
	if !ok {
		return
	}
	stare |= 0x01
	stare &^= 0x10
	if !scriereps2Comandă(0x60) || !scriereps2data(stare) {
		return
	}

	if !scriereps2data(0xF4) {
		return
	}
	ack, ok := citireps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func mânerTastaturăIntrerupere(esp uint32) uint32 {
	if activTastaturădriver == nil {
		PortCitirebyte(dataport_2)
		return esp
	}
	return activTastaturădriver.MânerIntrerupere(esp)
}

const tastaturăqueueMărime = 64

var tastaturăqueue [tastaturăqueueMărime]byte
var tastaturăqueueCitire uint8
var tastaturăqueueScriere uint8
var stângashift bool
var dreaptashift bool
var extendedScaneazăcode bool

func queueTastaturăbyte(cheie byte) {
	înainte := (tastaturăqueueScriere + 1) % tastaturăqueueMărime
	if înainte == tastaturăqueueCitire {
		return
	}
	tastaturăqueue[tastaturăqueueScriere] = cheie
	tastaturăqueueScriere = înainte
}

func ProcespendingTastaturăevents() {
	for tastaturăqueueCitire != tastaturăqueueScriere {
		cheie := tastaturăqueue[tastaturăqueueCitire]
		tastaturăqueueCitire = (tastaturăqueueCitire + 1) % tastaturăqueueMărime
		Stdinputbyte(cheie)
		if iTastaturăEvenimenthandler != nil {
			iTastaturăEvenimenthandler.PornitCheieÎnjos(cheie)
		}
	}
}

func scaneazăcodetobyte(scaneazăcode uint8) (byte, bool) {
	shift := stângashift || dreaptashift

	if scaneazăcode >= 0x02 && scaneazăcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[scaneazăcode-0x02], true
		}
		return "1234567890"[scaneazăcode-0x02], true
	}
	if scaneazăcode >= 0x10 && scaneazăcode <= 0x19 {
		cheie := "qwertyuiop"[scaneazăcode-0x10]
		if shift {
			cheie -= 'a' - 'A'
		}
		return cheie, true
	}
	if scaneazăcode >= 0x1E && scaneazăcode <= 0x26 {
		cheie := "asdfghjkl"[scaneazăcode-0x1E]
		if shift {
			cheie -= 'a' - 'A'
		}
		return cheie, true
	}
	if scaneazăcode >= 0x2C && scaneazăcode <= 0x32 {
		cheie := "zxcvbnm"[scaneazăcode-0x2C]
		if shift {
			cheie -= 'a' - 'A'
		}
		return cheie, true
	}

	switch scaneazăcode {
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

func (sine *TTastaturădriver) MânerIntrerupere(esp uint32) uint32 {
	stare := PortCitirebyte(comandăport_2)
	if (stare&0x01) == 0 || (stare&0x20) != 0 {
		return esp
	}

	scaneazăcode := PortCitirebyte(dataport_2)
	if scaneazăcode == 0xE0 {
		extendedScaneazăcode = true
		return esp
	}
	if extendedScaneazăcode {
		extendedScaneazăcode = false
		return esp
	}

	released := (scaneazăcode & 0x80) != 0
	basecode := scaneazăcode & 0x7F
	if basecode == 0x2A {
		stângashift = !released
		return esp
	}
	if basecode == 0x36 {
		dreaptashift = !released
		return esp
	}
	if released {
		return esp
	}

	if cheie, ok := scaneazăcodetobyte(basecode); ok {
		queueTastaturăbyte(cheie)
	}

	return esp
}
