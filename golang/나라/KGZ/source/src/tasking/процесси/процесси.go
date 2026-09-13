package процесси

import . "unsafe"
import . "util/тизме"
import mem "эсиmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcКолдонуучуheapӨлчөм = 1 * 1024 * 1024

type Процесси struct {
	иДЕНТИФИКАТОР		uint32
	syscallИДЕНТИФИКАТОР	int
	IsКолдонуучуspace	bool
	arguments		*[]byte

	ThreadТизме	LinkedТизме
	Threads		*LinkedТизме
	ФайлАты		[]byte

	БАРАКкаталогentry	uintptr
}

func (self *Процесси) Init(mem *mem.TЭсиmanager) {
	self.ThreadТизме = LinkedТизме{}
	self.Threads = &self.ThreadТизме
	self.Threads.Init(mem)
}

type Процессиhelper struct {
	жараяндар		LinkedТизме
	mem			*mem.TЭсиmanager
	kernelБАРАКкаталогentry	uintptr
}

func (self *Процессиhelper) Init(mem *mem.TЭсиmanager, kernelБАРАКкаталогentry uintptr) {
	self.mem = mem
	self.жараяндар = LinkedТизме{}
	self.жараяндар.Init(self.mem)
	self.kernelБАРАКкаталогentry = kernelБАРАКкаталогentry
}

func (self *Процессиhelper) Create(entrypoint func(), threadhelper *TThreadhelper, БАРАКкаталогentry uint32, iskernel bool) Процесси {
	процесси := (*Процесси)(self.mem.Malloc(uint32(Sizeof(Процесси{}))))
	if процесси == nil {
		return Процесси{}
	}
	процесси.Init(self.mem)
	процесси.иДЕНТИФИКАТОР = Allocatepid()
	процесси.БАРАКкаталогentry = uintptr(БАРАКкаталогentry)
	негизгиthread := threadhelper.CreateКөрсөткүчfromfunction(entrypoint, БАРАКкаталогentry, iskernel)
	if негизгиthread != nil {
		негизгиthread.Pid = процесси.иДЕНТИФИКАТОР
		негизгиthread.Атаэнеpid = 0
		процесси.Threads.Append_to_list(uintptr(Pointer(негизгиthread)))
	}

	self.жараяндар.Append_to_list(uintptr(Pointer(процесси)))

	return *процесси
}

func (self *Процессиhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, БАРАКкаталогentry uint32, iskernel bool) Процесси {
	процесси := self.Create(entrypoint, threadhelper, БАРАКкаталогentry, iskernel)
	if процесси.Threads != nil && процесси.Threads.Өлчөм_2 > 0 {
		thread := (*TThread)(процесси.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Кошууthread(thread)
		}
	}
	return процесси
}

func (self *Процессиhelper) көчүрүүБАРАКкаталог(баштапкытекстentry uintptr, destinationentry uintptr) {
	баштапкытекст_2 := Getunsignedinteger32МассивfromКөрсөткүч(баштапкытекстentry, 1024, 1024)
	destination_2 := Getunsignedinteger32МассивfromКөрсөткүч(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = баштапкытекст_2[i]
	}
}
func (self *Процессиhelper) Createfromdata() Процесси {
	процесси := Процесси{}
	return процесси
}
