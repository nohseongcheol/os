/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "konzola"

import mem "memorijamanager"

type Veza struct {
	Rastegljivo	uintptr
	Previous	*Veza
	Sledeće		*Veza
}
type Vezamap struct {
	First	*Veza
	Zadnja	*Veza

	Veličina_2	int

	mem	*mem.TMemorijamanager
}

func (isti *Vezamap) Init(mem *mem.TMemorijamanager) {
	isti.mem = mem
}
func (isti *Vezamap) Clone() Vezamap {
	var vezamap Vezamap

	vezamap.Init(isti.mem)

	Veza := isti.First

	for ; Veza != nil; Veza = Veza.Sledeće {
		vezamap.Append_to_list(Veza.Rastegljivo)
	}
	return vezamap
}
func (isti *Vezamap) Prepend_to_list(Rastegljivo uintptr) {
	novaVeza := (*Veza)(isti.mem.Malloc(uint32(Sizeof(Veza{}))))
	novaVeza.Rastegljivo = Rastegljivo
	novaVeza.Sledeće = isti.First
	isti.First = novaVeza
	isti.Veličina_2++

	if isti.First.Sledeće == nil {
		isti.Zadnja = isti.First
	}
}
func (isti *Vezamap) Append_to_list(Rastegljivo uintptr) {
	if Rastegljivo == 0 {
		return
	}

	if isti.Veličina_2 == 0 {
		isti.Prepend_to_list(Rastegljivo)
	} else {
		novaVeza := (*Veza)(isti.mem.Malloc(uint32(Sizeof(Veza{}))))
		novaVeza.Rastegljivo = Rastegljivo
		novaVeza.Sledeće = nil
		isti.Zadnja.Sledeće = novaVeza
		isti.Zadnja = novaVeza
		isti.Veličina_2++
	}
}
func (isti *Vezamap) Štampaj(x uint16, y uint16) {
	Veza := isti.First
	konzola_2 := TKonzola{}
	konzola_2.MŠtampajxy("linkmap : ", x, y)
	for ; Veza != nil; Veza = Veza.Sledeće {
		konzola_2.MUnsignedinteger32Štampaj(uint32(Veza.Rastegljivo))
		konzola_2.MŠtampaj("+")

	}
}
