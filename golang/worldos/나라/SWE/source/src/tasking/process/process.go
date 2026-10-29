/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package process

import . "unsafe"
import . "util/lista"
import mem "minnemanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcAnvändareheapStorlek = 1 * 1024 * 1024

type Process struct {
	id			uint32
	syscallid		int
	IsAnvändareMellanslag	bool
	argument		*[]byte

	ThreadLista	LinkedLista
	Threads		*LinkedLista
	ArkivNamn	[]byte

	SidaKatalogpost	uintptr
}

func (själv *Process) Init(mem *mem.TMinnemanager) {
	själv.ThreadLista = LinkedLista{}
	själv.Threads = &själv.ThreadLista
	själv.Threads.Init(mem)
}

type Processhelper struct {
	processer		LinkedLista
	mem			*mem.TMinnemanager
	kernelSidaKatalogpost	uintptr
}

func (själv *Processhelper) Init(mem *mem.TMinnemanager, kernelSidaKatalogpost uintptr) {
	själv.mem = mem
	själv.processer = LinkedLista{}
	själv.processer.Init(själv.mem)
	själv.kernelSidaKatalogpost = kernelSidaKatalogpost
}

func (själv *Processhelper) Create(postpoint func(), threadhelper *TThreadhelper, SidaKatalogpost uint32, iskernel bool) Process {
	process := (*Process)(själv.mem.Tilldela_minne(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(själv.mem)
	process.id = Allocateprocessid()
	process.SidaKatalogpost = uintptr(SidaKatalogpost)
	huvudthread := threadhelper.CreateMuspekarefromFunktion(postpoint, SidaKatalogpost, iskernel)
	if huvudthread != nil {
		huvudthread.Processid = process.id
		huvudthread.Förälderprocessid = 0
		process.Threads.Lägg_till_sist_i_listan(uintptr(Pointer(huvudthread)))
	}

	själv.processer.Lägg_till_sist_i_listan(uintptr(Pointer(process)))

	return *process
}

func (själv *Processhelper) Spawn(postpoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, SidaKatalogpost uint32, iskernel bool) Process {
	process := själv.Create(postpoint, threadhelper, SidaKatalogpost, iskernel)
	if process.Threads != nil && process.Threads.Storlek_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Läggtillthread(thread)
		}
	}
	return process
}

func (själv *Processhelper) kopieraSidaKatalog(källapost uintptr, målpost uintptr) {
	källa_2 := Getunsignedinteger32VektorfromMuspekare(källapost, 1024, 1024)
	mål_2 := Getunsignedinteger32VektorfromMuspekare(målpost, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		mål_2[i] = källa_2[i]
	}
}
func (själv *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
