package procesas

import . "unsafe"
import . "util/sąrašas"
import mem "atmintismanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcNaudotojasheapDydis = 1 * 1024 * 1024

type Procesas struct {
	id			uint32
	syscallid		int
	IsNaudotojasTarpas	bool
	argumentai		*[]byte

	ThreadSąrašas		LinkedSąrašas
	Threads			*LinkedSąrašas
	FailasPavadinimas	[]byte

	Puslapiskatalogasįrašas	uintptr
}

func (self *Procesas) Init(mem *mem.TAtmintismanager) {
	self.ThreadSąrašas = LinkedSąrašas{}
	self.Threads = &self.ThreadSąrašas
	self.Threads.Init(mem)
}

type Procesashelper struct {
	procesai			LinkedSąrašas
	mem				*mem.TAtmintismanager
	kernelPuslapiskatalogasįrašas	uintptr
}

func (self *Procesashelper) Init(mem *mem.TAtmintismanager, kernelPuslapiskatalogasįrašas uintptr) {
	self.mem = mem
	self.procesai = LinkedSąrašas{}
	self.procesai.Init(self.mem)
	self.kernelPuslapiskatalogasįrašas = kernelPuslapiskatalogasįrašas
}

func (self *Procesashelper) Create(įrašaspoint func(), threadhelper *TThreadhelper, Puslapiskatalogasįrašas uint32, iskernel bool) Procesas {
	procesas := (*Procesas)(self.mem.Malloc(uint32(Sizeof(Procesas{}))))
	if procesas == nil {
		return Procesas{}
	}
	procesas.Init(self.mem)
	procesas.id = Allocatepid()
	procesas.Puslapiskatalogasįrašas = uintptr(Puslapiskatalogasįrašas)
	pagrindinisthread := threadhelper.CreateRodyklėfromFunkcija(įrašaspoint, Puslapiskatalogasįrašas, iskernel)
	if pagrindinisthread != nil {
		pagrindinisthread.Pid = procesas.id
		pagrindinisthread.Parentpid = 0
		procesas.Threads.Append_to_list(uintptr(Pointer(pagrindinisthread)))
	}

	self.procesai.Append_to_list(uintptr(Pointer(procesas)))

	return *procesas
}

func (self *Procesashelper) Spawn(įrašaspoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Puslapiskatalogasįrašas uint32, iskernel bool) Procesas {
	procesas := self.Create(įrašaspoint, threadhelper, Puslapiskatalogasįrašas, iskernel)
	if procesas.Threads != nil && procesas.Threads.Dydis_2 > 0 {
		thread := (*TThread)(procesas.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Pridėtithread(thread)
		}
	}
	return procesas
}

func (self *Procesashelper) kopijuotiPuslapiskatalogas(šaltinisįrašas uintptr, tikslasįrašas uintptr) {
	šaltinis_2 := Getunsignedinteger32MasyvasfromRodyklė(šaltinisįrašas, 1024, 1024)
	tikslas_2 := Getunsignedinteger32MasyvasfromRodyklė(tikslasįrašas, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		tikslas_2[i] = šaltinis_2[i]
	}
}
func (self *Procesashelper) Createfromdata() Procesas {
	procesas := Procesas{}
	return procesas
}
