/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package โพรเซส

import . "unsafe"
import . "util/list"
import mem "memorymanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const Procuserheapขนาด = 1 * 1024 * 1024

type Pโพรเซส struct {
	id		uint32
	syscallid	int
	Isuserspace	bool
	arguments	*[]byte

	Threadlist	Linkedlist
	Threads		*Linkedlist
	Filename	[]byte

	Pagedirectoryentry	uintptr
}

func (self *Pโพรเซส) Init(mem *mem.TMemorymanager) {
	self.Threadlist = Linkedlist{}
	self.Threads = &self.Threadlist
	self.Threads.Init(mem)
}

type Pโพรเซสhelper struct {
	โพรเซส_2			Linkedlist
	mem				*mem.TMemorymanager
	kernelpagedirectoryentry	uintptr
}

func (self *Pโพรเซสhelper) Init(mem *mem.TMemorymanager, kernelpagedirectoryentry uintptr) {
	self.mem = mem
	self.โพรเซส_2 = Linkedlist{}
	self.โพรเซส_2.Init(self.mem)
	self.kernelpagedirectoryentry = kernelpagedirectoryentry
}

func (self *Pโพรเซสhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Pagedirectoryentry uint32, iskernel bool) Pโพรเซส {
	โพรเซส := (*Pโพรเซส)(self.mem.Malloc(uint32(Sizeof(Pโพรเซส{}))))
	if โพรเซส == nil {
		return Pโพรเซส{}
	}
	โพรเซส.Init(self.mem)
	โพรเซส.id = Allocatepid()
	โพรเซส.Pagedirectoryentry = uintptr(Pagedirectoryentry)
	lakthread := threadhelper.Createpointerfromfunction(entrypoint, Pagedirectoryentry, iskernel)
	if lakthread != nil {
		lakthread.Pid = โพรเซส.id
		lakthread.Parentpid = 0
		โพรเซส.Threads.Append_to_list(uintptr(Pointer(lakthread)))
	}

	self.โพรเซส_2.Append_to_list(uintptr(Pointer(โพรเซส)))

	return *โพรเซส
}

func (self *Pโพรเซสhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Pagedirectoryentry uint32, iskernel bool) Pโพรเซส {
	โพรเซส := self.Create(entrypoint, threadhelper, Pagedirectoryentry, iskernel)
	if โพรเซส.Threads != nil && โพรเซส.Threads.Sขนาด_2 > 0 {
		thread := (*TThread)(โพรเซส.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Addthread(thread)
		}
	}
	return โพรเซส
}

func (self *Pโพรเซสhelper) copypagedirectory(sourceentry uintptr, ปลายทางentry uintptr) {
	source_2 := Getunsignedinteger32arrayfrompointer(sourceentry, 1024, 1024)
	ปลายทาง_2 := Getunsignedinteger32arrayfrompointer(ปลายทางentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		ปลายทาง_2[i] = source_2[i]
	}
}
func (self *Pโพรเซสhelper) Createfromdata() Pโพรเซส {
	โพรเซส := Pโพรเซส{}
	return โพรเซส
}
