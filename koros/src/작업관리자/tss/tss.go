/*
        Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/


package tss

import . "unsafe"
import . "gdt"

type TSSEntry struct{
	prevTSS uint32
	esp0 uint32
	ss0 uint32
	esp1 uint32
	ss1 uint32
	esp2 uint32
	ss2 uint32
	cr3 uint32
	eip uint32
	Eflags uint32
	eax uint32
	ecx uint32
	edx uint32
	ebx uint32
	esp uint32
	ebp uint32
	esi uint32
	edi uint32
	es uint32
	cs uint32
	ss uint32
	ds uint32
	fs uint32
	gs uint32
	ldt uint32
	trap uint16
	iomap uint16
}

var tss TSSEntry = TSSEntry{}

func flush_tss(uint32)

func (self *TSSEntry) New(){
}
func (self *TSSEntry) Install(gdt *T공용서술자표, idx int, kernelSS uint32, kernelESP uint32){

	var base uint32 = uint32(uintptr(Pointer(&tss)))
	gdt.M설명자_설정(idx, base, uint32(Sizeof(TSSEntry{})), 0xE9, 0)
	tss.ss0 = kernelSS
	tss.esp0 = kernelESP
	tss.iomap = uint16(Sizeof(TSSEntry{}))

	flush_tss(SEG_TASK_STATE)
	
}
func (self *TSSEntry) M스택_설정(kernelSS uint32, kernelESP uint32){
	tss.ss0 = kernelSS
	tss.esp0 = kernelESP
}
