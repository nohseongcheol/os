package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssieraksts struct {
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

var tssSaturs uint32 = 0
var flushSaturs uint32 = 0

func flushtss(uint32)
func (pats *Tssieraksts) Instalēt(gdt *TShareddescriptorTabula, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MDrukātxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(pats)))
	console_2.MUnsignedinteger32Drukāt(base)
	console_2.MDrukāt(":")

	gdt.Kopadescriptor(idx, base, uint32(Sizeof(Tssieraksts{})), 0xE9, 0)
	pats.ss0 = kernelss
	pats.esp0 = kernelesp
	pats.iomap = uint16(Sizeof(Tssieraksts{}))

	flushtss(SegtaskStāvoklis)

}
func (pats *Tssieraksts) Kopastack(kernelss uint32, kernelesp uint32) {
	pats.ss0 = kernelss
	pats.esp0 = kernelesp
}
func (pats *Tssieraksts) Getesp0() uint32 {
	return pats.esp0
}
func (pats *Tssieraksts) Getss0() uint32 {
	return pats.ss0
}
