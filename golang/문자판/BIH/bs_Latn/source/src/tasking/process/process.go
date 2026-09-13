package process

import . "unsafe"
import . "util/list"
import mem "memorijamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcKorisnikheapVeličina = 1 * 1024 * 1024

type Process struct {
	id		uint32
	syscallid	int
	IsKorisnikspace	bool
	argumenti	*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	DatotekaNaziv	[]byte

	StranicaDirektorijunos	uintptr
}

func (self *Process) Init(mem *mem.TMemorijamanager) {
	self.Threadlist = Linkedlist{}
	self.Threads = &self.Threadlist
	self.Threads.Init(mem)
}

type Processhelper struct {
	processes			Linkedlist
	mem				*mem.TMemorijamanager
	kernelStranicaDirektorijunos	uintptr
}

func (self *Processhelper) Init(mem *mem.TMemorijamanager, kernelStranicaDirektorijunos uintptr) {
	self.mem = mem
	self.processes = Linkedlist{}
	self.processes.Init(self.mem)
	self.kernelStranicaDirektorijunos = kernelStranicaDirektorijunos
}

func (self *Processhelper) Create(unospoint func(), threadhelper *TThreadhelper, StranicaDirektorijunos uint32, iskernel bool) Process {
	process := (*Process)(self.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(self.mem)
	process.id = Allocatepid()
	process.StranicaDirektorijunos = uintptr(StranicaDirektorijunos)
	glavnithread := threadhelper.CreatepointerfromFunkcija(unospoint, StranicaDirektorijunos, iskernel)
	if glavnithread != nil {
		glavnithread.Pid = process.id
		glavnithread.Parentpid = 0
		process.Threads.Append_to_list(uintptr(Pointer(glavnithread)))
	}

	self.processes.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (self *Processhelper) Spawn(unospoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, StranicaDirektorijunos uint32, iskernel bool) Process {
	process := self.Create(unospoint, threadhelper, StranicaDirektorijunos, iskernel)
	if process.Threads != nil && process.Threads.Veličina_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Dodajthread(thread)
		}
	}
	return process
}

func (self *Processhelper) kopirajStranicaDirektorij(izvorunos uintptr, odredišteunos uintptr) {
	izvor_2 := Getunsignedinteger32arrayfrompointer(izvorunos, 1024, 1024)
	odredište_2 := Getunsignedinteger32arrayfrompointer(odredišteunos, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		odredište_2[i] = izvor_2[i]
	}
}
func (self *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
