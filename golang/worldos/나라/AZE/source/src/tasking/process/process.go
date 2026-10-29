/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package process

import . "unsafe"
import . "util/list"
import mem "yaddaşmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcİstifadəçiheapBöyüklük = 1 * 1024 * 1024

type Process struct {
	id			uint32
	syscallid		int
	Isİstifadəçispace	bool
	arguments		*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	FaylAd		[]byte

	SəhifəCərgəentry	uintptr
}

func (self *Process) Init(mem *mem.TYaddaşmanager) {
	self.Threadlist = Linkedlist{}
	self.Threads = &self.Threadlist
	self.Threads.Init(mem)
}

type Processhelper struct {
	processes		Linkedlist
	mem			*mem.TYaddaşmanager
	kernelSəhifəCərgəentry	uintptr
}

func (self *Processhelper) Init(mem *mem.TYaddaşmanager, kernelSəhifəCərgəentry uintptr) {
	self.mem = mem
	self.processes = Linkedlist{}
	self.processes.Init(self.mem)
	self.kernelSəhifəCərgəentry = kernelSəhifəCərgəentry
}

func (self *Processhelper) Create(entrypoint func(), threadhelper *TThreadhelper, SəhifəCərgəentry uint32, iskernel bool) Process {
	process := (*Process)(self.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Init(self.mem)
	process.id = Allocatepid()
	process.SəhifəCərgəentry = uintptr(SəhifəCərgəentry)
	əsasthread := threadhelper.Createpointerfromfunction(entrypoint, SəhifəCərgəentry, iskernel)
	if əsasthread != nil {
		əsasthread.Pid = process.id
		əsasthread.Parentpid = 0
		process.Threads.Append_to_list(uintptr(Pointer(əsasthread)))
	}

	self.processes.Append_to_list(uintptr(Pointer(process)))

	return *process
}

func (self *Processhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, SəhifəCərgəentry uint32, iskernel bool) Process {
	process := self.Create(entrypoint, threadhelper, SəhifəCərgəentry, iskernel)
	if process.Threads != nil && process.Threads.Böyüklük_2 > 0 {
		thread := (*TThread)(process.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.ƏlavəEtthread(thread)
		}
	}
	return process
}

func (self *Processhelper) köçürSəhifəCərgə(mənbəentry uintptr, destinationentry uintptr) {
	mənbə_2 := Getunsignedinteger32arrayfrompointer(mənbəentry, 1024, 1024)
	destination_2 := Getunsignedinteger32arrayfrompointer(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = mənbə_2[i]
	}
}
func (self *Processhelper) Createfromdata() Process {
	process := Process{}
	return process
}
