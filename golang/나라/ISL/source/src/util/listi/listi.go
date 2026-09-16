/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package listi

import . "unsafe"
import . "console"
import mem "minnimanager"

type Hnútur struct {
	bendill		uintptr
	previous	*Hnútur
	næsta		*Hnútur
}

type LinkedListi struct {
	head	*Hnútur
	tail	*Hnútur
	Stærð_2	int

	mem	*mem.TMinnimanager
}

func (sjálft *LinkedListi) Init(mem *mem.TMinnimanager) {
	sjálft.head = nil
	sjálft.tail = nil
	sjálft.Stærð_2 = 0

	sjálft.mem = mem
}
func (sjálft *LinkedListi) Prepend_to_list(bendill uintptr) {
	nýttHnútur := (*Hnútur)(sjálft.mem.Malloc(uint32(Sizeof(Hnútur{}))))
	if nýttHnútur == nil {
		return
	}
	nýttHnútur.bendill = bendill
	nýttHnútur.previous = nil
	nýttHnútur.næsta = sjálft.head
	if sjálft.head != nil {
		sjálft.head.previous = nýttHnútur
	}
	sjálft.head = nýttHnútur
	sjálft.Stærð_2++

	if sjálft.head.næsta == nil {
		sjálft.tail = sjálft.head
	}

}
func (sjálft *LinkedListi) Append_to_list(bendill uintptr) {
	if sjálft.Stærð_2 == 0 {
		sjálft.Prepend_to_list(bendill)
	} else {
		nýttHnútur := (*Hnútur)(sjálft.mem.Malloc(uint32(Sizeof(Hnútur{}))))
		if nýttHnútur == nil {
			return
		}
		nýttHnútur.bendill = bendill
		nýttHnútur.previous = sjálft.tail
		nýttHnútur.næsta = nil
		sjálft.tail.næsta = nýttHnútur
		sjálft.tail = nýttHnútur
		sjálft.Stærð_2++
	}
}
func (sjálft *LinkedListi) Insert_at_index(index int, bendill uintptr) {
	if index == 0 {
		sjálft.Prepend_to_list(bendill)
	} else {
		previousHnútur := sjálft.GetHnúturat(index - 1)
		næstaHnútur := previousHnútur.næsta
		nýttHnútur := (*Hnútur)(sjálft.mem.Malloc(uint32(Sizeof(Hnútur{}))))
		if nýttHnútur == nil {
			return
		}
		nýttHnútur.bendill = bendill

		previousHnútur.næsta = nýttHnútur
		nýttHnútur.previous = previousHnútur
		nýttHnútur.næsta = næstaHnútur
		if næstaHnútur != nil {
			næstaHnútur.previous = nýttHnútur
		}

		sjálft.Stærð_2++

		if nýttHnútur.næsta == nil {
			sjálft.tail = nýttHnútur
		}
	}
}
func (sjálft *LinkedListi) GetHnúturat(index int) *Hnútur {
	if index < 0 || index >= sjálft.Stærð_2 {
		return nil
	}
	var x *Hnútur = sjálft.head
	for i := 0; i < index; i++ {
		x = x.næsta
	}
	return x
}

func (sjálft *LinkedListi) SetjaHnúturat(index int, bendill uintptr) {
	var x *Hnútur = sjálft.head
	for i := 0; i < index; i++ {
		x = x.næsta
	}
	if x != nil {
		x.bendill = bendill
	}
}
func (sjálft *LinkedListi) Getat(index int) Pointer {
	hnútur := sjálft.GetHnúturat(index)
	if hnútur == nil {
		return nil
	}
	var bendill uintptr = hnútur.bendill
	return Pointer(bendill)
}
func (sjálft *LinkedListi) Indexaf(bendill uintptr) int {
	var n *Hnútur = sjálft.head
	i := 0
	for ; i < sjálft.Stærð_2; i++ {
		if bendill == n.bendill {
			return i
		}
		n = n.næsta
	}
	return -1
}
func (sjálft *LinkedListi) Fjarlægja(bendill uintptr) {
	index := sjálft.Indexaf(bendill)
	if index < 0 {
		return
	}
	sjálft.Fjarlægjaat(index)
}
func (sjálft *LinkedListi) Fjarlægjaat(index int) {
	if index < 0 || index >= sjálft.Stærð_2 {
		return
	}
	hnútur := sjálft.GetHnúturat(index)
	if hnútur == nil {
		return
	}
	if hnútur.previous != nil {
		hnútur.previous.næsta = hnútur.næsta
	} else {
		sjálft.head = hnútur.næsta
	}
	if hnútur.næsta != nil {
		hnútur.næsta.previous = hnútur.previous
	} else {
		sjálft.tail = hnútur.previous
	}
	sjálft.Stærð_2 = sjálft.Stærð_2 - 1

	if sjálft.mem != nil {
		sjálft.mem.Laust(Pointer(hnútur))
	}
}

var console_2 = TConsole{}

func (sjálft *LinkedListi) Prenta() {
	console_2.MPrentaxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Prenta(uint32(uintptr(Pointer(sjálft))))
	for i := 0; i < sjálft.Stærð_2; i++ {
		hnútur := (*Hnútur)(sjálft.Getat(i))
		console_2.MUnsignedinteger32Prenta(uint32(hnútur.bendill))
		console_2.MPrenta(":")
	}
}
