package tss

import . "unsafe"
import . "gdt"
import . "konsoly"

var konsoly_2 = TKonsoly{}

type Tssentry struct {
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

var tssFizahantakila uint32 = 0
var flushFizahantakila uint32 = 0

func flushtss(uint32)
func (nytena *Tssentry) Hametraka(gdt *TShareddescriptorFafana, idx int, kernelss uint32, kernelesp uint32) {

	konsoly_2.MAtontayxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(nytena)))
	konsoly_2.MUnsignedinteger32Atontay(base)
	konsoly_2.MAtontay(":")

	gdt.Setdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	nytena.ss0 = kernelss
	nytena.esp0 = kernelesp
	nytena.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segtaskstate)

}
func (nytena *Tssentry) Setstack(kernelss uint32, kernelesp uint32) {
	nytena.ss0 = kernelss
	nytena.esp0 = kernelesp
}
func (nytena *Tssentry) Getesp0() uint32 {
	return nytena.esp0
}
func (nytena *Tssentry) Getss0() uint32 {
	return nytena.ss0
}
