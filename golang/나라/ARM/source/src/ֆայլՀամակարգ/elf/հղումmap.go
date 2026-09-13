package elf

import . "unsafe"
import . "console"

import mem "հիշողությունmanager"

type Հղում struct {
	Dynamic		uintptr
	Previous	*Հղում
	Հաջորդ		*Հղում
}
type Հղումmap struct {
	First	*Հղում
	Վերջին	*Հղում

	Չափս_2	int

	mem	*mem.TՀիշողությունmanager
}

func (ինքնուրույն *Հղումmap) Init(mem *mem.TՀիշողությունmanager) {
	ինքնուրույն.mem = mem
}
func (ինքնուրույն *Հղումmap) Clone() Հղումmap {
	var հղումmap Հղումmap

	հղումmap.Init(ինքնուրույն.mem)

	Հղում := ինքնուրույն.First

	for ; Հղում != nil; Հղում = Հղում.Հաջորդ {
		հղումmap.Append_to_list(Հղում.Dynamic)
	}
	return հղումmap
}
func (ինքնուրույն *Հղումmap) Prepend_to_list(Dynamic uintptr) {
	նորհղում := (*Հղում)(ինքնուրույն.mem.Malloc(uint32(Sizeof(Հղում{}))))
	նորհղում.Dynamic = Dynamic
	նորհղում.Հաջորդ = ինքնուրույն.First
	ինքնուրույն.First = նորհղում
	ինքնուրույն.Չափս_2++

	if ինքնուրույն.First.Հաջորդ == nil {
		ինքնուրույն.Վերջին = ինքնուրույն.First
	}
}
func (ինքնուրույն *Հղումmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if ինքնուրույն.Չափս_2 == 0 {
		ինքնուրույն.Prepend_to_list(Dynamic)
	} else {
		նորհղում := (*Հղում)(ինքնուրույն.mem.Malloc(uint32(Sizeof(Հղում{}))))
		նորհղում.Dynamic = Dynamic
		նորհղում.Հաջորդ = nil
		ինքնուրույն.Վերջին.Հաջորդ = նորհղում
		ինքնուրույն.Վերջին = նորհղում
		ինքնուրույն.Չափս_2++
	}
}
func (ինքնուրույն *Հղումmap) Տպել(x uint16, y uint16) {
	Հղում := ինքնուրույն.First
	console_2 := TConsole{}
	console_2.MՏպելxy("linkmap : ", x, y)
	for ; Հղում != nil; Հղում = Հղում.Հաջորդ {
		console_2.MUnsignedinteger32Տպել(uint32(Հղում.Dynamic))
		console_2.MՏպել("+")

	}
}
