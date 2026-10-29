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

var tss目次 uint32 = 0
var flush目次 uint32 = 0

func flushtss(uint32)
func (self *Tssentry) Iインストール(gdt *TShareddescriptortable, idx int, 中核ss uint32, 中核esp uint32) {

	コンソール_2.M印刷xy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	コンソール_2.MUnsignedinteger32印刷(base)
	コンソール_2.M印刷(":")

	gdt.Sありdescriptor(idx, base, uint32(Sizeof(Tssentry{})), 0xE9, 0)
	self.ss0 = 中核ss
	self.esp0 = 中核esp
	self.iomap = uint16(Sizeof(Tssentry{}))

	flushtss(Segタスク状態)

}
func (self *Tssentry) Sありstack(中核ss uint32, 中核esp uint32) {
	self.ss0 = 中核ss
	self.esp0 = 中核esp
}
func (self *Tssentry) Getesp0() uint32 {
	return self.esp0
}
func (self *Tssentry) Getss0() uint32 {
	return self.ss0
}
