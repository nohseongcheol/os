package tipkovnica

import . "unsafe"

import . "port"
import . "prekid"

import . "console"
import . "sustavcall"

type ITipkovnicaDogađajhandler interface {
	UključenoKljučDolje(ključ byte)
	UključenoKljučGore(ključ byte)
}

var iTipkovnicaDogađajhandler ITipkovnicaDogađajhandler
var zadanoTipkovnicaDogađajhandler TZadanoTipkovnicaDogađajhandler

type TZadanoTipkovnicaDogađajhandler struct {
}

func (sam *TZadanoTipkovnicaDogađajhandler) UključenoKljučDolje(ključ byte) {
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heks[((ključ >> 4) & 0xF)]
	buffer[18] = heks[ključ&0xF]

	console_2 := TConsole{}
	console_2.MIspis(buffer)

}
func (sam *TZadanoTipkovnicaDogađajhandler) UključenoKljučGore(ključ byte) {
}

type TTipkovnicadriver struct {
	TPrekidhandler
}

var aktivanTipkovnicadriver *TTipkovnicadriver
var prekidhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var naredbaport_2 uint16 = 0x64

const ps2ČekajOgraničenje = 100000

func čekajps2UlazPrazno() bool {
	for i := 0; i < ps2ČekajOgraničenje; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func čekajps2IzlazPun() bool {
	for i := 0; i < ps2ČekajOgraničenje; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zapišips2Naredba(vrijednost uint8) bool {
	if !čekajps2UlazPrazno() {
		return false
	}
	PortZapišibyte(naredbaport_2, vrijednost)
	return true
}

func zapišips2data(vrijednost uint8) bool {
	if !čekajps2UlazPrazno() {
		return false
	}
	PortZapišibyte(dataport_2, vrijednost)
	return true
}

func čitajps2data() (uint8, bool) {
	if !čekajps2IzlazPun() {
		return 0, false
	}
	return PortČitajbyte(dataport_2), true
}

func (sam *TTipkovnicadriver) Initdriver(manager *TPrekidmanager, tipkovnicaDogađajhandler ITipkovnicaDogađajhandler) {

	iTipkovnicaDogađajhandler = &zadanoTipkovnicaDogađajhandler
	if tipkovnicaDogađajhandler != nil {
		iTipkovnicaDogađajhandler = tipkovnicaDogađajhandler
	}

	aktivanTipkovnicadriver = sam
	prekidhandler = ručkaTipkovnicaPrekid
	var address uintptr
	address = uintptr(Pointer(&prekidhandler))

	sam.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortČitajbyte(naredbaport_2)&0x01) != 0; i++ {
		PortČitajbyte(dataport_2)
	}

	if !zapišips2Naredba(0xAE) || !zapišips2Naredba(0x20) {
		return
	}
	stanje, uredu := čitajps2data()
	if !uredu {
		return
	}
	stanje |= 0x01
	stanje &^= 0x10
	if !zapišips2Naredba(0x60) || !zapišips2data(stanje) {
		return
	}

	if !zapišips2data(0xF4) {
		return
	}
	ack, uredu := čitajps2data()
	if !uredu || ack != 0xFA {
		return
	}

}

func ručkaTipkovnicaPrekid(esp uint32) uint32 {
	if aktivanTipkovnicadriver == nil {
		PortČitajbyte(dataport_2)
		return esp
	}
	return aktivanTipkovnicadriver.RučkaPrekid(esp)
}

const tipkovnicaqueueVeličina = 64

var tipkovnicaqueue [tipkovnicaqueueVeličina]byte
var tipkovnicaqueueČitaj uint8
var tipkovnicaqueueZapiši uint8
var lijevoshift bool
var desnoshift bool
var extendedPretražicode bool

func queueTipkovnicabyte(ključ byte) {
	slijedeće := (tipkovnicaqueueZapiši + 1) % tipkovnicaqueueVeličina
	if slijedeće == tipkovnicaqueueČitaj {
		return
	}
	tipkovnicaqueue[tipkovnicaqueueZapiši] = ključ
	tipkovnicaqueueZapiši = slijedeće
}

func ProcespendingTipkovnicaevents() {
	for tipkovnicaqueueČitaj != tipkovnicaqueueZapiši {
		ključ := tipkovnicaqueue[tipkovnicaqueueČitaj]
		tipkovnicaqueueČitaj = (tipkovnicaqueueČitaj + 1) % tipkovnicaqueueVeličina
		Stdinputbyte(ključ)
		if iTipkovnicaDogađajhandler != nil {
			iTipkovnicaDogađajhandler.UključenoKljučDolje(ključ)
		}
	}
}

func pretražicodetobyte(pretražicode uint8) (byte, bool) {
	shift := lijevoshift || desnoshift

	if pretražicode >= 0x02 && pretražicode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[pretražicode-0x02], true
		}
		return "1234567890"[pretražicode-0x02], true
	}
	if pretražicode >= 0x10 && pretražicode <= 0x19 {
		ključ := "qwertyuiop"[pretražicode-0x10]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if pretražicode >= 0x1E && pretražicode <= 0x26 {
		ključ := "asdfghjkl"[pretražicode-0x1E]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}
	if pretražicode >= 0x2C && pretražicode <= 0x32 {
		ključ := "zxcvbnm"[pretražicode-0x2C]
		if shift {
			ključ -= 'a' - 'A'
		}
		return ključ, true
	}

	switch pretražicode {
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

func (sam *TTipkovnicadriver) RučkaPrekid(esp uint32) uint32 {
	stanje := PortČitajbyte(naredbaport_2)
	if (stanje&0x01) == 0 || (stanje&0x20) != 0 {
		return esp
	}

	pretražicode := PortČitajbyte(dataport_2)
	if pretražicode == 0xE0 {
		extendedPretražicode = true
		return esp
	}
	if extendedPretražicode {
		extendedPretražicode = false
		return esp
	}

	released := (pretražicode & 0x80) != 0
	basecode := pretražicode & 0x7F
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

	if ključ, uredu := pretražicodetobyte(basecode); uredu {
		queueTipkovnicabyte(ključ)
	}

	return esp
}
