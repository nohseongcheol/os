/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klawiatura

import . "unsafe"

import . "port"
import . "przerwanie"

import . "konsola"
import . "systemowecall"

type IKlawiaturaWydarzeniehandler interface {
	WłączKluczWdół(klucz byte)
	WłączKluczGóra(klucz byte)
}

var iKlawiaturaWydarzeniehandler IKlawiaturaWydarzeniehandler
var domyślneKlawiaturaWydarzeniehandler TDomyślneKlawiaturaWydarzeniehandler

type TDomyślneKlawiaturaWydarzeniehandler struct {
}

func (bieżący *TDomyślneKlawiaturaWydarzeniehandler) WłączKluczWdół(klucz byte) {
	szesnastkowo := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = szesnastkowo[((klucz >> 4) & 0xF)]
	buffer[18] = szesnastkowo[klucz&0xF]

	konsola_2 := TKonsola{}
	konsola_2.MWydrukuj(buffer)

}
func (bieżący *TDomyślneKlawiaturaWydarzeniehandler) WłączKluczGóra(klucz byte) {
}

type TKlawiaturadriver struct {
	TPrzerwaniehandler
}

var aktywneKlawiaturadriver *TKlawiaturadriver
var przerwaniehandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var polecenieport_2 uint16 = 0x64

const ps2Czekajlimit = 100000

func czekajps2WejściePusty() bool {
	for i := 0; i < ps2Czekajlimit; i++ {
		if (PortOdczytbyte(polecenieport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func czekajps2DanewyjściowePełne() bool {
	for i := 0; i < ps2Czekajlimit; i++ {
		if (PortOdczytbyte(polecenieport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zapisps2Polecenie(wartość uint8) bool {
	if !czekajps2WejściePusty() {
		return false
	}
	PortZapisbyte(polecenieport_2, wartość)
	return true
}

func zapisps2data(wartość uint8) bool {
	if !czekajps2WejściePusty() {
		return false
	}
	PortZapisbyte(dataport_2, wartość)
	return true
}

func odczytps2data() (uint8, bool) {
	if !czekajps2DanewyjściowePełne() {
		return 0, false
	}
	return PortOdczytbyte(dataport_2), true
}

func (bieżący *TKlawiaturadriver) Initdriver(manager *TPrzerwaniemanager, klawiaturaWydarzeniehandler IKlawiaturaWydarzeniehandler) {

	iKlawiaturaWydarzeniehandler = &domyślneKlawiaturaWydarzeniehandler
	if klawiaturaWydarzeniehandler != nil {
		iKlawiaturaWydarzeniehandler = klawiaturaWydarzeniehandler
	}

	aktywneKlawiaturadriver = bieżący
	przerwaniehandler = uchwytKlawiaturaPrzerwanie
	var adres uintptr
	adres = uintptr(Pointer(&przerwaniehandler))

	bieżący.Init(0x21, uintptr(Pointer(manager)), adres)

	for i := 0; i < 32 && (PortOdczytbyte(polecenieport_2)&0x01) != 0; i++ {
		PortOdczytbyte(dataport_2)
	}

	if !zapisps2Polecenie(0xAE) || !zapisps2Polecenie(0x20) {
		return
	}
	stan, ok := odczytps2data()
	if !ok {
		return
	}
	stan |= 0x01
	stan &^= 0x10
	if !zapisps2Polecenie(0x60) || !zapisps2data(stan) {
		return
	}

	if !zapisps2data(0xF4) {
		return
	}
	ack, ok := odczytps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func uchwytKlawiaturaPrzerwanie(esp uint32) uint32 {
	if aktywneKlawiaturadriver == nil {
		PortOdczytbyte(dataport_2)
		return esp
	}
	return aktywneKlawiaturadriver.UchwytPrzerwanie(esp)
}

const klawiaturaqueueRozmiar = 64

var klawiaturaqueue [klawiaturaqueueRozmiar]byte
var klawiaturaqueueOdczyt uint8
var klawiaturaqueueZapis uint8
var lewoshift bool
var prawoshift bool
var extendedSkanujcode bool

func queueKlawiaturabyte(klucz byte) {
	następny := (klawiaturaqueueZapis + 1) % klawiaturaqueueRozmiar
	if następny == klawiaturaqueueOdczyt {
		return
	}
	klawiaturaqueue[klawiaturaqueueZapis] = klucz
	klawiaturaqueueZapis = następny
}

func ProcespendingKlawiaturaWydarzenia() {
	for klawiaturaqueueOdczyt != klawiaturaqueueZapis {
		klucz := klawiaturaqueue[klawiaturaqueueOdczyt]
		klawiaturaqueueOdczyt = (klawiaturaqueueOdczyt + 1) % klawiaturaqueueRozmiar
		Stdinputbyte(klucz)
		if iKlawiaturaWydarzeniehandler != nil {
			iKlawiaturaWydarzeniehandler.WłączKluczWdół(klucz)
		}
	}
}

func skanujcodetobyte(skanujcode uint8) (byte, bool) {
	shift := lewoshift || prawoshift

	if skanujcode >= 0x02 && skanujcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[skanujcode-0x02], true
		}
		return "1234567890"[skanujcode-0x02], true
	}
	if skanujcode >= 0x10 && skanujcode <= 0x19 {
		klucz := "qwertyuiop"[skanujcode-0x10]
		if shift {
			klucz -= 'a' - 'A'
		}
		return klucz, true
	}
	if skanujcode >= 0x1E && skanujcode <= 0x26 {
		klucz := "asdfghjkl"[skanujcode-0x1E]
		if shift {
			klucz -= 'a' - 'A'
		}
		return klucz, true
	}
	if skanujcode >= 0x2C && skanujcode <= 0x32 {
		klucz := "zxcvbnm"[skanujcode-0x2C]
		if shift {
			klucz -= 'a' - 'A'
		}
		return klucz, true
	}

	switch skanujcode {
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

func (bieżący *TKlawiaturadriver) UchwytPrzerwanie(esp uint32) uint32 {
	stan := PortOdczytbyte(polecenieport_2)
	if (stan&0x01) == 0 || (stan&0x20) != 0 {
		return esp
	}

	skanujcode := PortOdczytbyte(dataport_2)
	if skanujcode == 0xE0 {
		extendedSkanujcode = true
		return esp
	}
	if extendedSkanujcode {
		extendedSkanujcode = false
		return esp
	}

	released := (skanujcode & 0x80) != 0
	basecode := skanujcode & 0x7F
	if basecode == 0x2A {
		lewoshift = !released
		return esp
	}
	if basecode == 0x36 {
		prawoshift = !released
		return esp
	}
	if released {
		return esp
	}

	if klucz, ok := skanujcodetobyte(basecode); ok {
		queueKlawiaturabyte(klucz)
	}

	return esp
}
