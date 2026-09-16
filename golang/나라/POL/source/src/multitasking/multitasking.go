/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konsola"
import . "reflect"
import mem "pamięćmanager"
import . "gdt"

var Przetestuj uint8

func halt()

type TcpuStan struct {
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

type TZadanie struct {
	pamięć_stosu		[4096]uint8
	procesorStan	*TcpuStan
}

func (bieżący *TZadanie) Init(gdt *TShareddescriptorTabela, mem *mem.TPamięćmanager, wpispoint_2 func()) {

	bieżący.procesorStan = (*TcpuStan)(Pointer(uintptr(mem.Przydziel_pamięć(1024*1024)) + 1024*1024 - Sizeof(TcpuStan{})))

	bieżący.procesorStan.Eax = 0
	bieżący.procesorStan.Ebx = 0
	bieżący.procesorStan.Ecx = 0
	bieżący.procesorStan.Edx = 0

	bieżący.procesorStan.Esi = 0
	bieżący.procesorStan.Edi = 0

	bieżący.procesorStan.Gs = 0
	bieżący.procesorStan.Fs = 0
	bieżący.procesorStan.Es = 0
	bieżący.procesorStan.Ds = 0

	bieżący.procesorStan.Eip = uint32(ValueOf(wpispoint_2).Pointer())
	bieżący.procesorStan.Cs = Segkernelcode
	bieżący.procesorStan.Eflags = 0x202

	var stackAdres = uint32(uintptr(Pointer(bieżący.procesorStan)))

	bieżący.procesorStan.Esp = stackAdres
	bieżący.procesorStan.Ebp = stackAdres
	bieżący.procesorStan.Ss = 0

}

type TZadaniemanager struct {
}

var zadania [256]TZadanie
var liczbaZadania int
var bieżącyZadanie int

func (bieżący *TZadaniemanager) Init() {
	liczbaZadania = 0
	bieżącyZadanie = -1
}

func (bieżący *TZadaniemanager) DodajZadanie(zadanie TZadanie) bool {
	if liczbaZadania >= 255 {
		return false
	}
	zadania[liczbaZadania] = zadanie
	liczbaZadania++
	return true
}

func (bieżący *TZadaniemanager) Schedule(procesorStan *TcpuStan) *TcpuStan {

	konsola_2 := TKonsola{}
	for i := 0; i < liczbaZadania; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(zadania[i].procesorStan)))

		konsola_2.MUnsignedinteger32Wydrukujxy(x, 10, uint16(15+i))
	}
	if liczbaZadania <= 0 {
		return procesorStan
	}

	if bieżącyZadanie >= 0 {
		zadania[bieżącyZadanie].procesorStan = procesorStan
	}

	bieżącyZadanie++
	if bieżącyZadanie >= liczbaZadania {
		bieżącyZadanie %= liczbaZadania

	}

	return zadania[bieżącyZadanie].procesorStan
}
