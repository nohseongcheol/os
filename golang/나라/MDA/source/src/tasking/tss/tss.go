package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssînregistrare struct {
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
func (sine *Tssînregistrare) Instalează(gdt *TShareddescriptorTabel, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MTipăreștexy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(sine)))
	console_2.MUnsignedinteger32Tipărește(base)
	console_2.MTipărește(":")

	gdt.Definitdescriptor(idx, base, uint32(Sizeof(Tssînregistrare{})), 0xE9, 0)
	sine.ss0 = kernelss
	sine.esp0 = kernelesp
	sine.iomap = uint16(Sizeof(Tssînregistrare{}))

	flushtss(SegtaskStare)

}
func (sine *Tssînregistrare) Definitstack(kernelss uint32, kernelesp uint32) {
	sine.ss0 = kernelss
	sine.esp0 = kernelesp
}
func (sine *Tssînregistrare) Getesp0() uint32 {
	return sine.esp0
}
func (sine *Tssînregistrare) Getss0() uint32 {
	return sine.ss0
}
