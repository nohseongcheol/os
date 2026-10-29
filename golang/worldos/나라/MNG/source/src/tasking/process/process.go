/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package process

import . "unsafe"
import . "util/list"
import mem "санахойЗохицуулагч"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcХэрэглэгчheapХэмжээ = 1 * 1024 * 1024

type Process struct {
	дугаар			uint32
	syscallДугаар		int
	IsХэрэглэгчspace	bool
	arguments		*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	ФайлНэр		[]byte

	ХУУДАСЛавлахentry	uintptr
}

func (self *Process) Init(mem *mem.TСанахойЗохицуулагч) {
	self.Threadlist = Linkedlist{}
	self.Threads = &self.Threadlist
	self.Threads.Init(mem)
}

type Processhelper struct {
	processes		Linkedlist
	mem			*mem.TСанахойЗохицуулагч
	kernelХУУДАСЛавлахentry	uintptr
}

func (self *Processhelper) Init(mem *mem.TСанахойЗохицуулагч, kernelХУУДАСЛавлахentry uintptr) {
	self.mem = mem
	self.processes = Linkedlist{}
	self.processes.Init(self.mem)
	self.kernelХУУДАСЛавлахentry = kernelХУУДАСЛавлахentry
}

func (self *Processhelper) Create(entrypoint func(), threadhelper *TThreadhelper, ХУУДАСЛавлахentry uint32, iskernel bool) Process {
	process := (*Process)(self.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(self.mem)
	process.дугаар = Allocatepid()
	process.ХУУДАСЛавлахentry = uintptr(ХУУДАСЛавлахentry)
	үндсэнthread := threadhelper.Createpointerfromfunction(entrypoint, ХУУДАСЛавлахentry, iskernel)
	if үндсэнthread != nil {
		үндсэнthread.Pid = process.дугаар
		үндсэнthread.Parentpid = 0
		process.Threads.Append_to_list(uintptr(Pointer(үндсэнthread)))
	}

	self.processes.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (self *Processhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, ХУУДАСЛавлахentry uint32, iskernel bool) Process {
	process := self.Create(entrypoint, threadhelper, ХУУДАСЛавлахentry, iskernel)
	if process.Threads != nil && process.Threads.Хэмжээ_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Нэмэхthread(thread)
		}
	}
	return process
}

func (self *Processhelper) хуулахХУУДАСЛавлах(эхentry uintptr, destinationentry uintptr) {
	эх_2 := Getunsignedinteger32arrayfrompointer(эхentry, 1024, 1024)
	destination_2 := Getunsignedinteger32arrayfrompointer(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = эх_2[i]
	}
}
func (self *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
