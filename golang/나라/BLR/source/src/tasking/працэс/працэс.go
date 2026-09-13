package працэс

import . "unsafe"
import . "util/спіс"
import mem "памяцьmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcКарыстальнікheapПамер = 1 * 1024 * 1024

type Працэс struct {
	іДЭНТЫФІКАТАР		uint32
	syscallІДЭНТЫФІКАТАР	int
	IsКарыстальнікПрагал	bool
	arguments		*[]byte

	ThreadСпіс	LinkedСпіс
	Threads		*LinkedСпіс
	ФайлНазва	[]byte

	СтаронкаКаталогentry	uintptr
}

func (self *Працэс) Init(mem *mem.TПамяцьmanager) {
	self.ThreadСпіс = LinkedСпіс{}
	self.Threads = &self.ThreadСпіс
	self.Threads.Init(mem)
}

type Працэсhelper struct {
	працэсы				LinkedСпіс
	mem				*mem.TПамяцьmanager
	kernelСтаронкаКаталогentry	uintptr
}

func (self *Працэсhelper) Init(mem *mem.TПамяцьmanager, kernelСтаронкаКаталогentry uintptr) {
	self.mem = mem
	self.працэсы = LinkedСпіс{}
	self.працэсы.Init(self.mem)
	self.kernelСтаронкаКаталогentry = kernelСтаронкаКаталогentry
}

func (self *Працэсhelper) Create(entrypoint func(), threadhelper *TThreadhelper, СтаронкаКаталогentry uint32, iskernel bool) Працэс {
	працэс := (*Працэс)(self.mem.Malloc(uint32(Sizeof(Працэс{}))))
	if працэс == nil {
		return Працэс{}
	}
	працэс.Init(self.mem)
	працэс.іДЭНТЫФІКАТАР = Allocatepid()
	працэс.СтаронкаКаталогentry = uintptr(СтаронкаКаталогentry)
	галоўныthread := threadhelper.CreateПаказальнікfromФункцыя(entrypoint, СтаронкаКаталогentry, iskernel)
	if галоўныthread != nil {
		галоўныthread.Pid = працэс.іДЭНТЫФІКАТАР
		галоўныthread.Parentpid = 0
		працэс.Threads.Append_to_list(uintptr(Pointer(галоўныthread)))
	}

	self.працэсы.Append_to_list(uintptr(Pointer(працэс)))

	return *працэс
}

func (self *Працэсhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, СтаронкаКаталогentry uint32, iskernel bool) Працэс {
	працэс := self.Create(entrypoint, threadhelper, СтаронкаКаталогentry, iskernel)
	if працэс.Threads != nil && працэс.Threads.Памер_2 > 0 {
		thread := (*TThread)(працэс.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Дадацьthread(thread)
		}
	}
	return працэс
}

func (self *Працэсhelper) скапіявацьСтаронкаКаталог(крыніцаentry uintptr, destinationentry uintptr) {
	крыніца_2 := Getunsignedinteger32МасіўfromПаказальнік(крыніцаentry, 1024, 1024)
	destination_2 := Getunsignedinteger32МасіўfromПаказальнік(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = крыніца_2[i]
	}
}
func (self *Працэсhelper) Createfromdata() Працэс {
	працэс := Працэс{}
	return працэс
}
