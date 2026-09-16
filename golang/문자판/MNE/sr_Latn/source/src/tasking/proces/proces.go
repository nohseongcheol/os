/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proces

import . "unsafe"
import . "util/spisak"
import mem "memorijamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcKorisnikheapVeličina = 1 * 1024 * 1024

type Proces struct {
	iB			uint32
	syscallIB		int
	IsKorisnikrazmak	bool
	argumenti		*[]byte

	ThreadSpisak	LinkedSpisak
	Threads		*LinkedSpisak
	DatotekaNaziv	[]byte

	STRANADirektorijumunos	uintptr
}

func (isti *Proces) Init(mem *mem.TMemorijamanager) {
	isti.ThreadSpisak = LinkedSpisak{}
	isti.Threads = &isti.ThreadSpisak
	isti.Threads.Init(mem)
}

type Proceshelper struct {
	procesi				LinkedSpisak
	mem				*mem.TMemorijamanager
	kernelSTRANADirektorijumunos	uintptr
}

func (isti *Proceshelper) Init(mem *mem.TMemorijamanager, kernelSTRANADirektorijumunos uintptr) {
	isti.mem = mem
	isti.procesi = LinkedSpisak{}
	isti.procesi.Init(isti.mem)
	isti.kernelSTRANADirektorijumunos = kernelSTRANADirektorijumunos
}

func (isti *Proceshelper) Create(unospoint func(), threadhelper *TThreadhelper, STRANADirektorijumunos uint32, iskernel bool) Proces {
	proces := (*Proces)(isti.mem.Malloc(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(isti.mem)
	proces.iB = AllocatePID()
	proces.STRANADirektorijumunos = uintptr(STRANADirektorijumunos)
	glavnithread := threadhelper.CreatePokazivačsafunkcija(unospoint, STRANADirektorijumunos, iskernel)
	if glavnithread != nil {
		glavnithread.PID = proces.iB
		glavnithread.NadređeniPID = 0
		proces.Threads.Append_to_list(uintptr(Pointer(glavnithread)))
	}

	isti.procesi.Append_to_list(uintptr(Pointer(proces)))

	return *proces
}

func (isti *Proceshelper) Spawn(unospoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, STRANADirektorijumunos uint32, iskernel bool) Proces {
	proces := isti.Create(unospoint, threadhelper, STRANADirektorijumunos, iskernel)
	if proces.Threads != nil && proces.Threads.Veličina_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Dodajthread(thread)
		}
	}
	return proces
}

func (isti *Proceshelper) umnožiSTRANADirektorijum(izvorunos uintptr, odredišteunos uintptr) {
	izvor_2 := Getunsignedinteger32NizsaPokazivač(izvorunos, 1024, 1024)
	odredište_2 := Getunsignedinteger32NizsaPokazivač(odredišteunos, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		odredište_2[i] = izvor_2[i]
	}
}
func (isti *Proceshelper) Createsadata() Proces {
	proces := Proces{}
	return proces
}
