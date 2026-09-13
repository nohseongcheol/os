package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "меморијаmanager"
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

func (само *TTask) Init(gdt *TShareddescriptorТабела, mem *mem.TМеморијаmanager, entrypoint_2 func()) {

	само.cpustate = (*Tcpustate)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpustate{})))

	само.cpustate.Eax = 0
	само.cpustate.Ebx = 0
	само.cpustate.Ecx = 0
	само.cpustate.Edx = 0

	само.cpustate.Esi = 0
	само.cpustate.Edi = 0

	само.cpustate.Gs = 0
	само.cpustate.Fs = 0
	само.cpustate.Es = 0
	само.cpustate.Ds = 0

	само.cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	само.cpustate.Cs = Segkernelcode
	само.cpustate.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(само.cpustate)))

	само.cpustate.Esp = stackaddress
	само.cpustate.Ebp = stackaddress
	само.cpustate.Ss = 0

}

type TTaskmanager struct {
}

var задачи [256]TTask
var numberЗадачи int
var currenttask int

func (само *TTaskmanager) Init() {
	numberЗадачи = 0
	currenttask = -1
}

func (само *TTaskmanager) Додајtask(task TTask) bool {
	if numberЗадачи >= 255 {
		return false
	}
	задачи[numberЗадачи] = task
	numberЗадачи++
	return true
}

func (само *TTaskmanager) Schedule(cpustate *Tcpustate) *Tcpustate {

	console_2 := TConsole{}
	for i := 0; i < numberЗадачи; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(задачи[i].cpustate)))

		console_2.MUnsignedinteger32Печатиxy(x, 10, uint16(15+i))
	}
	if numberЗадачи <= 0 {
		return cpustate
	}

	if currenttask >= 0 {
		задачи[currenttask].cpustate = cpustate
	}

	currenttask++
	if currenttask >= numberЗадачи {
		currenttask %= numberЗадачи

	}

	return задачи[currenttask].cpustate
}
