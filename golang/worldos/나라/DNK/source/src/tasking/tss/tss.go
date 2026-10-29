/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssemne struct {
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

var tssIndeks uint32 = 0
var flushIndeks uint32 = 0

func flushtss(uint32)
func (selv *Tssemne) Installér(gdt *TShareddescriptorTabel, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MUdskrivxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(selv)))
	console_2.MUnsignedinteger32Udskriv(base)
	console_2.MUdskriv(":")

	gdt.Satdescriptor(idx, base, uint32(Sizeof(Tssemne{})), 0xE9, 0)
	selv.ss0 = kernelss
	selv.esp0 = kernelesp
	selv.iomap = uint16(Sizeof(Tssemne{}))

	flushtss(SegOpgaveStatus)

}
func (selv *Tssemne) Satstack(kernelss uint32, kernelesp uint32) {
	selv.ss0 = kernelss
	selv.esp0 = kernelesp
}
func (selv *Tssemne) Getesp0() uint32 {
	return selv.esp0
}
func (selv *Tssemne) Getss0() uint32 {
	return selv.ss0
}
