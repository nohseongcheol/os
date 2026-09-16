/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package uitvoerbaar_en_koppelbaar_formaat

import . "unsafe"
import . "console"

import mem "geheugenmanager"

type Koppeling struct {
	Dynamisch	uintptr
	Previous	*Koppeling
	Volgende	*Koppeling
}
type Koppelingmap struct {
	First	*Koppeling
	Laatst	*Koppeling

	Grootte_2	int

	mem	*mem.TGeheugenmanager
}

func (zelf *Koppelingmap) Init(mem *mem.TGeheugenmanager) {
	zelf.mem = mem
}
func (zelf *Koppelingmap) Clone() Koppelingmap {
	var koppelingmap Koppelingmap

	koppelingmap.Init(zelf.mem)

	Koppeling := zelf.First

	for ; Koppeling != nil; Koppeling = Koppeling.Volgende {
		koppelingmap.Achteraan_toevoegen(Koppeling.Dynamisch)
	}
	return koppelingmap
}
func (zelf *Koppelingmap) Vooraan_toevoegen(Dynamisch uintptr) {
	nieuwKoppeling := (*Koppeling)(zelf.mem.Geheugen_toewijzen(uint32(Sizeof(Koppeling{}))))
	nieuwKoppeling.Dynamisch = Dynamisch
	nieuwKoppeling.Volgende = zelf.First
	zelf.First = nieuwKoppeling
	zelf.Grootte_2++

	if zelf.First.Volgende == nil {
		zelf.Laatst = zelf.First
	}
}
func (zelf *Koppelingmap) Achteraan_toevoegen(Dynamisch uintptr) {
	if Dynamisch == 0 {
		return
	}

	if zelf.Grootte_2 == 0 {
		zelf.Vooraan_toevoegen(Dynamisch)
	} else {
		nieuwKoppeling := (*Koppeling)(zelf.mem.Geheugen_toewijzen(uint32(Sizeof(Koppeling{}))))
		nieuwKoppeling.Dynamisch = Dynamisch
		nieuwKoppeling.Volgende = nil
		zelf.Laatst.Volgende = nieuwKoppeling
		zelf.Laatst = nieuwKoppeling
		zelf.Grootte_2++
	}
}
func (zelf *Koppelingmap) Afdrukken(x uint16, y uint16) {
	Koppeling := zelf.First
	console_2 := TConsole{}
	console_2.MAfdrukkenxy("linkmap : ", x, y)
	for ; Koppeling != nil; Koppeling = Koppeling.Volgende {
		console_2.MUnsignedinteger32Afdrukken(uint32(Koppeling.Dynamisch))
		console_2.MAfdrukken("+")

	}
}
