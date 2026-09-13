package proces

import . "unsafe"
import . "util/lista"
import mem "pamięćmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcUżytkownikheapRozmiar = 1 * 1024 * 1024

type Proces struct {
	identyfikator		uint32
	syscallIdentyfikator	int
	IsUżytkownikSpacja	bool
	argumenty		*[]byte

	ThreadLista	LinkedLista
	Threads		*LinkedLista
	PlikNazwa	[]byte

	StronaKatalogwpis	uintptr
}

func (bieżący *Proces) Init(mem *mem.TPamięćmanager) {
	bieżący.ThreadLista = LinkedLista{}
	bieżący.Threads = &bieżący.ThreadLista
	bieżący.Threads.Init(mem)
}

type Proceshelper struct {
	procesy			LinkedLista
	mem			*mem.TPamięćmanager
	kernelStronaKatalogwpis	uintptr
}

func (bieżący *Proceshelper) Init(mem *mem.TPamięćmanager, kernelStronaKatalogwpis uintptr) {
	bieżący.mem = mem
	bieżący.procesy = LinkedLista{}
	bieżący.procesy.Init(bieżący.mem)
	bieżący.kernelStronaKatalogwpis = kernelStronaKatalogwpis
}

func (bieżący *Proceshelper) Create(wpispoint func(), threadhelper *TThreadhelper, StronaKatalogwpis uint32, iskernel bool) Proces {
	proces := (*Proces)(bieżący.mem.Przydziel_pamięć(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(bieżący.mem)
	proces.identyfikator = AllocateIdentyfikator()
	proces.StronaKatalogwpis = uintptr(StronaKatalogwpis)
	głównythread := threadhelper.CreateKursorzFunkcja(wpispoint, StronaKatalogwpis, iskernel)
	if głównythread != nil {
		głównythread.Identyfikator = proces.identyfikator
		głównythread.RodzicIdentyfikator = 0
		proces.Threads.Dodaj_na_końcu_listy(uintptr(Pointer(głównythread)))
	}

	bieżący.procesy.Dodaj_na_końcu_listy(uintptr(Pointer(proces)))

	return *proces
}

func (bieżący *Proceshelper) Spawn(wpispoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, StronaKatalogwpis uint32, iskernel bool) Proces {
	proces := bieżący.Create(wpispoint, threadhelper, StronaKatalogwpis, iskernel)
	if proces.Threads != nil && proces.Threads.Rozmiar_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Dodajthread(thread)
		}
	}
	return proces
}

func (bieżący *Proceshelper) kopiujStronaKatalog(źródłowpis uintptr, celwpis uintptr) {
	źródło_2 := Getunsignedinteger32TablicazKursor(źródłowpis, 1024, 1024)
	cel_2 := Getunsignedinteger32TablicazKursor(celwpis, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		cel_2[i] = źródło_2[i]
	}
}
func (bieżący *Proceshelper) Createzdata() Proces {
	proces := Proces{}
	return proces
}
