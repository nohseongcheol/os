package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "xotiramanager"
import . "virtualXotira"

const (
	Blocked	= 1
	Tayyor	= 2
	Stopped	= 3
	Started	= 4
)

const ThreadstackHajmi = 32 * 1024

type TThread struct {
	Cpustate			*Tcpustate
	Stack				uint32
	Foydalanuvchistack_2		uint32
	FoydalanuvchistackHajmi_2	uint32
	Pid				uint32
	Parentpid			uint32

	SAHIFAJildentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	vaqtdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Yangi() {
}

type TThreadhelper struct {
	mem *mem.TXotiramanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TXotiramanager) {
	self.mem = mem
	console_2.MChopetishxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), SAHIFAJildentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackHajmi)))
	if result.Stack == 0 {
		return result
	}
	console_2.MChopetish(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Chopetish(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + ThreadstackHajmi - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + ThreadstackHajmi
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Foydalanuvchistack_2 = Foydalanuvchistack
	result.FoydalanuvchistackHajmi_2 = FoydalanuvchistackHajmi
	result.Pid = 0
	result.Parentpid = 0
	result.SAHIFAJildentry = SAHIFAJildentry
	console_2.MChopetish((([]byte)("cpu")))

	console_2.MUnsignedinteger32Chopetish(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.MChopetish((([]byte)(":")))
	console_2.MUnsignedinteger32Chopetish(result.Cpustate.Eip)

	console_2.MChopetish("]")
	if iskernel == true {
		result.Cpustate.Cs = Segkernelcode
		result.Cpustate.Ds = Segkerneldata
		result.Cpustate.Es = Segkerneldata
		result.Cpustate.Fs = Segkerneldata
		result.Cpustate.Gs = Segkernelgs
		result.Cpustate.Ss = Segkerneldata
		result.Threadstate = Tayyor
		result.Cpustate.Eflags = 0x202
	} else {
		result.Cpustate.Cs = SegFoydalanuvchicode
		result.Cpustate.Ds = SegFoydalanuvchidata
		result.Cpustate.Es = SegFoydalanuvchidata
		result.Cpustate.Fs = SegFoydalanuvchidata
		result.Cpustate.Gs = SegFoydalanuvchigs
		result.Cpustate.Ss = SegFoydalanuvchidata
		result.Threadstate = Started
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) CreateKorsatgichfromfunction(entrypoint_2 func(), SAHIFAJildentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, SAHIFAJildentry, iskernel)
	if result.Cpustate == nil {
		self.mem.Bosh(Pointer(result))
		return nil
	}
	return result
}
