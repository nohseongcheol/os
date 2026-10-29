/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "atmiņamanager"

type Saite struct {
	Dynamic		uintptr
	Previous	*Saite
	Nākamais	*Saite
}
type Saitemap struct {
	Pirmais		*Saite
	Pēdējais	*Saite

	Izmērs_2	int

	mem	*mem.TAtmiņamanager
}

func (pats *Saitemap) Init(mem *mem.TAtmiņamanager) {
	pats.mem = mem
}
func (pats *Saitemap) Clone() Saitemap {
	var saitemap Saitemap

	saitemap.Init(pats.mem)

	Saite := pats.Pirmais

	for ; Saite != nil; Saite = Saite.Nākamais {
		saitemap.Append_to_list(Saite.Dynamic)
	}
	return saitemap
}
func (pats *Saitemap) Prepend_to_list(Dynamic uintptr) {
	jaunsSaite := (*Saite)(pats.mem.Malloc(uint32(Sizeof(Saite{}))))
	jaunsSaite.Dynamic = Dynamic
	jaunsSaite.Nākamais = pats.Pirmais
	pats.Pirmais = jaunsSaite
	pats.Izmērs_2++

	if pats.Pirmais.Nākamais == nil {
		pats.Pēdējais = pats.Pirmais
	}
}
func (pats *Saitemap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if pats.Izmērs_2 == 0 {
		pats.Prepend_to_list(Dynamic)
	} else {
		jaunsSaite := (*Saite)(pats.mem.Malloc(uint32(Sizeof(Saite{}))))
		jaunsSaite.Dynamic = Dynamic
		jaunsSaite.Nākamais = nil
		pats.Pēdējais.Nākamais = jaunsSaite
		pats.Pēdējais = jaunsSaite
		pats.Izmērs_2++
	}
}
func (pats *Saitemap) Drukāt(x uint16, y uint16) {
	Saite := pats.Pirmais
	console_2 := TConsole{}
	console_2.MDrukātxy("linkmap : ", x, y)
	for ; Saite != nil; Saite = Saite.Nākamais {
		console_2.MUnsignedinteger32Drukāt(uint32(Saite.Dynamic))
		console_2.MDrukāt("+")

	}
}
