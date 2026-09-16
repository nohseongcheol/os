/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "memorijamanager"

type Veza struct {
	Dynamic		uintptr
	Previous	*Veza
	Sljedeće	*Veza
}
type Vezamap struct {
	First	*Veza
	Zadnja	*Veza

	Veličina_2	int

	mem	*mem.TMemorijamanager
}

func (self *Vezamap) Init(mem *mem.TMemorijamanager) {
	self.mem = mem
}
func (self *Vezamap) Clone() Vezamap {
	var vezamap Vezamap

	vezamap.Init(self.mem)

	Veza := self.First

	for ; Veza != nil; Veza = Veza.Sljedeće {
		vezamap.Append_to_list(Veza.Dynamic)
	}
	return vezamap
}
func (self *Vezamap) Prepend_to_list(Dynamic uintptr) {
	novaVeza := (*Veza)(self.mem.Malloc(uint32(Sizeof(Veza{}))))
	novaVeza.Dynamic = Dynamic
	novaVeza.Sljedeće = self.First
	self.First = novaVeza
	self.Veličina_2++

	if self.First.Sljedeće == nil {
		self.Zadnja = self.First
	}
}
func (self *Vezamap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Veličina_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		novaVeza := (*Veza)(self.mem.Malloc(uint32(Sizeof(Veza{}))))
		novaVeza.Dynamic = Dynamic
		novaVeza.Sljedeće = nil
		self.Zadnja.Sljedeće = novaVeza
		self.Zadnja = novaVeza
		self.Veličina_2++
	}
}
func (self *Vezamap) Štampaj(x uint16, y uint16) {
	Veza := self.First
	console_2 := TConsole{}
	console_2.MŠtampajxy("linkmap : ", x, y)
	for ; Veza != nil; Veza = Veza.Sljedeće {
		console_2.MUnsignedinteger32Štampaj(uint32(Veza.Dynamic))
		console_2.MŠtampaj("+")

	}
}
