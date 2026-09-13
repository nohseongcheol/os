package elf

import . "unsafe"
import . "console"

import mem "mälumanager"

type Viit struct {
	Dünaamiline	uintptr
	Previous	*Viit
	Järgmine	*Viit
}
type Viitmap struct {
	First	*Viit
	Eelmine	*Viit

	Suurus_2	int

	mem	*mem.TMälumanager
}

func (ise *Viitmap) Init(mem *mem.TMälumanager) {
	ise.mem = mem
}
func (ise *Viitmap) Clone() Viitmap {
	var viitmap Viitmap

	viitmap.Init(ise.mem)

	Viit := ise.First

	for ; Viit != nil; Viit = Viit.Järgmine {
		viitmap.Append_to_list(Viit.Dünaamiline)
	}
	return viitmap
}
func (ise *Viitmap) Prepend_to_list(Dünaamiline uintptr) {
	uusViit := (*Viit)(ise.mem.Malloc(uint32(Sizeof(Viit{}))))
	uusViit.Dünaamiline = Dünaamiline
	uusViit.Järgmine = ise.First
	ise.First = uusViit
	ise.Suurus_2++

	if ise.First.Järgmine == nil {
		ise.Eelmine = ise.First
	}
}
func (ise *Viitmap) Append_to_list(Dünaamiline uintptr) {
	if Dünaamiline == 0 {
		return
	}

	if ise.Suurus_2 == 0 {
		ise.Prepend_to_list(Dünaamiline)
	} else {
		uusViit := (*Viit)(ise.mem.Malloc(uint32(Sizeof(Viit{}))))
		uusViit.Dünaamiline = Dünaamiline
		uusViit.Järgmine = nil
		ise.Eelmine.Järgmine = uusViit
		ise.Eelmine = uusViit
		ise.Suurus_2++
	}
}
func (ise *Viitmap) Prindi(x uint16, y uint16) {
	Viit := ise.First
	console_2 := TConsole{}
	console_2.MPrindixy("linkmap : ", x, y)
	for ; Viit != nil; Viit = Viit.Järgmine {
		console_2.MUnsignedinteger32Prindi(uint32(Viit.Dünaamiline))
		console_2.MPrindi("+")

	}
}
