/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "konsoly"

import mem "arikaMpandrindra"

type Rohy struct {
	Dynamic		uintptr
	Previous	*Rohy
	Manaraka	*Rohy
}
type Rohymap struct {
	First	*Rohy
	Last	*Rohy

	Habe_2	int

	mem	*mem.TArikaMpandrindra
}

func (nytena *Rohymap) Init(mem *mem.TArikaMpandrindra) {
	nytena.mem = mem
}
func (nytena *Rohymap) Clone() Rohymap {
	var rohymap Rohymap

	rohymap.Init(nytena.mem)

	Rohy := nytena.First

	for ; Rohy != nil; Rohy = Rohy.Manaraka {
		rohymap.Append_to_list(Rohy.Dynamic)
	}
	return rohymap
}
func (nytena *Rohymap) Prepend_to_list(Dynamic uintptr) {
	vaovaorohy := (*Rohy)(nytena.mem.Malloc(uint32(Sizeof(Rohy{}))))
	vaovaorohy.Dynamic = Dynamic
	vaovaorohy.Manaraka = nytena.First
	nytena.First = vaovaorohy
	nytena.Habe_2++

	if nytena.First.Manaraka == nil {
		nytena.Last = nytena.First
	}
}
func (nytena *Rohymap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if nytena.Habe_2 == 0 {
		nytena.Prepend_to_list(Dynamic)
	} else {
		vaovaorohy := (*Rohy)(nytena.mem.Malloc(uint32(Sizeof(Rohy{}))))
		vaovaorohy.Dynamic = Dynamic
		vaovaorohy.Manaraka = nil
		nytena.Last.Manaraka = vaovaorohy
		nytena.Last = vaovaorohy
		nytena.Habe_2++
	}
}
func (nytena *Rohymap) Atontay(x uint16, y uint16) {
	Rohy := nytena.First
	konsoly_2 := TKonsoly{}
	konsoly_2.MAtontayxy("linkmap : ", x, y)
	for ; Rohy != nil; Rohy = Rohy.Manaraka {
		konsoly_2.MUnsignedinteger32Atontay(uint32(Rohy.Dynamic))
		konsoly_2.MAtontay("+")

	}
}
