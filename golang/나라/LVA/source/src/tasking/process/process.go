package process

import . "unsafe"
import . "util/saraksts"
import mem "atmiņamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcLietotājsheapIzmērs = 1 * 1024 * 1024

type Process struct {
	id			uint32
	syscallid		int
	IsLietotājsspace	bool
	parametri		*[]byte

	ThreadSaraksts	LinkedSaraksts
	Threads		*LinkedSaraksts
	FailsNosaukums	[]byte

	LapaMapeieraksts	uintptr
}

func (pats *Process) Init(mem *mem.TAtmiņamanager) {
	pats.ThreadSaraksts = LinkedSaraksts{}
	pats.Threads = &pats.ThreadSaraksts
	pats.Threads.Init(mem)
}

type Processhelper struct {
	procesi			LinkedSaraksts
	mem			*mem.TAtmiņamanager
	kernelLapaMapeieraksts	uintptr
}

func (pats *Processhelper) Init(mem *mem.TAtmiņamanager, kernelLapaMapeieraksts uintptr) {
	pats.mem = mem
	pats.procesi = LinkedSaraksts{}
	pats.procesi.Init(pats.mem)
	pats.kernelLapaMapeieraksts = kernelLapaMapeieraksts
}

func (pats *Processhelper) Create(ierakstspoint func(), threadhelper *TThreadhelper, LapaMapeieraksts uint32, iskernel bool) Process {
	process := (*Process)(pats.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(pats.mem)
	process.id = Allocatepid()
	process.LapaMapeieraksts = uintptr(LapaMapeieraksts)
	galvenaisthread := threadhelper.CreateKursorsfromFunkcija(ierakstspoint, LapaMapeieraksts, iskernel)
	if galvenaisthread != nil {
		galvenaisthread.Pid = process.id
		galvenaisthread.Vecākspid = 0
		process.Threads.Append_to_list(uintptr(Pointer(galvenaisthread)))
	}

	pats.procesi.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (pats *Processhelper) Spawn(ierakstspoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, LapaMapeieraksts uint32, iskernel bool) Process {
	process := pats.Create(ierakstspoint, threadhelper, LapaMapeieraksts, iskernel)
	if process.Threads != nil && process.Threads.Izmērs_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Pievienotthread(thread)
		}
	}
	return process
}

func (pats *Processhelper) kopētLapaMape(avotsieraksts uintptr, mērķisieraksts uintptr) {
	avots_2 := Getunsignedinteger32MasīvsfromKursors(avotsieraksts, 1024, 1024)
	mērķis_2 := Getunsignedinteger32MasīvsfromKursors(mērķisieraksts, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		mērķis_2[i] = avots_2[i]
	}
}
func (pats *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
