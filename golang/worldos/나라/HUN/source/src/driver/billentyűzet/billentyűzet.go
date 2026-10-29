/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package billentyűzet

import . "unsafe"

import . "port"
import . "megszakítás"

import . "konzol"
import . "rendszercall"

type IBillentyűzetEseményhandler interface {
	BeBillentyűLe(billentyű byte)
	BeBillentyűFel(billentyű byte)
}

var iBillentyűzetEseményhandler IBillentyűzetEseményhandler
var alapértelmezettBillentyűzetEseményhandler TAlapértelmezettBillentyűzetEseményhandler

type TAlapértelmezettBillentyűzetEseményhandler struct {
}

func (self *TAlapértelmezettBillentyűzetEseményhandler) BeBillentyűLe(billentyű byte) {
	hexadecimális := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hexadecimális[((billentyű >> 4) & 0xF)]
	buffer[18] = hexadecimális[billentyű&0xF]

	konzol_2 := TKonzol{}
	konzol_2.MNyomtatás(buffer)

}
func (self *TAlapértelmezettBillentyűzetEseményhandler) BeBillentyűFel(billentyű byte) {
}

type TBillentyűzetdriver struct {
	TMegszakításhandler
}

var aktívBillentyűzetdriver *TBillentyűzetdriver
var megszakításhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var parancsport_2 uint16 = 0x64

const ps2VárakozásKorlátozás = 100000

func várakozásps2BemenetÜres() bool {
	for i := 0; i < ps2VárakozásKorlátozás; i++ {
		if (PortOlvasásbyte(parancsport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func várakozásps2KimenetTeljes() bool {
	for i := 0; i < ps2VárakozásKorlátozás; i++ {
		if (PortOlvasásbyte(parancsport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func írásps2Parancs(érték uint8) bool {
	if !várakozásps2BemenetÜres() {
		return false
	}
	PortÍrásbyte(parancsport_2, érték)
	return true
}

func írásps2data(érték uint8) bool {
	if !várakozásps2BemenetÜres() {
		return false
	}
	PortÍrásbyte(dataport_2, érték)
	return true
}

func olvasásps2data() (uint8, bool) {
	if !várakozásps2KimenetTeljes() {
		return 0, false
	}
	return PortOlvasásbyte(dataport_2), true
}

func (self *TBillentyűzetdriver) Initdriver(manager *TMegszakításmanager, billentyűzetEseményhandler IBillentyűzetEseményhandler) {

	iBillentyűzetEseményhandler = &alapértelmezettBillentyűzetEseményhandler
	if billentyűzetEseményhandler != nil {
		iBillentyűzetEseményhandler = billentyűzetEseményhandler
	}

	aktívBillentyűzetdriver = self
	megszakításhandler = fogantyúBillentyűzetMegszakítás
	var address uintptr
	address = uintptr(Pointer(&megszakításhandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortOlvasásbyte(parancsport_2)&0x01) != 0; i++ {
		PortOlvasásbyte(dataport_2)
	}

	if !írásps2Parancs(0xAE) || !írásps2Parancs(0x20) {
		return
	}
	állapot, ok := olvasásps2data()
	if !ok {
		return
	}
	állapot |= 0x01
	állapot &^= 0x10
	if !írásps2Parancs(0x60) || !írásps2data(állapot) {
		return
	}

	if !írásps2data(0xF4) {
		return
	}
	ack, ok := olvasásps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func fogantyúBillentyűzetMegszakítás(esp uint32) uint32 {
	if aktívBillentyűzetdriver == nil {
		PortOlvasásbyte(dataport_2)
		return esp
	}
	return aktívBillentyűzetdriver.FogantyúMegszakítás(esp)
}

const billentyűzetqueueMéret = 64

var billentyűzetqueue [billentyűzetqueueMéret]byte
var billentyűzetqueueOlvasás uint8
var billentyűzetqueueÍrás uint8
var balrashift bool
var jobbrashift bool
var extendedVizsgálatcode bool

func queueBillentyűzetbyte(billentyű byte) {
	következő := (billentyűzetqueueÍrás + 1) % billentyűzetqueueMéret
	if következő == billentyűzetqueueOlvasás {
		return
	}
	billentyűzetqueue[billentyűzetqueueÍrás] = billentyű
	billentyűzetqueueÍrás = következő
}

func FolyamatpendingBillentyűzetEsemények() {
	for billentyűzetqueueOlvasás != billentyűzetqueueÍrás {
		billentyű := billentyűzetqueue[billentyűzetqueueOlvasás]
		billentyűzetqueueOlvasás = (billentyűzetqueueOlvasás + 1) % billentyűzetqueueMéret
		Stdinputbyte(billentyű)
		if iBillentyűzetEseményhandler != nil {
			iBillentyűzetEseményhandler.BeBillentyűLe(billentyű)
		}
	}
}

func vizsgálatcodetobyte(vizsgálatcode uint8) (byte, bool) {
	shift := balrashift || jobbrashift

	if vizsgálatcode >= 0x02 && vizsgálatcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[vizsgálatcode-0x02], true
		}
		return "1234567890"[vizsgálatcode-0x02], true
	}
	if vizsgálatcode >= 0x10 && vizsgálatcode <= 0x19 {
		billentyű := "qwertyuiop"[vizsgálatcode-0x10]
		if shift {
			billentyű -= 'a' - 'A'
		}
		return billentyű, true
	}
	if vizsgálatcode >= 0x1E && vizsgálatcode <= 0x26 {
		billentyű := "asdfghjkl"[vizsgálatcode-0x1E]
		if shift {
			billentyű -= 'a' - 'A'
		}
		return billentyű, true
	}
	if vizsgálatcode >= 0x2C && vizsgálatcode <= 0x32 {
		billentyű := "zxcvbnm"[vizsgálatcode-0x2C]
		if shift {
			billentyű -= 'a' - 'A'
		}
		return billentyű, true
	}

	switch vizsgálatcode {
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

func (self *TBillentyűzetdriver) FogantyúMegszakítás(esp uint32) uint32 {
	állapot := PortOlvasásbyte(parancsport_2)
	if (állapot&0x01) == 0 || (állapot&0x20) != 0 {
		return esp
	}

	vizsgálatcode := PortOlvasásbyte(dataport_2)
	if vizsgálatcode == 0xE0 {
		extendedVizsgálatcode = true
		return esp
	}
	if extendedVizsgálatcode {
		extendedVizsgálatcode = false
		return esp
	}

	released := (vizsgálatcode & 0x80) != 0
	basecode := vizsgálatcode & 0x7F
	if basecode == 0x2A {
		balrashift = !released
		return esp
	}
	if basecode == 0x36 {
		jobbrashift = !released
		return esp
	}
	if released {
		return esp
	}

	if billentyű, ok := vizsgálatcodetobyte(basecode); ok {
		queueBillentyűzetbyte(billentyű)
	}

	return esp
}
