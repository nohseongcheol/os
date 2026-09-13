package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "memorymanager"
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

func (self *TTask) Init(gdt *TShareddescriptortable, mem *mem.TMemorymanager, entrypoint_2 func()) {

	self.cpustate = (*Tcpustate)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpustate{})))

	self.cpustate.Eax = 0
	self.cpustate.Ebx = 0
	self.cpustate.Ecx = 0
	self.cpustate.Edx = 0

	self.cpustate.Esi = 0
	self.cpustate.Edi = 0

	self.cpustate.Gs = 0
	self.cpustate.Fs = 0
	self.cpustate.Es = 0
	self.cpustate.Ds = 0

	self.cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.cpustate.Cs = Segkernelcode
	self.cpustate.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpustate)))

	self.cpustate.Esp = stackaddress
	self.cpustate.Ebp = stackaddress
	self.cpustate.Ss = 0

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

func (self *TTaskmanager) Schedule(cpustate *Tcpustate) *Tcpustate {

	console_2 := TConsole{}
	for i := 0; i < numbertasks; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tasks[i].cpustate)))

		console_2.MUnsignedinteger32printxy(x, 10, uint16(15+i))
	}
	if numbertasks <= 0 {
		return cpustate
	}

	if currenttask >= 0 {
		tasks[currenttask].cpustate = cpustate
	}

	currenttask++
	if currenttask >= numbertasks {
		currenttask %= numbertasks

	}

	return tasks[currenttask].cpustate
}
