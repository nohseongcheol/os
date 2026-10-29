/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tastatur

import . "unsafe"

import . "anschluss"
import . "unterbrechung"

import . "konsole"
import . "systemAufruf"

type ITastaturEreignishandler interface {
	BeiSchlüsselAbwärts(schlüssel byte)
	BeiSchlüsselAufwärts(schlüssel byte)
}

var iTastaturEreignishandler ITastaturEreignishandler
var standardTastaturEreignishandler TStandardTastaturEreignishandler

type TStandardTastaturEreignishandler struct {
}

func (selbst *TStandardTastaturEreignishandler) BeiSchlüsselAbwärts(schlüssel byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((schlüssel >> 4) & 0xF)]
	buffer[18] = hex[schlüssel&0xF]

	konsole_2 := TKonsole{}
	konsole_2.MDrucken(buffer)

}
func (selbst *TStandardTastaturEreignishandler) BeiSchlüsselAufwärts(schlüssel byte) {
}

type TTastaturTreiber struct {
	TUnterbrechunghandler
}

var aktivTastaturTreiber *TTastaturTreiber
var unterbrechunghandler func(uint32) uint32

var datenAnschluss_2 uint16 = 0x60
var befehlAnschluss_2 uint16 = 0x64

const ps2WartenBeschränkung = 100000

func wartenps2EingabeLeer() bool {
	for i := 0; i < ps2WartenBeschränkung; i++ {
		if (AnschlussLesenByte(befehlAnschluss_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func wartenps2AusgabeStark() bool {
	for i := 0; i < ps2WartenBeschränkung; i++ {
		if (AnschlussLesenByte(befehlAnschluss_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func schreibenps2Befehl(wert uint8) bool {
	if !wartenps2EingabeLeer() {
		return false
	}
	AnschlussSchreibenByte(befehlAnschluss_2, wert)
	return true
}

func schreibenps2Daten(wert uint8) bool {
	if !wartenps2EingabeLeer() {
		return false
	}
	AnschlussSchreibenByte(datenAnschluss_2, wert)
	return true
}

func lesenps2Daten() (uint8, bool) {
	if !wartenps2AusgabeStark() {
		return 0, false
	}
	return AnschlussLesenByte(datenAnschluss_2), true
}

func (selbst *TTastaturTreiber) InitTreiber(verwalter *TUnterbrechungVerwalter, tastaturEreignishandler ITastaturEreignishandler) {

	iTastaturEreignishandler = &standardTastaturEreignishandler
	if tastaturEreignishandler != nil {
		iTastaturEreignishandler = tastaturEreignishandler
	}

	aktivTastaturTreiber = selbst
	unterbrechunghandler = griffTastaturUnterbrechung
	var address uintptr
	address = uintptr(Pointer(&unterbrechunghandler))

	selbst.Init(0x21, uintptr(Pointer(verwalter)), address)

	for i := 0; i < 32 && (AnschlussLesenByte(befehlAnschluss_2)&0x01) != 0; i++ {
		AnschlussLesenByte(datenAnschluss_2)
	}

	if !schreibenps2Befehl(0xAE) || !schreibenps2Befehl(0x20) {
		return
	}
	status, bestätigen := lesenps2Daten()
	if !bestätigen {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !schreibenps2Befehl(0x60) || !schreibenps2Daten(status) {
		return
	}

	if !schreibenps2Daten(0xF4) {
		return
	}
	ack, bestätigen := lesenps2Daten()
	if !bestätigen || ack != 0xFA {
		return
	}

}

func griffTastaturUnterbrechung(esp uint32) uint32 {
	if aktivTastaturTreiber == nil {
		AnschlussLesenByte(datenAnschluss_2)
		return esp
	}
	return aktivTastaturTreiber.GriffUnterbrechung(esp)
}

const tastaturWarteschlangeGröße = 64

var tastaturWarteschlange [tastaturWarteschlangeGröße]byte
var tastaturWarteschlangeLesen uint8
var tastaturWarteschlangeSchreiben uint8
var linksUmschalt bool
var rechtsUmschalt bool
var extendedEinlesencode bool

func warteschlangeTastaturByte(schlüssel byte) {
	weiter := (tastaturWarteschlangeSchreiben + 1) % tastaturWarteschlangeGröße
	if weiter == tastaturWarteschlangeLesen {
		return
	}
	tastaturWarteschlange[tastaturWarteschlangeSchreiben] = schlüssel
	tastaturWarteschlangeSchreiben = weiter
}

func ProzessausstehendTastaturEreignisse() {
	for tastaturWarteschlangeLesen != tastaturWarteschlangeSchreiben {
		schlüssel := tastaturWarteschlange[tastaturWarteschlangeLesen]
		tastaturWarteschlangeLesen = (tastaturWarteschlangeLesen + 1) % tastaturWarteschlangeGröße
		StdinputByte(schlüssel)
		if iTastaturEreignishandler != nil {
			iTastaturEreignishandler.BeiSchlüsselAbwärts(schlüssel)
		}
	}
}

func einlesencodetoByte(einlesencode uint8) (byte, bool) {
	umschalt := linksUmschalt || rechtsUmschalt

	if einlesencode >= 0x02 && einlesencode <= 0x0B {
		if umschalt {
			return "!@#$%^&*()"[einlesencode-0x02], true
		}
		return "1234567890"[einlesencode-0x02], true
	}
	if einlesencode >= 0x10 && einlesencode <= 0x19 {
		schlüssel := "qwertyuiop"[einlesencode-0x10]
		if umschalt {
			schlüssel -= 'a' - 'A'
		}
		return schlüssel, true
	}
	if einlesencode >= 0x1E && einlesencode <= 0x26 {
		schlüssel := "asdfghjkl"[einlesencode-0x1E]
		if umschalt {
			schlüssel -= 'a' - 'A'
		}
		return schlüssel, true
	}
	if einlesencode >= 0x2C && einlesencode <= 0x32 {
		schlüssel := "zxcvbnm"[einlesencode-0x2C]
		if umschalt {
			schlüssel -= 'a' - 'A'
		}
		return schlüssel, true
	}

	switch einlesencode {
	case 0x0C:
		if umschalt {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if umschalt {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if umschalt {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if umschalt {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if umschalt {
			return ':', true
		}
		return ';', true
	case 0x28:
		if umschalt {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if umschalt {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if umschalt {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if umschalt {
			return '<', true
		}
		return ',', true
	case 0x34:
		if umschalt {
			return '>', true
		}
		return '.', true
	case 0x35:
		if umschalt {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (selbst *TTastaturTreiber) GriffUnterbrechung(esp uint32) uint32 {
	status := AnschlussLesenByte(befehlAnschluss_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	einlesencode := AnschlussLesenByte(datenAnschluss_2)
	if einlesencode == 0xE0 {
		extendedEinlesencode = true
		return esp
	}
	if extendedEinlesencode {
		extendedEinlesencode = false
		return esp
	}

	released := (einlesencode & 0x80) != 0
	basecode := einlesencode & 0x7F
	if basecode == 0x2A {
		linksUmschalt = !released
		return esp
	}
	if basecode == 0x36 {
		rechtsUmschalt = !released
		return esp
	}
	if released {
		return esp
	}

	if schlüssel, bestätigen := einlesencodetoByte(basecode); bestätigen {
		warteschlangeTastaturByte(schlüssel)
	}

	return esp
}
