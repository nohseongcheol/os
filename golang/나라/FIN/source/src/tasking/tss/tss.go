package tss

import . "unsafe"
import . "gdt"
import . "konsoli"

var konsoli_2 = TKonsoli{}

type Tsshakusana struct {
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

var tssHakemisto uint32 = 0
var flushHakemisto uint32 = 0

func flushtss(uint32)
func (itse *Tsshakusana) Asenna(gdt *TShareddescriptorTaulukko, idx int, kernelss uint32, kernelesp uint32) {

	konsoli_2.MTulostaxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(itse)))
	konsoli_2.MUnsignedinteger32Tulosta(base)
	konsoli_2.MTulosta(":")

	gdt.Asetadescriptor(idx, base, uint32(Sizeof(Tsshakusana{})), 0xE9, 0)
	itse.ss0 = kernelss
	itse.esp0 = kernelesp
	itse.iomap = uint16(Sizeof(Tsshakusana{}))

	flushtss(SegTehtäväTila)

}
func (itse *Tsshakusana) Asetastack(kernelss uint32, kernelesp uint32) {
	itse.ss0 = kernelss
	itse.esp0 = kernelesp
}
func (itse *Tsshakusana) Getesp0() uint32 {
	return itse.esp0
}
func (itse *Tsshakusana) Getss0() uint32 {
	return itse.ss0
}
