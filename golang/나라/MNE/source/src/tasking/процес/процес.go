package процес

import . "unsafe"
import . "util/spisak"
import mem "memorijamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcKorisnikheapВеличина = 1 * 1024 * 1024

type Процес struct {
	iB			uint32
	syscallIB		int
	IsKorisnikrazmak	bool
	argumenti		*[]byte

	ThreadSpisak	LinkedSpisak
	Threads		*LinkedSpisak
	ДатотекаНазив	[]byte

	ListDirektorijumунос	uintptr
}

func (isti *Процес) Init(mem *mem.TMemorijamanager) {
	isti.ThreadSpisak = LinkedSpisak{}
	isti.Threads = &isti.ThreadSpisak
	isti.Threads.Init(mem)
}

type Процесhelper struct {
	procesi				LinkedSpisak
	mem				*mem.TMemorijamanager
	kernellistDirektorijumунос	uintptr
}

func (isti *Процесhelper) Init(mem *mem.TMemorijamanager, kernellistDirektorijumунос uintptr) {
	isti.mem = mem
	isti.procesi = LinkedSpisak{}
	isti.procesi.Init(isti.mem)
	isti.kernellistDirektorijumунос = kernellistDirektorijumунос
}

func (isti *Процесhelper) Create(уносpoint func(), threadhelper *TThreadhelper, ListDirektorijumунос uint32, iskernel bool) Процес {
	процес := (*Процес)(isti.mem.Malloc(uint32(Sizeof(Процес{}))))
	if процес == nil {
		return Процес{}
	}
	процес.Init(isti.mem)
	процес.iB = AllocateПИД()
	процес.ListDirektorijumунос = uintptr(ListDirektorijumунос)
	glavnithread := threadhelper.CreatePokazivačsaфункција(уносpoint, ListDirektorijumунос, iskernel)
	if glavnithread != nil {
		glavnithread.ПИД = процес.iB
		glavnithread.NadređeniПИД = 0
		процес.Threads.Append_to_list(uintptr(Pointer(glavnithread)))
	}

	isti.procesi.Append_to_list(uintptr(Pointer(процес)))

	return *процес
}

func (isti *Процесhelper) Spawn(уносpoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, ListDirektorijumунос uint32, iskernel bool) Процес {
	процес := isti.Create(уносpoint, threadhelper, ListDirektorijumунос, iskernel)
	if процес.Threads != nil && процес.Threads.Величина_2 > 0 {
		thread := (*TThread)(процес.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Додајthread(thread)
		}
	}
	return процес
}

func (isti *Процесhelper) умножиlistDirektorijum(izvorунос uintptr, odredišteунос uintptr) {
	izvor_2 := Getunsignedinteger32НизsaPokazivač(izvorунос, 1024, 1024)
	odredište_2 := Getunsignedinteger32НизsaPokazivač(odredišteунос, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		odredište_2[i] = izvor_2[i]
	}
}
func (isti *Процесhelper) Createsadata() Процес {
	процес := Процес{}
	return процес
}
