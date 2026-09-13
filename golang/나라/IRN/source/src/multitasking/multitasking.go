package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "حافظهmanager"
import . "gdt"

var Test uint8

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
	stack	[4096]uint8
	cpuحالت	*Tcpuحالت
}

func (خود *TTask) Init(gdt *TShareddescriptorجدول, mem *mem.Tحافظهmanager, entrypoint_2 func()) {

	خود.cpuحالت = (*Tcpuحالت)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpuحالت{})))

	خود.cpuحالت.Eax = 0
	خود.cpuحالت.Ebx = 0
	خود.cpuحالت.Ecx = 0
	خود.cpuحالت.Edx = 0

	خود.cpuحالت.Esi = 0
	خود.cpuحالت.Edi = 0

	خود.cpuحالت.Gs = 0
	خود.cpuحالت.Fs = 0
	خود.cpuحالت.Es = 0
	خود.cpuحالت.Ds = 0

	خود.cpuحالت.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	خود.cpuحالت.Cs = Segkernelcode
	خود.cpuحالت.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(خود.cpuحالت)))

	خود.cpuحالت.Esp = stackaddress
	خود.cpuحالت.Ebp = stackaddress
	خود.cpuحالت.Ss = 0

}

type TTaskmanager struct {
}

var وظایف [256]TTask
var numberوظایف int
var currenttask int

func (خود *TTaskmanager) Init() {
	numberوظایف = 0
	currenttask = -1
}

func (خود *TTaskmanager) Aاضافهکردنtask(task TTask) bool {
	if numberوظایف >= 255 {
		return false
	}
	وظایف[numberوظایف] = task
	numberوظایف++
	return true
}

func (خود *TTaskmanager) Schedule(cpuحالت *Tcpuحالت) *Tcpuحالت {

	console_2 := TConsole{}
	for i := 0; i < numberوظایف; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(وظایف[i].cpuحالت)))

		console_2.MUnsignedinteger32چاپxy(x, 10, uint16(15+i))
	}
	if numberوظایف <= 0 {
		return cpuحالت
	}

	if currenttask >= 0 {
		وظایف[currenttask].cpuحالت = cpuحالت
	}

	currenttask++
	if currenttask >= numberوظایف {
		currenttask %= numberوظایف

	}

	return وظایف[currenttask].cpuحالت
}
