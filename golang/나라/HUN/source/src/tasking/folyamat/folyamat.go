package folyamat

import . "unsafe"
import . "util/lista"
import mem "memóriamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcFelhasználóheapMéret = 1 * 1024 * 1024

type Folyamat struct {
	azonosító		uint32
	syscallAzonosító	int
	IsFelhasználóSzóköz	bool
	argumentumok		*[]byte

	ThreadLista	LinkedLista
	Threads		*LinkedLista
	FájlNév		[]byte

	OldalKönyvtárbejegyzés	uintptr
}

func (self *Folyamat) Init(mem *mem.TMemóriamanager) {
	self.ThreadLista = LinkedLista{}
	self.Threads = &self.ThreadLista
	self.Threads.Init(mem)
}

type Folyamathelper struct {
	folyamatok			LinkedLista
	mem				*mem.TMemóriamanager
	kernelOldalKönyvtárbejegyzés	uintptr
}

func (self *Folyamathelper) Init(mem *mem.TMemóriamanager, kernelOldalKönyvtárbejegyzés uintptr) {
	self.mem = mem
	self.folyamatok = LinkedLista{}
	self.folyamatok.Init(self.mem)
	self.kernelOldalKönyvtárbejegyzés = kernelOldalKönyvtárbejegyzés
}

func (self *Folyamathelper) Create(bejegyzéspoint func(), threadhelper *TThreadhelper, OldalKönyvtárbejegyzés uint32, iskernel bool) Folyamat {
	folyamat := (*Folyamat)(self.mem.Malloc(uint32(Sizeof(Folyamat{}))))
	if folyamat == nil {
		return Folyamat{}
	}
	folyamat.Init(self.mem)
	folyamat.azonosító = Allocatepid()
	folyamat.OldalKönyvtárbejegyzés = uintptr(OldalKönyvtárbejegyzés)
	főthread := threadhelper.CreateMutatófromFüggvény(bejegyzéspoint, OldalKönyvtárbejegyzés, iskernel)
	if főthread != nil {
		főthread.Pid = folyamat.azonosító
		főthread.Parentpid = 0
		folyamat.Threads.Append_to_list(uintptr(Pointer(főthread)))
	}

	self.folyamatok.Append_to_list(uintptr(Pointer(folyamat)))

	return *folyamat
}

func (self *Folyamathelper) Spawn(bejegyzéspoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, OldalKönyvtárbejegyzés uint32, iskernel bool) Folyamat {
	folyamat := self.Create(bejegyzéspoint, threadhelper, OldalKönyvtárbejegyzés, iskernel)
	if folyamat.Threads != nil && folyamat.Threads.Méret_2 > 0 {
		thread := (*TThread)(folyamat.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Hozzáadásthread(thread)
		}
	}
	return folyamat
}

func (self *Folyamathelper) másolásOldalKönyvtár(forrásbejegyzés uintptr, célbejegyzés uintptr) {
	forrás_2 := Getunsignedinteger32TömbfromMutató(forrásbejegyzés, 1024, 1024)
	cél_2 := Getunsignedinteger32TömbfromMutató(célbejegyzés, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		cél_2[i] = forrás_2[i]
	}
}
func (self *Folyamathelper) Createfromdata() Folyamat {
	folyamat := Folyamat{}
	return folyamat
}
