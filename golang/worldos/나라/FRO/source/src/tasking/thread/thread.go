/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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

const ThreadstackStødd = 32 * 1024

type TThread struct {
	CpuStøða		*TcpuStøða
	Stack			uint32
	Brúkaristack_2		uint32
	BrúkaristackStødd_2	uint32
	Pid			uint32
	Parentpid		uint32

	PageFíluskráentry	uint32

	ThreadStøða	uint8
	BlockedStøða	uint8

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
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), PageFíluskráentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackStødd)))
	if result.Stack == 0 {
		return result
	}
	console_2.MPrint(([]byte)("[mem:"))
	console_2.MUnsignedinteger32print(result.Stack)

	result.CpuStøða = (*TcpuStøða)(Pointer(uintptr(result.Stack) + ThreadstackStødd - Sizeof(TcpuStøða{})))
	result.CpuStøða.Esp = result.Stack + ThreadstackStødd
	result.CpuStøða.Ebp = result.CpuStøða.Esp
	result.CpuStøða.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Brúkaristack_2 = Brúkaristack
	result.BrúkaristackStødd_2 = BrúkaristackStødd
	result.Pid = 0
	result.Parentpid = 0
	result.PageFíluskráentry = PageFíluskráentry
	console_2.MPrint((([]byte)("cpu")))

	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(result.CpuStøða))))

	console_2.MPrint((([]byte)(":")))
	console_2.MUnsignedinteger32print(result.CpuStøða.Eip)

	console_2.MPrint("]")
	if iskernel == true {
		result.CpuStøða.Cs = Segkernelcode
		result.CpuStøða.Ds = Segkerneldata
		result.CpuStøða.Es = Segkerneldata
		result.CpuStøða.Fs = Segkerneldata
		result.CpuStøða.Gs = Segkernelgs
		result.CpuStøða.Ss = Segkerneldata
		result.ThreadStøða = Ready
		result.CpuStøða.Eflags = 0x202
	} else {
		result.CpuStøða.Cs = SegBrúkaricode
		result.CpuStøða.Ds = SegBrúkaridata
		result.CpuStøða.Es = SegBrúkaridata
		result.CpuStøða.Fs = SegBrúkaridata
		result.CpuStøða.Gs = SegBrúkarigs
		result.CpuStøða.Ss = SegBrúkaridata
		result.ThreadStøða = Started
		result.CpuStøða.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createpointerfromfunction(entrypoint_2 func(), PageFíluskráentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, PageFíluskráentry, iskernel)
	if result.CpuStøða == nil {
		self.mem.Free(Pointer(result))
		return nil
	}
	return result
}
