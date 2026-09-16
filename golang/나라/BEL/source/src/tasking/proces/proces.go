/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proces

import . "unsafe"
import . "util/lijst"
import mem "geheugenmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcGebruikerheapGrootte = 1 * 1024 * 1024

type Proces struct {
	id			uint32
	syscallid		int
	IsGebruikerSpatie	bool
	argumenten		*[]byte

	ThreadLijst	LinkedLijst
	Threads		*LinkedLijst
	BestandNaam	[]byte

	PaginaMapItem	uintptr
}

func (zelf *Proces) Init(mem *mem.TGeheugenmanager) {
	zelf.ThreadLijst = LinkedLijst{}
	zelf.Threads = &zelf.ThreadLijst
	zelf.Threads.Init(mem)
}

type Proceshelper struct {
	processen		LinkedLijst
	mem			*mem.TGeheugenmanager
	kernelPaginaMapItem	uintptr
}

func (zelf *Proceshelper) Init(mem *mem.TGeheugenmanager, kernelPaginaMapItem uintptr) {
	zelf.mem = mem
	zelf.processen = LinkedLijst{}
	zelf.processen.Init(zelf.mem)
	zelf.kernelPaginaMapItem = kernelPaginaMapItem
}

func (zelf *Proceshelper) Create(itempoint func(), threadhelper *TThreadhelper, PaginaMapItem uint32, iskernel bool) Proces {
	proces := (*Proces)(zelf.mem.Geheugen_toewijzen(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(zelf.mem)
	proces.id = Allocatepid()
	proces.PaginaMapItem = uintptr(PaginaMapItem)
	hoofdthread := threadhelper.CreateMuisaanwijzervanFunctie(itempoint, PaginaMapItem, iskernel)
	if hoofdthread != nil {
		hoofdthread.Pid = proces.id
		hoofdthread.Ouderpid = 0
		proces.Threads.Achteraan_toevoegen(uintptr(Pointer(hoofdthread)))
	}

	zelf.processen.Achteraan_toevoegen(uintptr(Pointer(proces)))

	return *proces
}

func (zelf *Proceshelper) Spawn(itempoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, PaginaMapItem uint32, iskernel bool) Proces {
	proces := zelf.Create(itempoint, threadhelper, PaginaMapItem, iskernel)
	if proces.Threads != nil && proces.Threads.Grootte_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Toevoegenthread(thread)
		}
	}
	return proces
}

func (zelf *Proceshelper) kopiërenPaginaMap(bronItem uintptr, bestemmingItem uintptr) {
	bron_2 := Getunsignedinteger32ReeksvanMuisaanwijzer(bronItem, 1024, 1024)
	bestemming_2 := Getunsignedinteger32ReeksvanMuisaanwijzer(bestemmingItem, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		bestemming_2[i] = bron_2[i]
	}
}
func (zelf *Proceshelper) Createvandata() Proces {
	proces := Proces{}
	return proces
}
