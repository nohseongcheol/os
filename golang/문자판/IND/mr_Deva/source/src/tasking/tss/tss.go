package tss

import . "unsafe"
import . "gdt"
import . "console"

var 콘솔 = T콘솔{}

type TSSEntry struct {
	PrevTSS	uint32
	esp0		uint32
	ss0		uint32
	esp1		uint32
	ss1		uint32
	esp2		uint32
	ss2		uint32
	cr3		uint32
	eip		uint32
	eflags	uint32
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

var tssIndex uint32 = 0
var flushIndex uint32 = 0

func flush_tss(uint32)
func (self *TSSEntry) Install(gdt *T공용서술자테이블, idx int, kernelSS uint32, kernelESP uint32) {

	콘솔.M출력XY(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(self)))
	콘솔.MUint32출력(base)
	콘솔.M출력(":")

	gdt.SetDescriptor(idx, base, uint32(Sizeof(TSSEntry{})), 0xE9, 0)
	self.ss0 = kernelSS
	self.esp0 = kernelESP
	self.iomap = uint16(Sizeof(TSSEntry{}))

	flush_tss(SEG_TASK_STATE)

}
func (self *TSSEntry) SetStack(kernelSS uint32, kernelESP uint32) {
	self.ss0 = kernelSS
	self.esp0 = kernelESP
}
func (self *TSSEntry) GetESP0() uint32 {
	return self.esp0
}
func (self *TSSEntry) GetSS0() uint32 {
	return self.ss0
}
