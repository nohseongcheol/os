package elf

import . "unsafe"
import . "console"

import mem "atmintismanager"

type Nuoroda struct {
	Dinaminis	uintptr
	Previous	*Nuoroda
	Kitas		*Nuoroda
}
type Nuorodamap struct {
	First		*Nuoroda
	Paskutinis	*Nuoroda

	Dydis_2	int

	mem	*mem.TAtmintismanager
}

func (self *Nuorodamap) Init(mem *mem.TAtmintismanager) {
	self.mem = mem
}
func (self *Nuorodamap) Clone() Nuorodamap {
	var nuorodamap Nuorodamap

	nuorodamap.Init(self.mem)

	Nuoroda := self.First

	for ; Nuoroda != nil; Nuoroda = Nuoroda.Kitas {
		nuorodamap.Append_to_list(Nuoroda.Dinaminis)
	}
	return nuorodamap
}
func (self *Nuorodamap) Prepend_to_list(Dinaminis uintptr) {
	naujasNuoroda := (*Nuoroda)(self.mem.Malloc(uint32(Sizeof(Nuoroda{}))))
	naujasNuoroda.Dinaminis = Dinaminis
	naujasNuoroda.Kitas = self.First
	self.First = naujasNuoroda
	self.Dydis_2++

	if self.First.Kitas == nil {
		self.Paskutinis = self.First
	}
}
func (self *Nuorodamap) Append_to_list(Dinaminis uintptr) {
	if Dinaminis == 0 {
		return
	}

	if self.Dydis_2 == 0 {
		self.Prepend_to_list(Dinaminis)
	} else {
		naujasNuoroda := (*Nuoroda)(self.mem.Malloc(uint32(Sizeof(Nuoroda{}))))
		naujasNuoroda.Dinaminis = Dinaminis
		naujasNuoroda.Kitas = nil
		self.Paskutinis.Kitas = naujasNuoroda
		self.Paskutinis = naujasNuoroda
		self.Dydis_2++
	}
}
func (self *Nuorodamap) Spausdinti(x uint16, y uint16) {
	Nuoroda := self.First
	console_2 := TConsole{}
	console_2.MSpausdintixy("linkmap : ", x, y)
	for ; Nuoroda != nil; Nuoroda = Nuoroda.Kitas {
		console_2.MUnsignedinteger32Spausdinti(uint32(Nuoroda.Dinaminis))
		console_2.MSpausdinti("+")

	}
}
