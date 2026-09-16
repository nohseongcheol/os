/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "ማስታወሻmanager"
import . "gdt"

var Tመሞከሪያ uint8

func halt()

type Tcpuሁኔታ struct {
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
	stack	[4096]uint8
	cpuሁኔታ	*Tcpuሁኔታ
}

func (self *TTask) Init(gdt *TShareddescriptorሰንጠረዥ, mem *mem.Tማስታወሻmanager, entrypoint_2 func()) {

	self.cpuሁኔታ = (*Tcpuሁኔታ)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpuሁኔታ{})))

	self.cpuሁኔታ.Eax = 0
	self.cpuሁኔታ.Ebx = 0
	self.cpuሁኔታ.Ecx = 0
	self.cpuሁኔታ.Edx = 0

	self.cpuሁኔታ.Esi = 0
	self.cpuሁኔታ.Edi = 0

	self.cpuሁኔታ.Gs = 0
	self.cpuሁኔታ.Fs = 0
	self.cpuሁኔታ.Es = 0
	self.cpuሁኔታ.Ds = 0

	self.cpuሁኔታ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.cpuሁኔታ.Cs = Segkernelcode
	self.cpuሁኔታ.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpuሁኔታ)))

	self.cpuሁኔታ.Esp = stackaddress
	self.cpuሁኔታ.Ebp = stackaddress
	self.cpuሁኔታ.Ss = 0

}

type TTaskmanager struct {
}

var tasks [256]TTask
var ቁጥርtasks int
var currenttask int

func (self *TTaskmanager) Init() {
	ቁጥርtasks = 0
	currenttask = -1
}

func (self *TTaskmanager) Aመጨመሪያtask(task TTask) bool {
	if ቁጥርtasks >= 255 {
		return false
	}
	tasks[ቁጥርtasks] = task
	ቁጥርtasks++
	return true
}

func (self *TTaskmanager) Schedule(cpuሁኔታ *Tcpuሁኔታ) *Tcpuሁኔታ {

	console_2 := TConsole{}
	for i := 0; i < ቁጥርtasks; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tasks[i].cpuሁኔታ)))

		console_2.MUnsignedinteger32ማተሚያxy(x, 10, uint16(15+i))
	}
	if ቁጥርtasks <= 0 {
		return cpuሁኔታ
	}

	if currenttask >= 0 {
		tasks[currenttask].cpuሁኔታ = cpuሁኔታ
	}

	currenttask++
	if currenttask >= ቁጥርtasks {
		currenttask %= ቁጥርtasks

	}

	return tasks[currenttask].cpuሁኔታ
}
