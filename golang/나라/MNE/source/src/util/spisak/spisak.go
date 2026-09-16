/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package spisak

import . "unsafe"
import . "конзола"
import mem "memorijamanager"

type Чвор struct {
	pokazivač	uintptr
	previous	*Чвор
	следеће		*Чвор
}

type LinkedSpisak struct {
	head		*Чвор
	tail		*Чвор
	Величина_2	int

	mem	*mem.TMemorijamanager
}

func (isti *LinkedSpisak) Init(mem *mem.TMemorijamanager) {
	isti.head = nil
	isti.tail = nil
	isti.Величина_2 = 0

	isti.mem = mem
}
func (isti *LinkedSpisak) Prepend_to_list(pokazivač uintptr) {
	новаЧвор := (*Чвор)(isti.mem.Malloc(uint32(Sizeof(Чвор{}))))
	if новаЧвор == nil {
		return
	}
	новаЧвор.pokazivač = pokazivač
	новаЧвор.previous = nil
	новаЧвор.следеће = isti.head
	if isti.head != nil {
		isti.head.previous = новаЧвор
	}
	isti.head = новаЧвор
	isti.Величина_2++

	if isti.head.следеће == nil {
		isti.tail = isti.head
	}

}
func (isti *LinkedSpisak) Append_to_list(pokazivač uintptr) {
	if isti.Величина_2 == 0 {
		isti.Prepend_to_list(pokazivač)
	} else {
		новаЧвор := (*Чвор)(isti.mem.Malloc(uint32(Sizeof(Чвор{}))))
		if новаЧвор == nil {
			return
		}
		новаЧвор.pokazivač = pokazivač
		новаЧвор.previous = isti.tail
		новаЧвор.следеће = nil
		isti.tail.следеће = новаЧвор
		isti.tail = новаЧвор
		isti.Величина_2++
	}
}
func (isti *LinkedSpisak) Insert_at_index(popis int, pokazivač uintptr) {
	if popis == 0 {
		isti.Prepend_to_list(pokazivač)
	} else {
		previousЧвор := isti.GetЧворat(popis - 1)
		следећеЧвор := previousЧвор.следеће
		новаЧвор := (*Чвор)(isti.mem.Malloc(uint32(Sizeof(Чвор{}))))
		if новаЧвор == nil {
			return
		}
		новаЧвор.pokazivač = pokazivač

		previousЧвор.следеће = новаЧвор
		новаЧвор.previous = previousЧвор
		новаЧвор.следеће = следећеЧвор
		if следећеЧвор != nil {
			следећеЧвор.previous = новаЧвор
		}

		isti.Величина_2++

		if новаЧвор.следеће == nil {
			isti.tail = новаЧвор
		}
	}
}
func (isti *LinkedSpisak) GetЧворat(popis int) *Чвор {
	if popis < 0 || popis >= isti.Величина_2 {
		return nil
	}
	var x *Чвор = isti.head
	for i := 0; i < popis; i++ {
		x = x.следеће
	}
	return x
}

func (isti *LinkedSpisak) СкупЧворat(popis int, pokazivač uintptr) {
	var x *Чвор = isti.head
	for i := 0; i < popis; i++ {
		x = x.следеће
	}
	if x != nil {
		x.pokazivač = pokazivač
	}
}
func (isti *LinkedSpisak) Getat(popis int) Pointer {
	чвор := isti.GetЧворat(popis)
	if чвор == nil {
		return nil
	}
	var pokazivač uintptr = чвор.pokazivač
	return Pointer(pokazivač)
}
func (isti *LinkedSpisak) Popisod(pokazivač uintptr) int {
	var n *Чвор = isti.head
	i := 0
	for ; i < isti.Величина_2; i++ {
		if pokazivač == n.pokazivač {
			return i
		}
		n = n.следеће
	}
	return -1
}
func (isti *LinkedSpisak) Уклони(pokazivač uintptr) {
	popis := isti.Popisod(pokazivač)
	if popis < 0 {
		return
	}
	isti.Уклониat(popis)
}
func (isti *LinkedSpisak) Уклониat(popis int) {
	if popis < 0 || popis >= isti.Величина_2 {
		return
	}
	чвор := isti.GetЧворat(popis)
	if чвор == nil {
		return
	}
	if чвор.previous != nil {
		чвор.previous.следеће = чвор.следеће
	} else {
		isti.head = чвор.следеће
	}
	if чвор.следеће != nil {
		чвор.следеће.previous = чвор.previous
	} else {
		isti.tail = чвор.previous
	}
	isti.Величина_2 = isti.Величина_2 - 1

	if isti.mem != nil {
		isti.mem.Slobodno(Pointer(чвор))
	}
}

var конзола_2 = TКонзола{}

func (isti *LinkedSpisak) Štampaj() {
	конзола_2.MŠtampajxy("LinkedList:", 1, 1)
	конзола_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(isti))))
	for i := 0; i < isti.Величина_2; i++ {
		чвор := (*Чвор)(isti.Getat(i))
		конзола_2.MUnsignedinteger32Štampaj(uint32(чвор.pokazivač))
		конзола_2.MŠtampaj(":")
	}
}
