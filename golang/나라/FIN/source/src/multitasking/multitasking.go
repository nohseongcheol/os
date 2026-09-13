package multitasking

import . "unsafe"
import . "konsoli"
import . "reflect"
import mem "muistimanager"
import . "gdt"

var Kokeile uint8

func halt()

type TcpuTila struct {
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

type TTehtävä struct {
	pinomuisti	[4096]uint8
	cpuTila	*TcpuTila
}

func (itse *TTehtävä) Init(gdt *TShareddescriptorTaulukko, mem *mem.TMuistimanager, hakusanapoint_2 func()) {

	itse.cpuTila = (*TcpuTila)(Pointer(uintptr(mem.Varaa_muistia(1024*1024)) + 1024*1024 - Sizeof(TcpuTila{})))

	itse.cpuTila.Eax = 0
	itse.cpuTila.Ebx = 0
	itse.cpuTila.Ecx = 0
	itse.cpuTila.Edx = 0

	itse.cpuTila.Esi = 0
	itse.cpuTila.Edi = 0

	itse.cpuTila.Gs = 0
	itse.cpuTila.Fs = 0
	itse.cpuTila.Es = 0
	itse.cpuTila.Ds = 0

	itse.cpuTila.Eip = uint32(ValueOf(hakusanapoint_2).Pointer())
	itse.cpuTila.Cs = Segkernelcode
	itse.cpuTila.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(itse.cpuTila)))

	itse.cpuTila.Esp = stackaddress
	itse.cpuTila.Ebp = stackaddress
	itse.cpuTila.Ss = 0

}

type TTehtävämanager struct {
}

var tehtävät [256]TTehtävä
var numeroTehtävät int
var nykyinenTehtävä int

func (itse *TTehtävämanager) Init() {
	numeroTehtävät = 0
	nykyinenTehtävä = -1
}

func (itse *TTehtävämanager) LisääTehtävä(tehtävä TTehtävä) bool {
	if numeroTehtävät >= 255 {
		return false
	}
	tehtävät[numeroTehtävät] = tehtävä
	numeroTehtävät++
	return true
}

func (itse *TTehtävämanager) Schedule(cpuTila *TcpuTila) *TcpuTila {

	konsoli_2 := TKonsoli{}
	for i := 0; i < numeroTehtävät; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tehtävät[i].cpuTila)))

		konsoli_2.MUnsignedinteger32Tulostaxy(x, 10, uint16(15+i))
	}
	if numeroTehtävät <= 0 {
		return cpuTila
	}

	if nykyinenTehtävä >= 0 {
		tehtävät[nykyinenTehtävä].cpuTila = cpuTila
	}

	nykyinenTehtävä++
	if nykyinenTehtävä >= numeroTehtävät {
		nykyinenTehtävä %= numeroTehtävät

	}

	return tehtävät[nykyinenTehtävä].cpuTila
}
