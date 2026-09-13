package elf

import . "unsafe"
import . "конзола"

import mem "memorijamanager"

type Веза struct {
	Rastegǉivo	uintptr
	Previous	*Веза
	Следеће		*Веза
}
type Везаmap struct {
	First	*Веза
	Задња	*Веза

	Величина_2	int

	mem	*mem.TMemorijamanager
}

func (isti *Везаmap) Init(mem *mem.TMemorijamanager) {
	isti.mem = mem
}
func (isti *Везаmap) Clone() Везаmap {
	var везаmap Везаmap

	везаmap.Init(isti.mem)

	Веза := isti.First

	for ; Веза != nil; Веза = Веза.Следеће {
		везаmap.Append_to_list(Веза.Rastegǉivo)
	}
	return везаmap
}
func (isti *Везаmap) Prepend_to_list(Rastegǉivo uintptr) {
	новаВеза := (*Веза)(isti.mem.Malloc(uint32(Sizeof(Веза{}))))
	новаВеза.Rastegǉivo = Rastegǉivo
	новаВеза.Следеће = isti.First
	isti.First = новаВеза
	isti.Величина_2++

	if isti.First.Следеће == nil {
		isti.Задња = isti.First
	}
}
func (isti *Везаmap) Append_to_list(Rastegǉivo uintptr) {
	if Rastegǉivo == 0 {
		return
	}

	if isti.Величина_2 == 0 {
		isti.Prepend_to_list(Rastegǉivo)
	} else {
		новаВеза := (*Веза)(isti.mem.Malloc(uint32(Sizeof(Веза{}))))
		новаВеза.Rastegǉivo = Rastegǉivo
		новаВеза.Следеће = nil
		isti.Задња.Следеће = новаВеза
		isti.Задња = новаВеза
		isti.Величина_2++
	}
}
func (isti *Везаmap) Štampaj(x uint16, y uint16) {
	Веза := isti.First
	конзола_2 := TКонзола{}
	конзола_2.MŠtampajxy("linkmap : ", x, y)
	for ; Веза != nil; Веза = Веза.Следеће {
		конзола_2.MUnsignedinteger32Štampaj(uint32(Веза.Rastegǉivo))
		конзола_2.MŠtampaj("+")

	}
}
