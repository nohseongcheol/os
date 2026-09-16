/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package процес

import . "unsafe"
import . "util/списък"
import mem "паметmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcСобственикheapРазмер = 1 * 1024 * 1024

type Процес struct {
	иДЕНТИФИКАТОР		uint32
	syscallИДЕНТИФИКАТОР	int
	IsСобственикИнтервал	bool
	параметри		*[]byte

	ThreadСписък	LinkedСписък
	Threads		*LinkedСписък
	ФайлИме		[]byte

	Страницапапказапис	uintptr
}

func (себеси *Процес) Init(mem *mem.TПаметmanager) {
	себеси.ThreadСписък = LinkedСписък{}
	себеси.Threads = &себеси.ThreadСписък
	себеси.Threads.Init(mem)
}

type Процесhelper struct {
	процеси				LinkedСписък
	mem				*mem.TПаметmanager
	kernelСтраницапапказапис	uintptr
}

func (себеси *Процесhelper) Init(mem *mem.TПаметmanager, kernelСтраницапапказапис uintptr) {
	себеси.mem = mem
	себеси.процеси = LinkedСписък{}
	себеси.процеси.Init(себеси.mem)
	себеси.kernelСтраницапапказапис = kernelСтраницапапказапис
}

func (себеси *Процесhelper) Create(записpoint func(), threadhelper *TThreadhelper, Страницапапказапис uint32, iskernel bool) Процес {
	процес := (*Процес)(себеси.mem.Malloc(uint32(Sizeof(Процес{}))))
	if процес == nil {
		return Процес{}
	}
	процес.Init(себеси.mem)
	процес.иДЕНТИФИКАТОР = AllocateИдПр()
	процес.Страницапапказапис = uintptr(Страницапапказапис)
	главенthread := threadhelper.CreateПоказалциfromфункция(записpoint, Страницапапказапис, iskernel)
	if главенthread != nil {
		главенthread.ИдПр = процес.иДЕНТИФИКАТОР
		главенthread.РодителИдПр = 0
		процес.Threads.Append_to_list(uintptr(Pointer(главенthread)))
	}

	себеси.процеси.Append_to_list(uintptr(Pointer(процес)))

	return *процес
}

func (себеси *Процесhelper) Spawn(записpoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Страницапапказапис uint32, iskernel bool) Процес {
	процес := себеси.Create(записpoint, threadhelper, Страницапапказапис, iskernel)
	if процес.Threads != nil && процес.Threads.Размер_2 > 0 {
		thread := (*TThread)(процес.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Добавянеthread(thread)
		}
	}
	return процес
}

func (себеси *Процесhelper) копиранеСтраницапапка(източникзапис uintptr, назначениезапис uintptr) {
	източник_2 := Getunsignedinteger32МасивfromПоказалци(източникзапис, 1024, 1024)
	назначение_2 := Getunsignedinteger32МасивfromПоказалци(назначениезапис, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		назначение_2[i] = източник_2[i]
	}
}
func (себеси *Процесhelper) Createfromdata() Процес {
	процес := Процес{}
	return процес
}
