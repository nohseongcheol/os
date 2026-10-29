/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "memoriemanager"
import . "virtualăMemorie"

const (
	Blocked		= 1
	Pregătit	= 2
	Oprit		= 3
	Pornit		= 4
)

const ThreadstackMărime = 32 * 1024

type TThread struct {
	CpuStare		*TcpuStare
	Stack			uint32
	Utilizatorstack_2	uint32
	UtilizatorstackMărime_2	uint32
	Pid			uint32
	Părintepid		uint32

	PAGINĂDirectorînregistrare	uint32

	ThreadStare	uint8
	BlockedStare	uint8

	orădelta	uint32

	Tlssegments	[Gdtînregistrare]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (sine *TThread) Nou() {
}

type TThreadhelper struct {
	mem *mem.TMemoriemanager
}

var console_2 = TConsole{}

func (sine *TThreadhelper) Init(mem *mem.TMemoriemanager) {
	sine.mem = mem
	console_2.MTipăreștexy(([]byte)("thread:"), 1, 14)
}
func (sine *TThreadhelper) CreatefromFuncție(înregistrarepoint_2 func(), PAGINĂDirectorînregistrare uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(sine.mem.Malloc(ThreadstackMărime)))
	if result.Stack == 0 {
		return result
	}
	console_2.MTipărește(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Tipărește(result.Stack)

	result.CpuStare = (*TcpuStare)(Pointer(uintptr(result.Stack) + ThreadstackMărime - Sizeof(TcpuStare{})))
	result.CpuStare.Esp = result.Stack + ThreadstackMărime
	result.CpuStare.Ebp = result.CpuStare.Esp
	result.CpuStare.Eip = uint32(ValueOf(înregistrarepoint_2).Pointer())
	result.Utilizatorstack_2 = Utilizatorstack
	result.UtilizatorstackMărime_2 = UtilizatorstackMărime
	result.Pid = 0
	result.Părintepid = 0
	result.PAGINĂDirectorînregistrare = PAGINĂDirectorînregistrare
	console_2.MTipărește((([]byte)("cpu")))

	console_2.MUnsignedinteger32Tipărește(uint32(uintptr(Pointer(result.CpuStare))))

	console_2.MTipărește((([]byte)(":")))
	console_2.MUnsignedinteger32Tipărește(result.CpuStare.Eip)

	console_2.MTipărește("]")
	if iskernel == true {
		result.CpuStare.Cs = Segkernelcode
		result.CpuStare.Ds = Segkerneldata
		result.CpuStare.Es = Segkerneldata
		result.CpuStare.Fs = Segkerneldata
		result.CpuStare.Gs = Segkernelgs
		result.CpuStare.Ss = Segkerneldata
		result.ThreadStare = Pregătit
		result.CpuStare.Eflags = 0x202
	} else {
		result.CpuStare.Cs = SegUtilizatorcode
		result.CpuStare.Ds = SegUtilizatordata
		result.CpuStare.Es = SegUtilizatordata
		result.CpuStare.Fs = SegUtilizatordata
		result.CpuStare.Gs = SegUtilizatorgs
		result.CpuStare.Ss = SegUtilizatordata
		result.ThreadStare = Pornit
		result.CpuStare.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (sine *TThreadhelper) CreateIndicatorfromFuncție(înregistrarepoint_2 func(), PAGINĂDirectorînregistrare uint32, iskernel bool) *TThread {
	result := (*TThread)(sine.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = sine.CreatefromFuncție(înregistrarepoint_2, PAGINĂDirectorînregistrare, iskernel)
	if result.CpuStare == nil {
		sine.mem.Liber(Pointer(result))
		return nil
	}
	return result
}
