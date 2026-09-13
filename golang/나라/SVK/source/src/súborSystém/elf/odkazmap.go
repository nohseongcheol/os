package elf

import . "unsafe"
import . "konzola"

import mem "pamäťmanager"

type Odkaz struct {
	Dynamická	uintptr
	Previous	*Odkaz
	Nasledujúci	*Odkaz
}
type Odkazmap struct {
	First		*Odkaz
	Posledné	*Odkaz

	Veľkosť_2	int

	mem	*mem.TPamäťmanager
}

func (vlastný *Odkazmap) Init(mem *mem.TPamäťmanager) {
	vlastný.mem = mem
}
func (vlastný *Odkazmap) Clone() Odkazmap {
	var odkazmap Odkazmap

	odkazmap.Init(vlastný.mem)

	Odkaz := vlastný.First

	for ; Odkaz != nil; Odkaz = Odkaz.Nasledujúci {
		odkazmap.Append_to_list(Odkaz.Dynamická)
	}
	return odkazmap
}
func (vlastný *Odkazmap) Prepend_to_list(Dynamická uintptr) {
	novýOdkaz := (*Odkaz)(vlastný.mem.Malloc(uint32(Sizeof(Odkaz{}))))
	novýOdkaz.Dynamická = Dynamická
	novýOdkaz.Nasledujúci = vlastný.First
	vlastný.First = novýOdkaz
	vlastný.Veľkosť_2++

	if vlastný.First.Nasledujúci == nil {
		vlastný.Posledné = vlastný.First
	}
}
func (vlastný *Odkazmap) Append_to_list(Dynamická uintptr) {
	if Dynamická == 0 {
		return
	}

	if vlastný.Veľkosť_2 == 0 {
		vlastný.Prepend_to_list(Dynamická)
	} else {
		novýOdkaz := (*Odkaz)(vlastný.mem.Malloc(uint32(Sizeof(Odkaz{}))))
		novýOdkaz.Dynamická = Dynamická
		novýOdkaz.Nasledujúci = nil
		vlastný.Posledné.Nasledujúci = novýOdkaz
		vlastný.Posledné = novýOdkaz
		vlastný.Veľkosť_2++
	}
}
func (vlastný *Odkazmap) Tlačiť(x uint16, y uint16) {
	Odkaz := vlastný.First
	konzola_2 := TKonzola{}
	konzola_2.MTlačiťxy("linkmap : ", x, y)
	for ; Odkaz != nil; Odkaz = Odkaz.Nasledujúci {
		konzola_2.MUnsignedinteger32Tlačiť(uint32(Odkaz.Dynamická))
		konzola_2.MTlačiť("+")

	}
}
