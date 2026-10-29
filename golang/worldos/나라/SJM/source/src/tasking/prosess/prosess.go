/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package prosess

import . "unsafe"
import . "util/liste"
import mem "minnemanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcBrukerheapStørrelse = 1 * 1024 * 1024

type Prosess struct {
	id			uint32
	syscallid		int
	IsBrukerMellomrom	bool
	argumenter		*[]byte

	ThreadListe	LinkedListe
	Threads		*LinkedListe
	FilNavn		[]byte

	SideKatalogentry	uintptr
}

func (selv *Prosess) Init(mem *mem.TMinnemanager) {
	selv.ThreadListe = LinkedListe{}
	selv.Threads = &selv.ThreadListe
	selv.Threads.Init(mem)
}

type Prosesshelper struct {
	prosesser		LinkedListe
	mem			*mem.TMinnemanager
	kernelSideKatalogentry	uintptr
}

func (selv *Prosesshelper) Init(mem *mem.TMinnemanager, kernelSideKatalogentry uintptr) {
	selv.mem = mem
	selv.prosesser = LinkedListe{}
	selv.prosesser.Init(selv.mem)
	selv.kernelSideKatalogentry = kernelSideKatalogentry
}

func (selv *Prosesshelper) Create(entrypoint func(), threadhelper *TThreadhelper, SideKatalogentry uint32, iskernel bool) Prosess {
	prosess := (*Prosess)(selv.mem.Malloc(uint32(Sizeof(Prosess{}))))
	if prosess == nil {
		return Prosess{}
	}
	prosess.Init(selv.mem)
	prosess.id = Allocatepid()
	prosess.SideKatalogentry = uintptr(SideKatalogentry)
	hovedthread := threadhelper.CreatePekerfromFunksjon(entrypoint, SideKatalogentry, iskernel)
	if hovedthread != nil {
		hovedthread.Pid = prosess.id
		hovedthread.Opphavpid = 0
		prosess.Threads.Append_to_list(uintptr(Pointer(hovedthread)))
	}

	selv.prosesser.Append_to_list(uintptr(Pointer(prosess)))

	return *prosess
}

func (selv *Prosesshelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, SideKatalogentry uint32, iskernel bool) Prosess {
	prosess := selv.Create(entrypoint, threadhelper, SideKatalogentry, iskernel)
	if prosess.Threads != nil && prosess.Threads.Størrelse_2 > 0 {
		thread := (*TThread)(prosess.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Leggtilthread(thread)
		}
	}
	return prosess
}

func (selv *Prosesshelper) kopierSideKatalog(kildeentry uintptr, målentry uintptr) {
	kilde_2 := Getunsignedinteger32TabellfromPeker(kildeentry, 1024, 1024)
	mål_2 := Getunsignedinteger32TabellfromPeker(målentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		mål_2[i] = kilde_2[i]
	}
}
func (selv *Prosesshelper) Createfromdata() Prosess {
	prosess := Prosess{}
	return prosess
}
