/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "паметmanager"

type Връзка struct {
	Динамично	uintptr
	Previous	*Връзка
	Следващо	*Връзка
}
type Връзкаmap struct {
	First		*Връзка
	Последно	*Връзка

	Размер_2	int

	mem	*mem.TПаметmanager
}

func (себеси *Връзкаmap) Init(mem *mem.TПаметmanager) {
	себеси.mem = mem
}
func (себеси *Връзкаmap) Clone() Връзкаmap {
	var връзкаmap Връзкаmap

	връзкаmap.Init(себеси.mem)

	Връзка := себеси.First

	for ; Връзка != nil; Връзка = Връзка.Следващо {
		връзкаmap.Append_to_list(Връзка.Динамично)
	}
	return връзкаmap
}
func (себеси *Връзкаmap) Prepend_to_list(Динамично uintptr) {
	новВръзка := (*Връзка)(себеси.mem.Malloc(uint32(Sizeof(Връзка{}))))
	новВръзка.Динамично = Динамично
	новВръзка.Следващо = себеси.First
	себеси.First = новВръзка
	себеси.Размер_2++

	if себеси.First.Следващо == nil {
		себеси.Последно = себеси.First
	}
}
func (себеси *Връзкаmap) Append_to_list(Динамично uintptr) {
	if Динамично == 0 {
		return
	}

	if себеси.Размер_2 == 0 {
		себеси.Prepend_to_list(Динамично)
	} else {
		новВръзка := (*Връзка)(себеси.mem.Malloc(uint32(Sizeof(Връзка{}))))
		новВръзка.Динамично = Динамично
		новВръзка.Следващо = nil
		себеси.Последно.Следващо = новВръзка
		себеси.Последно = новВръзка
		себеси.Размер_2++
	}
}
func (себеси *Връзкаmap) Печат(x uint16, y uint16) {
	Връзка := себеси.First
	console_2 := TConsole{}
	console_2.MПечатxy("linkmap : ", x, y)
	for ; Връзка != nil; Връзка = Връзка.Следващо {
		console_2.MUnsignedinteger32Печат(uint32(Връзка.Динамично))
		console_2.MПечат("+")

	}
}
