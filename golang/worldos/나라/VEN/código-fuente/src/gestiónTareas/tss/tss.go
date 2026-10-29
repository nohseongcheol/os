/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tss

import . "unsafe"
import . "gdt"
import . "consola"

var consola_2 = TConsola{}

type Tssentrada struct {
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
func (propio *Tssentrada) Instalar(gdt *TShareddescriptorTabla, idx int, núcleoss uint32, núcleoesp uint32) {

	consola_2.MImprimirxy(([]byte)("tss:"), 20, 13)
	base := uint32(uintptr(Pointer(propio)))
	consola_2.MUnsignedinteger32Imprimir(base)
	consola_2.MImprimir(":")

	gdt.Establecerdescriptor(idx, base, uint32(Sizeof(Tssentrada{})), 0xE9, 0)
	propio.ss0 = núcleoss
	propio.esp0 = núcleoesp
	propio.iomap = uint16(Sizeof(Tssentrada{}))

	flushtss(SegtareaEstado)

}
func (propio *Tssentrada) Establecerstack(núcleoss uint32, núcleoesp uint32) {
	propio.ss0 = núcleoss
	propio.esp0 = núcleoesp
}
func (propio *Tssentrada) Getesp0() uint32 {
	return propio.esp0
}
func (propio *Tssentrada) Getss0() uint32 {
	return propio.ss0
}
