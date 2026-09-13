package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "yaddaşmanager"
import . "virtualYaddaş"

const (
	Blocked		= 1
	Ready		= 2
	Dayandırılıb	= 3
	Started		= 4
)

const ThreadstackBöyüklük = 32 * 1024

type TThread struct {
	Cpustate			*Tcpustate
	Stack				uint32
	İstifadəçistack_2		uint32
	İstifadəçistackBöyüklük_2	uint32
	Pid				uint32
	Parentpid			uint32

	SəhifəCərgəentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	zamandelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Yeni() {
}

type TThreadhelper struct {
	mem *mem.TYaddaşmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TYaddaşmanager) {
	self.mem = mem
	console_2.MÇapEtxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), SəhifəCərgəentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackBöyüklük)))
	if result.Stack == 0 {
		return result
	}
	console_2.MÇapEt(([]byte)("[mem:"))
	console_2.MUnsignedinteger32ÇapEt(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + ThreadstackBöyüklük - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + ThreadstackBöyüklük
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.İstifadəçistack_2 = İstifadəçistack
	result.İstifadəçistackBöyüklük_2 = İstifadəçistackBöyüklük
	result.Pid = 0
	result.Parentpid = 0
	result.SəhifəCərgəentry = SəhifəCərgəentry
	console_2.MÇapEt((([]byte)("cpu")))

	console_2.MUnsignedinteger32ÇapEt(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.MÇapEt((([]byte)(":")))
	console_2.MUnsignedinteger32ÇapEt(result.Cpustate.Eip)

	console_2.MÇapEt("]")
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
		result.Cpustate.Cs = Segİstifadəçicode
		result.Cpustate.Ds = Segİstifadəçidata
		result.Cpustate.Es = Segİstifadəçidata
		result.Cpustate.Fs = Segİstifadəçidata
		result.Cpustate.Gs = Segİstifadəçigs
		result.Cpustate.Ss = Segİstifadəçidata
		result.Threadstate = Started
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createpointerfromfunction(entrypoint_2 func(), SəhifəCərgəentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, SəhifəCərgəentry, iskernel)
	if result.Cpustate == nil {
		self.mem.Boş(Pointer(result))
		return nil
	}
	return result
}
