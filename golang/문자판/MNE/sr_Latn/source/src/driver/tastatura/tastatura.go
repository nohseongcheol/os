package tastatura

import . "unsafe"

import . "port"
import . "ometanje"

import . "konzola"
import . "sistemcall"

type ITastaturaDogađajhandler interface {
	NaKljučNiže(ključ byte)
	NaKljučGore(ključ byte)
}

var iTastaturaDogađajhandler ITastaturaDogađajhandler
var podrazumevanoTastaturaDogađajhandler TPodrazumevanoTastaturaDogađajhandler

type TPodrazumevanoTastaturaDogađajhandler struct {
}

func (isti *TPodrazumevanoTastaturaDogađajhandler) NaKljučNiže(ključ byte) {
	heksadecimalno := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heksadecimalno[((ključ >> 4) & 0xF)]
	buffer[18] = heksadecimalno[ključ&0xF]

	konzola_2 := TKonzola{}
	konzola_2.MŠtampaj(buffer)

}
func (isti *TPodrazumevanoTastaturaDogađajhandler) NaKljučGore(ključ byte) {
}

type TTastaturadriver struct {
	TOmetanjehandler
}

var aktivnaTastaturadriver *TTastaturadriver
var ometanjehandler func(uint32) uint32

var dataPort_2 uint16 = 0x60
var naredbaPort_2 uint16 = 0x64

const ps2SačekajOgraniči = 100000

func sačekajps2UlazPrazno() bool {
	for i := 0; i < ps2SačekajOgraniči; i++ {
		if (Portčitanjebyte(naredbaPort_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func sačekajps2Izlazpotpuno() bool {
	for i := 0; i < ps2SačekajOgraniči; i++ {
		if (Portčitanjebyte(naredbaPort_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func pišeps2Naredba(vrednost uint8) bool {
	if !sačekajps2UlazPrazno() {
		return false
	}
	PortPišebyte(naredbaPort_2, vrednost)
	return true
}

func pišeps2data(vrednost uint8) bool {
	if !sačekajps2UlazPrazno() {
		return false
	}
	PortPišebyte(dataPort_2, vrednost)
	return true
}

func čitanjeps2data() (uint8, bool) {
	if !sačekajps2Izlazpotpuno() {
		return 0, false
	}
	return Portčitanjebyte(dataPort_2), true
}

func (isti *TTastaturadriver) Initdriver(manager *TOmetanjemanager, tastaturaDogađajhandler ITastaturaDogađajhandler) {

	iTastaturaDogađajhandler = &podrazumevanoTastaturaDogađajhandler
	if tastaturaDogađajhandler != nil {
		iTastaturaDogađajhandler = tastaturaDogađajhandler
	}

	aktivnaTastaturadriver = isti
	ometanjehandler = ručkaTastaturaOmetanje
	var address uintptr
	address = uintptr(Pointer(&ometanjehandler))

	isti.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portčitanjebyte(naredbaPort_2)&0x01) != 0; i++ {
		Portčitanjebyte(dataPort_2)
	}

	if !pišeps2Naredba(0xAE) || !pišeps2Naredba(0x20) {
		return
	}
	stanje, uredu := čitanjeps2data()
	if !uredu {
		return
	}
	stanje |= 0x01
	stanje &^= 0x10
	if !pišeps2Naredba(0x60) || !pišeps2data(stanje) {
		return
	}

	if !pišeps2data(0xF4) {
		return
	}
	ack, uredu := čitanjeps2data()
	if !uredu || ack != 0xFA {
		return
	}

}

func ručkaTastaturaOmetanje(esp uint32) uint32 {
	if aktivnaTastaturadriver == nil {
		Portčitanjebyte(dataPort_2)
		return esp
	}
	return aktivnaTastaturadriver.RučkaOmetanje(esp)
}

const tastaturaqueueVeličina = 64

var tastaturaqueue [tastaturaqueueVeličina]byte
var tastaturaqueuečitanje uint8
var tastaturaqueuePiše uint8
var levoŠift bool
var desnoŠift bool
var extendedPregledajcode bool

func queueTastaturabyte(ključ byte) {
	sledeće := (tastaturaqueuePiše + 1) % tastaturaqueueVeličina
	if sledeće == tastaturaqueuečitanje {
		return
	}
	tastaturaqueue[tastaturaqueuePiše] = ključ
	tastaturaqueuePiše = sledeće
}

func ProcespendingTastaturaDogađaji() {
	for tastaturaqueuečitanje != tastaturaqueuePiše {
		ključ := tastaturaqueue[tastaturaqueuečitanje]
		tastaturaqueuečitanje = (tastaturaqueuečitanje + 1) % tastaturaqueueVeličina
		Stdinputbyte(ključ)
		if iTastaturaDogađajhandler != nil {
			iTastaturaDogađajhandler.NaKljučNiže(ključ)
		}
	}
}

func pregledajcodetobyte(pregledajcode uint8) (byte, bool) {
	šift := levoŠift || desnoŠift

	if pregledajcode >= 0x02 && pregledajcode <= 0x0B {
		if šift {
			return "!@#$%^&*()"[pregledajcode-0x02], true
		}
		return "1234567890"[pregledajcode-0x02], true
	}
	if pregledajcode >= 0x10 && pregledajcode <= 0x19 {
		ključ := "qwertyuiop"[pregledajcode-0x10]
		if šift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if pregledajcode >= 0x1E && pregledajcode <= 0x26 {
		ključ := "asdfghjkl"[pregledajcode-0x1E]
		if šift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if pregledajcode >= 0x2C && pregledajcode <= 0x32 {
		ključ := "zxcvbnm"[pregledajcode-0x2C]
		if šift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}

	switch pregledajcode {
	case 0x0C:
		if šift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if šift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if šift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if šift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if šift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if šift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if šift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if šift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if šift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if šift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if šift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (isti *TTastaturadriver) RučkaOmetanje(esp uint32) uint32 {
	stanje := Portčitanjebyte(naredbaPort_2)
	if (stanje&0x01) == 0 || (stanje&0x20) != 0 {
		return esp
	}

	pregledajcode := Portčitanjebyte(dataPort_2)
	if pregledajcode == 0xE0 {
		extendedPregledajcode = true
		return esp
	}
	if extendedPregledajcode {
		extendedPregledajcode = false
		return esp
	}

	released := (pregledajcode & 0x80) != 0
	basecode := pregledajcode & 0x7F
	if basecode == 0x2A {
		levoŠift = !released
		return esp
	}
	if basecode == 0x36 {
		desnoŠift = !released
		return esp
	}
	if released {
		return esp
	}

	if ključ, uredu := pregledajcodetobyte(basecode); uredu {
		queueTastaturabyte(ključ)
	}

	return esp
}
