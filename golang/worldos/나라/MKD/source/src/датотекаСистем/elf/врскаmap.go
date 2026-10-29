/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "меморијаmanager"

type Врска struct {
	Dynamic		uintptr
	Previous	*Врска
	Следна		*Врска
}
type Врскаmap struct {
	First		*Врска
	Последно	*Врска

	Големина_2	int

	mem	*mem.TМеморијаmanager
}

func (само *Врскаmap) Init(mem *mem.TМеморијаmanager) {
	само.mem = mem
}
func (само *Врскаmap) Clone() Врскаmap {
	var врскаmap Врскаmap

	врскаmap.Init(само.mem)

	Врска := само.First

	for ; Врска != nil; Врска = Врска.Следна {
		врскаmap.Append_to_list(Врска.Dynamic)
	}
	return врскаmap
}
func (само *Врскаmap) Prepend_to_list(Dynamic uintptr) {
	новВрска := (*Врска)(само.mem.Malloc(uint32(Sizeof(Врска{}))))
	новВрска.Dynamic = Dynamic
	новВрска.Следна = само.First
	само.First = новВрска
	само.Големина_2++

	if само.First.Следна == nil {
		само.Последно = само.First
	}
}
func (само *Врскаmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if само.Големина_2 == 0 {
		само.Prepend_to_list(Dynamic)
	} else {
		новВрска := (*Врска)(само.mem.Malloc(uint32(Sizeof(Врска{}))))
		новВрска.Dynamic = Dynamic
		новВрска.Следна = nil
		само.Последно.Следна = новВрска
		само.Последно = новВрска
		само.Големина_2++
	}
}
func (само *Врскаmap) Печати(x uint16, y uint16) {
	Врска := само.First
	console_2 := TConsole{}
	console_2.MПечатиxy("linkmap : ", x, y)
	for ; Врска != nil; Врска = Врска.Следна {
		console_2.MUnsignedinteger32Печати(uint32(Врска.Dynamic))
		console_2.MПечати("+")

	}
}
