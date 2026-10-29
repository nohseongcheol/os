/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "консол"
import . "multitasking"
import mem "санахойЗохицуулагч"
import . "virtualСанахой"

const (
	Blocked	= 1
	Ready	= 2
	Зогсоох	= 3
	Started	= 4
)

const ThreadstackХэмжээ = 32 * 1024

type TThread struct {
	Cpustate		*Tcpustate
	Stack			uint32
	Хэрэглэгчstack_2	uint32
	ХэрэглэгчstackХэмжээ_2	uint32
	Pid			uint32
	Parentpid		uint32

	ХУУДАСЛавлахentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	цагdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Шинэ() {
}

type TThreadhelper struct {
	mem *mem.TСанахойЗохицуулагч
}

var консол_2 = TКонсол{}

func (self *TThreadhelper) Init(mem *mem.TСанахойЗохицуулагч) {
	self.mem = mem
	консол_2.MХэвлэхxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), ХУУДАСЛавлахentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackХэмжээ)))
	if result.Stack == 0 {
		return result
	}
	консол_2.MХэвлэх(([]byte)("[mem:"))
	консол_2.MUnsignedinteger32Хэвлэх(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + ThreadstackХэмжээ - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + ThreadstackХэмжээ
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Хэрэглэгчstack_2 = Хэрэглэгчstack
	result.ХэрэглэгчstackХэмжээ_2 = ХэрэглэгчstackХэмжээ
	result.Pid = 0
	result.Parentpid = 0
	result.ХУУДАСЛавлахentry = ХУУДАСЛавлахentry
	консол_2.MХэвлэх((([]byte)("cpu")))

	консол_2.MUnsignedinteger32Хэвлэх(uint32(uintptr(Pointer(result.Cpustate))))

	консол_2.MХэвлэх((([]byte)(":")))
	консол_2.MUnsignedinteger32Хэвлэх(result.Cpustate.Eip)

	консол_2.MХэвлэх("]")
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
		result.Cpustate.Cs = SegХэрэглэгчcode
		result.Cpustate.Ds = SegХэрэглэгчdata
		result.Cpustate.Es = SegХэрэглэгчdata
		result.Cpustate.Fs = SegХэрэглэгчdata
		result.Cpustate.Gs = SegХэрэглэгчgs
		result.Cpustate.Ss = SegХэрэглэгчdata
		result.Threadstate = Started
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createpointerfromfunction(entrypoint_2 func(), ХУУДАСЛавлахentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, ХУУДАСЛавлахentry, iskernel)
	if result.Cpustate == nil {
		self.mem.Чөлөөт(Pointer(result))
		return nil
	}
	return result
}
