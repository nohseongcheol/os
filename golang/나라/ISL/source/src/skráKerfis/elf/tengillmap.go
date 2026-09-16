/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "minnimanager"

type Tengill struct {
	Breytilegt	uintptr
	Previous	*Tengill
	Næsta		*Tengill
}
type Tengillmap struct {
	First	*Tengill
	Síðasta	*Tengill

	Stærð_2	int

	mem	*mem.TMinnimanager
}

func (sjálft *Tengillmap) Init(mem *mem.TMinnimanager) {
	sjálft.mem = mem
}
func (sjálft *Tengillmap) Clone() Tengillmap {
	var tengillmap Tengillmap

	tengillmap.Init(sjálft.mem)

	Tengill := sjálft.First

	for ; Tengill != nil; Tengill = Tengill.Næsta {
		tengillmap.Append_to_list(Tengill.Breytilegt)
	}
	return tengillmap
}
func (sjálft *Tengillmap) Prepend_to_list(Breytilegt uintptr) {
	nýttTengill := (*Tengill)(sjálft.mem.Malloc(uint32(Sizeof(Tengill{}))))
	nýttTengill.Breytilegt = Breytilegt
	nýttTengill.Næsta = sjálft.First
	sjálft.First = nýttTengill
	sjálft.Stærð_2++

	if sjálft.First.Næsta == nil {
		sjálft.Síðasta = sjálft.First
	}
}
func (sjálft *Tengillmap) Append_to_list(Breytilegt uintptr) {
	if Breytilegt == 0 {
		return
	}

	if sjálft.Stærð_2 == 0 {
		sjálft.Prepend_to_list(Breytilegt)
	} else {
		nýttTengill := (*Tengill)(sjálft.mem.Malloc(uint32(Sizeof(Tengill{}))))
		nýttTengill.Breytilegt = Breytilegt
		nýttTengill.Næsta = nil
		sjálft.Síðasta.Næsta = nýttTengill
		sjálft.Síðasta = nýttTengill
		sjálft.Stærð_2++
	}
}
func (sjálft *Tengillmap) Prenta(x uint16, y uint16) {
	Tengill := sjálft.First
	console_2 := TConsole{}
	console_2.MPrentaxy("linkmap : ", x, y)
	for ; Tengill != nil; Tengill = Tengill.Næsta {
		console_2.MUnsignedinteger32Prenta(uint32(Tengill.Breytilegt))
		console_2.MPrenta("+")

	}
}
