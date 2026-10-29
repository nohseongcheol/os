/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssvoce struct {
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

var tssIndice uint32 = 0
var flushIndice uint32 = 0

func flushtss(uint32)
func (séstesso *Tssvoce) Installa(gdt *TShareddescriptorTabella, idx int, kernelss uint32, kernelesp uint32) {

	console_2.MStampaxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(séstesso)))
	console_2.MUnsignedinteger32Stampa(base)
	console_2.MStampa(":")

	gdt.Impostadescriptor(idx, base, uint32(Sizeof(Tssvoce{})), 0xE9, 0)
	séstesso.ss0 = kernelss
	séstesso.esp0 = kernelesp
	séstesso.iomap = uint16(Sizeof(Tssvoce{}))

	flushtss(SegProcessoStato)

}
func (séstesso *Tssvoce) Impostastack(kernelss uint32, kernelesp uint32) {
	séstesso.ss0 = kernelss
	séstesso.esp0 = kernelesp
}
func (séstesso *Tssvoce) Getesp0() uint32 {
	return séstesso.esp0
}
func (séstesso *Tssvoce) Getss0() uint32 {
	return séstesso.ss0
}
