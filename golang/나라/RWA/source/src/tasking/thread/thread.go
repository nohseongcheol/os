package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "ububikomanager"
import . "virtualUbubiko"

const (
	Blocked		= 1
	Ready		= 2
	Kyahagariswe	= 3
	Started		= 4
)

const ThreadstackIngano = 32 * 1024

type TThread struct {
	Cpustate		*Tcpustate
	Stack			uint32
	Ukoreshastack_2		uint32
	UkoreshastackIngano_2	uint32
	Pid			uint32
	Parentpid		uint32

	IpajiUbubikoentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	igihedelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) New() {
}

type TThreadhelper struct {
	mem *mem.TUbubikomanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TUbubikomanager) {
	self.mem = mem
	console_2.MGucapaxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), IpajiUbubikoentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackIngano)))
	if result.Stack == 0 {
		return result
	}
	console_2.MGucapa(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Gucapa(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + ThreadstackIngano - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + ThreadstackIngano
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Ukoreshastack_2 = Ukoreshastack
	result.UkoreshastackIngano_2 = UkoreshastackIngano
	result.Pid = 0
	result.Parentpid = 0
	result.IpajiUbubikoentry = IpajiUbubikoentry
	console_2.MGucapa((([]byte)("cpu")))

	console_2.MUnsignedinteger32Gucapa(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.MGucapa((([]byte)(":")))
	console_2.MUnsignedinteger32Gucapa(result.Cpustate.Eip)

	console_2.MGucapa("]")
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
		result.Cpustate.Cs = SegUkoreshacode
		result.Cpustate.Ds = SegUkoreshadata
		result.Cpustate.Es = SegUkoreshadata
		result.Cpustate.Fs = SegUkoreshadata
		result.Cpustate.Gs = SegUkoreshags
		result.Cpustate.Ss = SegUkoreshadata
		result.Threadstate = Started
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createpointerfromfunction(entrypoint_2 func(), IpajiUbubikoentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, IpajiUbubikoentry, iskernel)
	if result.Cpustate == nil {
		self.mem.Kigenga(Pointer(result))
		return nil
	}
	return result
}
