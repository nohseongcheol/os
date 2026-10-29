/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package process

import . "unsafe"
import . "util/list"
import mem "ਯਾਦਾਸ਼ਤ"
import . "tasking/ਕਾਰਜਧਾਰਾ"
import . "tasking/scheduler"
import . "util"

const PROC_USER_HEAP_SIZE = 1 * 1024 * 1024

type Process struct {
	id		uint32
	syscallID	int
	IsUserSpace	bool
	args	*[]byte

	ThreadList	LinkedList
	Threads		*LinkedList
	FileName	[]byte

	PageDirEntry	uintptr
}

func (self *Process) Vਆਰੰਭ_ਕਰਨਾ(mem *mem.TMemoryManager) {
	self.ThreadList = LinkedList{}
	self.Threads = &self.ThreadList
	self.Threads.Vਆਰੰਭ_ਕਰਨਾ(mem)
}

type ProcessHelper struct {
	processes			LinkedList
	mem				*mem.TMemoryManager
	kernelPageDirEntry	uintptr
}

func (self *ProcessHelper) Vਆਰੰਭ_ਕਰਨਾ(mem *mem.TMemoryManager, kernelPageDirEntry uintptr) {
	self.mem = mem
	self.processes = LinkedList{}
	self.processes.Vਆਰੰਭ_ਕਰਨਾ(self.mem)
	self.kernelPageDirEntry = kernelPageDirEntry
}

func (self *ProcessHelper) Create(entryPoint func(), threadHelper *TThreadHelper, PageDirEntry uint32, isKernel bool) Process {
	process := (*Process)(self.mem.Malloc(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Vਆਰੰਭ_ਕਰਨਾ(self.mem)
	process.id = AllocatePID()
	process.PageDirEntry = uintptr(PageDirEntry)
	mainThread := threadHelper.CreatePtrFromFunction(entryPoint, PageDirEntry, isKernel)
	if mainThread != nil {
		mainThread.Pid = process.id
		mainThread.ParentPid = 0
		process.Threads.PushBack(uintptr(Pointer(mainThread)))
	}

	self.processes.PushBack(uintptr(Pointer(process)))

	return *process
}

func (self *ProcessHelper) Spawn(entryPoint func(), threadHelper *TThreadHelper, scheduler *Scheduler, PageDirEntry uint32, isKernel bool) Process {
	process := self.Create(entryPoint, threadHelper, PageDirEntry, isKernel)
	if process.Threads != nil && process.Threads.Vਆਕਾਰ > 0 {
		thread := (*Tਕਾਰਜਧਾਰਾ)(process.Threads.GetAt(0))
		if thread != nil && scheduler != nil {
			scheduler.AddThread(thread)
		}
	}
	return process
}

func (self *ProcessHelper) copyPageDir(srcEntry uintptr, dstEntry uintptr) {
	src := GetUint32ArrayFromPtr(srcEntry, 1024, 1024)
	dst := GetUint32ArrayFromPtr(dstEntry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		dst[i] = src[i]
	}
}
func (self *ProcessHelper) CreateFromData() Process {
	process := Process{}
	return process
}
