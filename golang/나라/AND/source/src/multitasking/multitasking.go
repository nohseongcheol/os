package multitasking

import . "unsafe"
import . "consola"
import . "reflect"
import mem "memòriamanager"
import . "gdt"

var Prova uint8

func halt()

type TcpuEstat struct {
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

type TTasca struct {
	stack		[4096]uint8
	cpuEstat	*TcpuEstat
}

func (unmateix *TTasca) Init(gdt *TShareddescriptorTaula, mem *mem.TMemòriamanager, entradapoint_2 func()) {

	unmateix.cpuEstat = (*TcpuEstat)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuEstat{})))

	unmateix.cpuEstat.Eax = 0
	unmateix.cpuEstat.Ebx = 0
	unmateix.cpuEstat.Ecx = 0
	unmateix.cpuEstat.Edx = 0

	unmateix.cpuEstat.Esi = 0
	unmateix.cpuEstat.Edi = 0

	unmateix.cpuEstat.Gs = 0
	unmateix.cpuEstat.Fs = 0
	unmateix.cpuEstat.Es = 0
	unmateix.cpuEstat.Ds = 0

	unmateix.cpuEstat.Eip = uint32(ValueOf(entradapoint_2).Pointer())
	unmateix.cpuEstat.Cs = Segkernelcode
	unmateix.cpuEstat.Eflags = 0x202

	var stackAdreça = uint32(uintptr(Pointer(unmateix.cpuEstat)))

	unmateix.cpuEstat.Esp = stackAdreça
	unmateix.cpuEstat.Ebp = stackAdreça
	unmateix.cpuEstat.Ss = 0

}

type TTascamanager struct {
}

var tasques [256]TTasca
var nombreTasques int
var actualTasca int

func (unmateix *TTascamanager) Init() {
	nombreTasques = 0
	actualTasca = -1
}

func (unmateix *TTascamanager) AfegeixTasca(tasca TTasca) bool {
	if nombreTasques >= 255 {
		return false
	}
	tasques[nombreTasques] = tasca
	nombreTasques++
	return true
}

func (unmateix *TTascamanager) Schedule(cpuEstat *TcpuEstat) *TcpuEstat {

	consola_2 := TConsola{}
	for i := 0; i < nombreTasques; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tasques[i].cpuEstat)))

		consola_2.MUnsignedinteger32Imprimeixxy(x, 10, uint16(15+i))
	}
	if nombreTasques <= 0 {
		return cpuEstat
	}

	if actualTasca >= 0 {
		tasques[actualTasca].cpuEstat = cpuEstat
	}

	actualTasca++
	if actualTasca >= nombreTasques {
		actualTasca %= nombreTasques

	}

	return tasques[actualTasca].cpuEstat
}
