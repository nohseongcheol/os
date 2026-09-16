/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package spisak

import . "unsafe"
import . "konzola"
import mem "memorijamanager"

type Čvor struct {
	pokazivač	uintptr
	previous	*Čvor
	sledeće		*Čvor
}

type LinkedSpisak struct {
	head		*Čvor
	tail		*Čvor
	Veličina_2	int

	mem	*mem.TMemorijamanager
}

func (isti *LinkedSpisak) Init(mem *mem.TMemorijamanager) {
	isti.head = nil
	isti.tail = nil
	isti.Veličina_2 = 0

	isti.mem = mem
}
func (isti *LinkedSpisak) Prepend_to_list(pokazivač uintptr) {
	novaČvor := (*Čvor)(isti.mem.Malloc(uint32(Sizeof(Čvor{}))))
	if novaČvor == nil {
		return
	}
	novaČvor.pokazivač = pokazivač
	novaČvor.previous = nil
	novaČvor.sledeće = isti.head
	if isti.head != nil {
		isti.head.previous = novaČvor
	}
	isti.head = novaČvor
	isti.Veličina_2++

	if isti.head.sledeće == nil {
		isti.tail = isti.head
	}

}
func (isti *LinkedSpisak) Append_to_list(pokazivač uintptr) {
	if isti.Veličina_2 == 0 {
		isti.Prepend_to_list(pokazivač)
	} else {
		novaČvor := (*Čvor)(isti.mem.Malloc(uint32(Sizeof(Čvor{}))))
		if novaČvor == nil {
			return
		}
		novaČvor.pokazivač = pokazivač
		novaČvor.previous = isti.tail
		novaČvor.sledeće = nil
		isti.tail.sledeće = novaČvor
		isti.tail = novaČvor
		isti.Veličina_2++
	}
}
func (isti *LinkedSpisak) Insert_at_index(popis int, pokazivač uintptr) {
	if popis == 0 {
		isti.Prepend_to_list(pokazivač)
	} else {
		previousČvor := isti.GetČvorat(popis - 1)
		sledećeČvor := previousČvor.sledeće
		novaČvor := (*Čvor)(isti.mem.Malloc(uint32(Sizeof(Čvor{}))))
		if novaČvor == nil {
			return
		}
		novaČvor.pokazivač = pokazivač

		previousČvor.sledeće = novaČvor
		novaČvor.previous = previousČvor
		novaČvor.sledeće = sledećeČvor
		if sledećeČvor != nil {
			sledećeČvor.previous = novaČvor
		}

		isti.Veličina_2++

		if novaČvor.sledeće == nil {
			isti.tail = novaČvor
		}
	}
}
func (isti *LinkedSpisak) GetČvorat(popis int) *Čvor {
	if popis < 0 || popis >= isti.Veličina_2 {
		return nil
	}
	var x *Čvor = isti.head
	for i := 0; i < popis; i++ {
		x = x.sledeće
	}
	return x
}

func (isti *LinkedSpisak) SkupČvorat(popis int, pokazivač uintptr) {
	var x *Čvor = isti.head
	for i := 0; i < popis; i++ {
		x = x.sledeće
	}
	if x != nil {
		x.pokazivač = pokazivač
	}
}
func (isti *LinkedSpisak) Getat(popis int) Pointer {
	čvor := isti.GetČvorat(popis)
	if čvor == nil {
		return nil
	}
	var pokazivač uintptr = čvor.pokazivač
	return Pointer(pokazivač)
}
func (isti *LinkedSpisak) Popisod(pokazivač uintptr) int {
	var n *Čvor = isti.head
	i := 0
	for ; i < isti.Veličina_2; i++ {
		if pokazivač == n.pokazivač {
			return i
		}
		n = n.sledeće
	}
	return -1
}
func (isti *LinkedSpisak) Ukloni(pokazivač uintptr) {
	popis := isti.Popisod(pokazivač)
	if popis < 0 {
		return
	}
	isti.Ukloniat(popis)
}
func (isti *LinkedSpisak) Ukloniat(popis int) {
	if popis < 0 || popis >= isti.Veličina_2 {
		return
	}
	čvor := isti.GetČvorat(popis)
	if čvor == nil {
		return
	}
	if čvor.previous != nil {
		čvor.previous.sledeće = čvor.sledeće
	} else {
		isti.head = čvor.sledeće
	}
	if čvor.sledeće != nil {
		čvor.sledeće.previous = čvor.previous
	} else {
		isti.tail = čvor.previous
	}
	isti.Veličina_2 = isti.Veličina_2 - 1

	if isti.mem != nil {
		isti.mem.Slobodno(Pointer(čvor))
	}
}

var konzola_2 = TKonzola{}

func (isti *LinkedSpisak) Štampaj() {
	konzola_2.MŠtampajxy("LinkedList:", 1, 1)
	konzola_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(isti))))
	for i := 0; i < isti.Veličina_2; i++ {
		čvor := (*Čvor)(isti.Getat(i))
		konzola_2.MUnsignedinteger32Štampaj(uint32(čvor.pokazivač))
		konzola_2.MŠtampaj(":")
	}
}
