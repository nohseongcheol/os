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

const Threadstackขนาด = 32 * 1024

type TThread struct {
	Cpuสถานะ	*Tcpuสถานะ
	Stack		uint32
	Userstack_2	uint32
	Userstackขนาด_2	uint32
	Pid		uint32
	Parentpid	uint32

	Pagedirectoryentry	uint32

	Threadสถานะ	uint8
	Blockedสถานะ	uint8

	เวลาเดลตา	uint32

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

	result.Stack = uint32(uintptr(self.mem.Malloc(Threadstackขนาด)))
	if result.Stack == 0 {
		return result
	}
	console_2.MPrint(([]byte)("[mem:"))
	console_2.MUnsignedinteger32print(result.Stack)

	result.Cpuสถานะ = (*Tcpuสถานะ)(Pointer(uintptr(result.Stack) + Threadstackขนาด - Sizeof(Tcpuสถานะ{})))
	result.Cpuสถานะ.Esp = result.Stack + Threadstackขนาด
	result.Cpuสถานะ.Ebp = result.Cpuสถานะ.Esp
	result.Cpuสถานะ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Userstack_2 = Userstack
	result.Userstackขนาด_2 = Userstackขนาด
	result.Pid = 0
	result.Parentpid = 0
	result.Pagedirectoryentry = Pagedirectoryentry
	console_2.MPrint((([]byte)("cpu")))

	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(result.Cpuสถานะ))))

	console_2.MPrint((([]byte)(":")))
	console_2.MUnsignedinteger32print(result.Cpuสถานะ.Eip)

	console_2.MPrint("]")
	if iskernel == true {
		result.Cpuสถานะ.Cs = Segkernelcode
		result.Cpuสถานะ.Ds = Segkerneldata
		result.Cpuสถานะ.Es = Segkerneldata
		result.Cpuสถานะ.Fs = Segkerneldata
		result.Cpuสถานะ.Gs = Segkernelgs
		result.Cpuสถานะ.Ss = Segkerneldata
		result.Threadสถานะ = Ready
		result.Cpuสถานะ.Eflags = 0x202
	} else {
		result.Cpuสถานะ.Cs = Segusercode
		result.Cpuสถานะ.Ds = Seguserdata
		result.Cpuสถานะ.Es = Seguserdata
		result.Cpuสถานะ.Fs = Seguserdata
		result.Cpuสถานะ.Gs = Segusergs
		result.Cpuสถานะ.Ss = Seguserdata
		result.Threadสถานะ = Started
		result.Cpuสถานะ.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createpointerfromfunction(entrypoint_2 func(), Pagedirectoryentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, Pagedirectoryentry, iskernel)
	if result.Cpuสถานะ == nil {
		self.mem.Free(Pointer(result))
		return nil
	}
	return result
}
