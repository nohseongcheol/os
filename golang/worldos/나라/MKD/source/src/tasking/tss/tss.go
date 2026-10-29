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

var tssИндекс uint32 = 0
var flushИндекс uint32 = 0

func flushtss(uint32)
func (само *Tssentry) Инсталирај(gdt *TShareddescriptorТабела, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MПечатиxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(само)))
	console_2.MUnsignedinteger32Печати(base)
	console_2.MПечати(":")

	gdt.Поставиdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	само.ss0 = kernelss
	само.esp0 = kernelesp
	само.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segtaskstate)

}
func (само *Tssentry) Поставиstack(kernelss uint32, kernelesp uint32) {
	само.ss0 = kernelss
	само.esp0 = kernelesp
}
func (само *Tssentry) Getesp0() uint32 {
	return само.esp0
}
func (само *Tssentry) Getss0() uint32 {
	return само.ss0
}
