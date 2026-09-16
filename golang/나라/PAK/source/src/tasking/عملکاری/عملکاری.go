/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package عملکاری

import . "unsafe"
import . "util/فہرست"
import mem "یادداشتmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const Procصارفheapحجم = 1 * 1024 * 1024

type Pعملکاری struct {
	آئیڈی		uint32
	syscallآئیڈی	int
	Isصارفspace	bool
	arguments	*[]byte

	Threadفہرست	Linkedفہرست
	Threads		*Linkedفہرست
	Fفائلنام	[]byte

	Pصفحہڈائریکٹریentry	uintptr
}

func (self *Pعملکاری) Init(mem *mem.Tیادداشتmanager) {
	self.Threadفہرست = Linkedفہرست{}
	self.Threads = &self.Threadفہرست
	self.Threads.Init(mem)
}

type Pعملکاریhelper struct {
	عملکاریاں			Linkedفہرست
	mem				*mem.Tیادداشتmanager
	kernelصفحہڈائریکٹریentry	uintptr
}

func (self *Pعملکاریhelper) Init(mem *mem.Tیادداشتmanager, kernelصفحہڈائریکٹریentry uintptr) {
	self.mem = mem
	self.عملکاریاں = Linkedفہرست{}
	self.عملکاریاں.Init(self.mem)
	self.kernelصفحہڈائریکٹریentry = kernelصفحہڈائریکٹریentry
}

func (self *Pعملکاریhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Pصفحہڈائریکٹریentry uint32, iskernel bool) Pعملکاری {
	عملکاری := (*Pعملکاری)(self.mem.Malloc(uint32(Sizeof(Pعملکاری{}))))
	if عملکاری == nil {
		return Pعملکاری{}
	}
	عملکاری.Init(self.mem)
	عملکاری.آئیڈی = Allocatepid()
	عملکاری.Pصفحہڈائریکٹریentry = uintptr(Pصفحہڈائریکٹریentry)
	بنیادیthread := threadhelper.Createپؤائنٹرfromfunction(entrypoint, Pصفحہڈائریکٹریentry, iskernel)
	if بنیادیthread != nil {
		بنیادیthread.Pid = عملکاری.آئیڈی
		بنیادیthread.Pآبائیpid = 0
		عملکاری.Threads.Append_to_list(uintptr(Pointer(بنیادیthread)))
	}

	self.عملکاریاں.Append_to_list(uintptr(Pointer(عملکاری)))

	return *عملکاری
}

func (self *Pعملکاریhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Pصفحہڈائریکٹریentry uint32, iskernel bool) Pعملکاری {
	عملکاری := self.Create(entrypoint, threadhelper, Pصفحہڈائریکٹریentry, iskernel)
	if عملکاری.Threads != nil && عملکاری.Threads.Sحجم_2 > 0 {
		thread := (*TThread)(عملکاری.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Aشاملکریںthread(thread)
		}
	}
	return عملکاری
}

func (self *Pعملکاریhelper) کاپیصفحہڈائریکٹری(مصدرentry uintptr, destinationentry uintptr) {
	مصدر_2 := Getunsignedinteger32لڑیfromپؤائنٹر(مصدرentry, 1024, 1024)
	destination_2 := Getunsignedinteger32لڑیfromپؤائنٹر(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = مصدر_2[i]
	}
}
func (self *Pعملکاریhelper) Createfromdata() Pعملکاری {
	عملکاری := Pعملکاری{}
	return عملکاری
}
