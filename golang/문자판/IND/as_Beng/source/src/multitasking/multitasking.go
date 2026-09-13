package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "স্মৃতি"
import . "gdt"

var Test uint8

func 멈추기()

type TCPUState struct {
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
	cpustate	*TCPUState
}

func (self *TTask) Vআৰম্ভ_কৰা(gdt *T공용서술자테이블, mem *mem.TMemoryManager, entrypoint func()) {

	self.cpustate = (*TCPUState)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TCPUState{})))

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

	self.cpustate.Eip = uint32(ValueOf(entrypoint).Pointer())
	self.cpustate.Cs = SEG_KERNEL_CODE
	self.cpustate.Eflags = 0x202

	var stack_addr = uint32(uintptr(Pointer(self.cpustate)))

	self.cpustate.Esp = stack_addr
	self.cpustate.Ebp = stack_addr
	self.cpustate.Ss = 0

}

type T작업관리자 struct {
}

var tasks [256]TTask
var numTasks int
var currentTask int

func (self *T작업관리자) Vআৰম্ভ_কৰা() {
	numTasks = 0
	currentTask = -1
}

func (self *T작업관리자) AddTask(task TTask) bool {
	if numTasks >= 255 {
		return false
	}
	tasks[numTasks] = task
	numTasks++
	return true
}

func (self *T작업관리자) Schedule(cpustate *TCPUState) *TCPUState {

	콘솔 := T콘솔{}
	for i := 0; i < numTasks; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tasks[i].cpustate)))

		콘솔.MUint32출력XY(x, 10, uint16(15+i))
	}
	if numTasks <= 0 {
		return cpustate
	}

	if currentTask >= 0 {
		tasks[currentTask].cpustate = cpustate
	}

	currentTask++
	if currentTask >= numTasks {
		currentTask %= numTasks

	}

	return tasks[currentTask].cpustate
}
