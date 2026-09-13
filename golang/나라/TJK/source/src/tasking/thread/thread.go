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
	Cpustate			*Tcpustate
	Stack				uint32
	Истифодакунандаstack_2		uint32
	Истифодакунандаstacksize_2	uint32
	Pid				uint32
	Parentpid			uint32

	PageФеҳрастentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	timedelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Нав() {
}

type TThreadhelper struct {
	mem *mem.TMemorymanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TMemorymanager) {
	self.mem = mem
	console_2.MЧопкарданxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatefromФунксия(entrypoint_2 func(), PageФеҳрастentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(Threadstacksize)))
	if result.Stack == 0 {
		return result
	}
	console_2.MЧопкардан(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Чопкардан(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + Threadstacksize - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + Threadstacksize
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Истифодакунандаstack_2 = Истифодакунандаstack
	result.Истифодакунандаstacksize_2 = Истифодакунандаstacksize
	result.Pid = 0
	result.Parentpid = 0
	result.PageФеҳрастentry = PageФеҳрастentry
	console_2.MЧопкардан((([]byte)("cpu")))

	console_2.MUnsignedinteger32Чопкардан(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.MЧопкардан((([]byte)(":")))
	console_2.MUnsignedinteger32Чопкардан(result.Cpustate.Eip)

	console_2.MЧопкардан("]")
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
		result.Cpustate.Cs = SegИстифодакунандаcode
		result.Cpustate.Ds = SegИстифодакунандаdata
		result.Cpustate.Es = SegИстифодакунандаdata
		result.Cpustate.Fs = SegИстифодакунандаdata
		result.Cpustate.Gs = SegИстифодакунандаgs
		result.Cpustate.Ss = SegИстифодакунандаdata
		result.Threadstate = Started
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) CreatepointerfromФунксия(entrypoint_2 func(), PageФеҳрастentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.CreatefromФунксия(entrypoint_2, PageФеҳрастentry, iskernel)
	if result.Cpustate == nil {
		self.mem.Free(Pointer(result))
		return nil
	}
	return result
}
