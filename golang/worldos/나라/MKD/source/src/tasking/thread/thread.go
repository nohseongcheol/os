/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "меморијаmanager"
import . "виртуелноМеморија"

const (
	Blocked		= 1
	Подготвено	= 2
	Стопирано	= 3
	Работи		= 4
)

const ThreadstackГолемина = 32 * 1024

type TThread struct {
	Cpustate		*Tcpustate
	Stack			uint32
	Корисникstack_2		uint32
	КорисникstackГолемина_2	uint32
	Pid			uint32
	Parentpid		uint32

	СтраницаДиректориумentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	времеdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (само *TThread) Нов() {
}

type TThreadhelper struct {
	mem *mem.TМеморијаmanager
}

var console_2 = TConsole{}

func (само *TThreadhelper) Init(mem *mem.TМеморијаmanager) {
	само.mem = mem
	console_2.MПечатиxy(([]byte)("thread:"), 1, 14)
}
func (само *TThreadhelper) CreatefromФункција(entrypoint_2 func(), СтраницаДиректориумentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(само.mem.Malloc(ThreadstackГолемина)))
	if result.Stack == 0 {
		return result
	}
	console_2.MПечати(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Печати(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + ThreadstackГолемина - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + ThreadstackГолемина
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Корисникstack_2 = Корисникstack
	result.КорисникstackГолемина_2 = КорисникstackГолемина
	result.Pid = 0
	result.Parentpid = 0
	result.СтраницаДиректориумentry = СтраницаДиректориумentry
	console_2.MПечати((([]byte)("cpu")))

	console_2.MUnsignedinteger32Печати(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.MПечати((([]byte)(":")))
	console_2.MUnsignedinteger32Печати(result.Cpustate.Eip)

	console_2.MПечати("]")
	if iskernel == true {
		result.Cpustate.Cs = Segkernelcode
		result.Cpustate.Ds = Segkerneldata
		result.Cpustate.Es = Segkerneldata
		result.Cpustate.Fs = Segkerneldata
		result.Cpustate.Gs = Segkernelgs
		result.Cpustate.Ss = Segkerneldata
		result.Threadstate = Подготвено
		result.Cpustate.Eflags = 0x202
	} else {
		result.Cpustate.Cs = SegКорисникcode
		result.Cpustate.Ds = SegКорисникdata
		result.Cpustate.Es = SegКорисникdata
		result.Cpustate.Fs = SegКорисникdata
		result.Cpustate.Gs = SegКорисникgs
		result.Cpustate.Ss = SegКорисникdata
		result.Threadstate = Работи
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (само *TThreadhelper) CreateСтрелкаfromФункција(entrypoint_2 func(), СтраницаДиректориумentry uint32, iskernel bool) *TThread {
	result := (*TThread)(само.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = само.CreatefromФункција(entrypoint_2, СтраницаДиректориумentry, iskernel)
	if result.Cpustate == nil {
		само.mem.Слободни(Pointer(result))
		return nil
	}
	return result
}
