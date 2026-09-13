package liste

import . "unsafe"
import . "console"
import mem "hukommelsemanager"

type Knudepunkt struct {
	markør		uintptr
	previous	*Knudepunkt
	næste		*Knudepunkt
}

type LinkedListe struct {
	head		*Knudepunkt
	tail		*Knudepunkt
	Størrelse_2	int

	mem	*mem.THukommelsemanager
}

func (selv *LinkedListe) Init(mem *mem.THukommelsemanager) {
	selv.head = nil
	selv.tail = nil
	selv.Størrelse_2 = 0

	selv.mem = mem
}
func (selv *LinkedListe) Prepend_to_list(markør uintptr) {
	nyKnudepunkt := (*Knudepunkt)(selv.mem.Malloc(uint32(Sizeof(Knudepunkt{}))))
	if nyKnudepunkt == nil {
		return
	}
	nyKnudepunkt.markør = markør
	nyKnudepunkt.previous = nil
	nyKnudepunkt.næste = selv.head
	if selv.head != nil {
		selv.head.previous = nyKnudepunkt
	}
	selv.head = nyKnudepunkt
	selv.Størrelse_2++

	if selv.head.næste == nil {
		selv.tail = selv.head
	}

}
func (selv *LinkedListe) Append_to_list(markør uintptr) {
	if selv.Størrelse_2 == 0 {
		selv.Prepend_to_list(markør)
	} else {
		nyKnudepunkt := (*Knudepunkt)(selv.mem.Malloc(uint32(Sizeof(Knudepunkt{}))))
		if nyKnudepunkt == nil {
			return
		}
		nyKnudepunkt.markør = markør
		nyKnudepunkt.previous = selv.tail
		nyKnudepunkt.næste = nil
		selv.tail.næste = nyKnudepunkt
		selv.tail = nyKnudepunkt
		selv.Størrelse_2++
	}
}
func (selv *LinkedListe) Insert_at_index(indeks int, markør uintptr) {
	if indeks == 0 {
		selv.Prepend_to_list(markør)
	} else {
		previousKnudepunkt := selv.GetKnudepunktat(indeks - 1)
		næsteKnudepunkt := previousKnudepunkt.næste
		nyKnudepunkt := (*Knudepunkt)(selv.mem.Malloc(uint32(Sizeof(Knudepunkt{}))))
		if nyKnudepunkt == nil {
			return
		}
		nyKnudepunkt.markør = markør

		previousKnudepunkt.næste = nyKnudepunkt
		nyKnudepunkt.previous = previousKnudepunkt
		nyKnudepunkt.næste = næsteKnudepunkt
		if næsteKnudepunkt != nil {
			næsteKnudepunkt.previous = nyKnudepunkt
		}

		selv.Størrelse_2++

		if nyKnudepunkt.næste == nil {
			selv.tail = nyKnudepunkt
		}
	}
}
func (selv *LinkedListe) GetKnudepunktat(indeks int) *Knudepunkt {
	if indeks < 0 || indeks >= selv.Størrelse_2 {
		return nil
	}
	var x *Knudepunkt = selv.head
	for i := 0; i < indeks; i++ {
		x = x.næste
	}
	return x
}

func (selv *LinkedListe) SatKnudepunktat(indeks int, markør uintptr) {
	var x *Knudepunkt = selv.head
	for i := 0; i < indeks; i++ {
		x = x.næste
	}
	if x != nil {
		x.markør = markør
	}
}
func (selv *LinkedListe) Getat(indeks int) Pointer {
	knudepunkt := selv.GetKnudepunktat(indeks)
	if knudepunkt == nil {
		return nil
	}
	var markør uintptr = knudepunkt.markør
	return Pointer(markør)
}
func (selv *LinkedListe) Indeksaf(markør uintptr) int {
	var n *Knudepunkt = selv.head
	i := 0
	for ; i < selv.Størrelse_2; i++ {
		if markør == n.markør {
			return i
		}
		n = n.næste
	}
	return -1
}
func (selv *LinkedListe) Fjern(markør uintptr) {
	indeks := selv.Indeksaf(markør)
	if indeks < 0 {
		return
	}
	selv.Fjernat(indeks)
}
func (selv *LinkedListe) Fjernat(indeks int) {
	if indeks < 0 || indeks >= selv.Størrelse_2 {
		return
	}
	knudepunkt := selv.GetKnudepunktat(indeks)
	if knudepunkt == nil {
		return
	}
	if knudepunkt.previous != nil {
		knudepunkt.previous.næste = knudepunkt.næste
	} else {
		selv.head = knudepunkt.næste
	}
	if knudepunkt.næste != nil {
		knudepunkt.næste.previous = knudepunkt.previous
	} else {
		selv.tail = knudepunkt.previous
	}
	selv.Størrelse_2 = selv.Størrelse_2 - 1

	if selv.mem != nil {
		selv.mem.Fri(Pointer(knudepunkt))
	}
}

var console_2 = TConsole{}

func (selv *LinkedListe) Udskriv() {
	console_2.MUdskrivxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Udskriv(uint32(uintptr(Pointer(selv))))
	for i := 0; i < selv.Størrelse_2; i++ {
		knudepunkt := (*Knudepunkt)(selv.Getat(i))
		console_2.MUnsignedinteger32Udskriv(uint32(knudepunkt.markør))
		console_2.MUdskriv(":")
	}
}
