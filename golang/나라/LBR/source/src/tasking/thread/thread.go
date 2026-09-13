package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "memorymanager"
import . "virtualmemory"

const (
	Blocked	= 1
	Ready	= 2
	Stopped	= 3
	Started	= 4
)

const Threadstacksize = 32 * 1024

type TThread struct {
	Cpustate	*Tcpustate
	Stack		uint32
	Userstack_2	uint32
	Userstacksize_2	uint32
	Pid		uint32
	Parentpid	uint32

	Pagedirectoryentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	timedelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) New() {
}

type TThreadhelper struct {
	mem *mem.TMemorymanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TMemorymanager) {
	self.mem = mem
	console_2.MPrintxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), Pagedirectoryentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Allocate_memory(Threadstacksize)))
	if result.Stack == 0 {
		return result
	}
	console_2.MPrint(([]byte)("[mem:"))
	console_2.MUnsignedinteger32print(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + Threadstacksize - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + Threadstacksize
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Userstack_2 = Userstack
	result.Userstacksize_2 = Userstacksize
	result.Pid = 0
	result.Parentpid = 0
	result.Pagedirectoryentry = Pagedirectoryentry
	console_2.MPrint((([]byte)("cpu")))

	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.MPrint((([]byte)(":")))
	console_2.MUnsignedinteger32print(result.Cpustate.Eip)

	console_2.MPrint("]")
	if iskernel == true {
		result.Cpustate.Cs = Segkernelcode
		result.Cpustate.Ds = Segkerneldata
		result.Cpustate.Es = Segkerneldata
		result.Cpustate.Fs = Segkerneldata
		result.Cpustate.Gs = Segkernelgs
		result.Cpustate.Ss = Segkerneldata
		result.Threadstate = Ready
		result.Cpustate.Eflags = 0x202
	} else {
		result.Cpustate.Cs = Segusercode
		result.Cpustate.Ds = Seguserdata
		result.Cpustate.Es = Seguserdata
		result.Cpustate.Fs = Seguserdata
		result.Cpustate.Gs = Segusergs
		result.Cpustate.Ss = Seguserdata
		result.Threadstate = Started
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createpointerfromfunction(entrypoint_2 func(), Pagedirectoryentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Allocate_memory(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, Pagedirectoryentry, iskernel)
	if result.Cpustate == nil {
		self.mem.Free(Pointer(result))
		return nil
	}
	return result
}
