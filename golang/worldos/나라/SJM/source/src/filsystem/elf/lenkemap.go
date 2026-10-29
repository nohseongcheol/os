/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "minnemanager"

type Lenke struct {
	Dynamisk	uintptr
	Previous	*Lenke
	Neste		*Lenke
}
type Lenkemap struct {
	First	*Lenke
	Siste	*Lenke

	Størrelse_2	int

	mem	*mem.TMinnemanager
}

func (selv *Lenkemap) Init(mem *mem.TMinnemanager) {
	selv.mem = mem
}
func (selv *Lenkemap) Clone() Lenkemap {
	var lenkemap Lenkemap

	lenkemap.Init(selv.mem)

	Lenke := selv.First

	for ; Lenke != nil; Lenke = Lenke.Neste {
		lenkemap.Append_to_list(Lenke.Dynamisk)
	}
	return lenkemap
}
func (selv *Lenkemap) Prepend_to_list(Dynamisk uintptr) {
	nyLenke := (*Lenke)(selv.mem.Malloc(uint32(Sizeof(Lenke{}))))
	nyLenke.Dynamisk = Dynamisk
	nyLenke.Neste = selv.First
	selv.First = nyLenke
	selv.Størrelse_2++

	if selv.First.Neste == nil {
		selv.Siste = selv.First
	}
}
func (selv *Lenkemap) Append_to_list(Dynamisk uintptr) {
	if Dynamisk == 0 {
		return
	}

	if selv.Størrelse_2 == 0 {
		selv.Prepend_to_list(Dynamisk)
	} else {
		nyLenke := (*Lenke)(selv.mem.Malloc(uint32(Sizeof(Lenke{}))))
		nyLenke.Dynamisk = Dynamisk
		nyLenke.Neste = nil
		selv.Siste.Neste = nyLenke
		selv.Siste = nyLenke
		selv.Størrelse_2++
	}
}
func (selv *Lenkemap) Skrivut(x uint16, y uint16) {
	Lenke := selv.First
	console_2 := TConsole{}
	console_2.MSkrivutxy("linkmap : ", x, y)
	for ; Lenke != nil; Lenke = Lenke.Neste {
		console_2.MUnsignedinteger32Skrivut(uint32(Lenke.Dynamisk))
		console_2.MSkrivut("+")

	}
}
