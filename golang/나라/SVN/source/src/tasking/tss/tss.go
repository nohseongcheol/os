/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssvnos struct {
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
func (sam *Tssvnos) Namesti(gdt *TShareddescriptorPreglednica, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MNatisnixy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(sam)))
	console_2.MUnsignedinteger32Natisni(base)
	console_2.MNatisni(":")

	gdt.Množicadescriptor(idx, base, uint32(Sizeof(Tssvnos{})), 0xE9, 0)
	sam.ss0 = kernelss
	sam.esp0 = kernelesp
	sam.iomap = uint16(Sizeof(Tssvnos{}))

	flushtss(SegNalogaStanje)

}
func (sam *Tssvnos) Množicastack(kernelss uint32, kernelesp uint32) {
	sam.ss0 = kernelss
	sam.esp0 = kernelesp
}
func (sam *Tssvnos) Getesp0() uint32 {
	return sam.esp0
}
func (sam *Tssvnos) Getss0() uint32 {
	return sam.ss0
}
