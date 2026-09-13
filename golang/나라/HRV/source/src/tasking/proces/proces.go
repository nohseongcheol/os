package proces

import . "unsafe"
import . "util/popis"
import mem "memorijamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcKorisnikheapVeličina = 1 * 1024 * 1024

type Proces struct {
	identifikacija		uint32
	syscallIdentifikacija	int
	IsKorisnikRazmaknica	bool
	argumenti		*[]byte

	ThreadPopis	LinkedPopis
	Threads		*LinkedPopis
	DatotekaIme	[]byte

	StranicaDirektorijentry	uintptr
}

func (sam *Proces) Init(mem *mem.TMemorijamanager) {
	sam.ThreadPopis = LinkedPopis{}
	sam.Threads = &sam.ThreadPopis
	sam.Threads.Init(mem)
}

type Proceshelper struct {
	procesi				LinkedPopis
	mem				*mem.TMemorijamanager
	kernelStranicaDirektorijentry	uintptr
}

func (sam *Proceshelper) Init(mem *mem.TMemorijamanager, kernelStranicaDirektorijentry uintptr) {
	sam.mem = mem
	sam.procesi = LinkedPopis{}
	sam.procesi.Init(sam.mem)
	sam.kernelStranicaDirektorijentry = kernelStranicaDirektorijentry
}

func (sam *Proceshelper) Create(entrypoint func(), threadhelper *TThreadhelper, StranicaDirektorijentry uint32, iskernel bool) Proces {
	proces := (*Proces)(sam.mem.Malloc(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(sam.mem)
	proces.identifikacija = Allocatepid()
	proces.StranicaDirektorijentry = uintptr(StranicaDirektorijentry)
	glavnithread := threadhelper.CreatePokazivačfromFunkcija(entrypoint, StranicaDirektorijentry, iskernel)
	if glavnithread != nil {
		glavnithread.Pid = proces.identifikacija
		glavnithread.Roditeljpid = 0
		proces.Threads.Append_to_list(uintptr(Pointer(glavnithread)))
	}

	sam.procesi.Append_to_list(uintptr(Pointer(proces)))

	return *proces
}

func (sam *Proceshelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, StranicaDirektorijentry uint32, iskernel bool) Proces {
	proces := sam.Create(entrypoint, threadhelper, StranicaDirektorijentry, iskernel)
	if proces.Threads != nil && proces.Threads.Veličina_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Dodajthread(thread)
		}
	}
	return proces
}

func (sam *Proceshelper) kopirajStranicaDirektorij(izvorentry uintptr, odredišteentry uintptr) {
	izvor_2 := Getunsignedinteger32NizfromPokazivač(izvorentry, 1024, 1024)
	odredište_2 := Getunsignedinteger32NizfromPokazivač(odredišteentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		odredište_2[i] = izvor_2[i]
	}
}
func (sam *Proceshelper) Createfromdata() Proces {
	proces := Proces{}
	return proces
}
