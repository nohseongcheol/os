package tss

import . "unsafe"
import . "gdt"
import . "こんそーる"

var こんそーる_2 = Tこんそーる{}

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

var tssもくじ uint32 = 0
var flushもくじ uint32 = 0

func flushtss(uint32)
func (self *Tssentry) Iいんすとーる(gdt *TShareddescriptortable, idx int, ちゅうかくss uint32, ちゅうかくesp uint32) {

	こんそーる_2.Mいんさつxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	こんそーる_2.MUnsignedinteger32いんさつ(base)
	こんそーる_2.Mいんさつ(":")

	gdt.Sありdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	self.ss0 = ちゅうかくss
	self.esp0 = ちゅうかくesp
	self.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segたすくじょうたい)

}
func (self *Tssentry) Sありstack(ちゅうかくss uint32, ちゅうかくesp uint32) {
	self.ss0 = ちゅうかくss
	self.esp0 = ちゅうかくesp
}
func (self *Tssentry) Getesp0() uint32 {
	return self.esp0
}
func (self *Tssentry) Getss0() uint32 {
	return self.ss0
}
