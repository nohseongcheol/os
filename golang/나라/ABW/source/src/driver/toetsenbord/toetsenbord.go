package toetsenbord

import . "unsafe"

import . "poort"
import . "interrupt"

import . "console"
import . "systeemcall"

type IToetsenbordGebeurtenishandler interface {
	AanSleutelOmlaag(sleutel byte)
	AanSleutelOmhoog(sleutel byte)
}

var iToetsenbordGebeurtenishandler IToetsenbordGebeurtenishandler
var standaardToetsenbordGebeurtenishandler TStandaardToetsenbordGebeurtenishandler

type TStandaardToetsenbordGebeurtenishandler struct {
}

func (zelf *TStandaardToetsenbordGebeurtenishandler) AanSleutelOmlaag(sleutel byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((sleutel >> 4) & 0xF)]
	buffer[18] = hex[sleutel&0xF]

	console_2 := TConsole{}
	console_2.MAfdrukken(buffer)

}
func (zelf *TStandaardToetsenbordGebeurtenishandler) AanSleutelOmhoog(sleutel byte) {
}

type TToetsenborddriver struct {
	TInterrupthandler
}

var actiefToetsenborddriver *TToetsenborddriver
var interrupthandler func(uint32) uint32

var dataPoort_2 uint16 = 0x60
var opdrachtPoort_2 uint16 = 0x64

const ps2WachtenBeperken = 100000

func wachtenps2InvoerLeeg() bool {
	for i := 0; i < ps2WachtenBeperken; i++ {
		if (PoortLezenbyte(opdrachtPoort_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func wachtenps2UitvoerVolledig() bool {
	for i := 0; i < ps2WachtenBeperken; i++ {
		if (PoortLezenbyte(opdrachtPoort_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func schrijvenps2Opdracht(waarde uint8) bool {
	if !wachtenps2InvoerLeeg() {
		return false
	}
	PoortSchrijvenbyte(opdrachtPoort_2, waarde)
	return true
}

func schrijvenps2data(waarde uint8) bool {
	if !wachtenps2InvoerLeeg() {
		return false
	}
	PoortSchrijvenbyte(dataPoort_2, waarde)
	return true
}

func lezenps2data() (uint8, bool) {
	if !wachtenps2UitvoerVolledig() {
		return 0, false
	}
	return PoortLezenbyte(dataPoort_2), true
}

func (zelf *TToetsenborddriver) Initdriver(manager *TInterruptmanager, toetsenbordGebeurtenishandler IToetsenbordGebeurtenishandler) {

	iToetsenbordGebeurtenishandler = &standaardToetsenbordGebeurtenishandler
	if toetsenbordGebeurtenishandler != nil {
		iToetsenbordGebeurtenishandler = toetsenbordGebeurtenishandler
	}

	actiefToetsenborddriver = zelf
	interrupthandler = handgreepToetsenbordinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	zelf.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PoortLezenbyte(opdrachtPoort_2)&0x01) != 0; i++ {
		PoortLezenbyte(dataPoort_2)
	}

	if !schrijvenps2Opdracht(0xAE) || !schrijvenps2Opdracht(0x20) {
		return
	}
	status, ok := lezenps2data()
	if !ok {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !schrijvenps2Opdracht(0x60) || !schrijvenps2data(status) {
		return
	}

	if !schrijvenps2data(0xF4) {
		return
	}
	ack, ok := lezenps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handgreepToetsenbordinterrupt(esp uint32) uint32 {
	if actiefToetsenborddriver == nil {
		PoortLezenbyte(dataPoort_2)
		return esp
	}
	return actiefToetsenborddriver.Handgreepinterrupt(esp)
}

const toetsenbordqueueGrootte = 64

var toetsenbordqueue [toetsenbordqueueGrootte]byte
var toetsenbordqueueLezen uint8
var toetsenbordqueueSchrijven uint8
var linksshift bool
var rechtsshift bool
var extendedOnderzoekencode bool

func queueToetsenbordbyte(sleutel byte) {
	volgende := (toetsenbordqueueSchrijven + 1) % toetsenbordqueueGrootte
	if volgende == toetsenbordqueueLezen {
		return
	}
	toetsenbordqueue[toetsenbordqueueSchrijven] = sleutel
	toetsenbordqueueSchrijven = volgende
}

func ProcespendingToetsenbordGebeurtenissen() {
	for toetsenbordqueueLezen != toetsenbordqueueSchrijven {
		sleutel := toetsenbordqueue[toetsenbordqueueLezen]
		toetsenbordqueueLezen = (toetsenbordqueueLezen + 1) % toetsenbordqueueGrootte
		Stdinputbyte(sleutel)
		if iToetsenbordGebeurtenishandler != nil {
			iToetsenbordGebeurtenishandler.AanSleutelOmlaag(sleutel)
		}
	}
}

func onderzoekencodenaarbyte(onderzoekencode uint8) (byte, bool) {
	shift := linksshift || rechtsshift

	if onderzoekencode >= 0x02 && onderzoekencode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[onderzoekencode-0x02], true
		}
		return "1234567890"[onderzoekencode-0x02], true
	}
	if onderzoekencode >= 0x10 && onderzoekencode <= 0x19 {
		sleutel := "qwertyuiop"[onderzoekencode-0x10]
		if shift {
			sleutel -= 'a' - 'A'
		}
		return sleutel, true
	}
	if onderzoekencode >= 0x1E && onderzoekencode <= 0x26 {
		sleutel := "asdfghjkl"[onderzoekencode-0x1E]
		if shift {
			sleutel -= 'a' - 'A'
		}
		return sleutel, true
	}
	if onderzoekencode >= 0x2C && onderzoekencode <= 0x32 {
		sleutel := "zxcvbnm"[onderzoekencode-0x2C]
		if shift {
			sleutel -= 'a' - 'A'
		}
		return sleutel, true
	}

	switch onderzoekencode {
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

func (zelf *TToetsenborddriver) Handgreepinterrupt(esp uint32) uint32 {
	status := PoortLezenbyte(opdrachtPoort_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	onderzoekencode := PoortLezenbyte(dataPoort_2)
	if onderzoekencode == 0xE0 {
		extendedOnderzoekencode = true
		return esp
	}
	if extendedOnderzoekencode {
		extendedOnderzoekencode = false
		return esp
	}

	released := (onderzoekencode & 0x80) != 0
	basecode := onderzoekencode & 0x7F
	if basecode == 0x2A {
		linksshift = !released
		return esp
	}
	if basecode == 0x36 {
		rechtsshift = !released
		return esp
	}
	if released {
		return esp
	}

	if sleutel, ok := onderzoekencodenaarbyte(basecode); ok {
		queueToetsenbordbyte(sleutel)
	}

	return esp
}
