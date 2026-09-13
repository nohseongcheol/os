package tangentbord

import . "unsafe"

import . "port"
import . "avbrott"

import . "konsol"
import . "systemcall"

type ITangentbordHändelsehandler interface {
	PåNyckelNer(nyckel byte)
	PåNyckelUpp(nyckel byte)
}

var iTangentbordHändelsehandler ITangentbordHändelsehandler
var standardTangentbordHändelsehandler TStandardTangentbordHändelsehandler

type TStandardTangentbordHändelsehandler struct {
}

func (själv *TStandardTangentbordHändelsehandler) PåNyckelNer(nyckel byte) {
	hexadecimalt := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hexadecimalt[((nyckel >> 4) & 0xF)]
	buffer[18] = hexadecimalt[nyckel&0xF]

	konsol_2 := TKonsol{}
	konsol_2.MSkrivut(buffer)

}
func (själv *TStandardTangentbordHändelsehandler) PåNyckelUpp(nyckel byte) {
}

type TTangentborddriver struct {
	TAvbrotthandler
}

var aktivTangentborddriver *TTangentborddriver
var avbrotthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var kommandoport_2 uint16 = 0x64

const ps2VäntaGräns = 100000

func väntaps2InmatningTom() bool {
	for i := 0; i < ps2VäntaGräns; i++ {
		if (PortLäsbyte(kommandoport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func väntaps2UtmatningFullständig() bool {
	for i := 0; i < ps2VäntaGräns; i++ {
		if (PortLäsbyte(kommandoport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skrivps2Kommando(värde uint8) bool {
	if !väntaps2InmatningTom() {
		return false
	}
	PortSkrivbyte(kommandoport_2, värde)
	return true
}

func skrivps2data(värde uint8) bool {
	if !väntaps2InmatningTom() {
		return false
	}
	PortSkrivbyte(dataport_2, värde)
	return true
}

func läsps2data() (uint8, bool) {
	if !väntaps2UtmatningFullständig() {
		return 0, false
	}
	return PortLäsbyte(dataport_2), true
}

func (själv *TTangentborddriver) Initdriver(manager *TAvbrottmanager, tangentbordHändelsehandler ITangentbordHändelsehandler) {

	iTangentbordHändelsehandler = &standardTangentbordHändelsehandler
	if tangentbordHändelsehandler != nil {
		iTangentbordHändelsehandler = tangentbordHändelsehandler
	}

	aktivTangentborddriver = själv
	avbrotthandler = handtagTangentbordAvbrott
	var adress uintptr
	adress = uintptr(Pointer(&avbrotthandler))

	själv.Init(0x21, uintptr(Pointer(manager)), adress)

	for i := 0; i < 32 && (PortLäsbyte(kommandoport_2)&0x01) != 0; i++ {
		PortLäsbyte(dataport_2)
	}

	if !skrivps2Kommando(0xAE) || !skrivps2Kommando(0x20) {
		return
	}
	status, ok := läsps2data()
	if !ok {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !skrivps2Kommando(0x60) || !skrivps2data(status) {
		return
	}

	if !skrivps2data(0xF4) {
		return
	}
	ack, ok := läsps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handtagTangentbordAvbrott(esp uint32) uint32 {
	if aktivTangentborddriver == nil {
		PortLäsbyte(dataport_2)
		return esp
	}
	return aktivTangentborddriver.HandtagAvbrott(esp)
}

const tangentbordqueueStorlek = 64

var tangentbordqueue [tangentbordqueueStorlek]byte
var tangentbordqueueLäs uint8
var tangentbordqueueSkriv uint8
var vänsterSkift bool
var högerSkift bool
var extendedSökavcode bool

func queueTangentbordbyte(nyckel byte) {
	nästa := (tangentbordqueueSkriv + 1) % tangentbordqueueStorlek
	if nästa == tangentbordqueueLäs {
		return
	}
	tangentbordqueue[tangentbordqueueSkriv] = nyckel
	tangentbordqueueSkriv = nästa
}

func ProcesspendingTangentbordHändelser() {
	for tangentbordqueueLäs != tangentbordqueueSkriv {
		nyckel := tangentbordqueue[tangentbordqueueLäs]
		tangentbordqueueLäs = (tangentbordqueueLäs + 1) % tangentbordqueueStorlek
		Stdinputbyte(nyckel)
		if iTangentbordHändelsehandler != nil {
			iTangentbordHändelsehandler.PåNyckelNer(nyckel)
		}
	}
}

func sökavcodetobyte(sökavcode uint8) (byte, bool) {
	skift := vänsterSkift || högerSkift

	if sökavcode >= 0x02 && sökavcode <= 0x0B {
		if skift {
			return "!@#$%^&*()"[sökavcode-0x02], true
		}
		return "1234567890"[sökavcode-0x02], true
	}
	if sökavcode >= 0x10 && sökavcode <= 0x19 {
		nyckel := "qwertyuiop"[sökavcode-0x10]
		if skift {
			nyckel -= 'a' - 'A'
		}
		return nyckel, true
	}
	if sökavcode >= 0x1E && sökavcode <= 0x26 {
		nyckel := "asdfghjkl"[sökavcode-0x1E]
		if skift {
			nyckel -= 'a' - 'A'
		}
		return nyckel, true
	}
	if sökavcode >= 0x2C && sökavcode <= 0x32 {
		nyckel := "zxcvbnm"[sökavcode-0x2C]
		if skift {
			nyckel -= 'a' - 'A'
		}
		return nyckel, true
	}

	switch sökavcode {
	case 0x0C:
		if skift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if skift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if skift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if skift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if skift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if skift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if skift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if skift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if skift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if skift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if skift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (själv *TTangentborddriver) HandtagAvbrott(esp uint32) uint32 {
	status := PortLäsbyte(kommandoport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	sökavcode := PortLäsbyte(dataport_2)
	if sökavcode == 0xE0 {
		extendedSökavcode = true
		return esp
	}
	if extendedSökavcode {
		extendedSökavcode = false
		return esp
	}

	released := (sökavcode & 0x80) != 0
	basecode := sökavcode & 0x7F
	if basecode == 0x2A {
		vänsterSkift = !released
		return esp
	}
	if basecode == 0x36 {
		högerSkift = !released
		return esp
	}
	if released {
		return esp
	}

	if nyckel, ok := sökavcodetobyte(basecode); ok {
		queueTangentbordbyte(nyckel)
	}

	return esp
}
