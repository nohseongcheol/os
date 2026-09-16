/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proces

import . "unsafe"
import . "util/listă"
import mem "memoriemanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcUtilizatorheapMărime = 1 * 1024 * 1024

type Proces struct {
	id			uint32
	syscallid		int
	IsUtilizatorSpațiu	bool
	argumente		*[]byte

	ThreadListă	LinkedListă
	Threads		*LinkedListă
	FișierNume	[]byte

	PAGINĂDirectorînregistrare	uintptr
}

func (sine *Proces) Init(mem *mem.TMemoriemanager) {
	sine.ThreadListă = LinkedListă{}
	sine.Threads = &sine.ThreadListă
	sine.Threads.Init(mem)
}

type Proceshelper struct {
	procese					LinkedListă
	mem					*mem.TMemoriemanager
	kernelPAGINĂDirectorînregistrare	uintptr
}

func (sine *Proceshelper) Init(mem *mem.TMemoriemanager, kernelPAGINĂDirectorînregistrare uintptr) {
	sine.mem = mem
	sine.procese = LinkedListă{}
	sine.procese.Init(sine.mem)
	sine.kernelPAGINĂDirectorînregistrare = kernelPAGINĂDirectorînregistrare
}

func (sine *Proceshelper) Create(înregistrarepoint func(), threadhelper *TThreadhelper, PAGINĂDirectorînregistrare uint32, iskernel bool) Proces {
	proces := (*Proces)(sine.mem.Malloc(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(sine.mem)
	proces.id = Allocatepid()
	proces.PAGINĂDirectorînregistrare = uintptr(PAGINĂDirectorînregistrare)
	principalthread := threadhelper.CreateIndicatorfromFuncție(înregistrarepoint, PAGINĂDirectorînregistrare, iskernel)
	if principalthread != nil {
		principalthread.Pid = proces.id
		principalthread.Părintepid = 0
		proces.Threads.Append_to_list(uintptr(Pointer(principalthread)))
	}

	sine.procese.Append_to_list(uintptr(Pointer(proces)))

	return *proces
}

func (sine *Proceshelper) Spawn(înregistrarepoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, PAGINĂDirectorînregistrare uint32, iskernel bool) Proces {
	proces := sine.Create(înregistrarepoint, threadhelper, PAGINĂDirectorînregistrare, iskernel)
	if proces.Threads != nil && proces.Threads.Mărime_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Adaugăthread(thread)
		}
	}
	return proces
}

func (sine *Proceshelper) copiazăPAGINĂDirector(sursăînregistrare uintptr, destinațieînregistrare uintptr) {
	sursă_2 := Getunsignedinteger32VectorfromIndicator(sursăînregistrare, 1024, 1024)
	destinație_2 := Getunsignedinteger32VectorfromIndicator(destinațieînregistrare, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destinație_2[i] = sursă_2[i]
	}
}
func (sine *Proceshelper) Createfromdata() Proces {
	proces := Proces{}
	return proces
}
