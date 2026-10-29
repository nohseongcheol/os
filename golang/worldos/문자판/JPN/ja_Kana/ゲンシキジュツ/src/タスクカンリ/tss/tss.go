/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "コンソール"

var コンソール_2 = Tコンソール{}

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

var tssモクジ uint32 = 0
var flushモクジ uint32 = 0

func flushtss(uint32)
func (self *Tssentry) Iインストール(gdt *TShareddescriptortable, idx int, チュウカクss uint32, チュウカクesp uint32) {

	コンソール_2.Mインサツxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	コンソール_2.MUnsignedinteger32インサツ(base)
	コンソール_2.Mインサツ(":")

	gdt.Sアリdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	self.ss0 = チュウカクss
	self.esp0 = チュウカクesp
	self.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segタスクジョウタイ)

}
func (self *Tssentry) Sアリstack(チュウカクss uint32, チュウカクesp uint32) {
	self.ss0 = チュウカクss
	self.esp0 = チュウカクesp
}
func (self *Tssentry) Getesp0() uint32 {
	return self.esp0
}
func (self *Tssentry) Getss0() uint32 {
	return self.ss0
}
