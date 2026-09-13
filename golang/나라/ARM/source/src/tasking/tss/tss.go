package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

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

var tssԻնդեքս uint32 = 0
var flushԻնդեքս uint32 = 0

func flushtss(uint32)
func (ինքնուրույն *Tssentry) Տեղադրել(gdt *TShareddescriptorԱղյուսակ, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MՏպելxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(ինքնուրույն)))
	console_2.MUnsignedinteger32Տպել(base)
	console_2.MՏպել(":")

	gdt.Setdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	ինքնուրույն.ss0 = kernelss
	ինքնուրույն.esp0 = kernelesp
	ինքնուրույն.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(SegtaskՎիճակ)

}
func (ինքնուրույն *Tssentry) Setstack(kernelss uint32, kernelesp uint32) {
	ինքնուրույն.ss0 = kernelss
	ինքնուրույն.esp0 = kernelesp
}
func (ինքնուրույն *Tssentry) Getesp0() uint32 {
	return ինքնուրույն.esp0
}
func (ինքնուրույն *Tssentry) Getss0() uint32 {
	return ինքնուրույն.ss0
}
