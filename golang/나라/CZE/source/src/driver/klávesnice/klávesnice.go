/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klávesnice

import . "unsafe"

import . "port"
import . "přerušení"

import . "konzole"
import . "systémcall"

type IKlávesniceUdálostihandler interface {
	ZapnutoKlíčDolů(klíč byte)
	ZapnutoKlíčNahoru(klíč byte)
}

var iKlávesniceUdálostihandler IKlávesniceUdálostihandler
var výchozíKlávesniceUdálostihandler TVýchozíKlávesniceUdálostihandler

type TVýchozíKlávesniceUdálostihandler struct {
}

func (self *TVýchozíKlávesniceUdálostihandler) ZapnutoKlíčDolů(klíč byte) {
	šestnáctkově := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = šestnáctkově[((klíč >> 4) & 0xF)]
	buffer[18] = šestnáctkově[klíč&0xF]

	konzole_2 := TKonzole{}
	konzole_2.MTisknout(buffer)

}
func (self *TVýchozíKlávesniceUdálostihandler) ZapnutoKlíčNahoru(klíč byte) {
}

type TKlávesnicedriver struct {
	TPřerušeníhandler
}

var aktivníKlávesnicedriver *TKlávesnicedriver
var přerušeníhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var příkazport_2 uint16 = 0x64

const ps2PočkatOmezení = 100000

func počkatps2VstupPrázdné() bool {
	for i := 0; i < ps2PočkatOmezení; i++ {
		if (PortČteníbyte(příkazport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func počkatps2VýstupÚplný() bool {
	for i := 0; i < ps2PočkatOmezení; i++ {
		if (PortČteníbyte(příkazport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zápisps2Příkaz(hodnota uint8) bool {
	if !počkatps2VstupPrázdné() {
		return false
	}
	PortZápisbyte(příkazport_2, hodnota)
	return true
}

func zápisps2data(hodnota uint8) bool {
	if !počkatps2VstupPrázdné() {
		return false
	}
	PortZápisbyte(dataport_2, hodnota)
	return true
}

func čteníps2data() (uint8, bool) {
	if !počkatps2VýstupÚplný() {
		return 0, false
	}
	return PortČteníbyte(dataport_2), true
}

func (self *TKlávesnicedriver) Initdriver(manager *TPřerušenímanager, klávesniceUdálostihandler IKlávesniceUdálostihandler) {

	iKlávesniceUdálostihandler = &výchozíKlávesniceUdálostihandler
	if klávesniceUdálostihandler != nil {
		iKlávesniceUdálostihandler = klávesniceUdálostihandler
	}

	aktivníKlávesnicedriver = self
	přerušeníhandler = úchytkaKlávesnicePřerušení
	var adresa uintptr
	adresa = uintptr(Pointer(&přerušeníhandler))

	self.Init(0x21, uintptr(Pointer(manager)), adresa)

	for i := 0; i < 32 && (PortČteníbyte(příkazport_2)&0x01) != 0; i++ {
		PortČteníbyte(dataport_2)
	}

	if !zápisps2Příkaz(0xAE) || !zápisps2Příkaz(0x20) {
		return
	}
	stav, budiž := čteníps2data()
	if !budiž {
		return
	}
	stav |= 0x01
	stav &^= 0x10
	if !zápisps2Příkaz(0x60) || !zápisps2data(stav) {
		return
	}

	if !zápisps2data(0xF4) {
		return
	}
	ack, budiž := čteníps2data()
	if !budiž || ack != 0xFA {
		return
	}

}

func úchytkaKlávesnicePřerušení(esp uint32) uint32 {
	if aktivníKlávesnicedriver == nil {
		PortČteníbyte(dataport_2)
		return esp
	}
	return aktivníKlávesnicedriver.ÚchytkaPřerušení(esp)
}

const klávesnicequeueVelikost = 64

var klávesnicequeue [klávesnicequeueVelikost]byte
var klávesnicequeueČtení uint8
var klávesnicequeueZápis uint8
var vlevoshift bool
var vpravoshift bool
var extendedProhledatcode bool

func queueKlávesnicebyte(klíč byte) {
	následující := (klávesnicequeueZápis + 1) % klávesnicequeueVelikost
	if následující == klávesnicequeueČtení {
		return
	}
	klávesnicequeue[klávesnicequeueZápis] = klíč
	klávesnicequeueZápis = následující
}

func ProcespendingKlávesniceUdálosti() {
	for klávesnicequeueČtení != klávesnicequeueZápis {
		klíč := klávesnicequeue[klávesnicequeueČtení]
		klávesnicequeueČtení = (klávesnicequeueČtení + 1) % klávesnicequeueVelikost
		Stdinputbyte(klíč)
		if iKlávesniceUdálostihandler != nil {
			iKlávesniceUdálostihandler.ZapnutoKlíčDolů(klíč)
		}
	}
}

func prohledatcodedobyte(prohledatcode uint8) (byte, bool) {
	shift := vlevoshift || vpravoshift

	if prohledatcode >= 0x02 && prohledatcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[prohledatcode-0x02], true
		}
		return "1234567890"[prohledatcode-0x02], true
	}
	if prohledatcode >= 0x10 && prohledatcode <= 0x19 {
		klíč := "qwertyuiop"[prohledatcode-0x10]
		if shift {
			klíč -= 'a' - 'A'
		}
		return klíč, true
	}
	if prohledatcode >= 0x1E && prohledatcode <= 0x26 {
		klíč := "asdfghjkl"[prohledatcode-0x1E]
		if shift {
			klíč -= 'a' - 'A'
		}
		return klíč, true
	}
	if prohledatcode >= 0x2C && prohledatcode <= 0x32 {
		klíč := "zxcvbnm"[prohledatcode-0x2C]
		if shift {
			klíč -= 'a' - 'A'
		}
		return klíč, true
	}

	switch prohledatcode {
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

func (self *TKlávesnicedriver) ÚchytkaPřerušení(esp uint32) uint32 {
	stav := PortČteníbyte(příkazport_2)
	if (stav&0x01) == 0 || (stav&0x20) != 0 {
		return esp
	}

	prohledatcode := PortČteníbyte(dataport_2)
	if prohledatcode == 0xE0 {
		extendedProhledatcode = true
		return esp
	}
	if extendedProhledatcode {
		extendedProhledatcode = false
		return esp
	}

	released := (prohledatcode & 0x80) != 0
	basecode := prohledatcode & 0x7F
	if basecode == 0x2A {
		vlevoshift = !released
		return esp
	}
	if basecode == 0x36 {
		vpravoshift = !released
		return esp
	}
	if released {
		return esp
	}

	if klíč, budiž := prohledatcodedobyte(basecode); budiž {
		queueKlávesnicebyte(klíč)
	}

	return esp
}
