/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package процес

import . "unsafe"
import . "util/списак"
import mem "меморијаmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcКорисникheapВеличина = 1 * 1024 * 1024

type Процес struct {
	иБ			uint32
	syscallИБ		int
	IsКорисникразмак	bool
	аргументи		*[]byte

	ThreadСписак	LinkedСписак
	Threads		*LinkedСписак
	ДатотекаНазив	[]byte

	СТРАНАДиректоријумунос	uintptr
}

func (исти *Процес) Init(mem *mem.TМеморијаmanager) {
	исти.ThreadСписак = LinkedСписак{}
	исти.Threads = &исти.ThreadСписак
	исти.Threads.Init(mem)
}

type Процесhelper struct {
	процеси				LinkedСписак
	mem				*mem.TМеморијаmanager
	kernelСТРАНАДиректоријумунос	uintptr
}

func (исти *Процесhelper) Init(mem *mem.TМеморијаmanager, kernelСТРАНАДиректоријумунос uintptr) {
	исти.mem = mem
	исти.процеси = LinkedСписак{}
	исти.процеси.Init(исти.mem)
	исти.kernelСТРАНАДиректоријумунос = kernelСТРАНАДиректоријумунос
}

func (исти *Процесhelper) Create(уносpoint func(), threadhelper *TThreadhelper, СТРАНАДиректоријумунос uint32, iskernel bool) Процес {
	процес := (*Процес)(исти.mem.Malloc(uint32(Sizeof(Процес{}))))
	if процес == nil {
		return Процес{}
	}
	процес.Init(исти.mem)
	процес.иБ = AllocateПИД()
	процес.СТРАНАДиректоријумунос = uintptr(СТРАНАДиректоријумунос)
	главниthread := threadhelper.CreateПоказивачсафункција(уносpoint, СТРАНАДиректоријумунос, iskernel)
	if главниthread != nil {
		главниthread.ПИД = процес.иБ
		главниthread.НадређениПИД = 0
		процес.Threads.Append_to_list(uintptr(Pointer(главниthread)))
	}

	исти.процеси.Append_to_list(uintptr(Pointer(процес)))

	return *процес
}

func (исти *Процесhelper) Spawn(уносpoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, СТРАНАДиректоријумунос uint32, iskernel bool) Процес {
	процес := исти.Create(уносpoint, threadhelper, СТРАНАДиректоријумунос, iskernel)
	if процес.Threads != nil && процес.Threads.Величина_2 > 0 {
		thread := (*TThread)(процес.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Додајthread(thread)
		}
	}
	return процес
}

func (исти *Процесhelper) умножиСТРАНАДиректоријум(изворунос uintptr, одредиштеунос uintptr) {
	извор_2 := Getunsignedinteger32НизсаПоказивач(изворунос, 1024, 1024)
	одредиште_2 := Getunsignedinteger32НизсаПоказивач(одредиштеунос, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		одредиште_2[i] = извор_2[i]
	}
}
func (исти *Процесhelper) Createсаdata() Процес {
	процес := Процес{}
	return процес
}
