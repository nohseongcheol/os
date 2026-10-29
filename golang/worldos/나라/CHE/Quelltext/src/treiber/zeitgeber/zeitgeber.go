/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package zeitgeber

import . "unsafe"

import . "unterbrechung"
import . "konsole"

type IZeitgeberEreignishandler interface {
	Beitick()
}

var iZeitgeberEreignishandler IZeitgeberEreignishandler

type TStandardZeitgeberEreignishandler struct {
}

func (selbst *TStandardZeitgeberEreignishandler) Beitick() {
}

type TZeitgeberTreiber struct {
	TUnterbrechunghandler
}

var unterbrechunghandler func(*TZeitgeberTreiber, uint32) uint32

func (selbst *TZeitgeberTreiber) Init(verwalter *TUnterbrechungVerwalter, tastaturEreignishandler IZeitgeberEreignishandler) {
	iZeitgeberEreignishandler = &TStandardZeitgeberEreignishandler{}
	if tastaturEreignishandler != nil {
		iZeitgeberEreignishandler = tastaturEreignishandler
	}

	unterbrechunghandler = (*TZeitgeberTreiber).GriffUnterbrechung
	var address uintptr
	address = uintptr(Pointer(&unterbrechunghandler))

	selbst.TUnterbrechunghandler.Init(0x20, uintptr(Pointer(verwalter)), address)

}

var tickAnzahl uint32 = 0

func (selbst *TZeitgeberTreiber) GriffUnterbrechung(esp uint32) uint32 {
	konsole_2 := TKonsole{}
	konsole_2.MUnsignedinteger32Druckenxy(tickAnzahl, 3, 1)
	tickAnzahl++

	return esp
}
