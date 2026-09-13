package tss

import . "unsafe"
import . "gdt"
import . "控制台"

var 控制台_2 = T控制台{}

type Tss条目 struct {
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

var tss索引 uint32 = 0
var flush索引 uint32 = 0

func flushtss(uint32)
func (self *Tss条目) I安装(gdt *TShareddescriptor表格, idx int, 内核ss uint32, 内核esp uint32) {

	控制台_2.M打印xy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	控制台_2.MUnsignedinteger32打印(base)
	控制台_2.M打印(":")

	gdt.S集合descriptor(idx, base, uint32(Sizeof(Tss条目{})), 0xE9, 0)
	self.ss0 = 内核ss
	self.esp0 = 内核esp
	self.iomap = uint16(Sizeof(Tss条目{}))

	flushtss(Seg任务状态)

}
func (self *Tss条目) S集合stack(内核ss uint32, 内核esp uint32) {
	self.ss0 = 内核ss
	self.esp0 = 内核esp
}
func (self *Tss条目) Getesp0() uint32 {
	return self.esp0
}
func (self *Tss条目) Getss0() uint32 {
	return self.ss0
}
