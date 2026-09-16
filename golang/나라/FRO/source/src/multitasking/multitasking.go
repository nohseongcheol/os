/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "memorymanager"
import . "gdt"

var Test uint8

func halt()

type TcpuStøða struct {
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
	cpuStøða	*TcpuStøða
}

func (self *TTask) Init(gdt *TShareddescriptortable, mem *mem.TMemorymanager, entrypoint_2 func()) {

	self.cpuStøða = (*TcpuStøða)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStøða{})))

	self.cpuStøða.Eax = 0
	self.cpuStøða.Ebx = 0
	self.cpuStøða.Ecx = 0
	self.cpuStøða.Edx = 0

	self.cpuStøða.Esi = 0
	self.cpuStøða.Edi = 0

	self.cpuStøða.Gs = 0
	self.cpuStøða.Fs = 0
	self.cpuStøða.Es = 0
	self.cpuStøða.Ds = 0

	self.cpuStøða.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.cpuStøða.Cs = Segkernelcode
	self.cpuStøða.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpuStøða)))

	self.cpuStøða.Esp = stackaddress
	self.cpuStøða.Ebp = stackaddress
	self.cpuStøða.Ss = 0

}

type TTaskmanager struct {
}

var tasks [256]TTask
var numbertasks int
var currenttask int

func (self *TTaskmanager) Init() {
	numbertasks = 0
	currenttask = -1
}

func (self *TTaskmanager) Addtask(task TTask) bool {
	if numbertasks >= 255 {
		return false
	}
	tasks[numbertasks] = task
	numbertasks++
	return true
}

func (self *TTaskmanager) Schedule(cpuStøða *TcpuStøða) *TcpuStøða {

	console_2 := TConsole{}
	for i := 0; i < numbertasks; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tasks[i].cpuStøða)))

		console_2.MUnsignedinteger32printxy(x, 10, uint16(15+i))
	}
	if numbertasks <= 0 {
		return cpuStøða
	}

	if currenttask >= 0 {
		tasks[currenttask].cpuStøða = cpuStøða
	}

	currenttask++
	if currenttask >= numbertasks {
		currenttask %= numbertasks

	}

	return tasks[currenttask].cpuStøða
}
