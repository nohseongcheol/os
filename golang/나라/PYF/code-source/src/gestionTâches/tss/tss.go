/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tssélément struct {
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
func (self *Tssélément) Installer(gdt *TShareddescriptorTableau, idx int, noyauss uint32, noyauesp uint32) {

	console_2.MImprimerxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	console_2.MUnsignedinteger32Imprimer(base)
	console_2.MImprimer(":")

	gdt.Ensembledescriptor(idx, base, uint32(Sizeof(Tssélément{})), 0xE9, 0)
	self.ss0 = noyauss
	self.esp0 = noyauesp
	self.iomap = uint16(Sizeof(Tssélément{}))

	flushtss(SegtâcheÉtat)

}
func (self *Tssélément) Ensemblestack(noyauss uint32, noyauesp uint32) {
	self.ss0 = noyauss
	self.esp0 = noyauesp
}
func (self *Tssélément) Getesp0() uint32 {
	return self.esp0
}
func (self *Tssélément) Getss0() uint32 {
	return self.ss0
}
