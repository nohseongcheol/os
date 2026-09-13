package process

import . "unsafe"
import . "util/list"
import mem "memorymanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcBrúkariheapStødd = 1 * 1024 * 1024

type Process struct {
	id		uint32
	syscallid	int
	IsBrúkarispace	bool
	arguments	*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	FílaNavn	[]byte

	PageFíluskráentry	uintptr
}

func (self *Process) Init(mem *mem.TMemorymanager) {
	self.Threadlist = Linkedlist{}
	self.Threads = &self.Threadlist
	self.Threads.Init(mem)
}

type Processhelper struct {
	processes		Linkedlist
	mem			*mem.TMemorymanager
	kernelpageFíluskráentry	uintptr
}

func (self *Processhelper) Init(mem *mem.TMemorymanager, kernelpageFíluskráentry uintptr) {
	self.mem = mem
	self.processes = Linkedlist{}
	self.processes.Init(self.mem)
	self.kernelpageFíluskráentry = kernelpageFíluskráentry
}

func (self *Processhelper) Create(entrypoint func(), threadhelper *TThreadhelper, PageFíluskráentry uint32, iskernel bool) Process {
	process := (*Process)(self.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(self.mem)
	process.id = Allocatepid()
	process.PageFíluskráentry = uintptr(PageFíluskráentry)
	høvuðthread := threadhelper.Createpointerfromfunction(entrypoint, PageFíluskráentry, iskernel)
	if høvuðthread != nil {
		høvuðthread.Pid = process.id
		høvuðthread.Parentpid = 0
		process.Threads.Append_to_list(uintptr(Pointer(høvuðthread)))
	}

	self.processes.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (self *Processhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, PageFíluskráentry uint32, iskernel bool) Process {
	process := self.Create(entrypoint, threadhelper, PageFíluskráentry, iskernel)
	if process.Threads != nil && process.Threads.Stødd_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Addthread(thread)
		}
	}
	return process
}

func (self *Processhelper) copypageFíluskrá(sourceentry uintptr, destinationentry uintptr) {
	source_2 := Getunsignedinteger32arrayfrompointer(sourceentry, 1024, 1024)
	destination_2 := Getunsignedinteger32arrayfrompointer(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = source_2[i]
	}
}
func (self *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
