/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package process

import . "unsafe"
import . "util/list"
import mem "arikaMpandrindra"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcMpampiasaheapHabe = 1 * 1024 * 1024

type Process struct {
	id			uint32
	syscallid		int
	IsMpampiasaspace	bool
	arguments		*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	RakitraAnarana	[]byte

	PEJYLahatahiryentry	uintptr
}

func (nytena *Process) Init(mem *mem.TArikaMpandrindra) {
	nytena.Threadlist = Linkedlist{}
	nytena.Threads = &nytena.Threadlist
	nytena.Threads.Init(mem)
}

type Processhelper struct {
	asa				Linkedlist
	mem				*mem.TArikaMpandrindra
	kernelPEJYLahatahiryentry	uintptr
}

func (nytena *Processhelper) Init(mem *mem.TArikaMpandrindra, kernelPEJYLahatahiryentry uintptr) {
	nytena.mem = mem
	nytena.asa = Linkedlist{}
	nytena.asa.Init(nytena.mem)
	nytena.kernelPEJYLahatahiryentry = kernelPEJYLahatahiryentry
}

func (nytena *Processhelper) Create(entrypoint func(), threadhelper *TThreadhelper, PEJYLahatahiryentry uint32, iskernel bool) Process {
	process := (*Process)(nytena.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(nytena.mem)
	process.id = Allocatepid()
	process.PEJYLahatahiryentry = uintptr(PEJYLahatahiryentry)
	fototrathread := threadhelper.Createpointerfromfunction(entrypoint, PEJYLahatahiryentry, iskernel)
	if fototrathread != nil {
		fototrathread.Pid = process.id
		fototrathread.Renypid = 0
		process.Threads.Append_to_list(uintptr(Pointer(fototrathread)))
	}

	nytena.asa.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (nytena *Processhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, PEJYLahatahiryentry uint32, iskernel bool) Process {
	process := nytena.Create(entrypoint, threadhelper, PEJYLahatahiryentry, iskernel)
	if process.Threads != nil && process.Threads.Habe_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Ampidirothread(thread)
		}
	}
	return process
}

func (nytena *Processhelper) adikaoPEJYLahatahiry(loharanoentry uintptr, destinationentry uintptr) {
	loharano_2 := Getunsignedinteger32arrayfrompointer(loharanoentry, 1024, 1024)
	destination_2 := Getunsignedinteger32arrayfrompointer(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = loharano_2[i]
	}
}
func (nytena *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
