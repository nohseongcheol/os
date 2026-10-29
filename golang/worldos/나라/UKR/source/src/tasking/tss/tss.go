/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "консоль"

var консоль_2 = TКонсоль{}

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

var tssІндекс uint32 = 0
var flushІндекс uint32 = 0

func flushtss(uint32)
func (поточний *Tssзапис) Встановити(gdt *TShareddescriptorТаблиця, idx int, kernelss uint32, kernelesp uint32) {

	консоль_2.MДрукxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(поточний)))
	консоль_2.MUnsignedinteger32Друк(base)
	консоль_2.MДрук(":")

	gdt.Множинаdescriptor(idx, base, uint32(Sizeof(Tssзапис{})), 0xE9, 0)
	поточний.ss0 = kernelss
	поточний.esp0 = kernelesp
	поточний.iomap = uint16(Sizeof(Tssзапис{}))

	flushtss(SegЗадачаСтан)

}
func (поточний *Tssзапис) Множинаstack(kernelss uint32, kernelesp uint32) {
	поточний.ss0 = kernelss
	поточний.esp0 = kernelesp
}
func (поточний *Tssзапис) Getesp0() uint32 {
	return поточний.esp0
}
func (поточний *Tssзапис) Getss0() uint32 {
	return поточний.ss0
}
