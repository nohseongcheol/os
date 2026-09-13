package jarayon

import . "unsafe"
import . "util/royxat"
import mem "xotiramanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcFoydalanuvchiheapHajmi = 1 * 1024 * 1024

type Jarayon struct {
	id			uint32
	syscallid		int
	IsFoydalanuvchiBoʻshjoy	bool
	arguments		*[]byte

	Threadroyxat	Linkedroyxat
	Threads		*Linkedroyxat
	FaylNomi	[]byte

	SAHIFAJildentry	uintptr
}

func (self *Jarayon) Init(mem *mem.TXotiramanager) {
	self.Threadroyxat = Linkedroyxat{}
	self.Threads = &self.Threadroyxat
	self.Threads.Init(mem)
}

type Jarayonhelper struct {
	jarayonlar		Linkedroyxat
	mem			*mem.TXotiramanager
	kernelSAHIFAJildentry	uintptr
}

func (self *Jarayonhelper) Init(mem *mem.TXotiramanager, kernelSAHIFAJildentry uintptr) {
	self.mem = mem
	self.jarayonlar = Linkedroyxat{}
	self.jarayonlar.Init(self.mem)
	self.kernelSAHIFAJildentry = kernelSAHIFAJildentry
}

func (self *Jarayonhelper) Create(entrypoint func(), threadhelper *TThreadhelper, SAHIFAJildentry uint32, iskernel bool) Jarayon {
	jarayon := (*Jarayon)(self.mem.Malloc(uint32(Sizeof(Jarayon{}))))
	if jarayon == nil {
		return Jarayon{}
	}
	jarayon.Init(self.mem)
	jarayon.id = Allocatepid()
	jarayon.SAHIFAJildentry = uintptr(SAHIFAJildentry)
	asosiythread := threadhelper.CreateKorsatgichfromfunction(entrypoint, SAHIFAJildentry, iskernel)
	if asosiythread != nil {
		asosiythread.Pid = jarayon.id
		asosiythread.Parentpid = 0
		jarayon.Threads.Append_to_list(uintptr(Pointer(asosiythread)))
	}

	self.jarayonlar.Append_to_list(uintptr(Pointer(jarayon)))

	return *jarayon
}

func (self *Jarayonhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, SAHIFAJildentry uint32, iskernel bool) Jarayon {
	jarayon := self.Create(entrypoint, threadhelper, SAHIFAJildentry, iskernel)
	if jarayon.Threads != nil && jarayon.Threads.Hajmi_2 > 0 {
		thread := (*TThread)(jarayon.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Qoʻshishthread(thread)
		}
	}
	return jarayon
}

func (self *Jarayonhelper) nusxaolishSAHIFAJild(sourceentry uintptr, destinationentry uintptr) {
	source_2 := Getunsignedinteger32arrayfromKorsatgich(sourceentry, 1024, 1024)
	destination_2 := Getunsignedinteger32arrayfromKorsatgich(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = source_2[i]
	}
}
func (self *Jarayonhelper) Createfromdata() Jarayon {
	jarayon := Jarayon{}
	return jarayon
}
