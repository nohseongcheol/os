package elf

import . "unsafe"
import . "consola"

import mem "memòriamanager"

type Enllaç struct {
	Dinàmic		uintptr
	Previous	*Enllaç
	Següent		*Enllaç
}
type Enllaçmap struct {
	First	*Enllaç
	Últim	*Enllaç

	Mida_2	int

	mem	*mem.TMemòriamanager
}

func (unmateix *Enllaçmap) Init(mem *mem.TMemòriamanager) {
	unmateix.mem = mem
}
func (unmateix *Enllaçmap) Clone() Enllaçmap {
	var enllaçmap Enllaçmap

	enllaçmap.Init(unmateix.mem)

	Enllaç := unmateix.First

	for ; Enllaç != nil; Enllaç = Enllaç.Següent {
		enllaçmap.Append_to_list(Enllaç.Dinàmic)
	}
	return enllaçmap
}
func (unmateix *Enllaçmap) Prepend_to_list(Dinàmic uintptr) {
	nouEnllaç := (*Enllaç)(unmateix.mem.Malloc(uint32(Sizeof(Enllaç{}))))
	nouEnllaç.Dinàmic = Dinàmic
	nouEnllaç.Següent = unmateix.First
	unmateix.First = nouEnllaç
	unmateix.Mida_2++

	if unmateix.First.Següent == nil {
		unmateix.Últim = unmateix.First
	}
}
func (unmateix *Enllaçmap) Append_to_list(Dinàmic uintptr) {
	if Dinàmic == 0 {
		return
	}

	if unmateix.Mida_2 == 0 {
		unmateix.Prepend_to_list(Dinàmic)
	} else {
		nouEnllaç := (*Enllaç)(unmateix.mem.Malloc(uint32(Sizeof(Enllaç{}))))
		nouEnllaç.Dinàmic = Dinàmic
		nouEnllaç.Següent = nil
		unmateix.Últim.Següent = nouEnllaç
		unmateix.Últim = nouEnllaç
		unmateix.Mida_2++
	}
}
func (unmateix *Enllaçmap) Imprimeix(x uint16, y uint16) {
	Enllaç := unmateix.First
	consola_2 := TConsola{}
	consola_2.MImprimeixxy("linkmap : ", x, y)
	for ; Enllaç != nil; Enllaç = Enllaç.Següent {
		consola_2.MUnsignedinteger32Imprimeix(uint32(Enllaç.Dinàmic))
		consola_2.MImprimeix("+")

	}
}
