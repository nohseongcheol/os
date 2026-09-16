/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "konzola"

var konzola_2 = TKonzola{}

type Tssunos struct {
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

var tssPopis uint32 = 0
var flushPopis uint32 = 0

func flushtss(uint32)
func (isti *Tssunos) Instaliraj(gdt *TShareddescriptorTabela, idx int, kernelss uint32, kernelesp uint32) {

	konzola_2.MŠtampajxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(isti)))
	konzola_2.MUnsignedinteger32Štampaj(base)
	konzola_2.MŠtampaj(":")

	gdt.Skupdescriptor(idx, base, uint32(Sizeof(Tssunos{})), 0xE9, 0)
	isti.ss0 = kernelss
	isti.esp0 = kernelesp
	isti.iomap = uint16(Sizeof(Tssunos{}))

	flushtss(SegZadatakStanje)

}
func (isti *Tssunos) Skupstack(kernelss uint32, kernelesp uint32) {
	isti.ss0 = kernelss
	isti.esp0 = kernelesp
}
func (isti *Tssunos) Getesp0() uint32 {
	return isti.esp0
}
func (isti *Tssunos) Getss0() uint32 {
	return isti.ss0
}
