package tss

import . "unsafe"
import . "gdt"
import . "konzole"

var konzole_2 = TKonzole{}

type TssZáznam struct {
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

var tssRejstřík uint32 = 0
var flushRejstřík uint32 = 0

func flushtss(uint32)
func (self *TssZáznam) Instalovat(gdt *TShareddescriptorTabulka, idx int, kernelss uint32, kernelesp uint32) {

	konzole_2.MTisknoutxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	konzole_2.MUnsignedinteger32Tisknout(base)
	konzole_2.MTisknout(":")

	gdt.Nastavitdescriptor(idx, base, uint32(Sizeof(TssZáznam{})), 0xE9, 0)
	self.ss0 = kernelss
	self.esp0 = kernelesp
	self.iomap = uint16(Sizeof(TssZáznam{}))

	flushtss(SegÚlohaStav)

}
func (self *TssZáznam) Nastavitstack(kernelss uint32, kernelesp uint32) {
	self.ss0 = kernelss
	self.esp0 = kernelesp
}
func (self *TssZáznam) Getesp0() uint32 {
	return self.esp0
}
func (self *TssZáznam) Getss0() uint32 {
	return self.ss0
}
