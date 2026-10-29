/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "console"

var console_2 = TConsole{}

type Tsspontodeentrada struct {
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

var tssÍndice uint32 = 0
var flushÍndice uint32 = 0

func flushtss(uint32)
func (próprio *Tsspontodeentrada) Instalar(gdt *TShareddescriptorTabela, idx int, núcleoss uint32, núcleoesp uint32) {

	console_2.MImprimirxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(próprio)))
	console_2.MUnsignedinteger32Imprimir(base)
	console_2.MImprimir(":")

	gdt.Conjuntodescriptor(idx, base, uint32(Sizeof(Tsspontodeentrada{})), 0xE9, 0)
	próprio.ss0 = núcleoss
	próprio.esp0 = núcleoesp
	próprio.iomap = uint16(Sizeof(Tsspontodeentrada{}))

	flushtss(SegtarefaEstado)

}
func (próprio *Tsspontodeentrada) Conjuntostack(núcleoss uint32, núcleoesp uint32) {
	próprio.ss0 = núcleoss
	próprio.esp0 = núcleoesp
}
func (próprio *Tsspontodeentrada) Getesp0() uint32 {
	return próprio.esp0
}
func (próprio *Tsspontodeentrada) Getss0() uint32 {
	return próprio.ss0
}
