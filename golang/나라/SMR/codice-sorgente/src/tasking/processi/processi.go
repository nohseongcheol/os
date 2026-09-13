package processi

import . "unsafe"
import . "util/elenco"
import mem "memoriamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcUtenteheapDimensione = 1 * 1024 * 1024

type Processi struct {
	id		uint32
	syscallid	int
	IsUtenteSpazio	bool
	argomenti	*[]byte

	ThreadElenco	LinkedElenco
	Threads		*LinkedElenco
	FileNome	[]byte

	PAGINACartellavoce	uintptr
}

func (séstesso *Processi) Init(mem *mem.TMemoriamanager) {
	séstesso.ThreadElenco = LinkedElenco{}
	séstesso.Threads = &séstesso.ThreadElenco
	séstesso.Threads.Init(mem)
}

type Processihelper struct {
	processi_2			LinkedElenco
	mem				*mem.TMemoriamanager
	kernelPAGINACartellavoce	uintptr
}

func (séstesso *Processihelper) Init(mem *mem.TMemoriamanager, kernelPAGINACartellavoce uintptr) {
	séstesso.mem = mem
	séstesso.processi_2 = LinkedElenco{}
	séstesso.processi_2.Init(séstesso.mem)
	séstesso.kernelPAGINACartellavoce = kernelPAGINACartellavoce
}

func (séstesso *Processihelper) Create(vocepoint func(), threadhelper *TThreadhelper, PAGINACartellavoce uint32, iskernel bool) Processi {
	processi := (*Processi)(séstesso.mem.Alloca_memoria(uint32(Sizeof(Processi{}))))
	if processi == nil {
		return Processi{}
	}
	processi.Init(séstesso.mem)
	processi.id = Allocatepid()
	processi.PAGINACartellavoce = uintptr(PAGINACartellavoce)
	principalethread := threadhelper.CreatePuntatorefromFunzione(vocepoint, PAGINACartellavoce, iskernel)
	if principalethread != nil {
		principalethread.Pid = processi.id
		principalethread.Genitorepid = 0
		processi.Threads.Aggiungi_in_fondo_alla_lista(uintptr(Pointer(principalethread)))
	}

	séstesso.processi_2.Aggiungi_in_fondo_alla_lista(uintptr(Pointer(processi)))

	return *processi
}

func (séstesso *Processihelper) Spawn(vocepoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, PAGINACartellavoce uint32, iskernel bool) Processi {
	processi := séstesso.Create(vocepoint, threadhelper, PAGINACartellavoce, iskernel)
	if processi.Threads != nil && processi.Threads.Dimensione_2 > 0 {
		thread := (*TThread)(processi.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Aggiungithread(thread)
		}
	}
	return processi
}

func (séstesso *Processihelper) copiaPAGINACartella(originevoce uintptr, destinazionevoce uintptr) {
	origine_2 := Getunsignedinteger32SeriefromPuntatore(originevoce, 1024, 1024)
	destinazione_2 := Getunsignedinteger32SeriefromPuntatore(destinazionevoce, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destinazione_2[i] = origine_2[i]
	}
}
func (séstesso *Processihelper) Createfromdata() Processi {
	processi := Processi{}
	return processi
}
