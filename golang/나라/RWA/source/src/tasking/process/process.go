package process

import . "unsafe"
import . "util/list"
import mem "ububikomanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcUkoreshaheapIngano = 1 * 1024 * 1024

type Process struct {
	id		uint32
	syscallid	int
	IsUkoreshaspace	bool
	arguments	*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	IdosiyeIzina	[]byte

	IpajiUbubikoentry	uintptr
}

func (self *Process) Init(mem *mem.TUbubikomanager) {
	self.Threadlist = Linkedlist{}
	self.Threads = &self.Threadlist
	self.Threads.Init(mem)
}

type Processhelper struct {
	processes		Linkedlist
	mem			*mem.TUbubikomanager
	kernelIpajiUbubikoentry	uintptr
}

func (self *Processhelper) Init(mem *mem.TUbubikomanager, kernelIpajiUbubikoentry uintptr) {
	self.mem = mem
	self.processes = Linkedlist{}
	self.processes.Init(self.mem)
	self.kernelIpajiUbubikoentry = kernelIpajiUbubikoentry
}

func (self *Processhelper) Create(entrypoint func(), threadhelper *TThreadhelper, IpajiUbubikoentry uint32, iskernel bool) Process {
	process := (*Process)(self.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(self.mem)
	process.id = Allocatepid()
	process.IpajiUbubikoentry = uintptr(IpajiUbubikoentry)
	nyamukuruthread := threadhelper.Createpointerfromfunction(entrypoint, IpajiUbubikoentry, iskernel)
	if nyamukuruthread != nil {
		nyamukuruthread.Pid = process.id
		nyamukuruthread.Parentpid = 0
		process.Threads.Append_to_list(uintptr(Pointer(nyamukuruthread)))
	}

	self.processes.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (self *Processhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, IpajiUbubikoentry uint32, iskernel bool) Process {
	process := self.Create(entrypoint, threadhelper, IpajiUbubikoentry, iskernel)
	if process.Threads != nil && process.Threads.Ingano_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Kongerathread(thread)
		}
	}
	return process
}

func (self *Processhelper) gukopororaIpajiUbubiko(inkomokoentry uintptr, destinationentry uintptr) {
	inkomoko_2 := Getunsignedinteger32Imbonerahamwefrompointer(inkomokoentry, 1024, 1024)
	destination_2 := Getunsignedinteger32Imbonerahamwefrompointer(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = inkomoko_2[i]
	}
}
func (self *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
