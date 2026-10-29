/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "консоль"

var консоль_2 = TКонсоль{}

type Tssзапись struct {
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

var tssСодержание uint32 = 0
var flushСодержание uint32 = 0

func flushtss(uint32)
func (текущий *Tssзапись) Установить(gdt *TShareddescriptorТаблица, idx int, ядроss uint32, ядроesp uint32) {

	консоль_2.MПечатьxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(текущий)))
	консоль_2.MUnsignedinteger32Печать(base)
	консоль_2.MПечать(":")

	gdt.Указатьdescriptor(idx, base, uint32(Sizeof(Tssзапись{})), 0xE9, 0)
	текущий.ss0 = ядроss
	текущий.esp0 = ядроesp
	текущий.iomap = uint16(Sizeof(Tssзапись{}))

	flushtss(SegзадачаСостояние)

}
func (текущий *Tssзапись) Указатьstack(ядроss uint32, ядроesp uint32) {
	текущий.ss0 = ядроss
	текущий.esp0 = ядроesp
}
func (текущий *Tssзапись) Getesp0() uint32 {
	return текущий.esp0
}
func (текущий *Tssзапись) Getss0() uint32 {
	return текущий.ss0
}
