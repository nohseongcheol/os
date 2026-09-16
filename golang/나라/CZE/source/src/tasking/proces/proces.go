/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proces

import . "unsafe"
import . "util/seznam"
import mem "paměťmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcUživatelheapVelikost = 1 * 1024 * 1024

type Proces struct {
	id			uint32
	syscallid		int
	IsUživatelMezera	bool
	argumenty		*[]byte

	ThreadSeznam	LinkedSeznam
	Threads		*LinkedSeznam
	SouborNázev	[]byte

	StránkaadresářZáznam	uintptr
}

func (self *Proces) Init(mem *mem.TPaměťmanager) {
	self.ThreadSeznam = LinkedSeznam{}
	self.Threads = &self.ThreadSeznam
	self.Threads.Init(mem)
}

type Proceshelper struct {
	procesy				LinkedSeznam
	mem				*mem.TPaměťmanager
	kernelStránkaadresářZáznam	uintptr
}

func (self *Proceshelper) Init(mem *mem.TPaměťmanager, kernelStránkaadresářZáznam uintptr) {
	self.mem = mem
	self.procesy = LinkedSeznam{}
	self.procesy.Init(self.mem)
	self.kernelStránkaadresářZáznam = kernelStránkaadresářZáznam
}

func (self *Proceshelper) Create(záznampoint func(), threadhelper *TThreadhelper, StránkaadresářZáznam uint32, iskernel bool) Proces {
	proces := (*Proces)(self.mem.Přidělit_paměť(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(self.mem)
	proces.id = Allocatepid()
	proces.StránkaadresářZáznam = uintptr(StránkaadresářZáznam)
	hlavníthread := threadhelper.CreateKurzorzFunkce(záznampoint, StránkaadresářZáznam, iskernel)
	if hlavníthread != nil {
		hlavníthread.Pid = proces.id
		hlavníthread.Rodičpid = 0
		proces.Threads.Přidat_na_konec_seznamu(uintptr(Pointer(hlavníthread)))
	}

	self.procesy.Přidat_na_konec_seznamu(uintptr(Pointer(proces)))

	return *proces
}

func (self *Proceshelper) Spawn(záznampoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, StránkaadresářZáznam uint32, iskernel bool) Proces {
	proces := self.Create(záznampoint, threadhelper, StránkaadresářZáznam, iskernel)
	if proces.Threads != nil && proces.Threads.Velikost_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Přidatthread(thread)
		}
	}
	return proces
}

func (self *Proceshelper) kopírovatStránkaadresář(zdrojZáznam uintptr, cílZáznam uintptr) {
	zdroj_2 := Getunsignedinteger32PolezKurzor(zdrojZáznam, 1024, 1024)
	cíl_2 := Getunsignedinteger32PolezKurzor(cílZáznam, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		cíl_2[i] = zdroj_2[i]
	}
}
func (self *Proceshelper) Createzdata() Proces {
	proces := Proces{}
	return proces
}
