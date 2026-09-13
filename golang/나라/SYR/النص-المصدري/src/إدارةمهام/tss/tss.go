package tss

import . "unsafe"
import . "gdt"
import . "طرفية"

var طرفية_2 = Tطرفية{}

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

var tssفهرس uint32 = 0
var flushفهرس uint32 = 0

func flushtss(uint32)
func (نفسه *Tssentry) Install(gdt *TShareddescriptorجدول, idx int, نواةss uint32, نواةesp uint32) {

	طرفية_2.Mاطبعxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(نفسه)))
	طرفية_2.MUnsignedinteger32اطبع(base)
	طرفية_2.Mاطبع(":")

	gdt.Sتحديدdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	نفسه.ss0 = نواةss
	نفسه.esp0 = نواةesp
	نفسه.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segمهمةالحالة)

}
func (نفسه *Tssentry) Sتحديدstack(نواةss uint32, نواةesp uint32) {
	نفسه.ss0 = نواةss
	نفسه.esp0 = نواةesp
}
func (نفسه *Tssentry) Getesp0() uint32 {
	return نفسه.esp0
}
func (نفسه *Tssentry) Getss0() uint32 {
	return نفسه.ss0
}
