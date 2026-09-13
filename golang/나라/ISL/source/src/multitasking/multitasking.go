package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "minnimanager"
import . "gdt"

var Prófun uint8

func halt()

type TcpuStaða struct {
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

type TVerk struct {
	stack		[4096]uint8
	cpuStaða	*TcpuStaða
}

func (sjálft *TVerk) Init(gdt *TShareddescriptorTafla, mem *mem.TMinnimanager, entrypoint_2 func()) {

	sjálft.cpuStaða = (*TcpuStaða)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStaða{})))

	sjálft.cpuStaða.Eax = 0
	sjálft.cpuStaða.Ebx = 0
	sjálft.cpuStaða.Ecx = 0
	sjálft.cpuStaða.Edx = 0

	sjálft.cpuStaða.Esi = 0
	sjálft.cpuStaða.Edi = 0

	sjálft.cpuStaða.Gs = 0
	sjálft.cpuStaða.Fs = 0
	sjálft.cpuStaða.Es = 0
	sjálft.cpuStaða.Ds = 0

	sjálft.cpuStaða.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	sjálft.cpuStaða.Cs = Segkernelcode
	sjálft.cpuStaða.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(sjálft.cpuStaða)))

	sjálft.cpuStaða.Esp = stackaddress
	sjálft.cpuStaða.Ebp = stackaddress
	sjálft.cpuStaða.Ss = 0

}

type TVerkmanager struct {
}

var verkefni [256]TVerk
var numberVerkefni int
var núverandiVerk int

func (sjálft *TVerkmanager) Init() {
	numberVerkefni = 0
	núverandiVerk = -1
}

func (sjálft *TVerkmanager) BætaviðVerk(verk TVerk) bool {
	if numberVerkefni >= 255 {
		return false
	}
	verkefni[numberVerkefni] = verk
	numberVerkefni++
	return true
}

func (sjálft *TVerkmanager) Schedule(cpuStaða *TcpuStaða) *TcpuStaða {

	console_2 := TConsole{}
	for i := 0; i < numberVerkefni; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(verkefni[i].cpuStaða)))

		console_2.MUnsignedinteger32Prentaxy(x, 10, uint16(15+i))
	}
	if numberVerkefni <= 0 {
		return cpuStaða
	}

	if núverandiVerk >= 0 {
		verkefni[núverandiVerk].cpuStaða = cpuStaða
	}

	núverandiVerk++
	if núverandiVerk >= numberVerkefni {
		núverandiVerk %= numberVerkefni

	}

	return verkefni[núverandiVerk].cpuStaða
}
