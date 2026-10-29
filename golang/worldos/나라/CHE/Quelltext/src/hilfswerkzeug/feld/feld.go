/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package feld

import . "unsafe"
import . "konsole"

var knotenFeld [100]uintptr

type TFeld struct {
	Größe_2 int
}

func (selbst *TFeld) Hinzufügen(adressverweis uintptr) {
	knotenFeld[selbst.Größe_2] = adressverweis
	selbst.Größe_2++
}
func (selbst *TFeld) Getat(inhalt int) Pointer {
	return Pointer(knotenFeld[inhalt])
}
func (selbst *TFeld) Inhaltvon(adressverweis uintptr) int {
	i := 0
	for ; i < selbst.Größe_2; i++ {
		if adressverweis == knotenFeld[i] {
			return i
		}
	}
	return -1
}

var konsole_2 = TKonsole{}

func (selbst *TFeld) Drucken() {
	konsole_2.MDruckenxy("array:", 1, 1)

	for i := 0; i < selbst.Größe_2; i++ {
		konsole_2.MUnsignedinteger32Drucken(uint32(knotenFeld[i]))
		konsole_2.MDrucken(":")
	}
}
