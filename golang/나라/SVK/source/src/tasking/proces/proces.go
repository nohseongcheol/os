/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proces

import . "unsafe"
import . "util/zoznam"
import mem "pamäťmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcPoužívateľheapVeľkosť = 1 * 1024 * 1024

type Proces struct {
	identifikátor		uint32
	syscallIdentifikátor	int
	IsPoužívateľMedzera	bool
	argumenty		*[]byte

	ThreadZoznam	LinkedZoznam
	Threads		*LinkedZoznam
	SúborNázov	[]byte

	STRANAAdresárpoložka	uintptr
}

func (vlastný *Proces) Init(mem *mem.TPamäťmanager) {
	vlastný.ThreadZoznam = LinkedZoznam{}
	vlastný.Threads = &vlastný.ThreadZoznam
	vlastný.Threads.Init(mem)
}

type Proceshelper struct {
	procesy				LinkedZoznam
	mem				*mem.TPamäťmanager
	kernelSTRANAAdresárpoložka	uintptr
}

func (vlastný *Proceshelper) Init(mem *mem.TPamäťmanager, kernelSTRANAAdresárpoložka uintptr) {
	vlastný.mem = mem
	vlastný.procesy = LinkedZoznam{}
	vlastný.procesy.Init(vlastný.mem)
	vlastný.kernelSTRANAAdresárpoložka = kernelSTRANAAdresárpoložka
}

func (vlastný *Proceshelper) Create(položkapoint func(), threadhelper *TThreadhelper, STRANAAdresárpoložka uint32, iskernel bool) Proces {
	proces := (*Proces)(vlastný.mem.Malloc(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(vlastný.mem)
	proces.identifikátor = Allocatepid()
	proces.STRANAAdresárpoložka = uintptr(STRANAAdresárpoložka)
	hlavnýthread := threadhelper.CreateKurzorzFunkcia(položkapoint, STRANAAdresárpoložka, iskernel)
	if hlavnýthread != nil {
		hlavnýthread.Pid = proces.identifikátor
		hlavnýthread.Rodičpid = 0
		proces.Threads.Append_to_list(uintptr(Pointer(hlavnýthread)))
	}

	vlastný.procesy.Append_to_list(uintptr(Pointer(proces)))

	return *proces
}

func (vlastný *Proceshelper) Spawn(položkapoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, STRANAAdresárpoložka uint32, iskernel bool) Proces {
	proces := vlastný.Create(položkapoint, threadhelper, STRANAAdresárpoložka, iskernel)
	if proces.Threads != nil && proces.Threads.Veľkosť_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Pridaťthread(thread)
		}
	}
	return proces
}

func (vlastný *Proceshelper) kopírovaťSTRANAAdresár(zdrojpoložka uintptr, cieľpoložka uintptr) {
	zdroj_2 := Getunsignedinteger32PolezKurzor(zdrojpoložka, 1024, 1024)
	cieľ_2 := Getunsignedinteger32PolezKurzor(cieľpoložka, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		cieľ_2[i] = zdroj_2[i]
	}
}
func (vlastný *Proceshelper) Createzdata() Proces {
	proces := Proces{}
	return proces
}
