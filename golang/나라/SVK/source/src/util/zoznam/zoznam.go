/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package zoznam

import . "unsafe"
import . "konzola"
import mem "pamäťmanager"

type Uzol struct {
	kurzor		uintptr
	previous	*Uzol
	nasledujúci	*Uzol
}

type LinkedZoznam struct {
	head		*Uzol
	tail		*Uzol
	Veľkosť_2	int

	mem	*mem.TPamäťmanager
}

func (vlastný *LinkedZoznam) Init(mem *mem.TPamäťmanager) {
	vlastný.head = nil
	vlastný.tail = nil
	vlastný.Veľkosť_2 = 0

	vlastný.mem = mem
}
func (vlastný *LinkedZoznam) Prepend_to_list(kurzor uintptr) {
	novýUzol := (*Uzol)(vlastný.mem.Malloc(uint32(Sizeof(Uzol{}))))
	if novýUzol == nil {
		return
	}
	novýUzol.kurzor = kurzor
	novýUzol.previous = nil
	novýUzol.nasledujúci = vlastný.head
	if vlastný.head != nil {
		vlastný.head.previous = novýUzol
	}
	vlastný.head = novýUzol
	vlastný.Veľkosť_2++

	if vlastný.head.nasledujúci == nil {
		vlastný.tail = vlastný.head
	}

}
func (vlastný *LinkedZoznam) Append_to_list(kurzor uintptr) {
	if vlastný.Veľkosť_2 == 0 {
		vlastný.Prepend_to_list(kurzor)
	} else {
		novýUzol := (*Uzol)(vlastný.mem.Malloc(uint32(Sizeof(Uzol{}))))
		if novýUzol == nil {
			return
		}
		novýUzol.kurzor = kurzor
		novýUzol.previous = vlastný.tail
		novýUzol.nasledujúci = nil
		vlastný.tail.nasledujúci = novýUzol
		vlastný.tail = novýUzol
		vlastný.Veľkosť_2++
	}
}
func (vlastný *LinkedZoznam) Insert_at_index(index int, kurzor uintptr) {
	if index == 0 {
		vlastný.Prepend_to_list(kurzor)
	} else {
		previousUzol := vlastný.GetUzolat(index - 1)
		nasledujúciUzol := previousUzol.nasledujúci
		novýUzol := (*Uzol)(vlastný.mem.Malloc(uint32(Sizeof(Uzol{}))))
		if novýUzol == nil {
			return
		}
		novýUzol.kurzor = kurzor

		previousUzol.nasledujúci = novýUzol
		novýUzol.previous = previousUzol
		novýUzol.nasledujúci = nasledujúciUzol
		if nasledujúciUzol != nil {
			nasledujúciUzol.previous = novýUzol
		}

		vlastný.Veľkosť_2++

		if novýUzol.nasledujúci == nil {
			vlastný.tail = novýUzol
		}
	}
}
func (vlastný *LinkedZoznam) GetUzolat(index int) *Uzol {
	if index < 0 || index >= vlastný.Veľkosť_2 {
		return nil
	}
	var x *Uzol = vlastný.head
	for i := 0; i < index; i++ {
		x = x.nasledujúci
	}
	return x
}

func (vlastný *LinkedZoznam) SadaUzolat(index int, kurzor uintptr) {
	var x *Uzol = vlastný.head
	for i := 0; i < index; i++ {
		x = x.nasledujúci
	}
	if x != nil {
		x.kurzor = kurzor
	}
}
func (vlastný *LinkedZoznam) Getat(index int) Pointer {
	uzol := vlastný.GetUzolat(index)
	if uzol == nil {
		return nil
	}
	var kurzor uintptr = uzol.kurzor
	return Pointer(kurzor)
}
func (vlastný *LinkedZoznam) Indexz(kurzor uintptr) int {
	var n *Uzol = vlastný.head
	i := 0
	for ; i < vlastný.Veľkosť_2; i++ {
		if kurzor == n.kurzor {
			return i
		}
		n = n.nasledujúci
	}
	return -1
}
func (vlastný *LinkedZoznam) Odstrániť_2(kurzor uintptr) {
	index := vlastný.Indexz(kurzor)
	if index < 0 {
		return
	}
	vlastný.Odstrániťat(index)
}
func (vlastný *LinkedZoznam) Odstrániťat(index int) {
	if index < 0 || index >= vlastný.Veľkosť_2 {
		return
	}
	uzol := vlastný.GetUzolat(index)
	if uzol == nil {
		return
	}
	if uzol.previous != nil {
		uzol.previous.nasledujúci = uzol.nasledujúci
	} else {
		vlastný.head = uzol.nasledujúci
	}
	if uzol.nasledujúci != nil {
		uzol.nasledujúci.previous = uzol.previous
	} else {
		vlastný.tail = uzol.previous
	}
	vlastný.Veľkosť_2 = vlastný.Veľkosť_2 - 1

	if vlastný.mem != nil {
		vlastný.mem.Voľné(Pointer(uzol))
	}
}

var konzola_2 = TKonzola{}

func (vlastný *LinkedZoznam) Tlačiť() {
	konzola_2.MTlačiťxy("LinkedList:", 1, 1)
	konzola_2.MUnsignedinteger32Tlačiť(uint32(uintptr(Pointer(vlastný))))
	for i := 0; i < vlastný.Veľkosť_2; i++ {
		uzol := (*Uzol)(vlastný.Getat(i))
		konzola_2.MUnsignedinteger32Tlačiť(uint32(uzol.kurzor))
		konzola_2.MTlačiť(":")
	}
}
