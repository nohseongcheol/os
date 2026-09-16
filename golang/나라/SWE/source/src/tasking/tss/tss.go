/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "konsol"

var konsol_2 = TKonsol{}

type Tsspost struct {
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
func (själv *Tsspost) Installera(gdt *TShareddescriptorTabell, idx int, kernelss uint32, kernelesp uint32) {

	konsol_2.MSkrivutxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(själv)))
	konsol_2.MUnsignedinteger32Skrivut(base)
	konsol_2.MSkrivut(":")

	gdt.Mängddescriptor(idx, base, uint32(Sizeof(Tsspost{})), 0xE9, 0)
	själv.ss0 = kernelss
	själv.esp0 = kernelesp
	själv.iomap = uint16(Sizeof(Tsspost{}))

	flushtss(SegAktivitetTillstånd)

}
func (själv *Tsspost) Mängdstack(kernelss uint32, kernelesp uint32) {
	själv.ss0 = kernelss
	själv.esp0 = kernelesp
}
func (själv *Tsspost) Getesp0() uint32 {
	return själv.esp0
}
func (själv *Tsspost) Getss0() uint32 {
	return själv.ss0
}
