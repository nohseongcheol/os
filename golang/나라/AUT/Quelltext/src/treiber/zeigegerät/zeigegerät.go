package tastatur

import . "unsafe"

import . "anschluss"
import . "unterbrechung"
import . "konsole"

type IMausEreignishandler interface {
	BeiMausAbwärts(knopf int8)
	BeiMausAufwärts(knopf int8)
	BeiMausVerschieben(x int8, y int8)
}

var iMausEreignishandler IMausEreignishandler

type TStandardMausEreignishandler struct {
}

var konsole_2 TKonsole = TKonsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (selbst TStandardMausEreignishandler) BeiMausAbwärts(knopf int8) {
	buffer := []byte("+")
	konsole_2.MDruckenxy(buffer, uint16(previousx), uint16(previousy))
}
func (selbst TStandardMausEreignishandler) BeiMausAufwärts(knopf int8)	{}
func (selbst TStandardMausEreignishandler) BeiMausVerschieben(x int8, y int8) {

	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 80 {
		xposition = 79
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 25 {
		yposition = 24
	}

	buffer := []byte(" ")
	konsole_2.MDruckenxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konsole_2.MDruckenxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TMausTreiber struct {
	TUnterbrechunghandler
}

var aktivMausTreiber *TMausTreiber
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

func sendenMausBefehl(wert uint8) bool {
	if !schreibenps2Befehl(0xD4) || !schreibenps2Daten(wert) {
		return false
	}
	ack, bestätigen := lesenps2Daten()
	return bestätigen && ack == 0xFA
}

func (selbst *TMausTreiber) InitTreiber(verwalter *TUnterbrechungVerwalter, mausEreignishandler IMausEreignishandler) {

	iMausEreignishandler = TStandardMausEreignishandler{}

	if mausEreignishandler != nil {
		iMausEreignishandler = mausEreignishandler
	}

	aktivMausTreiber = selbst
	unterbrechunghandler = griffMausUnterbrechung
	var address uintptr
	address = uintptr(Pointer(&unterbrechunghandler))
	selbst.Init(0x2C, uintptr(Pointer(verwalter)), address)

	for i := 0; i < 32 && (AnschlussLesenByte(befehlAnschluss_2)&0x01) != 0; i++ {
		AnschlussLesenByte(datenAnschluss_2)
	}

	if !schreibenps2Befehl(0xA8) || !schreibenps2Befehl(0x20) {
		return
	}
	status, bestätigen := lesenps2Daten()
	if !bestätigen {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !schreibenps2Befehl(0x60) || !schreibenps2Daten(status) {
		return
	}

	if !sendenMausBefehl(0xF6) || !sendenMausBefehl(0xF4) {
		return
	}
	versatz = 0

}

func griffMausUnterbrechung(esp uint32) uint32 {
	if aktivMausTreiber == nil {
		AnschlussLesenByte(datenAnschluss_2)
		return esp
	}
	return aktivMausTreiber.GriffUnterbrechung(esp)
}

var anzahl uint8 = 0
var buffer_2 [3]int8
var versatz uint8 = 0

var knopf_2 int8
var ausstehendx int16
var ausstehendy int16
var ausstehendKnopf int8
var ausstehendMausEreignis bool

func (selbst *TMausTreiber) GriffUnterbrechung(esp uint32) uint32 {
	status := AnschlussLesenByte(befehlAnschluss_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	daten := AnschlussLesenByte(datenAnschluss_2)

	if versatz == 0 && (daten&0x08) == 0 {
		return esp
	}
	buffer_2[versatz] = int8(daten)
	versatz = (versatz + 1) % 3
	if versatz == 0 {
		pAKETstatus := uint8(buffer_2[0])

		if (pAKETstatus & 0xC0) == 0 {
			ausstehendx += int16(buffer_2[1])
			ausstehendy += int16(buffer_2[2])
			if ausstehendx > 127 {
				ausstehendx = 127
			} else if ausstehendx < -127 {
				ausstehendx = -127
			}
			if ausstehendy > 127 {
				ausstehendy = 127
			} else if ausstehendy < -127 {
				ausstehendy = -127
			}
		}
		ausstehendKnopf = int8(pAKETstatus & 0x07)
		ausstehendMausEreignis = true
	}

	return esp

}

func ProzessausstehendMausEreignisse() {
	if iMausEreignishandler == nil {
		return
	}

	Unterbrechungdeactive()
	if !ausstehendMausEreignis {
		UnterbrechungAktiv()
		return
	}
	x := int8(ausstehendx)
	y := int8(ausstehendy)
	neuKnopf := ausstehendKnopf
	altKnopf := knopf_2

	ausstehendx = 0
	ausstehendy = 0
	ausstehendMausEreignis = false
	UnterbrechungAktiv()

	if x != 0 || y != 0 {
		iMausEreignishandler.BeiMausVerschieben(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maske := int8(0x1 << i)
		if (neuKnopf & maske) != (altKnopf & maske) {
			if (neuKnopf & maske) != 0 {
				iMausEreignishandler.BeiMausAbwärts(int8(i + 1))
			} else {
				iMausEreignishandler.BeiMausAufwärts(int8(i + 1))
			}
		}
	}
	knopf_2 = neuKnopf
}
