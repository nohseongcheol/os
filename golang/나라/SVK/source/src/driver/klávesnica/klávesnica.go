package klávesnica

import . "unsafe"

import . "port"
import . "prerušenie"

import . "konzola"
import . "systémcall"

type IKlávesnicaUdalosťhandler interface {
	ZapnutéKľúčDole(kľúč byte)
	ZapnutéKľúčHore(kľúč byte)
}

var iKlávesnicaUdalosťhandler IKlávesnicaUdalosťhandler
var predvolenéKlávesnicaUdalosťhandler TPredvolenéKlávesnicaUdalosťhandler

type TPredvolenéKlávesnicaUdalosťhandler struct {
}

func (vlastný *TPredvolenéKlávesnicaUdalosťhandler) ZapnutéKľúčDole(kľúč byte) {
	šestnástkové := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = šestnástkové[((kľúč >> 4) & 0xF)]
	buffer[18] = šestnástkové[kľúč&0xF]

	konzola_2 := TKonzola{}
	konzola_2.MTlačiť(buffer)

}
func (vlastný *TPredvolenéKlávesnicaUdalosťhandler) ZapnutéKľúčHore(kľúč byte) {
}

type TKlávesnicadriver struct {
	TPrerušeniehandler
}

var aktívnyKlávesnicadriver *TKlávesnicadriver
var prerušeniehandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var príkazport_2 uint16 = 0x64

const ps2PočkaťObmedzenie = 100000

func počkaťps2VstupPrázdne() bool {
	for i := 0; i < ps2PočkaťObmedzenie; i++ {
		if (PortČítaniebyte(príkazport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func počkaťps2VýstupPlné() bool {
	for i := 0; i < ps2PočkaťObmedzenie; i++ {
		if (PortČítaniebyte(príkazport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zápisps2Príkaz(hodnota uint8) bool {
	if !počkaťps2VstupPrázdne() {
		return false
	}
	PortZápisbyte(príkazport_2, hodnota)
	return true
}

func zápisps2data(hodnota uint8) bool {
	if !počkaťps2VstupPrázdne() {
		return false
	}
	PortZápisbyte(dataport_2, hodnota)
	return true
}

func čítanieps2data() (uint8, bool) {
	if !počkaťps2VýstupPlné() {
		return 0, false
	}
	return PortČítaniebyte(dataport_2), true
}

func (vlastný *TKlávesnicadriver) Initdriver(manager *TPrerušeniemanager, klávesnicaUdalosťhandler IKlávesnicaUdalosťhandler) {

	iKlávesnicaUdalosťhandler = &predvolenéKlávesnicaUdalosťhandler
	if klávesnicaUdalosťhandler != nil {
		iKlávesnicaUdalosťhandler = klávesnicaUdalosťhandler
	}

	aktívnyKlávesnicadriver = vlastný
	prerušeniehandler = uškoKlávesnicaPrerušenie
	var address uintptr
	address = uintptr(Pointer(&prerušeniehandler))

	vlastný.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortČítaniebyte(príkazport_2)&0x01) != 0; i++ {
		PortČítaniebyte(dataport_2)
	}

	if !zápisps2Príkaz(0xAE) || !zápisps2Príkaz(0x20) {
		return
	}
	stav, ok := čítanieps2data()
	if !ok {
		return
	}
	stav |= 0x01
	stav &^= 0x10
	if !zápisps2Príkaz(0x60) || !zápisps2data(stav) {
		return
	}

	if !zápisps2data(0xF4) {
		return
	}
	ack, ok := čítanieps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func uškoKlávesnicaPrerušenie(esp uint32) uint32 {
	if aktívnyKlávesnicadriver == nil {
		PortČítaniebyte(dataport_2)
		return esp
	}
	return aktívnyKlávesnicadriver.UškoPrerušenie(esp)
}

const klávesnicaqueueVeľkosť = 64

var klávesnicaqueue [klávesnicaqueueVeľkosť]byte
var klávesnicaqueueČítanie uint8
var klávesnicaqueueZápis uint8
var vľavoshift bool
var vpravoshift bool
var extendedPrehľadaťcode bool

func queueKlávesnicabyte(kľúč byte) {
	nasledujúci := (klávesnicaqueueZápis + 1) % klávesnicaqueueVeľkosť
	if nasledujúci == klávesnicaqueueČítanie {
		return
	}
	klávesnicaqueue[klávesnicaqueueZápis] = kľúč
	klávesnicaqueueZápis = nasledujúci
}

func ProcespendingKlávesnicaUdalosti() {
	for klávesnicaqueueČítanie != klávesnicaqueueZápis {
		kľúč := klávesnicaqueue[klávesnicaqueueČítanie]
		klávesnicaqueueČítanie = (klávesnicaqueueČítanie + 1) % klávesnicaqueueVeľkosť
		Stdinputbyte(kľúč)
		if iKlávesnicaUdalosťhandler != nil {
			iKlávesnicaUdalosťhandler.ZapnutéKľúčDole(kľúč)
		}
	}
}

func prehľadaťcodetobyte(prehľadaťcode uint8) (byte, bool) {
	shift := vľavoshift || vpravoshift

	if prehľadaťcode >= 0x02 && prehľadaťcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[prehľadaťcode-0x02], true
		}
		return "1234567890"[prehľadaťcode-0x02], true
	}
	if prehľadaťcode >= 0x10 && prehľadaťcode <= 0x19 {
		kľúč := "qwertyuiop"[prehľadaťcode-0x10]
		if shift {
			kľúč -= 'a' - 'A'
		}
		return kľúč, true
	}
	if prehľadaťcode >= 0x1E && prehľadaťcode <= 0x26 {
		kľúč := "asdfghjkl"[prehľadaťcode-0x1E]
		if shift {
			kľúč -= 'a' - 'A'
		}
		return kľúč, true
	}
	if prehľadaťcode >= 0x2C && prehľadaťcode <= 0x32 {
		kľúč := "zxcvbnm"[prehľadaťcode-0x2C]
		if shift {
			kľúč -= 'a' - 'A'
		}
		return kľúč, true
	}

	switch prehľadaťcode {
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

func (vlastný *TKlávesnicadriver) UškoPrerušenie(esp uint32) uint32 {
	stav := PortČítaniebyte(príkazport_2)
	if (stav&0x01) == 0 || (stav&0x20) != 0 {
		return esp
	}

	prehľadaťcode := PortČítaniebyte(dataport_2)
	if prehľadaťcode == 0xE0 {
		extendedPrehľadaťcode = true
		return esp
	}
	if extendedPrehľadaťcode {
		extendedPrehľadaťcode = false
		return esp
	}

	released := (prehľadaťcode & 0x80) != 0
	basecode := prehľadaťcode & 0x7F
	if basecode == 0x2A {
		vľavoshift = !released
		return esp
	}
	if basecode == 0x36 {
		vpravoshift = !released
		return esp
	}
	if released {
		return esp
	}

	if kľúč, ok := prehľadaťcodetobyte(basecode); ok {
		queueKlávesnicabyte(kľúč)
	}

	return esp
}
