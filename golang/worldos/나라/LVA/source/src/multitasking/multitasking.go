/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "atmiņamanager"
import . "gdt"

var Pārbaudīt uint8

func halt()

type TcpuStāvoklis struct {
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
	cpuStāvoklis	*TcpuStāvoklis
}

func (pats *TTask) Init(gdt *TShareddescriptorTabula, mem *mem.TAtmiņamanager, ierakstspoint_2 func()) {

	pats.cpuStāvoklis = (*TcpuStāvoklis)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStāvoklis{})))

	pats.cpuStāvoklis.Eax = 0
	pats.cpuStāvoklis.Ebx = 0
	pats.cpuStāvoklis.Ecx = 0
	pats.cpuStāvoklis.Edx = 0

	pats.cpuStāvoklis.Esi = 0
	pats.cpuStāvoklis.Edi = 0

	pats.cpuStāvoklis.Gs = 0
	pats.cpuStāvoklis.Fs = 0
	pats.cpuStāvoklis.Es = 0
	pats.cpuStāvoklis.Ds = 0

	pats.cpuStāvoklis.Eip = uint32(ValueOf(ierakstspoint_2).Pointer())
	pats.cpuStāvoklis.Cs = Segkernelcode
	pats.cpuStāvoklis.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(pats.cpuStāvoklis)))

	pats.cpuStāvoklis.Esp = stackaddress
	pats.cpuStāvoklis.Ebp = stackaddress
	pats.cpuStāvoklis.Ss = 0

}

type TTaskmanager struct {
}

var uzdevumi [256]TTask
var skaitlisUzdevumi int
var pašreizējaistask int

func (pats *TTaskmanager) Init() {
	skaitlisUzdevumi = 0
	pašreizējaistask = -1
}

func (pats *TTaskmanager) Pievienottask(task TTask) bool {
	if skaitlisUzdevumi >= 255 {
		return false
	}
	uzdevumi[skaitlisUzdevumi] = task
	skaitlisUzdevumi++
	return true
}

func (pats *TTaskmanager) Schedule(cpuStāvoklis *TcpuStāvoklis) *TcpuStāvoklis {

	console_2 := TConsole{}
	for i := 0; i < skaitlisUzdevumi; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(uzdevumi[i].cpuStāvoklis)))

		console_2.MUnsignedinteger32Drukātxy(x, 10, uint16(15+i))
	}
	if skaitlisUzdevumi <= 0 {
		return cpuStāvoklis
	}

	if pašreizējaistask >= 0 {
		uzdevumi[pašreizējaistask].cpuStāvoklis = cpuStāvoklis
	}

	pašreizējaistask++
	if pašreizējaistask >= skaitlisUzdevumi {
		pašreizējaistask %= skaitlisUzdevumi

	}

	return uzdevumi[pašreizējaistask].cpuStāvoklis
}
