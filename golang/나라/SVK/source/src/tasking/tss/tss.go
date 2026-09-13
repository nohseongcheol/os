package tss

import . "unsafe"
import . "gdt"
import . "konzola"

var konzola_2 = TKonzola{}

type Tsspoložka struct {
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

var tssindex uint32 = 0
var flushindex uint32 = 0

func flushtss(uint32)
func (vlastný *Tsspoložka) Nainštalovať(gdt *TShareddescriptorTabuľka, idx int, kernelss uint32, kernelesp uint32) {

	konzola_2.MTlačiťxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(vlastný)))
	konzola_2.MUnsignedinteger32Tlačiť(base)
	konzola_2.MTlačiť(":")

	gdt.Sadadescriptor(idx, base, uint32(Sizeof(Tsspoložka{})), 0xE9, 0)
	vlastný.ss0 = kernelss
	vlastný.esp0 = kernelesp
	vlastný.iomap = uint16(Sizeof(Tsspoložka{}))

	flushtss(SegUlohaStav)

}
func (vlastný *Tsspoložka) Sadastack(kernelss uint32, kernelesp uint32) {
	vlastný.ss0 = kernelss
	vlastný.esp0 = kernelesp
}
func (vlastný *Tsspoložka) Getesp0() uint32 {
	return vlastný.esp0
}
func (vlastný *Tsspoložka) Getss0() uint32 {
	return vlastný.ss0
}
