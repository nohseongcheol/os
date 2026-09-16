/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "minnemanager"
import . "gdt"

var Test uint8

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

type TOppgave struct {
	stack		[4096]uint8
	cpuStatus	*TcpuStatus
}

func (selv *TOppgave) Init(gdt *TShareddescriptorTabell, mem *mem.TMinnemanager, entrypoint_2 func()) {

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

	selv.cpuStatus.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	selv.cpuStatus.Cs = Segkernelcode
	selv.cpuStatus.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(selv.cpuStatus)))

	selv.cpuStatus.Esp = stackaddress
	selv.cpuStatus.Ebp = stackaddress
	selv.cpuStatus.Ss = 0

}

type TOppgavemanager struct {
}

var oppgaver [256]TOppgave
var tallOppgaver int
var gjeldendeOppgave int

func (selv *TOppgavemanager) Init() {
	tallOppgaver = 0
	gjeldendeOppgave = -1
}

func (selv *TOppgavemanager) LeggtilOppgave(oppgave TOppgave) bool {
	if tallOppgaver >= 255 {
		return false
	}
	oppgaver[tallOppgaver] = oppgave
	tallOppgaver++
	return true
}

func (selv *TOppgavemanager) Schedule(cpuStatus *TcpuStatus) *TcpuStatus {

	console_2 := TConsole{}
	for i := 0; i < tallOppgaver; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(oppgaver[i].cpuStatus)))

		console_2.MUnsignedinteger32Skrivutxy(x, 10, uint16(15+i))
	}
	if tallOppgaver <= 0 {
		return cpuStatus
	}

	if gjeldendeOppgave >= 0 {
		oppgaver[gjeldendeOppgave].cpuStatus = cpuStatus
	}

	gjeldendeOppgave++
	if gjeldendeOppgave >= tallOppgaver {
		gjeldendeOppgave %= tallOppgaver

	}

	return oppgaver[gjeldendeOppgave].cpuStatus
}
