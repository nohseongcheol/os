package process

import . "unsafe"
import . "util/listi"
import mem "minnimanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcNotandiheapStærð = 1 * 1024 * 1024

type Process struct {
	auðkenni	uint32
	syscallAuðkenni	int
	IsNotandiBilslá	bool
	viðföng		*[]byte

	ThreadListi	LinkedListi
	Threads		*LinkedListi
	SkráHeiti	[]byte

	Síðamappaentry	uintptr
}

func (sjálft *Process) Init(mem *mem.TMinnimanager) {
	sjálft.ThreadListi = LinkedListi{}
	sjálft.Threads = &sjálft.ThreadListi
	sjálft.Threads.Init(mem)
}

type Processhelper struct {
	processes		LinkedListi
	mem			*mem.TMinnimanager
	kernelsíðamappaentry	uintptr
}

func (sjálft *Processhelper) Init(mem *mem.TMinnimanager, kernelsíðamappaentry uintptr) {
	sjálft.mem = mem
	sjálft.processes = LinkedListi{}
	sjálft.processes.Init(sjálft.mem)
	sjálft.kernelsíðamappaentry = kernelsíðamappaentry
}

func (sjálft *Processhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Síðamappaentry uint32, iskernel bool) Process {
	process := (*Process)(sjálft.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(sjálft.mem)
	process.auðkenni = Allocatepid()
	process.Síðamappaentry = uintptr(Síðamappaentry)
	aðalthread := threadhelper.CreateBendillfromAðgerð(entrypoint, Síðamappaentry, iskernel)
	if aðalthread != nil {
		aðalthread.Pid = process.auðkenni
		aðalthread.Foreldripid = 0
		process.Threads.Append_to_list(uintptr(Pointer(aðalthread)))
	}

	sjálft.processes.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (sjálft *Processhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Síðamappaentry uint32, iskernel bool) Process {
	process := sjálft.Create(entrypoint, threadhelper, Síðamappaentry, iskernel)
	if process.Threads != nil && process.Threads.Stærð_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Bætaviðthread(thread)
		}
	}
	return process
}

func (sjálft *Processhelper) afritasíðamappa(upprunientry uintptr, áfangastaðurentry uintptr) {
	uppruni_2 := Getunsignedinteger32FylkifromBendill(upprunientry, 1024, 1024)
	áfangastaður_2 := Getunsignedinteger32FylkifromBendill(áfangastaðurentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		áfangastaður_2[i] = uppruni_2[i]
	}
}
func (sjálft *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
