/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "یادداشتmanager"
import . "gdt"

var Tٹیسٹ uint8

func halt()

type Tcpuحالت struct {
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
	سیپییوحالت	*Tcpuحالت
}

func (self *TTask) Init(gdt *TShareddescriptorجدول, mem *mem.Tیادداشتmanager, entrypoint_2 func()) {

	self.سیپییوحالت = (*Tcpuحالت)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpuحالت{})))

	self.سیپییوحالت.Eax = 0
	self.سیپییوحالت.Ebx = 0
	self.سیپییوحالت.Ecx = 0
	self.سیپییوحالت.Edx = 0

	self.سیپییوحالت.Esi = 0
	self.سیپییوحالت.Edi = 0

	self.سیپییوحالت.Gs = 0
	self.سیپییوحالت.Fs = 0
	self.سیپییوحالت.Es = 0
	self.سیپییوحالت.Ds = 0

	self.سیپییوحالت.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.سیپییوحالت.Cs = Segkernelcode
	self.سیپییوحالت.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.سیپییوحالت)))

	self.سیپییوحالت.Esp = stackaddress
	self.سیپییوحالت.Ebp = stackaddress
	self.سیپییوحالت.Ss = 0

}

type TTaskmanager struct {
}

var tasks [256]TTask
var numbertasks int
var حالیہtask int

func (self *TTaskmanager) Init() {
	numbertasks = 0
	حالیہtask = -1
}

func (self *TTaskmanager) Aشاملکریںtask(task TTask) bool {
	if numbertasks >= 255 {
		return false
	}
	tasks[numbertasks] = task
	numbertasks++
	return true
}

func (self *TTaskmanager) Schedule(سیپییوحالت *Tcpuحالت) *Tcpuحالت {

	console_2 := TConsole{}
	for i := 0; i < numbertasks; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tasks[i].سیپییوحالت)))

		console_2.MUnsignedinteger32چھاپیںxy(x, 10, uint16(15+i))
	}
	if numbertasks <= 0 {
		return سیپییوحالت
	}

	if حالیہtask >= 0 {
		tasks[حالیہtask].سیپییوحالت = سیپییوحالت
	}

	حالیہtask++
	if حالیہtask >= numbertasks {
		حالیہtask %= numbertasks

	}

	return tasks[حالیہtask].سیپییوحالت
}
