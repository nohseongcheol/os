/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package popis

import . "unsafe"
import . "console"
import mem "memorijamanager"

type Čvor struct {
	pokazivač	uintptr
	previous	*Čvor
	slijedeće	*Čvor
}

type LinkedPopis struct {
	head		*Čvor
	tail		*Čvor
	Veličina_2	int

	mem	*mem.TMemorijamanager
}

func (sam *LinkedPopis) Init(mem *mem.TMemorijamanager) {
	sam.head = nil
	sam.tail = nil
	sam.Veličina_2 = 0

	sam.mem = mem
}
func (sam *LinkedPopis) Prepend_to_list(pokazivač uintptr) {
	noviČvor := (*Čvor)(sam.mem.Malloc(uint32(Sizeof(Čvor{}))))
	if noviČvor == nil {
		return
	}
	noviČvor.pokazivač = pokazivač
	noviČvor.previous = nil
	noviČvor.slijedeće = sam.head
	if sam.head != nil {
		sam.head.previous = noviČvor
	}
	sam.head = noviČvor
	sam.Veličina_2++

	if sam.head.slijedeće == nil {
		sam.tail = sam.head
	}

}
func (sam *LinkedPopis) Append_to_list(pokazivač uintptr) {
	if sam.Veličina_2 == 0 {
		sam.Prepend_to_list(pokazivač)
	} else {
		noviČvor := (*Čvor)(sam.mem.Malloc(uint32(Sizeof(Čvor{}))))
		if noviČvor == nil {
			return
		}
		noviČvor.pokazivač = pokazivač
		noviČvor.previous = sam.tail
		noviČvor.slijedeće = nil
		sam.tail.slijedeće = noviČvor
		sam.tail = noviČvor
		sam.Veličina_2++
	}
}
func (sam *LinkedPopis) Insert_at_index(kazalo int, pokazivač uintptr) {
	if kazalo == 0 {
		sam.Prepend_to_list(pokazivač)
	} else {
		previousČvor := sam.GetČvorat(kazalo - 1)
		slijedećeČvor := previousČvor.slijedeće
		noviČvor := (*Čvor)(sam.mem.Malloc(uint32(Sizeof(Čvor{}))))
		if noviČvor == nil {
			return
		}
		noviČvor.pokazivač = pokazivač

		previousČvor.slijedeće = noviČvor
		noviČvor.previous = previousČvor
		noviČvor.slijedeće = slijedećeČvor
		if slijedećeČvor != nil {
			slijedećeČvor.previous = noviČvor
		}

		sam.Veličina_2++

		if noviČvor.slijedeće == nil {
			sam.tail = noviČvor
		}
	}
}
func (sam *LinkedPopis) GetČvorat(kazalo int) *Čvor {
	if kazalo < 0 || kazalo >= sam.Veličina_2 {
		return nil
	}
	var x *Čvor = sam.head
	for i := 0; i < kazalo; i++ {
		x = x.slijedeće
	}
	return x
}

func (sam *LinkedPopis) PostaviČvorat(kazalo int, pokazivač uintptr) {
	var x *Čvor = sam.head
	for i := 0; i < kazalo; i++ {
		x = x.slijedeće
	}
	if x != nil {
		x.pokazivač = pokazivač
	}
}
func (sam *LinkedPopis) Getat(kazalo int) Pointer {
	čvor := sam.GetČvorat(kazalo)
	if čvor == nil {
		return nil
	}
	var pokazivač uintptr = čvor.pokazivač
	return Pointer(pokazivač)
}
func (sam *LinkedPopis) Kazalood(pokazivač uintptr) int {
	var n *Čvor = sam.head
	i := 0
	for ; i < sam.Veličina_2; i++ {
		if pokazivač == n.pokazivač {
			return i
		}
		n = n.slijedeće
	}
	return -1
}
func (sam *LinkedPopis) Ukloni(pokazivač uintptr) {
	kazalo := sam.Kazalood(pokazivač)
	if kazalo < 0 {
		return
	}
	sam.Ukloniat(kazalo)
}
func (sam *LinkedPopis) Ukloniat(kazalo int) {
	if kazalo < 0 || kazalo >= sam.Veličina_2 {
		return
	}
	čvor := sam.GetČvorat(kazalo)
	if čvor == nil {
		return
	}
	if čvor.previous != nil {
		čvor.previous.slijedeće = čvor.slijedeće
	} else {
		sam.head = čvor.slijedeće
	}
	if čvor.slijedeće != nil {
		čvor.slijedeće.previous = čvor.previous
	} else {
		sam.tail = čvor.previous
	}
	sam.Veličina_2 = sam.Veličina_2 - 1

	if sam.mem != nil {
		sam.mem.Slobodno(Pointer(čvor))
	}
}

var console_2 = TConsole{}

func (sam *LinkedPopis) Ispis() {
	console_2.MIspisxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Ispis(uint32(uintptr(Pointer(sam))))
	for i := 0; i < sam.Veličina_2; i++ {
		čvor := (*Čvor)(sam.Getat(i))
		console_2.MUnsignedinteger32Ispis(uint32(čvor.pokazivač))
		console_2.MIspis(":")
	}
}
