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

var tssindex uint32 = 0
var flushindex uint32 = 0

func flushtss(uint32)
func (sjálft *Tssentry) Setjaupp(gdt *TShareddescriptorTafla, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MPrentaxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(sjálft)))
	console_2.MUnsignedinteger32Prenta(base)
	console_2.MPrenta(":")

	gdt.Setjadescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	sjálft.ss0 = kernelss
	sjálft.esp0 = kernelesp
	sjálft.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(SegVerkStaða)

}
func (sjálft *Tssentry) Setjastack(kernelss uint32, kernelesp uint32) {
	sjálft.ss0 = kernelss
	sjálft.esp0 = kernelesp
}
func (sjálft *Tssentry) Getesp0() uint32 {
	return sjálft.esp0
}
func (sjálft *Tssentry) Getss0() uint32 {
	return sjálft.ss0
}
