/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "mälumanager"
import . "gdt"

var Testi uint8

func halt()

type TcpuOlek struct {
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
	protsessorOlek	*TcpuOlek
}

func (ise *TTask) Init(gdt *TShareddescriptorTabel, mem *mem.TMälumanager, kirjepoint_2 func()) {

	ise.protsessorOlek = (*TcpuOlek)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuOlek{})))

	ise.protsessorOlek.Eax = 0
	ise.protsessorOlek.Ebx = 0
	ise.protsessorOlek.Ecx = 0
	ise.protsessorOlek.Edx = 0

	ise.protsessorOlek.Esi = 0
	ise.protsessorOlek.Edi = 0

	ise.protsessorOlek.Gs = 0
	ise.protsessorOlek.Fs = 0
	ise.protsessorOlek.Es = 0
	ise.protsessorOlek.Ds = 0

	ise.protsessorOlek.Eip = uint32(ValueOf(kirjepoint_2).Pointer())
	ise.protsessorOlek.Cs = Segkernelcode
	ise.protsessorOlek.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(ise.protsessorOlek)))

	ise.protsessorOlek.Esp = stackaddress
	ise.protsessorOlek.Ebp = stackaddress
	ise.protsessorOlek.Ss = 0

}

type TTaskmanager struct {
}

var ülesanded [256]TTask
var arvÜlesanded int
var käesolevtask int

func (ise *TTaskmanager) Init() {
	arvÜlesanded = 0
	käesolevtask = -1
}

func (ise *TTaskmanager) Lisatask(task TTask) bool {
	if arvÜlesanded >= 255 {
		return false
	}
	ülesanded[arvÜlesanded] = task
	arvÜlesanded++
	return true
}

func (ise *TTaskmanager) Schedule(protsessorOlek *TcpuOlek) *TcpuOlek {

	console_2 := TConsole{}
	for i := 0; i < arvÜlesanded; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(ülesanded[i].protsessorOlek)))

		console_2.MUnsignedinteger32Prindixy(x, 10, uint16(15+i))
	}
	if arvÜlesanded <= 0 {
		return protsessorOlek
	}

	if käesolevtask >= 0 {
		ülesanded[käesolevtask].protsessorOlek = protsessorOlek
	}

	käesolevtask++
	if käesolevtask >= arvÜlesanded {
		käesolevtask %= arvÜlesanded

	}

	return ülesanded[käesolevtask].protsessorOlek
}
