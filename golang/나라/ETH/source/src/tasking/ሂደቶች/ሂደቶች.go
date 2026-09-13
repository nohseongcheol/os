package ሂደቶች

import . "unsafe"
import . "util/ዝርዝር"
import mem "ማስታወሻmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const Procተጠቃሚheapመጠን = 1 * 1024 * 1024

type Pሂደቶች struct {
	መለያ_2		uint32
	syscallመለያ	int
	Isተጠቃሚspace	bool
	arguments	*[]byte

	Threadዝርዝር	Linkedዝርዝር
	Threads		*Linkedዝርዝር
	Fፋይልስም		[]byte

	Pገጽዳይሬክቶሪentry	uintptr
}

func (self *Pሂደቶች) Init(mem *mem.Tማስታወሻmanager) {
	self.Threadዝርዝር = Linkedዝርዝር{}
	self.Threads = &self.Threadዝርዝር
	self.Threads.Init(mem)
}

type Pሂደቶችhelper struct {
	ሂደቶች_2			Linkedዝርዝር
	mem			*mem.Tማስታወሻmanager
	kernelገጽዳይሬክቶሪentry	uintptr
}

func (self *Pሂደቶችhelper) Init(mem *mem.Tማስታወሻmanager, kernelገጽዳይሬክቶሪentry uintptr) {
	self.mem = mem
	self.ሂደቶች_2 = Linkedዝርዝር{}
	self.ሂደቶች_2.Init(self.mem)
	self.kernelገጽዳይሬክቶሪentry = kernelገጽዳይሬክቶሪentry
}

func (self *Pሂደቶችhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Pገጽዳይሬክቶሪentry uint32, iskernel bool) Pሂደቶች {
	ሂደቶች := (*Pሂደቶች)(self.mem.Malloc(uint32(Sizeof(Pሂደቶች{}))))
	if ሂደቶች == nil {
		return Pሂደቶች{}
	}
	ሂደቶች.Init(self.mem)
	ሂደቶች.መለያ_2 = Allocatepid()
	ሂደቶች.Pገጽዳይሬክቶሪentry = uintptr(Pገጽዳይሬክቶሪentry)
	ዋናthread := threadhelper.Createጠቋሚfromfunction(entrypoint, Pገጽዳይሬክቶሪentry, iskernel)
	if ዋናthread != nil {
		ዋናthread.Pid = ሂደቶች.መለያ_2
		ዋናthread.Pወላጅpid = 0
		ሂደቶች.Threads.Append_to_list(uintptr(Pointer(ዋናthread)))
	}

	self.ሂደቶች_2.Append_to_list(uintptr(Pointer(ሂደቶች)))

	return *ሂደቶች
}

func (self *Pሂደቶችhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Pገጽዳይሬክቶሪentry uint32, iskernel bool) Pሂደቶች {
	ሂደቶች := self.Create(entrypoint, threadhelper, Pገጽዳይሬክቶሪentry, iskernel)
	if ሂደቶች.Threads != nil && ሂደቶች.Threads.Sመጠን_2 > 0 {
		thread := (*TThread)(ሂደቶች.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Aመጨመሪያthread(thread)
		}
	}
	return ሂደቶች
}

func (self *Pሂደቶችhelper) ኮፒገጽዳይሬክቶሪ(ምንጩentry uintptr, destinationentry uintptr) {
	ምንጩ_2 := Getunsignedinteger32ማዘጋጃfromጠቋሚ(ምንጩentry, 1024, 1024)
	destination_2 := Getunsignedinteger32ማዘጋጃfromጠቋሚ(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = ምንጩ_2[i]
	}
}
func (self *Pሂደቶችhelper) Createfromdata() Pሂደቶች {
	ሂደቶች := Pሂደቶች{}
	return ሂደቶች
}
