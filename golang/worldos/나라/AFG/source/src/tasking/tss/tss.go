/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
	eflags_2	uint32
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

var tssنمایه uint32 = 0
var flushنمایه uint32 = 0

func flushtss(uint32)
func (خود *Tssentry) Iنصب(gdt *TShareddescriptorجدول, idx int, kernelss uint32, kernelesp uint32) {

	console_2.Mچاپxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(خود)))
	console_2.MUnsignedinteger32چاپ(base)
	console_2.Mچاپ(":")

	gdt.Setdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	خود.ss0 = kernelss
	خود.esp0 = kernelesp
	خود.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segtaskحالت)

}
func (خود *Tssentry) Setstack(kernelss uint32, kernelesp uint32) {
	خود.ss0 = kernelss
	خود.esp0 = kernelesp
}
func (خود *Tssentry) Getesp0() uint32 {
	return خود.esp0
}
func (خود *Tssentry) Getss0() uint32 {
	return خود.ss0
}
