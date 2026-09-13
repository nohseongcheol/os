package process

import . "unsafe"
import . "util/list"
import mem "حافظهmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const Procکاربرheapاندازه = 1 * 1024 * 1024

type Process struct {
	شناسه		uint32
	syscallشناسه	int
	Isکاربرفاصله	bool
	نشانوندها	*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	Fپروندهنام	[]byte

	Pصفحهشاخهentry	uintptr
}

func (خود *Process) Init(mem *mem.Tحافظهmanager) {
	خود.Threadlist = Linkedlist{}
	خود.Threads = &خود.Threadlist
	خود.Threads.Init(mem)
}

type Processhelper struct {
	processes		Linkedlist
	mem			*mem.Tحافظهmanager
	kernelصفحهشاخهentry	uintptr
}

func (خود *Processhelper) Init(mem *mem.Tحافظهmanager, kernelصفحهشاخهentry uintptr) {
	خود.mem = mem
	خود.processes = Linkedlist{}
	خود.processes.Init(خود.mem)
	خود.kernelصفحهشاخهentry = kernelصفحهشاخهentry
}

func (خود *Processhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Pصفحهشاخهentry uint32, iskernel bool) Process {
	process := (*Process)(خود.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(خود.mem)
	process.شناسه = Allocateمشخصهبرنامه()
	process.Pصفحهشاخهentry = uintptr(Pصفحهشاخهentry)
	اصلیthread := threadhelper.Createpointerfromتابع(entrypoint, Pصفحهشاخهentry, iskernel)
	if اصلیthread != nil {
		اصلیthread.Pمشخصهبرنامه = process.شناسه
		اصلیthread.Pوالدمشخصهبرنامه = 0
		process.Threads.Append_to_list(uintptr(Pointer(اصلیthread)))
	}

	خود.processes.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (خود *Processhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Pصفحهشاخهentry uint32, iskernel bool) Process {
	process := خود.Create(entrypoint, threadhelper, Pصفحهشاخهentry, iskernel)
	if process.Threads != nil && process.Threads.Sاندازه_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Aاضافهکردنthread(thread)
		}
	}
	return process
}

func (خود *Processhelper) کپیصفحهشاخه(مبدأentry uintptr, مقصدentry uintptr) {
	مبدأ_2 := Getunsignedinteger32آرایهfrompointer(مبدأentry, 1024, 1024)
	مقصد_2 := Getunsignedinteger32آرایهfrompointer(مقصدentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		مقصد_2[i] = مبدأ_2[i]
	}
}
func (خود *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
