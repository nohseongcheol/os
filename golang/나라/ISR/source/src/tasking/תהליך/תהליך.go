package תהליך

import . "unsafe"
import . "util/רשימה"
import mem "זיכרוןmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const Procמשתמשheapגודל = 1 * 1024 * 1024

type Pתהליך struct {
	מזהה_2		uint32
	syscallמזהה	int
	Isמשתמשרווח	bool
	ארגומנטים	*[]byte

	Threadרשימה	Linkedרשימה
	Threads		*Linkedרשימה
	Fקובץשם		[]byte

	Pעמודספרייהentry	uintptr
}

func (self *Pתהליך) Init(mem *mem.Tזיכרוןmanager) {
	self.Threadרשימה = Linkedרשימה{}
	self.Threads = &self.Threadרשימה
	self.Threads.Init(mem)
}

type Pתהליךhelper struct {
	תהליכים			Linkedרשימה
	mem			*mem.Tזיכרוןmanager
	kernelעמודספרייהentry	uintptr
}

func (self *Pתהליךhelper) Init(mem *mem.Tזיכרוןmanager, kernelעמודספרייהentry uintptr) {
	self.mem = mem
	self.תהליכים = Linkedרשימה{}
	self.תהליכים.Init(self.mem)
	self.kernelעמודספרייהentry = kernelעמודספרייהentry
}

func (self *Pתהליךhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Pעמודספרייהentry uint32, iskernel bool) Pתהליך {
	תהליך := (*Pתהליך)(self.mem.Malloc(uint32(Sizeof(Pתהליך{}))))
	if תהליך == nil {
		return Pתהליך{}
	}
	תהליך.Init(self.mem)
	תהליך.מזהה_2 = Allocateמזההתהליך()
	תהליך.Pעמודספרייהentry = uintptr(Pעמודספרייהentry)
	ראשיthread := threadhelper.Createסמןfromפונקציה(entrypoint, Pעמודספרייהentry, iskernel)
	if ראשיthread != nil {
		ראשיthread.Pמזההתהליך = תהליך.מזהה_2
		ראשיthread.Parentמזההתהליך = 0
		תהליך.Threads.Append_to_list(uintptr(Pointer(ראשיthread)))
	}

	self.תהליכים.Append_to_list(uintptr(Pointer(תהליך)))

	return *תהליך
}

func (self *Pתהליךhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Pעמודספרייהentry uint32, iskernel bool) Pתהליך {
	תהליך := self.Create(entrypoint, threadhelper, Pעמודספרייהentry, iskernel)
	if תהליך.Threads != nil && תהליך.Threads.Sגודל_2 > 0 {
		thread := (*TThread)(תהליך.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Aהוספהthread(thread)
		}
	}
	return תהליך
}

func (self *Pתהליךhelper) העתקעמודספרייה(מקורentry uintptr, יעדentry uintptr) {
	מקור_2 := Getunsignedinteger32מערךfromסמן(מקורentry, 1024, 1024)
	יעד_2 := Getunsignedinteger32מערךfromסמן(יעדentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		יעד_2[i] = מקור_2[i]
	}
}
func (self *Pתהליךhelper) Createfromdata() Pתהליך {
	תהליך := Pתהליך{}
	return תהליך
}
