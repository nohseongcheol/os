package elf

import . "unsafe"
import . "konsolë"

import mem "memoriaManazhuesi"

type Lidhje struct {
	Dynamic		uintptr
	Previous	*Lidhje
	Pasuesen	*Lidhje
}
type Lidhjemap struct {
	First	*Lidhje
	Efundit	*Lidhje

	Madhësia_2	int

	mem	*mem.TMemoriaManazhuesi
}

func (vetvetja *Lidhjemap) Init(mem *mem.TMemoriaManazhuesi) {
	vetvetja.mem = mem
}
func (vetvetja *Lidhjemap) Clone() Lidhjemap {
	var lidhjemap Lidhjemap

	lidhjemap.Init(vetvetja.mem)

	Lidhje := vetvetja.First

	for ; Lidhje != nil; Lidhje = Lidhje.Pasuesen {
		lidhjemap.Append_to_list(Lidhje.Dynamic)
	}
	return lidhjemap
}
func (vetvetja *Lidhjemap) Prepend_to_list(Dynamic uintptr) {
	iRiLidhje := (*Lidhje)(vetvetja.mem.Malloc(uint32(Sizeof(Lidhje{}))))
	iRiLidhje.Dynamic = Dynamic
	iRiLidhje.Pasuesen = vetvetja.First
	vetvetja.First = iRiLidhje
	vetvetja.Madhësia_2++

	if vetvetja.First.Pasuesen == nil {
		vetvetja.Efundit = vetvetja.First
	}
}
func (vetvetja *Lidhjemap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if vetvetja.Madhësia_2 == 0 {
		vetvetja.Prepend_to_list(Dynamic)
	} else {
		iRiLidhje := (*Lidhje)(vetvetja.mem.Malloc(uint32(Sizeof(Lidhje{}))))
		iRiLidhje.Dynamic = Dynamic
		iRiLidhje.Pasuesen = nil
		vetvetja.Efundit.Pasuesen = iRiLidhje
		vetvetja.Efundit = iRiLidhje
		vetvetja.Madhësia_2++
	}
}
func (vetvetja *Lidhjemap) Printo(x uint16, y uint16) {
	Lidhje := vetvetja.First
	konsolë_2 := TKonsolë{}
	konsolë_2.MPrintoxy("linkmap : ", x, y)
	for ; Lidhje != nil; Lidhje = Lidhje.Pasuesen {
		konsolë_2.MUnsignedinteger32Printo(uint32(Lidhje.Dynamic))
		konsolë_2.MPrinto("+")

	}
}
