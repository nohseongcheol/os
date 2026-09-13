package opravilo

import . "unsafe"
import . "util/seznam"
import mem "pomnilnikmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcUporabnikheapVelikost = 1 * 1024 * 1024

type Opravilo struct {
	id			uint32
	syscallid		int
	IsUporabnikPresledek	bool
	argumenti		*[]byte

	ThreadSeznam	LinkedSeznam
	Threads		*LinkedSeznam
	DatotekaIme	[]byte

	StranMapavnos	uintptr
}

func (sam *Opravilo) Init(mem *mem.TPomnilnikmanager) {
	sam.ThreadSeznam = LinkedSeznam{}
	sam.Threads = &sam.ThreadSeznam
	sam.Threads.Init(mem)
}

type Opravilohelper struct {
	opravila		LinkedSeznam
	mem			*mem.TPomnilnikmanager
	kernelStranMapavnos	uintptr
}

func (sam *Opravilohelper) Init(mem *mem.TPomnilnikmanager, kernelStranMapavnos uintptr) {
	sam.mem = mem
	sam.opravila = LinkedSeznam{}
	sam.opravila.Init(sam.mem)
	sam.kernelStranMapavnos = kernelStranMapavnos
}

func (sam *Opravilohelper) Create(vnospoint func(), threadhelper *TThreadhelper, StranMapavnos uint32, iskernel bool) Opravilo {
	opravilo := (*Opravilo)(sam.mem.Malloc(uint32(Sizeof(Opravilo{}))))
	if opravilo == nil {
		return Opravilo{}
	}
	opravilo.Init(sam.mem)
	opravilo.id = Allocatepid()
	opravilo.StranMapavnos = uintptr(StranMapavnos)
	glavnithread := threadhelper.CreateKazalnikfromFunkcija(vnospoint, StranMapavnos, iskernel)
	if glavnithread != nil {
		glavnithread.Pid = opravilo.id
		glavnithread.Nadrejenipredmetpid = 0
		opravilo.Threads.Append_to_list(uintptr(Pointer(glavnithread)))
	}

	sam.opravila.Append_to_list(uintptr(Pointer(opravilo)))

	return *opravilo
}

func (sam *Opravilohelper) Spawn(vnospoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, StranMapavnos uint32, iskernel bool) Opravilo {
	opravilo := sam.Create(vnospoint, threadhelper, StranMapavnos, iskernel)
	if opravilo.Threads != nil && opravilo.Threads.Velikost_2 > 0 {
		thread := (*TThread)(opravilo.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Dodajthread(thread)
		}
	}
	return opravilo
}

func (sam *Opravilohelper) kopirajStranMapa(virvnos uintptr, ciljvnos uintptr) {
	vir_2 := Getunsignedinteger32PoljefromKazalnik(virvnos, 1024, 1024)
	cilj_2 := Getunsignedinteger32PoljefromKazalnik(ciljvnos, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		cilj_2[i] = vir_2[i]
	}
}
func (sam *Opravilohelper) Createfromdata() Opravilo {
	opravilo := Opravilo{}
	return opravilo
}
