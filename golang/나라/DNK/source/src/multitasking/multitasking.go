/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "hukommelsemanager"
import . "gdt"

var Prøv uint8

func halt()

type TcpuStatus struct {
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

type TOpgave struct {
	stack		[4096]uint8
	cpuStatus	*TcpuStatus
}

func (selv *TOpgave) Init(gdt *TShareddescriptorTabel, mem *mem.THukommelsemanager, emnepoint_2 func()) {

	selv.cpuStatus = (*TcpuStatus)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStatus{})))

	selv.cpuStatus.Eax = 0
	selv.cpuStatus.Ebx = 0
	selv.cpuStatus.Ecx = 0
	selv.cpuStatus.Edx = 0

	selv.cpuStatus.Esi = 0
	selv.cpuStatus.Edi = 0

	selv.cpuStatus.Gs = 0
	selv.cpuStatus.Fs = 0
	selv.cpuStatus.Es = 0
	selv.cpuStatus.Ds = 0

	selv.cpuStatus.Eip = uint32(ValueOf(emnepoint_2).Pointer())
	selv.cpuStatus.Cs = Segkernelcode
	selv.cpuStatus.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(selv.cpuStatus)))

	selv.cpuStatus.Esp = stackaddress
	selv.cpuStatus.Ebp = stackaddress
	selv.cpuStatus.Ss = 0

}

type TOpgavemanager struct {
}

var opgaver [256]TOpgave
var talOpgaver int
var aktiveOpgave int

func (selv *TOpgavemanager) Init() {
	talOpgaver = 0
	aktiveOpgave = -1
}

func (selv *TOpgavemanager) TilføjOpgave(opgave TOpgave) bool {
	if talOpgaver >= 255 {
		return false
	}
	opgaver[talOpgaver] = opgave
	talOpgaver++
	return true
}

func (selv *TOpgavemanager) Schedule(cpuStatus *TcpuStatus) *TcpuStatus {

	console_2 := TConsole{}
	for i := 0; i < talOpgaver; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(opgaver[i].cpuStatus)))

		console_2.MUnsignedinteger32Udskrivxy(x, 10, uint16(15+i))
	}
	if talOpgaver <= 0 {
		return cpuStatus
	}

	if aktiveOpgave >= 0 {
		opgaver[aktiveOpgave].cpuStatus = cpuStatus
	}

	aktiveOpgave++
	if aktiveOpgave >= talOpgaver {
		aktiveOpgave %= talOpgaver

	}

	return opgaver[aktiveOpgave].cpuStatus
}
