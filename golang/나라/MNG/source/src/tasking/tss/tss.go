package tss

import . "unsafe"
import . "gdt"
import . "консол"

var консол_2 = TКонсол{}

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

var tssҮзүүлэлт uint32 = 0
var flushҮзүүлэлт uint32 = 0

func flushtss(uint32)
func (self *Tssentry) Суулгах(gdt *TShareddescriptortable, idx int, kernelss uint32, kernelesp uint32) {

	консол_2.MХэвлэхxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	консол_2.MUnsignedinteger32Хэвлэх(base)
	консол_2.MХэвлэх(":")

	gdt.Setdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	self.ss0 = kernelss
	self.esp0 = kernelesp
	self.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segtaskstate)

}
func (self *Tssentry) Setstack(kernelss uint32, kernelesp uint32) {
	self.ss0 = kernelss
	self.esp0 = kernelesp
}
func (self *Tssentry) Getesp0() uint32 {
	return self.esp0
}
func (self *Tssentry) Getss0() uint32 {
	return self.ss0
}
