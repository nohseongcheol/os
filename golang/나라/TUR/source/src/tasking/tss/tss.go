package tss

import . "unsafe"
import . "gdt"
import . "konsol"

var konsol_2 = TKonsol{}

type Tssgirdi struct {
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

var tssİçindekiler uint32 = 0
var flushİçindekiler uint32 = 0

func flushtss(uint32)
func (self *Tssgirdi) Kur(gdt *TShareddescriptorTablo, idx int, kernelss uint32, kernelesp uint32) {

	konsol_2.MYazdırxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	konsol_2.MUnsignedinteger32Yazdır(base)
	konsol_2.MYazdır(":")

	gdt.Ayarladescriptor(idx, base, uint32(Sizeof(Tssgirdi{})), 0xE9, 0)
	self.ss0 = kernelss
	self.esp0 = kernelesp
	self.iomap = uint16(Sizeof(Tssgirdi{}))

	flushtss(SegGörevDurum)

}
func (self *Tssgirdi) Ayarlastack(kernelss uint32, kernelesp uint32) {
	self.ss0 = kernelss
	self.esp0 = kernelesp
}
func (self *Tssgirdi) Getesp0() uint32 {
	return self.esp0
}
func (self *Tssgirdi) Getss0() uint32 {
	return self.ss0
}
