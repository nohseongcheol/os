package elf

import . "unsafe"
import . "console"

import mem "memoriemanager"

type Legătură struct {
	Dinamică	uintptr
	Previous	*Legătură
	Înainte		*Legătură
}
type Legăturămap struct {
	First	*Legătură
	Ultima	*Legătură

	Mărime_2	int

	mem	*mem.TMemoriemanager
}

func (sine *Legăturămap) Init(mem *mem.TMemoriemanager) {
	sine.mem = mem
}
func (sine *Legăturămap) Clone() Legăturămap {
	var legăturămap Legăturămap

	legăturămap.Init(sine.mem)

	Legătură := sine.First

	for ; Legătură != nil; Legătură = Legătură.Înainte {
		legăturămap.Append_to_list(Legătură.Dinamică)
	}
	return legăturămap
}
func (sine *Legăturămap) Prepend_to_list(Dinamică uintptr) {
	nouLegătură := (*Legătură)(sine.mem.Malloc(uint32(Sizeof(Legătură{}))))
	nouLegătură.Dinamică = Dinamică
	nouLegătură.Înainte = sine.First
	sine.First = nouLegătură
	sine.Mărime_2++

	if sine.First.Înainte == nil {
		sine.Ultima = sine.First
	}
}
func (sine *Legăturămap) Append_to_list(Dinamică uintptr) {
	if Dinamică == 0 {
		return
	}

	if sine.Mărime_2 == 0 {
		sine.Prepend_to_list(Dinamică)
	} else {
		nouLegătură := (*Legătură)(sine.mem.Malloc(uint32(Sizeof(Legătură{}))))
		nouLegătură.Dinamică = Dinamică
		nouLegătură.Înainte = nil
		sine.Ultima.Înainte = nouLegătură
		sine.Ultima = nouLegătură
		sine.Mărime_2++
	}
}
func (sine *Legăturămap) Tipărește(x uint16, y uint16) {
	Legătură := sine.First
	console_2 := TConsole{}
	console_2.MTipăreștexy("linkmap : ", x, y)
	for ; Legătură != nil; Legătură = Legătură.Înainte {
		console_2.MUnsignedinteger32Tipărește(uint32(Legătură.Dinamică))
		console_2.MTipărește("+")

	}
}
