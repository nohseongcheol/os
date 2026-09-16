/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konsolë"
import . "reflect"
import mem "memoriaManazhuesi"
import . "gdt"

var Provo uint8

func halt()

type TcpuGjendje struct {
	p1	uint32
	p2	uint32

	Eax	uint32
	Ebx	uint32
	Ecx	uint32
	Edx	uint32

	Esi	uint32
	Edi	uint32
	Ebp	uint32

	Gs	uint32
	Fs	uint32
	Es	uint32
	Ds	uint32

	Eip	uint32

	Cs	uint32
	Eflags	uint32

	Esp	uint32
	Ss	uint32
}

type TProces struct {
	stack		[4096]uint8
	cpuGjendje	*TcpuGjendje
}

func (vetvetja *TProces) Init(gdt *TShareddescriptorTabela, mem *mem.TMemoriaManazhuesi, entrypoint_2 func()) {

	vetvetja.cpuGjendje = (*TcpuGjendje)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuGjendje{})))

	vetvetja.cpuGjendje.Eax = 0
	vetvetja.cpuGjendje.Ebx = 0
	vetvetja.cpuGjendje.Ecx = 0
	vetvetja.cpuGjendje.Edx = 0

	vetvetja.cpuGjendje.Esi = 0
	vetvetja.cpuGjendje.Edi = 0

	vetvetja.cpuGjendje.Gs = 0
	vetvetja.cpuGjendje.Fs = 0
	vetvetja.cpuGjendje.Es = 0
	vetvetja.cpuGjendje.Ds = 0

	vetvetja.cpuGjendje.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	vetvetja.cpuGjendje.Cs = Segkernelcode
	vetvetja.cpuGjendje.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(vetvetja.cpuGjendje)))

	vetvetja.cpuGjendje.Esp = stackaddress
	vetvetja.cpuGjendje.Ebp = stackaddress
	vetvetja.cpuGjendje.Ss = 0

}

type TProcesManazhuesi struct {
}

var detyra [256]TProces
var numberDetyra int
var etanishmeProces int

func (vetvetja *TProcesManazhuesi) Init() {
	numberDetyra = 0
	etanishmeProces = -1
}

func (vetvetja *TProcesManazhuesi) ShtoProces(proces TProces) bool {
	if numberDetyra >= 255 {
		return false
	}
	detyra[numberDetyra] = proces
	numberDetyra++
	return true
}

func (vetvetja *TProcesManazhuesi) Schedule(cpuGjendje *TcpuGjendje) *TcpuGjendje {

	konsolë_2 := TKonsolë{}
	for i := 0; i < numberDetyra; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(detyra[i].cpuGjendje)))

		konsolë_2.MUnsignedinteger32Printoxy(x, 10, uint16(15+i))
	}
	if numberDetyra <= 0 {
		return cpuGjendje
	}

	if etanishmeProces >= 0 {
		detyra[etanishmeProces].cpuGjendje = cpuGjendje
	}

	etanishmeProces++
	if etanishmeProces >= numberDetyra {
		etanishmeProces %= numberDetyra

	}

	return detyra[etanishmeProces].cpuGjendje
}
