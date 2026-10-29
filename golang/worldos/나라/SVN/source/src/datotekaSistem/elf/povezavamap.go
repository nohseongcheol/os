/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "pomnilnikmanager"

type Povezava struct {
	Dinamično	uintptr
	Previous	*Povezava
	Naslednje	*Povezava
}
type Povezavamap struct {
	Prvi	*Povezava
	Zadnji	*Povezava

	Velikost_2	int

	mem	*mem.TPomnilnikmanager
}

func (sam *Povezavamap) Init(mem *mem.TPomnilnikmanager) {
	sam.mem = mem
}
func (sam *Povezavamap) Clone() Povezavamap {
	var povezavamap Povezavamap

	povezavamap.Init(sam.mem)

	Povezava := sam.Prvi

	for ; Povezava != nil; Povezava = Povezava.Naslednje {
		povezavamap.Append_to_list(Povezava.Dinamično)
	}
	return povezavamap
}
func (sam *Povezavamap) Prepend_to_list(Dinamično uintptr) {
	novaPovezava := (*Povezava)(sam.mem.Malloc(uint32(Sizeof(Povezava{}))))
	novaPovezava.Dinamično = Dinamično
	novaPovezava.Naslednje = sam.Prvi
	sam.Prvi = novaPovezava
	sam.Velikost_2++

	if sam.Prvi.Naslednje == nil {
		sam.Zadnji = sam.Prvi
	}
}
func (sam *Povezavamap) Append_to_list(Dinamično uintptr) {
	if Dinamično == 0 {
		return
	}

	if sam.Velikost_2 == 0 {
		sam.Prepend_to_list(Dinamično)
	} else {
		novaPovezava := (*Povezava)(sam.mem.Malloc(uint32(Sizeof(Povezava{}))))
		novaPovezava.Dinamično = Dinamično
		novaPovezava.Naslednje = nil
		sam.Zadnji.Naslednje = novaPovezava
		sam.Zadnji = novaPovezava
		sam.Velikost_2++
	}
}
func (sam *Povezavamap) Natisni(x uint16, y uint16) {
	Povezava := sam.Prvi
	console_2 := TConsole{}
	console_2.MNatisnixy("linkmap : ", x, y)
	for ; Povezava != nil; Povezava = Povezava.Naslednje {
		console_2.MUnsignedinteger32Natisni(uint32(Povezava.Dinamično))
		console_2.MNatisni("+")

	}
}
