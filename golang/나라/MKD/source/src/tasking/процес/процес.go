package процес

import . "unsafe"
import . "util/листа"
import mem "меморијаmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcКорисникheapГолемина = 1 * 1024 * 1024

type Процес struct {
	ид		uint32
	syscallИд	int
	IsКорисникspace	bool
	аргументи	*[]byte

	ThreadЛиста	LinkedЛиста
	Threads		*LinkedЛиста
	ДатотекаИме	[]byte

	СтраницаДиректориумentry	uintptr
}

func (само *Процес) Init(mem *mem.TМеморијаmanager) {
	само.ThreadЛиста = LinkedЛиста{}
	само.Threads = &само.ThreadЛиста
	само.Threads.Init(mem)
}

type Процесhelper struct {
	процеси				LinkedЛиста
	mem				*mem.TМеморијаmanager
	kernelСтраницаДиректориумentry	uintptr
}

func (само *Процесhelper) Init(mem *mem.TМеморијаmanager, kernelСтраницаДиректориумentry uintptr) {
	само.mem = mem
	само.процеси = LinkedЛиста{}
	само.процеси.Init(само.mem)
	само.kernelСтраницаДиректориумentry = kernelСтраницаДиректориумentry
}

func (само *Процесhelper) Create(entrypoint func(), threadhelper *TThreadhelper, СтраницаДиректориумentry uint32, iskernel bool) Процес {
	процес := (*Процес)(само.mem.Malloc(uint32(Sizeof(Процес{}))))
	if процес == nil {
		return Процес{}
	}
	процес.Init(само.mem)
	процес.ид = Allocatepid()
	процес.СтраницаДиректориумentry = uintptr(СтраницаДиректориумentry)
	главенthread := threadhelper.CreateСтрелкаfromФункција(entrypoint, СтраницаДиректориумentry, iskernel)
	if главенthread != nil {
		главенthread.Pid = процес.ид
		главенthread.Parentpid = 0
		процес.Threads.Append_to_list(uintptr(Pointer(главенthread)))
	}

	само.процеси.Append_to_list(uintptr(Pointer(процес)))

	return *процес
}

func (само *Процесhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, СтраницаДиректориумentry uint32, iskernel bool) Процес {
	процес := само.Create(entrypoint, threadhelper, СтраницаДиректориумentry, iskernel)
	if процес.Threads != nil && процес.Threads.Големина_2 > 0 {
		thread := (*TThread)(процес.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Додајthread(thread)
		}
	}
	return процес
}

func (само *Процесhelper) копирајСтраницаДиректориум(изворentry uintptr, одредиштеentry uintptr) {
	извор_2 := Getunsignedinteger32ПостроиfromСтрелка(изворentry, 1024, 1024)
	одредиште_2 := Getunsignedinteger32ПостроиfromСтрелка(одредиштеentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		одредиште_2[i] = извор_2[i]
	}
}
func (само *Процесhelper) Createfromdata() Процес {
	процес := Процес{}
	return процес
}
