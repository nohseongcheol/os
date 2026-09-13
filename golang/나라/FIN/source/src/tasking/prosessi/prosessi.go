package prosessi

import . "unsafe"
import . "util/listaa"
import mem "muistimanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcKäyttäjäheapKoko = 1 * 1024 * 1024

type Prosessi struct {
	tUNNISTE	uint32
	syscallTUNNISTE	int
	IsKäyttäjäVäli	bool
	parametrit	*[]byte

	Threadlistaa	Linkedlistaa
	Threads		*Linkedlistaa
	TiedostoNimi	[]byte

	SivuKansiohakusana	uintptr
}

func (itse *Prosessi) Init(mem *mem.TMuistimanager) {
	itse.Threadlistaa = Linkedlistaa{}
	itse.Threads = &itse.Threadlistaa
	itse.Threads.Init(mem)
}

type Prosessihelper struct {
	prosessit			Linkedlistaa
	mem				*mem.TMuistimanager
	kernelSivuKansiohakusana	uintptr
}

func (itse *Prosessihelper) Init(mem *mem.TMuistimanager, kernelSivuKansiohakusana uintptr) {
	itse.mem = mem
	itse.prosessit = Linkedlistaa{}
	itse.prosessit.Init(itse.mem)
	itse.kernelSivuKansiohakusana = kernelSivuKansiohakusana
}

func (itse *Prosessihelper) Luo(hakusanapoint func(), threadhelper *TThreadhelper, SivuKansiohakusana uint32, iskernel bool) Prosessi {
	prosessi := (*Prosessi)(itse.mem.Varaa_muistia(uint32(Sizeof(Prosessi{}))))
	if prosessi == nil {
		return Prosessi{}
	}
	prosessi.Init(itse.mem)
	prosessi.tUNNISTE = Allocatepid()
	prosessi.SivuKansiohakusana = uintptr(SivuKansiohakusana)
	pääthread := threadhelper.LuoOsoitinlähteestäFunktio(hakusanapoint, SivuKansiohakusana, iskernel)
	if pääthread != nil {
		pääthread.Pid = prosessi.tUNNISTE
		pääthread.Vanhempipid = 0
		prosessi.Threads.Lisää_listan_loppuun(uintptr(Pointer(pääthread)))
	}

	itse.prosessit.Lisää_listan_loppuun(uintptr(Pointer(prosessi)))

	return *prosessi
}

func (itse *Prosessihelper) Spawn(hakusanapoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, SivuKansiohakusana uint32, iskernel bool) Prosessi {
	prosessi := itse.Luo(hakusanapoint, threadhelper, SivuKansiohakusana, iskernel)
	if prosessi.Threads != nil && prosessi.Threads.Koko_2 > 0 {
		thread := (*TThread)(prosessi.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Lisääthread(thread)
		}
	}
	return prosessi
}

func (itse *Prosessihelper) kopioiSivuKansio(lähdehakusana uintptr, kohdehakusana uintptr) {
	lähde_2 := Getunsignedinteger32TaulukkolähteestäOsoitin(lähdehakusana, 1024, 1024)
	kohde_2 := Getunsignedinteger32TaulukkolähteestäOsoitin(kohdehakusana, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		kohde_2[i] = lähde_2[i]
	}
}
func (itse *Prosessihelper) Luolähteestädata() Prosessi {
	prosessi := Prosessi{}
	return prosessi
}
