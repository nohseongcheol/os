package tipkovnica

import . "unsafe"

import . "vrata"
import . "prekinitev"

import . "console"
import . "sistemcall"

type ITipkovnicaeventhandler interface {
	VključenoKljučDol(ključ byte)
	VključenoKljučGor(ključ byte)
}

var iTipkovnicaeventhandler ITipkovnicaeventhandler
var privzetoTipkovnicaeventhandler TPrivzetoTipkovnicaeventhandler

type TPrivzetoTipkovnicaeventhandler struct {
}

func (sam *TPrivzetoTipkovnicaeventhandler) VključenoKljučDol(ključ byte) {
	šestnajstiško := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = šestnajstiško[((ključ >> 4) & 0xF)]
	buffer[18] = šestnajstiško[ključ&0xF]

	console_2 := TConsole{}
	console_2.MNatisni(buffer)

}
func (sam *TPrivzetoTipkovnicaeventhandler) VključenoKljučGor(ključ byte) {
}

type TTipkovnicadriver struct {
	TPrekinitevhandler
}

var dejavenTipkovnicadriver *TTipkovnicadriver
var prekinitevhandler func(uint32) uint32

var dataVrata_2 uint16 = 0x60
var ukazVrata_2 uint16 = 0x64

const ps2Počakajlimit = 100000

func počakajps2VhodPrazno() bool {
	for i := 0; i < ps2Počakajlimit; i++ {
		if (VrataBranjebyte(ukazVrata_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func počakajps2IzhodPolno() bool {
	for i := 0; i < ps2Počakajlimit; i++ {
		if (VrataBranjebyte(ukazVrata_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func pisanjeps2Ukaz(vrednost uint8) bool {
	if !počakajps2VhodPrazno() {
		return false
	}
	VrataPisanjebyte(ukazVrata_2, vrednost)
	return true
}

func pisanjeps2data(vrednost uint8) bool {
	if !počakajps2VhodPrazno() {
		return false
	}
	VrataPisanjebyte(dataVrata_2, vrednost)
	return true
}

func branjeps2data() (uint8, bool) {
	if !počakajps2IzhodPolno() {
		return 0, false
	}
	return VrataBranjebyte(dataVrata_2), true
}

func (sam *TTipkovnicadriver) Initdriver(manager *TPrekinitevmanager, tipkovnicaeventhandler ITipkovnicaeventhandler) {

	iTipkovnicaeventhandler = &privzetoTipkovnicaeventhandler
	if tipkovnicaeventhandler != nil {
		iTipkovnicaeventhandler = tipkovnicaeventhandler
	}

	dejavenTipkovnicadriver = sam
	prekinitevhandler = ročicaTipkovnicaPrekinitev
	var address uintptr
	address = uintptr(Pointer(&prekinitevhandler))

	sam.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (VrataBranjebyte(ukazVrata_2)&0x01) != 0; i++ {
		VrataBranjebyte(dataVrata_2)
	}

	if !pisanjeps2Ukaz(0xAE) || !pisanjeps2Ukaz(0x20) {
		return
	}
	stanje, vredu := branjeps2data()
	if !vredu {
		return
	}
	stanje |= 0x01
	stanje &^= 0x10
	if !pisanjeps2Ukaz(0x60) || !pisanjeps2data(stanje) {
		return
	}

	if !pisanjeps2data(0xF4) {
		return
	}
	ack, vredu := branjeps2data()
	if !vredu || ack != 0xFA {
		return
	}

}

func ročicaTipkovnicaPrekinitev(esp uint32) uint32 {
	if dejavenTipkovnicadriver == nil {
		VrataBranjebyte(dataVrata_2)
		return esp
	}
	return dejavenTipkovnicadriver.RočicaPrekinitev(esp)
}

const tipkovnicaqueueVelikost = 64

var tipkovnicaqueue [tipkovnicaqueueVelikost]byte
var tipkovnicaqueueBranje uint8
var tipkovnicaqueuePisanje uint8
var levoshift bool
var desnoshift bool
var extendedPreiščicode bool

func queueTipkovnicabyte(ključ byte) {
	naslednje := (tipkovnicaqueuePisanje + 1) % tipkovnicaqueueVelikost
	if naslednje == tipkovnicaqueueBranje {
		return
	}
	tipkovnicaqueue[tipkovnicaqueuePisanje] = ključ
	tipkovnicaqueuePisanje = naslednje
}

func OpravilopendingTipkovnicaDogodki() {
	for tipkovnicaqueueBranje != tipkovnicaqueuePisanje {
		ključ := tipkovnicaqueue[tipkovnicaqueueBranje]
		tipkovnicaqueueBranje = (tipkovnicaqueueBranje + 1) % tipkovnicaqueueVelikost
		Stdinputbyte(ključ)
		if iTipkovnicaeventhandler != nil {
			iTipkovnicaeventhandler.VključenoKljučDol(ključ)
		}
	}
}

func preiščicodetobyte(preiščicode uint8) (byte, bool) {
	shift := levoshift || desnoshift

	if preiščicode >= 0x02 && preiščicode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[preiščicode-0x02], true
		}
		return "1234567890"[preiščicode-0x02], true
	}
	if preiščicode >= 0x10 && preiščicode <= 0x19 {
		ključ := "qwertyuiop"[preiščicode-0x10]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if preiščicode >= 0x1E && preiščicode <= 0x26 {
		ključ := "asdfghjkl"[preiščicode-0x1E]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if preiščicode >= 0x2C && preiščicode <= 0x32 {
		ključ := "zxcvbnm"[preiščicode-0x2C]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}

	switch preiščicode {
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

func (sam *TTipkovnicadriver) RočicaPrekinitev(esp uint32) uint32 {
	stanje := VrataBranjebyte(ukazVrata_2)
	if (stanje&0x01) == 0 || (stanje&0x20) != 0 {
		return esp
	}

	preiščicode := VrataBranjebyte(dataVrata_2)
	if preiščicode == 0xE0 {
		extendedPreiščicode = true
		return esp
	}
	if extendedPreiščicode {
		extendedPreiščicode = false
		return esp
	}

	released := (preiščicode & 0x80) != 0
	basecode := preiščicode & 0x7F
	if basecode == 0x2A {
		levoshift = !released
		return esp
	}
	if basecode == 0x36 {
		desnoshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ključ, vredu := preiščicodetobyte(basecode); vredu {
		queueTipkovnicabyte(ključ)
	}

	return esp
}
