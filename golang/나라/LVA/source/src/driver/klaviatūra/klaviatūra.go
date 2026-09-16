/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klaviatūra

import . "unsafe"

import . "ports"
import . "pārtraukums"

import . "console"
import . "sistēmacall"

type IKlaviatūraNotikumshandler interface {
	IeslēgtsAtslēgaLejup(atslēga byte)
	IeslēgtsAtslēgaAugšup(atslēga byte)
}

var iKlaviatūraNotikumshandler IKlaviatūraNotikumshandler
var noklusētaisKlaviatūraNotikumshandler TNoklusētaisKlaviatūraNotikumshandler

type TNoklusētaisKlaviatūraNotikumshandler struct {
}

func (pats *TNoklusētaisKlaviatūraNotikumshandler) IeslēgtsAtslēgaLejup(atslēga byte) {
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heksa[((atslēga >> 4) & 0xF)]
	buffer[18] = heksa[atslēga&0xF]

	console_2 := TConsole{}
	console_2.MDrukāt(buffer)

}
func (pats *TNoklusētaisKlaviatūraNotikumshandler) IeslēgtsAtslēgaAugšup(atslēga byte) {
}

type TKlaviatūradriver struct {
	TPārtraukumshandler
}

var aktīvsKlaviatūradriver *TKlaviatūradriver
var pārtraukumshandler func(uint32) uint32

var dataPorts_2 uint16 = 0x60
var komandaPorts_2 uint16 = 0x64

const ps2GaidītIerobežot = 100000

func gaidītps2IevadeTukšs() bool {
	for i := 0; i < ps2GaidītIerobežot; i++ {
		if (PortsLasītbyte(komandaPorts_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func gaidītps2IzvadePilns() bool {
	for i := 0; i < ps2GaidītIerobežot; i++ {
		if (PortsLasītbyte(komandaPorts_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func rakstītps2Komanda(vērtība uint8) bool {
	if !gaidītps2IevadeTukšs() {
		return false
	}
	PortsRakstītbyte(komandaPorts_2, vērtība)
	return true
}

func rakstītps2data(vērtība uint8) bool {
	if !gaidītps2IevadeTukšs() {
		return false
	}
	PortsRakstītbyte(dataPorts_2, vērtība)
	return true
}

func lasītps2data() (uint8, bool) {
	if !gaidītps2IzvadePilns() {
		return 0, false
	}
	return PortsLasītbyte(dataPorts_2), true
}

func (pats *TKlaviatūradriver) Initdriver(manager *TPārtraukumsmanager, klaviatūraNotikumshandler IKlaviatūraNotikumshandler) {

	iKlaviatūraNotikumshandler = &noklusētaisKlaviatūraNotikumshandler
	if klaviatūraNotikumshandler != nil {
		iKlaviatūraNotikumshandler = klaviatūraNotikumshandler
	}

	aktīvsKlaviatūradriver = pats
	pārtraukumshandler = handleKlaviatūraPārtraukums
	var address uintptr
	address = uintptr(Pointer(&pārtraukumshandler))

	pats.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortsLasītbyte(komandaPorts_2)&0x01) != 0; i++ {
		PortsLasītbyte(dataPorts_2)
	}

	if !rakstītps2Komanda(0xAE) || !rakstītps2Komanda(0x20) {
		return
	}
	statuss, labi := lasītps2data()
	if !labi {
		return
	}
	statuss |= 0x01
	statuss &^= 0x10
	if !rakstītps2Komanda(0x60) || !rakstītps2data(statuss) {
		return
	}

	if !rakstītps2data(0xF4) {
		return
	}
	ack, labi := lasītps2data()
	if !labi || ack != 0xFA {
		return
	}

}

func handleKlaviatūraPārtraukums(esp uint32) uint32 {
	if aktīvsKlaviatūradriver == nil {
		PortsLasītbyte(dataPorts_2)
		return esp
	}
	return aktīvsKlaviatūradriver.HandlePārtraukums(esp)
}

const klaviatūraqueueIzmērs = 64

var klaviatūraqueue [klaviatūraqueueIzmērs]byte
var klaviatūraqueueLasīt uint8
var klaviatūraqueueRakstīt uint8
var pakreisishift bool
var palabishift bool
var extendedSkenētcode bool

func queueKlaviatūrabyte(atslēga byte) {
	nākamais := (klaviatūraqueueRakstīt + 1) % klaviatūraqueueIzmērs
	if nākamais == klaviatūraqueueLasīt {
		return
	}
	klaviatūraqueue[klaviatūraqueueRakstīt] = atslēga
	klaviatūraqueueRakstīt = nākamais
}

func ProcesspendingKlaviatūraevents() {
	for klaviatūraqueueLasīt != klaviatūraqueueRakstīt {
		atslēga := klaviatūraqueue[klaviatūraqueueLasīt]
		klaviatūraqueueLasīt = (klaviatūraqueueLasīt + 1) % klaviatūraqueueIzmērs
		Stdinputbyte(atslēga)
		if iKlaviatūraNotikumshandler != nil {
			iKlaviatūraNotikumshandler.IeslēgtsAtslēgaLejup(atslēga)
		}
	}
}

func skenētcodetobyte(skenētcode uint8) (byte, bool) {
	shift := pakreisishift || palabishift

	if skenētcode >= 0x02 && skenētcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[skenētcode-0x02], true
		}
		return "1234567890"[skenētcode-0x02], true
	}
	if skenētcode >= 0x10 && skenētcode <= 0x19 {
		atslēga := "qwertyuiop"[skenētcode-0x10]
		if shift {
			atslēga -= 'a' - 'A'
		}
		return atslēga, true
	}
	if skenētcode >= 0x1E && skenētcode <= 0x26 {
		atslēga := "asdfghjkl"[skenētcode-0x1E]
		if shift {
			atslēga -= 'a' - 'A'
		}
		return atslēga, true
	}
	if skenētcode >= 0x2C && skenētcode <= 0x32 {
		atslēga := "zxcvbnm"[skenētcode-0x2C]
		if shift {
			atslēga -= 'a' - 'A'
		}
		return atslēga, true
	}

	switch skenētcode {
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

func (pats *TKlaviatūradriver) HandlePārtraukums(esp uint32) uint32 {
	statuss := PortsLasītbyte(komandaPorts_2)
	if (statuss&0x01) == 0 || (statuss&0x20) != 0 {
		return esp
	}

	skenētcode := PortsLasītbyte(dataPorts_2)
	if skenētcode == 0xE0 {
		extendedSkenētcode = true
		return esp
	}
	if extendedSkenētcode {
		extendedSkenētcode = false
		return esp
	}

	released := (skenētcode & 0x80) != 0
	basecode := skenētcode & 0x7F
	if basecode == 0x2A {
		pakreisishift = !released
		return esp
	}
	if basecode == 0x36 {
		palabishift = !released
		return esp
	}
	if released {
		return esp
	}

	if atslēga, labi := skenētcodetobyte(basecode); labi {
		queueKlaviatūrabyte(atslēga)
	}

	return esp
}
