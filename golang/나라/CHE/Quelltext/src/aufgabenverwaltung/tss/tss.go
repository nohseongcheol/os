package tss

import . "unsafe"
import . "gdt"
import . "konsole"

var konsole_2 = TKonsole{}

type TssEintrag struct {
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

var tssInhalt uint32 = 0
var flushInhalt uint32 = 0

func flushtss(uint32)
func (selbst *TssEintrag) Installieren(gdt *TShareddescriptorTabelle, idx int, kernss uint32, kernesp uint32) {

	konsole_2.MDruckenxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(selbst)))
	konsole_2.MUnsignedinteger32Drucken(base)
	konsole_2.MDrucken(":")

	gdt.Setzendescriptor(idx, base, uint32(Sizeof(TssEintrag{})), 0xE9, 0)
	selbst.ss0 = kernss
	selbst.esp0 = kernesp
	selbst.iomap = uint16(Sizeof(TssEintrag{}))

	flushtss(SegAufgabeStatus)

}
func (selbst *TssEintrag) Setzenstack(kernss uint32, kernesp uint32) {
	selbst.ss0 = kernss
	selbst.esp0 = kernesp
}
func (selbst *TssEintrag) Getesp0() uint32 {
	return selbst.esp0
}
func (selbst *TssEintrag) Getss0() uint32 {
	return selbst.ss0
}
