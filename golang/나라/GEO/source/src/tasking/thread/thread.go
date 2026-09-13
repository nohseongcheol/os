package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "მეხსიერებაmanager"
import . "virtualმეხსიერება"

const (
	Blocked		= 1
	Ready		= 2
	Sგაჩერებულია	= 3
	Sგაშვებული	= 4
)

const Threadstackზომა = 32 * 1024

type TThread struct {
	Cpustate			*Tcpustate
	Stack				uint32
	Uმომხმარებელიstack_2		uint32
	Uმომხმარებელიstackზომა_2	uint32
	Pid				uint32
	Parentpid			uint32

	Pგვერდიდასტაentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	დროdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Nახალი() {
}

type TThreadhelper struct {
	mem *mem.Tმეხსიერებაmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.Tმეხსიერებაmanager) {
	self.mem = mem
	console_2.Mბეჭდვაxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromფუნქცია(entrypoint_2 func(), Pგვერდიდასტაentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(Threadstackზომა)))
	if result.Stack == 0 {
		return result
	}
	console_2.Mბეჭდვა(([]byte)("[mem:"))
	console_2.MUnsignedinteger32ბეჭდვა(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + Threadstackზომა - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + Threadstackზომა
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Uმომხმარებელიstack_2 = Uმომხმარებელიstack
	result.Uმომხმარებელიstackზომა_2 = Uმომხმარებელიstackზომა
	result.Pid = 0
	result.Parentpid = 0
	result.Pგვერდიდასტაentry = Pგვერდიდასტაentry
	console_2.Mბეჭდვა((([]byte)("cpu")))

	console_2.MUnsignedinteger32ბეჭდვა(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.Mბეჭდვა((([]byte)(":")))
	console_2.MUnsignedinteger32ბეჭდვა(result.Cpustate.Eip)

	console_2.Mბეჭდვა("]")
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
		result.Cpustate.Cs = Segმომხმარებელიcode
		result.Cpustate.Ds = Segმომხმარებელიdata
		result.Cpustate.Es = Segმომხმარებელიdata
		result.Cpustate.Fs = Segმომხმარებელიdata
		result.Cpustate.Gs = Segმომხმარებელიgs
		result.Cpustate.Ss = Segმომხმარებელიdata
		result.Threadstate = Sგაშვებული
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createკურსორიfromფუნქცია(entrypoint_2 func(), Pგვერდიდასტაentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromფუნქცია(entrypoint_2, Pგვერდიდასტაentry, iskernel)
	if result.Cpustate == nil {
		self.mem.Fთავისუფალი(Pointer(result))
		return nil
	}
	return result
}
