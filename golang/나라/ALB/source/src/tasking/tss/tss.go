package tss

import . "unsafe"
import . "gdt"
import . "konsolë"

var konsolë_2 = TKonsolë{}

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

var tssTreguesi uint32 = 0
var flushTreguesi uint32 = 0

func flushtss(uint32)
func (vetvetja *Tssentry) Instalo(gdt *TShareddescriptorTabela, idx int, kernelss uint32, kernelesp uint32) {

	konsolë_2.MPrintoxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(vetvetja)))
	konsolë_2.MUnsignedinteger32Printo(base)
	konsolë_2.MPrinto(":")

	gdt.Caktonidescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	vetvetja.ss0 = kernelss
	vetvetja.esp0 = kernelesp
	vetvetja.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(SegProcesGjendje)

}
func (vetvetja *Tssentry) Caktonistack(kernelss uint32, kernelesp uint32) {
	vetvetja.ss0 = kernelss
	vetvetja.esp0 = kernelesp
}
func (vetvetja *Tssentry) Getesp0() uint32 {
	return vetvetja.esp0
}
func (vetvetja *Tssentry) Getss0() uint32 {
	return vetvetja.ss0
}
