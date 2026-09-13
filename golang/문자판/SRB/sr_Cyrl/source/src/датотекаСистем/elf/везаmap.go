package elf

import . "unsafe"
import . "конзола"

import mem "меморијаmanager"

type Веза struct {
	Растегљиво	uintptr
	Previous	*Веза
	Следеће		*Веза
}
type Везаmap struct {
	First	*Веза
	Задња	*Веза

	Величина_2	int

	mem	*mem.TМеморијаmanager
}

func (исти *Везаmap) Init(mem *mem.TМеморијаmanager) {
	исти.mem = mem
}
func (исти *Везаmap) Clone() Везаmap {
	var везаmap Везаmap

	везаmap.Init(исти.mem)

	Веза := исти.First

	for ; Веза != nil; Веза = Веза.Следеће {
		везаmap.Append_to_list(Веза.Растегљиво)
	}
	return везаmap
}
func (исти *Везаmap) Prepend_to_list(Растегљиво uintptr) {
	новаВеза := (*Веза)(исти.mem.Malloc(uint32(Sizeof(Веза{}))))
	новаВеза.Растегљиво = Растегљиво
	новаВеза.Следеће = исти.First
	исти.First = новаВеза
	исти.Величина_2++

	if исти.First.Следеће == nil {
		исти.Задња = исти.First
	}
}
func (исти *Везаmap) Append_to_list(Растегљиво uintptr) {
	if Растегљиво == 0 {
		return
	}

	if исти.Величина_2 == 0 {
		исти.Prepend_to_list(Растегљиво)
	} else {
		новаВеза := (*Веза)(исти.mem.Malloc(uint32(Sizeof(Веза{}))))
		новаВеза.Растегљиво = Растегљиво
		новаВеза.Следеће = nil
		исти.Задња.Следеће = новаВеза
		исти.Задња = новаВеза
		исти.Величина_2++
	}
}
func (исти *Везаmap) Штампај(x uint16, y uint16) {
	Веза := исти.First
	конзола_2 := TКонзола{}
	конзола_2.MШтампајxy("linkmap : ", x, y)
	for ; Веза != nil; Веза = Веза.Следеће {
		конзола_2.MUnsignedinteger32Штампај(uint32(Веза.Растегљиво))
		конзола_2.MШтампај("+")

	}
}
