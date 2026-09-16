/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "memoriemanager"
import . "gdt"

var Testează uint8

func halt()

type TcpuStare struct {
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
	cpuStare	*TcpuStare
}

func (sine *TTask) Init(gdt *TShareddescriptorTabel, mem *mem.TMemoriemanager, înregistrarepoint_2 func()) {

	sine.cpuStare = (*TcpuStare)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStare{})))

	sine.cpuStare.Eax = 0
	sine.cpuStare.Ebx = 0
	sine.cpuStare.Ecx = 0
	sine.cpuStare.Edx = 0

	sine.cpuStare.Esi = 0
	sine.cpuStare.Edi = 0

	sine.cpuStare.Gs = 0
	sine.cpuStare.Fs = 0
	sine.cpuStare.Es = 0
	sine.cpuStare.Ds = 0

	sine.cpuStare.Eip = uint32(ValueOf(înregistrarepoint_2).Pointer())
	sine.cpuStare.Cs = Segkernelcode
	sine.cpuStare.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(sine.cpuStare)))

	sine.cpuStare.Esp = stackaddress
	sine.cpuStare.Ebp = stackaddress
	sine.cpuStare.Ss = 0

}

type TTaskmanager struct {
}

var sarcini [256]TTask
var numărSarcini int
var curentătask int

func (sine *TTaskmanager) Init() {
	numărSarcini = 0
	curentătask = -1
}

func (sine *TTaskmanager) Adaugătask(task TTask) bool {
	if numărSarcini >= 255 {
		return false
	}
	sarcini[numărSarcini] = task
	numărSarcini++
	return true
}

func (sine *TTaskmanager) Schedule(cpuStare *TcpuStare) *TcpuStare {

	console_2 := TConsole{}
	for i := 0; i < numărSarcini; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(sarcini[i].cpuStare)))

		console_2.MUnsignedinteger32Tipăreștexy(x, 10, uint16(15+i))
	}
	if numărSarcini <= 0 {
		return cpuStare
	}

	if curentătask >= 0 {
		sarcini[curentătask].cpuStare = cpuStare
	}

	curentătask++
	if curentătask >= numărSarcini {
		curentătask %= numărSarcini

	}

	return sarcini[curentătask].cpuStare
}
