/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konzola"
import . "reflect"
import mem "pamäťmanager"
import . "gdt"

var Otestovať uint8

func halt()

type TcpuStav struct {
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

type TUloha struct {
	stack		[4096]uint8
	procesorStav	*TcpuStav
}

func (vlastný *TUloha) Init(gdt *TShareddescriptorTabuľka, mem *mem.TPamäťmanager, položkapoint_2 func()) {

	vlastný.procesorStav = (*TcpuStav)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStav{})))

	vlastný.procesorStav.Eax = 0
	vlastný.procesorStav.Ebx = 0
	vlastný.procesorStav.Ecx = 0
	vlastný.procesorStav.Edx = 0

	vlastný.procesorStav.Esi = 0
	vlastný.procesorStav.Edi = 0

	vlastný.procesorStav.Gs = 0
	vlastný.procesorStav.Fs = 0
	vlastný.procesorStav.Es = 0
	vlastný.procesorStav.Ds = 0

	vlastný.procesorStav.Eip = uint32(ValueOf(položkapoint_2).Pointer())
	vlastný.procesorStav.Cs = Segkernelcode
	vlastný.procesorStav.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(vlastný.procesorStav)))

	vlastný.procesorStav.Esp = stackaddress
	vlastný.procesorStav.Ebp = stackaddress
	vlastný.procesorStav.Ss = 0

}

type TUlohamanager struct {
}

var úlohy [256]TUloha
var čísloÚlohy int
var aktuálnyUloha int

func (vlastný *TUlohamanager) Init() {
	čísloÚlohy = 0
	aktuálnyUloha = -1
}

func (vlastný *TUlohamanager) PridaťUloha(uloha TUloha) bool {
	if čísloÚlohy >= 255 {
		return false
	}
	úlohy[čísloÚlohy] = uloha
	čísloÚlohy++
	return true
}

func (vlastný *TUlohamanager) Schedule(procesorStav *TcpuStav) *TcpuStav {

	konzola_2 := TKonzola{}
	for i := 0; i < čísloÚlohy; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(úlohy[i].procesorStav)))

		konzola_2.MUnsignedinteger32Tlačiťxy(x, 10, uint16(15+i))
	}
	if čísloÚlohy <= 0 {
		return procesorStav
	}

	if aktuálnyUloha >= 0 {
		úlohy[aktuálnyUloha].procesorStav = procesorStav
	}

	aktuálnyUloha++
	if aktuálnyUloha >= čísloÚlohy {
		aktuálnyUloha %= čísloÚlohy

	}

	return úlohy[aktuálnyUloha].procesorStav
}
