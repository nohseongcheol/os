/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tastatur

import . "unsafe"

import . "port"
import . "avbrudd"

import . "console"
import . "systemcall"

type ITastaturHendelsehandler interface {
	PåNøkkelNed(nøkkel byte)
	PåNøkkelOpp(nøkkel byte)
}

var iTastaturHendelsehandler ITastaturHendelsehandler
var standardTastaturHendelsehandler TStandardTastaturHendelsehandler

type TStandardTastaturHendelsehandler struct {
}

func (selv *TStandardTastaturHendelsehandler) PåNøkkelNed(nøkkel byte) {
	heksadesimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heksadesimal[((nøkkel >> 4) & 0xF)]
	buffer[18] = heksadesimal[nøkkel&0xF]

	console_2 := TConsole{}
	console_2.MSkrivut(buffer)

}
func (selv *TStandardTastaturHendelsehandler) PåNøkkelOpp(nøkkel byte) {
}

type TTastaturdriver struct {
	TAvbruddhandler
}

var aktivTastaturdriver *TTastaturdriver
var avbruddhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var kommandoport_2 uint16 = 0x64

const ps2VentGrense = 100000

func ventps2InndataTom() bool {
	for i := 0; i < ps2VentGrense; i++ {
		if (PortLesbyte(kommandoport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ventps2Utdatafull() bool {
	for i := 0; i < ps2VentGrense; i++ {
		if (PortLesbyte(kommandoport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skrivps2Kommando(verdi uint8) bool {
	if !ventps2InndataTom() {
		return false
	}
	PortSkrivbyte(kommandoport_2, verdi)
	return true
}

func skrivps2data(verdi uint8) bool {
	if !ventps2InndataTom() {
		return false
	}
	PortSkrivbyte(dataport_2, verdi)
	return true
}

func lesps2data() (uint8, bool) {
	if !ventps2Utdatafull() {
		return 0, false
	}
	return PortLesbyte(dataport_2), true
}

func (selv *TTastaturdriver) Initdriver(manager *TAvbruddmanager, tastaturHendelsehandler ITastaturHendelsehandler) {

	iTastaturHendelsehandler = &standardTastaturHendelsehandler
	if tastaturHendelsehandler != nil {
		iTastaturHendelsehandler = tastaturHendelsehandler
	}

	aktivTastaturdriver = selv
	avbruddhandler = håndtakTastaturAvbrudd
	var address uintptr
	address = uintptr(Pointer(&avbruddhandler))

	selv.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLesbyte(kommandoport_2)&0x01) != 0; i++ {
		PortLesbyte(dataport_2)
	}

	if !skrivps2Kommando(0xAE) || !skrivps2Kommando(0x20) {
		return
	}
	status, ok := lesps2data()
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
	ack, ok := lesps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func håndtakTastaturAvbrudd(esp uint32) uint32 {
	if aktivTastaturdriver == nil {
		PortLesbyte(dataport_2)
		return esp
	}
	return aktivTastaturdriver.HåndtakAvbrudd(esp)
}

const tastaturqueueStørrelse = 64

var tastaturqueue [tastaturqueueStørrelse]byte
var tastaturqueueLes uint8
var tastaturqueueSkriv uint8
var venstreshift bool
var høyreshift bool
var extendedSøkcode bool

func queueTastaturbyte(nøkkel byte) {
	neste := (tastaturqueueSkriv + 1) % tastaturqueueStørrelse
	if neste == tastaturqueueLes {
		return
	}
	tastaturqueue[tastaturqueueSkriv] = nøkkel
	tastaturqueueSkriv = neste
}

func ProsesspendingTastaturevents() {
	for tastaturqueueLes != tastaturqueueSkriv {
		nøkkel := tastaturqueue[tastaturqueueLes]
		tastaturqueueLes = (tastaturqueueLes + 1) % tastaturqueueStørrelse
		Stdinputbyte(nøkkel)
		if iTastaturHendelsehandler != nil {
			iTastaturHendelsehandler.PåNøkkelNed(nøkkel)
		}
	}
}

func søkcodetobyte(søkcode uint8) (byte, bool) {
	shift := venstreshift || høyreshift

	if søkcode >= 0x02 && søkcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[søkcode-0x02], true
		}
		return "1234567890"[søkcode-0x02], true
	}
	if søkcode >= 0x10 && søkcode <= 0x19 {
		nøkkel := "qwertyuiop"[søkcode-0x10]
		if shift {
			nøkkel -= 'a' - 'A'
		}
		return nøkkel, true
	}
	if søkcode >= 0x1E && søkcode <= 0x26 {
		nøkkel := "asdfghjkl"[søkcode-0x1E]
		if shift {
			nøkkel -= 'a' - 'A'
		}
		return nøkkel, true
	}
	if søkcode >= 0x2C && søkcode <= 0x32 {
		nøkkel := "zxcvbnm"[søkcode-0x2C]
		if shift {
			nøkkel -= 'a' - 'A'
		}
		return nøkkel, true
	}

	switch søkcode {
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

func (selv *TTastaturdriver) HåndtakAvbrudd(esp uint32) uint32 {
	status := PortLesbyte(kommandoport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	søkcode := PortLesbyte(dataport_2)
	if søkcode == 0xE0 {
		extendedSøkcode = true
		return esp
	}
	if extendedSøkcode {
		extendedSøkcode = false
		return esp
	}

	released := (søkcode & 0x80) != 0
	basecode := søkcode & 0x7F
	if basecode == 0x2A {
		venstreshift = !released
		return esp
	}
	if basecode == 0x36 {
		høyreshift = !released
		return esp
	}
	if released {
		return esp
	}

	if nøkkel, ok := søkcodetobyte(basecode); ok {
		queueTastaturbyte(nøkkel)
	}

	return esp
}
