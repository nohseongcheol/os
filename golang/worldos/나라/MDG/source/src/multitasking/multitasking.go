/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konsoly"
import . "reflect"
import mem "arikaMpandrindra"
import . "gdt"

var Test uint8

func halt()

type Tcpustate struct {
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

type TTask struct {
	stack		[4096]uint8
	cpustate	*Tcpustate
}

func (nytena *TTask) Init(gdt *TShareddescriptorFafana, mem *mem.TArikaMpandrindra, entrypoint_2 func()) {

	nytena.cpustate = (*Tcpustate)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpustate{})))

	nytena.cpustate.Eax = 0
	nytena.cpustate.Ebx = 0
	nytena.cpustate.Ecx = 0
	nytena.cpustate.Edx = 0

	nytena.cpustate.Esi = 0
	nytena.cpustate.Edi = 0

	nytena.cpustate.Gs = 0
	nytena.cpustate.Fs = 0
	nytena.cpustate.Es = 0
	nytena.cpustate.Ds = 0

	nytena.cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	nytena.cpustate.Cs = Segkernelcode
	nytena.cpustate.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(nytena.cpustate)))

	nytena.cpustate.Esp = stackaddress
	nytena.cpustate.Ebp = stackaddress
	nytena.cpustate.Ss = 0

}

type TTaskMpandrindra struct {
}

var zaraasa [256]TTask
var numberZaraasa int
var currenttask int

func (nytena *TTaskMpandrindra) Init() {
	numberZaraasa = 0
	currenttask = -1
}

func (nytena *TTaskMpandrindra) Ampidirotask(task TTask) bool {
	if numberZaraasa >= 255 {
		return false
	}
	zaraasa[numberZaraasa] = task
	numberZaraasa++
	return true
}

func (nytena *TTaskMpandrindra) Schedule(cpustate *Tcpustate) *Tcpustate {

	konsoly_2 := TKonsoly{}
	for i := 0; i < numberZaraasa; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(zaraasa[i].cpustate)))

		konsoly_2.MUnsignedinteger32Atontayxy(x, 10, uint16(15+i))
	}
	if numberZaraasa <= 0 {
		return cpustate
	}

	if currenttask >= 0 {
		zaraasa[currenttask].cpustate = cpustate
	}

	currenttask++
	if currenttask >= numberZaraasa {
		currenttask %= numberZaraasa

	}

	return zaraasa[currenttask].cpustate
}
