/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "konsola"

var konsola_2 = TKonsola{}

type Tsswpis struct {
	Previoustss	uint32
	esp0		uint32
	ss0		uint32
	esp1		uint32
	ss1		uint32
	esp2		uint32
	ss2		uint32
	cr3		uint32
	eip		uint32
	eflags		uint32
	eax		uint32
	ecx		uint32
	edx		uint32
	ebx		uint32
	Esp		uint32
	ebp		uint32
	esi		uint32
	edi		uint32
	es		uint32
	cs		uint32
	ss		uint32
	ds		uint32
	fs		uint32
	gs		uint32
	ldt		uint32
	trap		uint16
	iomap		uint16
}

var tssIndeks uint32 = 0
var flushIndeks uint32 = 0

func flushtss(uint32)
func (bieżący *Tsswpis) Instalacja(gdt *TShareddescriptorTabela, idx int, kernelss uint32, kernelesp uint32) {

	konsola_2.MWydrukujxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(bieżący)))
	konsola_2.MUnsignedinteger32Wydrukuj(base)
	konsola_2.MWydrukuj(":")

	gdt.Zbiórdescriptor(idx, base, uint32(Sizeof(Tsswpis{})), 0xE9, 0)
	bieżący.ss0 = kernelss
	bieżący.esp0 = kernelesp
	bieżący.iomap = uint16(Sizeof(Tsswpis{}))

	flushtss(SegZadanieStan)

}
func (bieżący *Tsswpis) Zbiórstack(kernelss uint32, kernelesp uint32) {
	bieżący.ss0 = kernelss
	bieżący.esp0 = kernelesp
}
func (bieżący *Tsswpis) Getesp0() uint32 {
	return bieżący.esp0
}
func (bieżący *Tsswpis) Getss0() uint32 {
	return bieżący.ss0
}
