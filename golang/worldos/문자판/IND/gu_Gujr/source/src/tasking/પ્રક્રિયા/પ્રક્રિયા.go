/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package process

import . "unsafe"
import . "util/list"
import mem "સ્મૃતિ"
import . "tasking/અમલપ્રવાહ"
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

func (self *Process) Vઆરંભ_કરવો(mem *mem.TMemoryManager) {
	self.ThreadList = LinkedList{}
	self.Threads = &self.ThreadList
	self.Threads.Vઆરંભ_કરવો(mem)
}

type ProcessHelper struct {
	processes			LinkedList
	mem				*mem.TMemoryManager
	kernelPageDirEntry	uintptr
}

func (self *ProcessHelper) Vઆરંભ_કરવો(mem *mem.TMemoryManager, kernelPageDirEntry uintptr) {
	self.mem = mem
	self.processes = LinkedList{}
	self.processes.Vઆરંભ_કરવો(self.mem)
	self.kernelPageDirEntry = kernelPageDirEntry
}

func (self *ProcessHelper) Create(entryPoint func(), threadHelper *TThreadHelper, PageDirEntry uint32, isKernel bool) Process {
	process := (*Process)(self.mem.Vસ્મૃતિ_ફાળવવી(uint32(Sizeof(Process{}))))
	if process == nil {
		return Process{}
	}
	process.Vઆરંભ_કરવો(self.mem)
	process.id = AllocatePID()
	process.PageDirEntry = uintptr(PageDirEntry)
	mainThread := threadHelper.CreatePtrFromFunction(entryPoint, PageDirEntry, isKernel)
	if mainThread != nil {
		mainThread.Pid = process.id
		mainThread.ParentPid = 0
		process.Threads.Vસૂચિના_અંતે_ઉમેરવું(uintptr(Pointer(mainThread)))
	}

	self.processes.Vસૂચિના_અંતે_ઉમેરવું(uintptr(Pointer(process)))

	return *process
}

func (self *ProcessHelper) Spawn(entryPoint func(), threadHelper *TThreadHelper, scheduler *Scheduler, PageDirEntry uint32, isKernel bool) Process {
	process := self.Create(entryPoint, threadHelper, PageDirEntry, isKernel)
	if process.Threads != nil && process.Threads.Vકદ > 0 {
		thread := (*Tઅમલપ્રવાહ)(process.Threads.GetAt(0))
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
