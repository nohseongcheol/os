/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tastatur

import . "unsafe"

import . "port"
import . "interrupt"

import . "console"
import . "systemcall"

type ITastatureventhandler interface {
	TændtNøgleNed(nøgle byte)
	TændtNøgleOp(nøgle byte)
}

var iTastatureventhandler ITastatureventhandler
var standardTastatureventhandler TStandardTastatureventhandler

type TStandardTastatureventhandler struct {
}

func (selv *TStandardTastatureventhandler) TændtNøgleNed(nøgle byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((nøgle >> 4) & 0xF)]
	buffer[18] = hex[nøgle&0xF]

	console_2 := TConsole{}
	console_2.MUdskriv(buffer)

}
func (selv *TStandardTastatureventhandler) TændtNøgleOp(nøgle byte) {
}

type TTastaturdriver struct {
	TInterrupthandler
}

var aktivTastaturdriver *TTastaturdriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var kommandoport_2 uint16 = 0x64

const ps2Ventlimit = 100000

func ventps2IndgangTom() bool {
	for i := 0; i < ps2Ventlimit; i++ {
		if (PortLæsebyte(kommandoport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ventps2UdgangFuldt() bool {
	for i := 0; i < ps2Ventlimit; i++ {
		if (PortLæsebyte(kommandoport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skriveps2Kommando(værdi uint8) bool {
	if !ventps2IndgangTom() {
		return false
	}
	PortSkrivebyte(kommandoport_2, værdi)
	return true
}

func skriveps2data(værdi uint8) bool {
	if !ventps2IndgangTom() {
		return false
	}
	PortSkrivebyte(dataport_2, værdi)
	return true
}

func læseps2data() (uint8, bool) {
	if !ventps2UdgangFuldt() {
		return 0, false
	}
	return PortLæsebyte(dataport_2), true
}

func (selv *TTastaturdriver) Initdriver(manager *TInterruptmanager, tastatureventhandler ITastatureventhandler) {

	iTastatureventhandler = &standardTastatureventhandler
	if tastatureventhandler != nil {
		iTastatureventhandler = tastatureventhandler
	}

	aktivTastaturdriver = selv
	interrupthandler = håndtagTastaturinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	selv.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLæsebyte(kommandoport_2)&0x01) != 0; i++ {
		PortLæsebyte(dataport_2)
	}

	if !skriveps2Kommando(0xAE) || !skriveps2Kommando(0x20) {
		return
	}
	status, ok := læseps2data()
	if !ok {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !skriveps2Kommando(0x60) || !skriveps2data(status) {
		return
	}

	if !skriveps2data(0xF4) {
		return
	}
	ack, ok := læseps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func håndtagTastaturinterrupt(esp uint32) uint32 {
	if aktivTastaturdriver == nil {
		PortLæsebyte(dataport_2)
		return esp
	}
	return aktivTastaturdriver.Håndtaginterrupt(esp)
}

const tastaturqueueStørrelse = 64

var tastaturqueue [tastaturqueueStørrelse]byte
var tastaturqueueLæse uint8
var tastaturqueueSkrive uint8
var venstreSkift bool
var højreSkift bool
var extendedSkancode bool

func queueTastaturbyte(nøgle byte) {
	næste := (tastaturqueueSkrive + 1) % tastaturqueueStørrelse
	if næste == tastaturqueueLæse {
		return
	}
	tastaturqueue[tastaturqueueSkrive] = nøgle
	tastaturqueueSkrive = næste
}

func ProcespendingTastaturBegivenheder() {
	for tastaturqueueLæse != tastaturqueueSkrive {
		nøgle := tastaturqueue[tastaturqueueLæse]
		tastaturqueueLæse = (tastaturqueueLæse + 1) % tastaturqueueStørrelse
		Stdinputbyte(nøgle)
		if iTastatureventhandler != nil {
			iTastatureventhandler.TændtNøgleNed(nøgle)
		}
	}
}

func skancodetobyte(skancode uint8) (byte, bool) {
	skift := venstreSkift || højreSkift

	if skancode >= 0x02 && skancode <= 0x0B {
		if skift {
			return "!@#$%^&*()"[skancode-0x02], true
		}
		return "1234567890"[skancode-0x02], true
	}
	if skancode >= 0x10 && skancode <= 0x19 {
		nøgle := "qwertyuiop"[skancode-0x10]
		if skift {
			nøgle -= 'a' - 'A'
		}
		return nøgle, true
	}
	if skancode >= 0x1E && skancode <= 0x26 {
		nøgle := "asdfghjkl"[skancode-0x1E]
		if skift {
			nøgle -= 'a' - 'A'
		}
		return nøgle, true
	}
	if skancode >= 0x2C && skancode <= 0x32 {
		nøgle := "zxcvbnm"[skancode-0x2C]
		if skift {
			nøgle -= 'a' - 'A'
		}
		return nøgle, true
	}

	switch skancode {
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

func (selv *TTastaturdriver) Håndtaginterrupt(esp uint32) uint32 {
	status := PortLæsebyte(kommandoport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	skancode := PortLæsebyte(dataport_2)
	if skancode == 0xE0 {
		extendedSkancode = true
		return esp
	}
	if extendedSkancode {
		extendedSkancode = false
		return esp
	}

	released := (skancode & 0x80) != 0
	basecode := skancode & 0x7F
	if basecode == 0x2A {
		venstreSkift = !released
		return esp
	}
	if basecode == 0x36 {
		højreSkift = !released
		return esp
	}
	if released {
		return esp
	}

	if nøgle, ok := skancodetobyte(basecode); ok {
		queueTastaturbyte(nøgle)
	}

	return esp
}
