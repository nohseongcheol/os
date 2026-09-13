package διεργασία

import . "unsafe"
import . "util/λίστα"
import mem "μνήμηmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcΧρήστηςheapΜέγεθος = 1 * 1024 * 1024

type Διεργασία struct {
	τΑΥΤΌΤΗΤΑ		uint32
	syscallΤΑΥΤΌΤΗΤΑ	int
	IsΧρήστηςΔιάστημα	bool
	παράμετροι		*[]byte

	ThreadΛίστα	LinkedΛίστα
	Threads		*LinkedΛίστα
	ΑρχείοΌνομα	[]byte

	ΣελίδαΚατάλογοςκαταχώρηση	uintptr
}

func (self *Διεργασία) Init(mem *mem.TΜνήμηmanager) {
	self.ThreadΛίστα = LinkedΛίστα{}
	self.Threads = &self.ThreadΛίστα
	self.Threads.Init(mem)
}

type Διεργασίαhelper struct {
	διεργασίες			LinkedΛίστα
	mem				*mem.TΜνήμηmanager
	kernelΣελίδαΚατάλογοςκαταχώρηση	uintptr
}

func (self *Διεργασίαhelper) Init(mem *mem.TΜνήμηmanager, kernelΣελίδαΚατάλογοςκαταχώρηση uintptr) {
	self.mem = mem
	self.διεργασίες = LinkedΛίστα{}
	self.διεργασίες.Init(self.mem)
	self.kernelΣελίδαΚατάλογοςκαταχώρηση = kernelΣελίδαΚατάλογοςκαταχώρηση
}

func (self *Διεργασίαhelper) Create(καταχώρησηpoint func(), threadhelper *TThreadhelper, ΣελίδαΚατάλογοςκαταχώρηση uint32, iskernel bool) Διεργασία {
	διεργασία := (*Διεργασία)(self.mem.Malloc(uint32(Sizeof(Διεργασία{}))))
	if διεργασία == nil {
		return Διεργασία{}
	}
	διεργασία.Init(self.mem)
	διεργασία.τΑΥΤΌΤΗΤΑ = Allocatepid()
	διεργασία.ΣελίδαΚατάλογοςκαταχώρηση = uintptr(ΣελίδαΚατάλογοςκαταχώρηση)
	κύριοthread := threadhelper.CreateΔείκτηςfromΣυνάρτηση(καταχώρησηpoint, ΣελίδαΚατάλογοςκαταχώρηση, iskernel)
	if κύριοthread != nil {
		κύριοthread.Pid = διεργασία.τΑΥΤΌΤΗΤΑ
		κύριοthread.Γονικόpid = 0
		διεργασία.Threads.Append_to_list(uintptr(Pointer(κύριοthread)))
	}

	self.διεργασίες.Append_to_list(uintptr(Pointer(διεργασία)))

	return *διεργασία
}

func (self *Διεργασίαhelper) Spawn(καταχώρησηpoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, ΣελίδαΚατάλογοςκαταχώρηση uint32, iskernel bool) Διεργασία {
	διεργασία := self.Create(καταχώρησηpoint, threadhelper, ΣελίδαΚατάλογοςκαταχώρηση, iskernel)
	if διεργασία.Threads != nil && διεργασία.Threads.Μέγεθος_2 > 0 {
		thread := (*TThread)(διεργασία.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Προσθήκηthread(thread)
		}
	}
	return διεργασία
}

func (self *Διεργασίαhelper) αντιγραφήΣελίδαΚατάλογος(πηγήκαταχώρηση uintptr, προορισμόςκαταχώρηση uintptr) {
	πηγή_2 := Getunsignedinteger32ΔιάταξηfromΔείκτης(πηγήκαταχώρηση, 1024, 1024)
	προορισμός_2 := Getunsignedinteger32ΔιάταξηfromΔείκτης(προορισμόςκαταχώρηση, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		προορισμός_2[i] = πηγή_2[i]
	}
}
func (self *Διεργασίαhelper) Createfromdata() Διεργασία {
	διεργασία := Διεργασία{}
	return διεργασία
}
