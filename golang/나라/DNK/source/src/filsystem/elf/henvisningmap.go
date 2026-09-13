package elf

import . "unsafe"
import . "console"

import mem "hukommelsemanager"

type Henvisning struct {
	Dynamisk	uintptr
	Previous	*Henvisning
	Næste		*Henvisning
}
type Henvisningmap struct {
	First	*Henvisning
	Sidste	*Henvisning

	Størrelse_2	int

	mem	*mem.THukommelsemanager
}

func (selv *Henvisningmap) Init(mem *mem.THukommelsemanager) {
	selv.mem = mem
}
func (selv *Henvisningmap) Clone() Henvisningmap {
	var henvisningmap Henvisningmap

	henvisningmap.Init(selv.mem)

	Henvisning := selv.First

	for ; Henvisning != nil; Henvisning = Henvisning.Næste {
		henvisningmap.Append_to_list(Henvisning.Dynamisk)
	}
	return henvisningmap
}
func (selv *Henvisningmap) Prepend_to_list(Dynamisk uintptr) {
	nyHenvisning := (*Henvisning)(selv.mem.Malloc(uint32(Sizeof(Henvisning{}))))
	nyHenvisning.Dynamisk = Dynamisk
	nyHenvisning.Næste = selv.First
	selv.First = nyHenvisning
	selv.Størrelse_2++

	if selv.First.Næste == nil {
		selv.Sidste = selv.First
	}
}
func (selv *Henvisningmap) Append_to_list(Dynamisk uintptr) {
	if Dynamisk == 0 {
		return
	}

	if selv.Størrelse_2 == 0 {
		selv.Prepend_to_list(Dynamisk)
	} else {
		nyHenvisning := (*Henvisning)(selv.mem.Malloc(uint32(Sizeof(Henvisning{}))))
		nyHenvisning.Dynamisk = Dynamisk
		nyHenvisning.Næste = nil
		selv.Sidste.Næste = nyHenvisning
		selv.Sidste = nyHenvisning
		selv.Størrelse_2++
	}
}
func (selv *Henvisningmap) Udskriv(x uint16, y uint16) {
	Henvisning := selv.First
	console_2 := TConsole{}
	console_2.MUdskrivxy("linkmap : ", x, y)
	for ; Henvisning != nil; Henvisning = Henvisning.Næste {
		console_2.MUnsignedinteger32Udskriv(uint32(Henvisning.Dynamisk))
		console_2.MUdskriv("+")

	}
}
