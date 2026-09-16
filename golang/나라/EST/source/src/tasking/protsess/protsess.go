/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protsess

import . "unsafe"
import . "util/nimekiri"
import mem "mälumanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcKasutajaheapSuurus = 1 * 1024 * 1024

type Protsess struct {
	id		uint32
	syscallid	int
	IsKasutajaTühik	bool
	argumendid	*[]byte

	ThreadNimekiri	LinkedNimekiri
	Threads		*LinkedNimekiri
	FailNimi	[]byte

	LehekülgKataloogkirje	uintptr
}

func (ise *Protsess) Init(mem *mem.TMälumanager) {
	ise.ThreadNimekiri = LinkedNimekiri{}
	ise.Threads = &ise.ThreadNimekiri
	ise.Threads.Init(mem)
}

type Protsesshelper struct {
	protsessid			LinkedNimekiri
	mem				*mem.TMälumanager
	kernelLehekülgKataloogkirje	uintptr
}

func (ise *Protsesshelper) Init(mem *mem.TMälumanager, kernelLehekülgKataloogkirje uintptr) {
	ise.mem = mem
	ise.protsessid = LinkedNimekiri{}
	ise.protsessid.Init(ise.mem)
	ise.kernelLehekülgKataloogkirje = kernelLehekülgKataloogkirje
}

func (ise *Protsesshelper) Create(kirjepoint func(), threadhelper *TThreadhelper, LehekülgKataloogkirje uint32, iskernel bool) Protsess {
	protsess := (*Protsess)(ise.mem.Malloc(uint32(Sizeof(Protsess{}))))
	if protsess == nil {
		return Protsess{}
	}
	protsess.Init(ise.mem)
	protsess.id = Allocatepid()
	protsess.LehekülgKataloogkirje = uintptr(LehekülgKataloogkirje)
	peaminethread := threadhelper.CreateKursorfromFunktsioon(kirjepoint, LehekülgKataloogkirje, iskernel)
	if peaminethread != nil {
		peaminethread.Pid = protsess.id
		peaminethread.Vanempid = 0
		protsess.Threads.Append_to_list(uintptr(Pointer(peaminethread)))
	}

	ise.protsessid.Append_to_list(uintptr(Pointer(protsess)))

	return *protsess
}

func (ise *Protsesshelper) Spawn(kirjepoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, LehekülgKataloogkirje uint32, iskernel bool) Protsess {
	protsess := ise.Create(kirjepoint, threadhelper, LehekülgKataloogkirje, iskernel)
	if protsess.Threads != nil && protsess.Threads.Suurus_2 > 0 {
		thread := (*TThread)(protsess.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Lisathread(thread)
		}
	}
	return protsess
}

func (ise *Protsesshelper) kopeeriLehekülgKataloog(aLLIKASkirje uintptr, sihtfailkirje uintptr) {
	aLLIKAS_2 := Getunsignedinteger32MassiivfromKursor(aLLIKASkirje, 1024, 1024)
	sihtfail_2 := Getunsignedinteger32MassiivfromKursor(sihtfailkirje, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		sihtfail_2[i] = aLLIKAS_2[i]
	}
}
func (ise *Protsesshelper) Createfromdata() Protsess {
	protsess := Protsess{}
	return protsess
}
