/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package procés

import . "unsafe"
import . "util/llista"
import mem "memòriamanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcUsuariheapMida = 1 * 1024 * 1024

type Procés struct {
	identificador		uint32
	syscallIdentificador	int
	IsUsuariEspai		bool
	arguments		*[]byte

	ThreadLlista	LinkedLlista
	Threads		*LinkedLlista
	FitxerNom	[]byte

	PàginaDirectorientrada	uintptr
}

func (unmateix *Procés) Init(mem *mem.TMemòriamanager) {
	unmateix.ThreadLlista = LinkedLlista{}
	unmateix.Threads = &unmateix.ThreadLlista
	unmateix.Threads.Init(mem)
}

type Procéshelper struct {
	processos			LinkedLlista
	mem				*mem.TMemòriamanager
	kernelPàginaDirectorientrada	uintptr
}

func (unmateix *Procéshelper) Init(mem *mem.TMemòriamanager, kernelPàginaDirectorientrada uintptr) {
	unmateix.mem = mem
	unmateix.processos = LinkedLlista{}
	unmateix.processos.Init(unmateix.mem)
	unmateix.kernelPàginaDirectorientrada = kernelPàginaDirectorientrada
}

func (unmateix *Procéshelper) Create(entradapoint func(), threadhelper *TThreadhelper, PàginaDirectorientrada uint32, iskernel bool) Procés {
	procés := (*Procés)(unmateix.mem.Malloc(uint32(Sizeof(Procés{}))))
	if procés == nil {
		return Procés{}
	}
	procés.Init(unmateix.mem)
	procés.identificador = Allocatepid()
	procés.PàginaDirectorientrada = uintptr(PàginaDirectorientrada)
	principalthread := threadhelper.CreatePunterdesdeFunció(entradapoint, PàginaDirectorientrada, iskernel)
	if principalthread != nil {
		principalthread.Pid = procés.identificador
		principalthread.Parepid = 0
		procés.Threads.Append_to_list(uintptr(Pointer(principalthread)))
	}

	unmateix.processos.Append_to_list(uintptr(Pointer(procés)))

	return *procés
}

func (unmateix *Procéshelper) Spawn(entradapoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, PàginaDirectorientrada uint32, iskernel bool) Procés {
	procés := unmateix.Create(entradapoint, threadhelper, PàginaDirectorientrada, iskernel)
	if procés.Threads != nil && procés.Threads.Mida_2 > 0 {
		thread := (*TThread)(procés.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Afegeixthread(thread)
		}
	}
	return procés
}

func (unmateix *Procéshelper) copiaPàginaDirectori(origenentrada uintptr, destinacióentrada uintptr) {
	origen_2 := Getunsignedinteger32MatriudesdePunter(origenentrada, 1024, 1024)
	destinació_2 := Getunsignedinteger32MatriudesdePunter(destinacióentrada, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destinació_2[i] = origen_2[i]
	}
}
func (unmateix *Procéshelper) Createdesdedata() Procés {
	procés := Procés{}
	return procés
}
