package klaviatūra

import . "unsafe"

import . "prievadas"
import . "pertraukimas"

import . "console"
import . "sistemacall"

type IKlaviatūraĮvykishandler interface {
	ĮjungtaRaktasŽemyn(raktas byte)
	ĮjungtaRaktasAukštyn(raktas byte)
}

var iKlaviatūraĮvykishandler IKlaviatūraĮvykishandler
var numatytasisKlaviatūraĮvykishandler TNumatytasisKlaviatūraĮvykishandler

type TNumatytasisKlaviatūraĮvykishandler struct {
}

func (self *TNumatytasisKlaviatūraĮvykishandler) ĮjungtaRaktasŽemyn(raktas byte) {
	šešioliktainis := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = šešioliktainis[((raktas >> 4) & 0xF)]
	buffer[18] = šešioliktainis[raktas&0xF]

	console_2 := TConsole{}
	console_2.MSpausdinti(buffer)

}
func (self *TNumatytasisKlaviatūraĮvykishandler) ĮjungtaRaktasAukštyn(raktas byte) {
}

type TKlaviatūradriver struct {
	TPertraukimashandler
}

var aktyvusKlaviatūradriver *TKlaviatūradriver
var pertraukimashandler func(uint32) uint32

var dataPrievadas_2 uint16 = 0x60
var komandaPrievadas_2 uint16 = 0x64

const ps2LauktiRiba = 100000

func lauktips2ĮvestisTuščia() bool {
	for i := 0; i < ps2LauktiRiba; i++ {
		if (PrievadasSkaitymasbyte(komandaPrievadas_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func lauktips2IšvestisPilna() bool {
	for i := 0; i < ps2LauktiRiba; i++ {
		if (PrievadasSkaitymasbyte(komandaPrievadas_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func rašymasps2Komanda(reikšmė uint8) bool {
	if !lauktips2ĮvestisTuščia() {
		return false
	}
	PrievadasRašymasbyte(komandaPrievadas_2, reikšmė)
	return true
}

func rašymasps2data(reikšmė uint8) bool {
	if !lauktips2ĮvestisTuščia() {
		return false
	}
	PrievadasRašymasbyte(dataPrievadas_2, reikšmė)
	return true
}

func skaitymasps2data() (uint8, bool) {
	if !lauktips2IšvestisPilna() {
		return 0, false
	}
	return PrievadasSkaitymasbyte(dataPrievadas_2), true
}

func (self *TKlaviatūradriver) Initdriver(manager *TPertraukimasmanager, klaviatūraĮvykishandler IKlaviatūraĮvykishandler) {

	iKlaviatūraĮvykishandler = &numatytasisKlaviatūraĮvykishandler
	if klaviatūraĮvykishandler != nil {
		iKlaviatūraĮvykishandler = klaviatūraĮvykishandler
	}

	aktyvusKlaviatūradriver = self
	pertraukimashandler = pozicijaKlaviatūraPertraukimas
	var address uintptr
	address = uintptr(Pointer(&pertraukimashandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PrievadasSkaitymasbyte(komandaPrievadas_2)&0x01) != 0; i++ {
		PrievadasSkaitymasbyte(dataPrievadas_2)
	}

	if !rašymasps2Komanda(0xAE) || !rašymasps2Komanda(0x20) {
		return
	}
	būsena, gerai := skaitymasps2data()
	if !gerai {
		return
	}
	būsena |= 0x01
	būsena &^= 0x10
	if !rašymasps2Komanda(0x60) || !rašymasps2data(būsena) {
		return
	}

	if !rašymasps2data(0xF4) {
		return
	}
	ack, gerai := skaitymasps2data()
	if !gerai || ack != 0xFA {
		return
	}

}

func pozicijaKlaviatūraPertraukimas(esp uint32) uint32 {
	if aktyvusKlaviatūradriver == nil {
		PrievadasSkaitymasbyte(dataPrievadas_2)
		return esp
	}
	return aktyvusKlaviatūradriver.PozicijaPertraukimas(esp)
}

const klaviatūraqueueDydis = 64

var klaviatūraqueue [klaviatūraqueueDydis]byte
var klaviatūraqueueSkaitymas uint8
var klaviatūraqueueRašymas uint8
var kairėjeLyg2 bool
var dešinėLyg2 bool
var extendedSkaityticode bool

func queueKlaviatūrabyte(raktas byte) {
	kitas := (klaviatūraqueueRašymas + 1) % klaviatūraqueueDydis
	if kitas == klaviatūraqueueSkaitymas {
		return
	}
	klaviatūraqueue[klaviatūraqueueRašymas] = raktas
	klaviatūraqueueRašymas = kitas
}

func ProcesaspendingKlaviatūraĮvykiai() {
	for klaviatūraqueueSkaitymas != klaviatūraqueueRašymas {
		raktas := klaviatūraqueue[klaviatūraqueueSkaitymas]
		klaviatūraqueueSkaitymas = (klaviatūraqueueSkaitymas + 1) % klaviatūraqueueDydis
		Stdinputbyte(raktas)
		if iKlaviatūraĮvykishandler != nil {
			iKlaviatūraĮvykishandler.ĮjungtaRaktasŽemyn(raktas)
		}
	}
}

func skaityticodetobyte(skaityticode uint8) (byte, bool) {
	lyg2 := kairėjeLyg2 || dešinėLyg2

	if skaityticode >= 0x02 && skaityticode <= 0x0B {
		if lyg2 {
			return "!@#$%^&*()"[skaityticode-0x02], true
		}
		return "1234567890"[skaityticode-0x02], true
	}
	if skaityticode >= 0x10 && skaityticode <= 0x19 {
		raktas := "qwertyuiop"[skaityticode-0x10]
		if lyg2 {
			raktas -= 'a' - 'A'
		}
		return raktas, true
	}
	if skaityticode >= 0x1E && skaityticode <= 0x26 {
		raktas := "asdfghjkl"[skaityticode-0x1E]
		if lyg2 {
			raktas -= 'a' - 'A'
		}
		return raktas, true
	}
	if skaityticode >= 0x2C && skaityticode <= 0x32 {
		raktas := "zxcvbnm"[skaityticode-0x2C]
		if lyg2 {
			raktas -= 'a' - 'A'
		}
		return raktas, true
	}

	switch skaityticode {
	case 0x0C:
		if lyg2 {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if lyg2 {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if lyg2 {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if lyg2 {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if lyg2 {
			return ':', true
		}
		return ';', true
	case 0x28:
		if lyg2 {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if lyg2 {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if lyg2 {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if lyg2 {
			return '<', true
		}
		return ',', true
	case 0x34:
		if lyg2 {
			return '>', true
		}
		return '.', true
	case 0x35:
		if lyg2 {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (self *TKlaviatūradriver) PozicijaPertraukimas(esp uint32) uint32 {
	būsena := PrievadasSkaitymasbyte(komandaPrievadas_2)
	if (būsena&0x01) == 0 || (būsena&0x20) != 0 {
		return esp
	}

	skaityticode := PrievadasSkaitymasbyte(dataPrievadas_2)
	if skaityticode == 0xE0 {
		extendedSkaityticode = true
		return esp
	}
	if extendedSkaityticode {
		extendedSkaityticode = false
		return esp
	}

	released := (skaityticode & 0x80) != 0
	basecode := skaityticode & 0x7F
	if basecode == 0x2A {
		kairėjeLyg2 = !released
		return esp
	}
	if basecode == 0x36 {
		dešinėLyg2 = !released
		return esp
	}
	if released {
		return esp
	}

	if raktas, gerai := skaityticodetobyte(basecode); gerai {
		queueKlaviatūrabyte(raktas)
	}

	return esp
}
