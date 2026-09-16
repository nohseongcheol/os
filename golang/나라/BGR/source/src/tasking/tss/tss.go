/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssзапис struct {
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

var tssСъдържание uint32 = 0
var flushСъдържание uint32 = 0

func flushtss(uint32)
func (себеси *Tssзапис) Инсталиране(gdt *TShareddescriptorТаблица, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MПечатxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(себеси)))
	console_2.MUnsignedinteger32Печат(base)
	console_2.MПечат(":")

	gdt.Задайdescriptor(idx, base, uint32(Sizeof(Tssзапис{})), 0xE9, 0)
	себеси.ss0 = kernelss
	себеси.esp0 = kernelesp
	себеси.iomap = uint16(Sizeof(Tssзапис{}))

	flushtss(SegЗадачаСъстояние)

}
func (себеси *Tssзапис) Задайstack(kernelss uint32, kernelesp uint32) {
	себеси.ss0 = kernelss
	себеси.esp0 = kernelesp
}
func (себеси *Tssзапис) Getesp0() uint32 {
	return себеси.esp0
}
func (себеси *Tssзапис) Getss0() uint32 {
	return себеси.ss0
}
