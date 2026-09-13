package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tsskirje struct {
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

var tssSisukord uint32 = 0
var flushSisukord uint32 = 0

func flushtss(uint32)
func (ise *Tsskirje) Paigalda(gdt *TShareddescriptorTabel, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MPrindixy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(ise)))
	console_2.MUnsignedinteger32Prindi(base)
	console_2.MPrindi(":")

	gdt.Määradescriptor(idx, base, uint32(Sizeof(Tsskirje{})), 0xE9, 0)
	ise.ss0 = kernelss
	ise.esp0 = kernelesp
	ise.iomap = uint16(Sizeof(Tsskirje{}))

	flushtss(SegtaskOlek)

}
func (ise *Tsskirje) Määrastack(kernelss uint32, kernelesp uint32) {
	ise.ss0 = kernelss
	ise.esp0 = kernelesp
}
func (ise *Tsskirje) Getesp0() uint32 {
	return ise.esp0
}
func (ise *Tsskirje) Getss0() uint32 {
	return ise.ss0
}
