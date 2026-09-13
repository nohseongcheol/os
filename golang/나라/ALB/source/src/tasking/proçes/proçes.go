package proçes

import . "unsafe"
import . "util/listë"
import mem "memoriaManazhuesi"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcPërdoruesiheapMadhësia = 1 * 1024 * 1024

type Proçes struct {
	id			uint32
	syscallid		int
	IsPërdoruesiHapësira	bool
	argumente		*[]byte

	ThreadListë	LinkedListë
	Threads		*LinkedListë
	KartelëEmri	[]byte

	FaqeDosjeentry	uintptr
}

func (vetvetja *Proçes) Init(mem *mem.TMemoriaManazhuesi) {
	vetvetja.ThreadListë = LinkedListë{}
	vetvetja.Threads = &vetvetja.ThreadListë
	vetvetja.Threads.Init(mem)
}

type Proçeshelper struct {
	proçeset		LinkedListë
	mem			*mem.TMemoriaManazhuesi
	kernelfaqeDosjeentry	uintptr
}

func (vetvetja *Proçeshelper) Init(mem *mem.TMemoriaManazhuesi, kernelfaqeDosjeentry uintptr) {
	vetvetja.mem = mem
	vetvetja.proçeset = LinkedListë{}
	vetvetja.proçeset.Init(vetvetja.mem)
	vetvetja.kernelfaqeDosjeentry = kernelfaqeDosjeentry
}

func (vetvetja *Proçeshelper) Create(entrypoint func(), threadhelper *TThreadhelper, FaqeDosjeentry uint32, iskernel bool) Proçes {
	proçes := (*Proçes)(vetvetja.mem.Malloc(uint32(Sizeof(Proçes{}))))
	if proçes == nil {
		return Proçes{}
	}
	proçes.Init(vetvetja.mem)
	proçes.id = Allocatepid()
	proçes.FaqeDosjeentry = uintptr(FaqeDosjeentry)
	kryesorthread := threadhelper.CreateKursorifromFunksion(entrypoint, FaqeDosjeentry, iskernel)
	if kryesorthread != nil {
		kryesorthread.Pid = proçes.id
		kryesorthread.Prindpid = 0
		proçes.Threads.Append_to_list(uintptr(Pointer(kryesorthread)))
	}

	vetvetja.proçeset.Append_to_list(uintptr(Pointer(proçes)))

	return *proçes
}

func (vetvetja *Proçeshelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, FaqeDosjeentry uint32, iskernel bool) Proçes {
	proçes := vetvetja.Create(entrypoint, threadhelper, FaqeDosjeentry, iskernel)
	if proçes.Threads != nil && proçes.Threads.Madhësia_2 > 0 {
		thread := (*TThread)(proçes.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Shtothread(thread)
		}
	}
	return proçes
}

func (vetvetja *Proçeshelper) kopjofaqeDosje(burimientry uintptr, destinacionientry uintptr) {
	burimi_2 := Getunsignedinteger32RreshtimifromKursori(burimientry, 1024, 1024)
	destinacioni_2 := Getunsignedinteger32RreshtimifromKursori(destinacionientry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destinacioni_2[i] = burimi_2[i]
	}
}
func (vetvetja *Proçeshelper) Createfromdata() Proçes {
	proçes := Proçes{}
	return proçes
}
