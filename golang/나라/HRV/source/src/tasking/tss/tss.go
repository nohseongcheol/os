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

var tssKazalo uint32 = 0
var flushKazalo uint32 = 0

func flushtss(uint32)
func (sam *Tssentry) Instaliraj(gdt *TShareddescriptorTablica, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MIspisxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(sam)))
	console_2.MUnsignedinteger32Ispis(base)
	console_2.MIspis(":")

	gdt.Postavidescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	sam.ss0 = kernelss
	sam.esp0 = kernelesp
	sam.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(SegZadatakStanje)

}
func (sam *Tssentry) Postavistack(kernelss uint32, kernelesp uint32) {
	sam.ss0 = kernelss
	sam.esp0 = kernelesp
}
func (sam *Tssentry) Getesp0() uint32 {
	return sam.esp0
}
func (sam *Tssentry) Getss0() uint32 {
	return sam.ss0
}
