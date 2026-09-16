/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssentri struct {
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
func (dirisendiri *Tssentri) Pasang(gdt *TShareddescriptorTabel, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MCetakxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(dirisendiri)))
	console_2.MUnsignedinteger32Cetak(base)
	console_2.MCetak(":")

	gdt.Aturdescriptor(idx, base, uint32(Sizeof(Tssentri{})), 0xE9, 0)
	dirisendiri.ss0 = kernelss
	dirisendiri.esp0 = kernelesp
	dirisendiri.iomap = uint16(Sizeof(Tssentri{}))

	flushtss(SegTugasStatus)

}
func (dirisendiri *Tssentri) Aturstack(kernelss uint32, kernelesp uint32) {
	dirisendiri.ss0 = kernelss
	dirisendiri.esp0 = kernelesp
}
func (dirisendiri *Tssentri) Getesp0() uint32 {
	return dirisendiri.esp0
}
func (dirisendiri *Tssentri) Getss0() uint32 {
	return dirisendiri.ss0
}
