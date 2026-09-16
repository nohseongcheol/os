/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proces

import . "unsafe"
import . "util/liste"
import mem "hukommelsemanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcBrugerheapStørrelse = 1 * 1024 * 1024

type Proces struct {
	id			uint32
	syscallid		int
	IsBrugerMellemrum	bool
	argumenter		*[]byte

	ThreadListe	LinkedListe
	Threads		*LinkedListe
	FilNavn		[]byte

	SideMappeemne	uintptr
}

func (selv *Proces) Init(mem *mem.THukommelsemanager) {
	selv.ThreadListe = LinkedListe{}
	selv.Threads = &selv.ThreadListe
	selv.Threads.Init(mem)
}

type Proceshelper struct {
	processer		LinkedListe
	mem			*mem.THukommelsemanager
	kernelSideMappeemne	uintptr
}

func (selv *Proceshelper) Init(mem *mem.THukommelsemanager, kernelSideMappeemne uintptr) {
	selv.mem = mem
	selv.processer = LinkedListe{}
	selv.processer.Init(selv.mem)
	selv.kernelSideMappeemne = kernelSideMappeemne
}

func (selv *Proceshelper) Create(emnepoint func(), threadhelper *TThreadhelper, SideMappeemne uint32, iskernel bool) Proces {
	proces := (*Proces)(selv.mem.Malloc(uint32(Sizeof(Proces{}))))
	if proces == nil {
		return Proces{}
	}
	proces.Init(selv.mem)
	proces.id = Allocatepid()
	proces.SideMappeemne = uintptr(SideMappeemne)
	hovedthread := threadhelper.CreateMarkørfraFunktion(emnepoint, SideMappeemne, iskernel)
	if hovedthread != nil {
		hovedthread.Pid = proces.id
		hovedthread.Forælderpid = 0
		proces.Threads.Append_to_list(uintptr(Pointer(hovedthread)))
	}

	selv.processer.Append_to_list(uintptr(Pointer(proces)))

	return *proces
}

func (selv *Proceshelper) Spawn(emnepoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, SideMappeemne uint32, iskernel bool) Proces {
	proces := selv.Create(emnepoint, threadhelper, SideMappeemne, iskernel)
	if proces.Threads != nil && proces.Threads.Størrelse_2 > 0 {
		thread := (*TThread)(proces.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Tilføjthread(thread)
		}
	}
	return proces
}

func (selv *Proceshelper) kopiérSideMappe(kildeemne uintptr, destinationemne uintptr) {
	kilde_2 := Getunsignedinteger32TabelfraMarkør(kildeemne, 1024, 1024)
	destination_2 := Getunsignedinteger32TabelfraMarkør(destinationemne, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = kilde_2[i]
	}
}
func (selv *Proceshelper) Createfradata() Proces {
	proces := Proces{}
	return proces
}
