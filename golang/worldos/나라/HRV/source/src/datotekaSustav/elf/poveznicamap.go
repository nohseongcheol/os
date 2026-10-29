/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "memorijamanager"

type Poveznica struct {
	Dinamično	uintptr
	Previous	*Poveznica
	Slijedeće	*Poveznica
}
type Poveznicamap struct {
	First	*Poveznica
	Zadnje	*Poveznica

	Veličina_2	int

	mem	*mem.TMemorijamanager
}

func (sam *Poveznicamap) Init(mem *mem.TMemorijamanager) {
	sam.mem = mem
}
func (sam *Poveznicamap) Clone() Poveznicamap {
	var poveznicamap Poveznicamap

	poveznicamap.Init(sam.mem)

	Poveznica := sam.First

	for ; Poveznica != nil; Poveznica = Poveznica.Slijedeće {
		poveznicamap.Append_to_list(Poveznica.Dinamično)
	}
	return poveznicamap
}
func (sam *Poveznicamap) Prepend_to_list(Dinamično uintptr) {
	noviPoveznica := (*Poveznica)(sam.mem.Malloc(uint32(Sizeof(Poveznica{}))))
	noviPoveznica.Dinamično = Dinamično
	noviPoveznica.Slijedeće = sam.First
	sam.First = noviPoveznica
	sam.Veličina_2++

	if sam.First.Slijedeće == nil {
		sam.Zadnje = sam.First
	}
}
func (sam *Poveznicamap) Append_to_list(Dinamično uintptr) {
	if Dinamično == 0 {
		return
	}

	if sam.Veličina_2 == 0 {
		sam.Prepend_to_list(Dinamično)
	} else {
		noviPoveznica := (*Poveznica)(sam.mem.Malloc(uint32(Sizeof(Poveznica{}))))
		noviPoveznica.Dinamično = Dinamično
		noviPoveznica.Slijedeće = nil
		sam.Zadnje.Slijedeće = noviPoveznica
		sam.Zadnje = noviPoveznica
		sam.Veličina_2++
	}
}
func (sam *Poveznicamap) Ispis(x uint16, y uint16) {
	Poveznica := sam.First
	console_2 := TConsole{}
	console_2.MIspisxy("linkmap : ", x, y)
	for ; Poveznica != nil; Poveznica = Poveznica.Slijedeće {
		console_2.MUnsignedinteger32Ispis(uint32(Poveznica.Dinamično))
		console_2.MIspis("+")

	}
}
