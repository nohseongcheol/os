/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "pomnilnikmanager"
import . "gdt"

var Preizkus uint8

func halt()

type TcpuStanje struct {
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

type TNaloga struct {
	stack		[4096]uint8
	cPEStanje	*TcpuStanje
}

func (sam *TNaloga) Init(gdt *TShareddescriptorPreglednica, mem *mem.TPomnilnikmanager, vnospoint_2 func()) {

	sam.cPEStanje = (*TcpuStanje)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStanje{})))

	sam.cPEStanje.Eax = 0
	sam.cPEStanje.Ebx = 0
	sam.cPEStanje.Ecx = 0
	sam.cPEStanje.Edx = 0

	sam.cPEStanje.Esi = 0
	sam.cPEStanje.Edi = 0

	sam.cPEStanje.Gs = 0
	sam.cPEStanje.Fs = 0
	sam.cPEStanje.Es = 0
	sam.cPEStanje.Ds = 0

	sam.cPEStanje.Eip = uint32(ValueOf(vnospoint_2).Pointer())
	sam.cPEStanje.Cs = Segkernelcode
	sam.cPEStanje.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(sam.cPEStanje)))

	sam.cPEStanje.Esp = stackaddress
	sam.cPEStanje.Ebp = stackaddress
	sam.cPEStanje.Ss = 0

}

type TNalogamanager struct {
}

var naloge [256]TNaloga
var številkaNaloge int
var currentNaloga int

func (sam *TNalogamanager) Init() {
	številkaNaloge = 0
	currentNaloga = -1
}

func (sam *TNalogamanager) DodajNaloga(naloga TNaloga) bool {
	if številkaNaloge >= 255 {
		return false
	}
	naloge[številkaNaloge] = naloga
	številkaNaloge++
	return true
}

func (sam *TNalogamanager) Schedule(cPEStanje *TcpuStanje) *TcpuStanje {

	console_2 := TConsole{}
	for i := 0; i < številkaNaloge; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(naloge[i].cPEStanje)))

		console_2.MUnsignedinteger32Natisnixy(x, 10, uint16(15+i))
	}
	if številkaNaloge <= 0 {
		return cPEStanje
	}

	if currentNaloga >= 0 {
		naloge[currentNaloga].cPEStanje = cPEStanje
	}

	currentNaloga++
	if currentNaloga >= številkaNaloge {
		currentNaloga %= številkaNaloge

	}

	return naloge[currentNaloga].cPEStanje
}
