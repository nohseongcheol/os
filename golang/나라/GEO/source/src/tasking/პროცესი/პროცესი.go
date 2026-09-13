package პროცესი

import . "unsafe"
import . "util/სია"
import mem "მეხსიერებაmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const Procმომხმარებელიheapზომა = 1 * 1024 * 1024

type Pპროცესი struct {
	id			uint32
	syscallid		int
	Isმომხმარებელიspace	bool
	arguments		*[]byte

	Threadსია	Linkedსია
	Threads		*Linkedსია
	Fფაილისახელი	[]byte

	Pგვერდიდასტაentry	uintptr
}

func (self *Pპროცესი) Init(mem *mem.Tმეხსიერებაmanager) {
	self.Threadსია = Linkedსია{}
	self.Threads = &self.Threadსია
	self.Threads.Init(mem)
}

type Pპროცესიhelper struct {
	პროცესები		Linkedსია
	mem			*mem.Tმეხსიერებაmanager
	kernelგვერდიდასტაentry	uintptr
}

func (self *Pპროცესიhelper) Init(mem *mem.Tმეხსიერებაmanager, kernelგვერდიდასტაentry uintptr) {
	self.mem = mem
	self.პროცესები = Linkedსია{}
	self.პროცესები.Init(self.mem)
	self.kernelგვერდიდასტაentry = kernelგვერდიდასტაentry
}

func (self *Pპროცესიhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Pგვერდიდასტაentry uint32, iskernel bool) Pპროცესი {
	პროცესი := (*Pპროცესი)(self.mem.Malloc(uint32(Sizeof(Pპროცესი{}))))
	if პროცესი == nil {
		return Pპროცესი{}
	}
	პროცესი.Init(self.mem)
	პროცესი.id = Allocatepid()
	პროცესი.Pგვერდიდასტაentry = uintptr(Pგვერდიდასტაentry)
	მთავარიthread := threadhelper.Createკურსორიfromფუნქცია(entrypoint, Pგვერდიდასტაentry, iskernel)
	if მთავარიthread != nil {
		მთავარიthread.Pid = პროცესი.id
		მთავარიthread.Parentpid = 0
		პროცესი.Threads.Append_to_list(uintptr(Pointer(მთავარიthread)))
	}

	self.პროცესები.Append_to_list(uintptr(Pointer(პროცესი)))

	return *პროცესი
}

func (self *Pპროცესიhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Pგვერდიდასტაentry uint32, iskernel bool) Pპროცესი {
	პროცესი := self.Create(entrypoint, threadhelper, Pგვერდიდასტაentry, iskernel)
	if პროცესი.Threads != nil && პროცესი.Threads.Sზომა_2 > 0 {
		thread := (*TThread)(პროცესი.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Aდამატებაthread(thread)
		}
	}
	return პროცესი
}

func (self *Pპროცესიhelper) დააკოპირეგვერდიდასტა(წყაროentry uintptr, destinationentry uintptr) {
	წყარო_2 := Getunsignedinteger32მასივიfromკურსორი(წყაროentry, 1024, 1024)
	destination_2 := Getunsignedinteger32მასივიfromკურსორი(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = წყარო_2[i]
	}
}
func (self *Pპროცესიhelper) Createfromdata() Pპროცესი {
	პროცესი := Pპროცესი{}
	return პროცესი
}
