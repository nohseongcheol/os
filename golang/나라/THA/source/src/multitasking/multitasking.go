package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "memorymanager"
import . "gdt"

var Tทดสอบ uint8

func halt()

type Tcpuสถานะ struct {
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
	cpuสถานะ	*Tcpuสถานะ
}

func (self *TTask) Init(gdt *TShareddescriptorตาราง, mem *mem.TMemorymanager, entrypoint_2 func()) {

	self.cpuสถานะ = (*Tcpuสถานะ)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpuสถานะ{})))

	self.cpuสถานะ.Eax = 0
	self.cpuสถานะ.Ebx = 0
	self.cpuสถานะ.Ecx = 0
	self.cpuสถานะ.Edx = 0

	self.cpuสถานะ.Esi = 0
	self.cpuสถานะ.Edi = 0

	self.cpuสถานะ.Gs = 0
	self.cpuสถานะ.Fs = 0
	self.cpuสถานะ.Es = 0
	self.cpuสถานะ.Ds = 0

	self.cpuสถานะ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.cpuสถานะ.Cs = Segkernelcode
	self.cpuสถานะ.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpuสถานะ)))

	self.cpuสถานะ.Esp = stackaddress
	self.cpuสถานะ.Ebp = stackaddress
	self.cpuสถานะ.Ss = 0

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

func (self *TTaskmanager) Schedule(cpuสถานะ *Tcpuสถานะ) *Tcpuสถานะ {

	console_2 := TConsole{}
	for i := 0; i < numbertasks; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tasks[i].cpuสถานะ)))

		console_2.MUnsignedinteger32printxy(x, 10, uint16(15+i))
	}
	if numbertasks <= 0 {
		return cpuสถานะ
	}

	if currenttask >= 0 {
		tasks[currenttask].cpuสถานะ = cpuสถานะ
	}

	currenttask++
	if currenttask >= numbertasks {
		currenttask %= numbertasks

	}

	return tasks[currenttask].cpuสถานะ
}
