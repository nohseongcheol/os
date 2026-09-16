/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konzola"
import . "multitasking"
import mem "pamäťmanager"
import . "virtuálnyPamäť"

const (
	Blocked		= 1
	Pripravený	= 2
	Zastavený	= 3
	Začaté		= 4
)

const ThreadstackVeľkosť = 32 * 1024

type TThread struct {
	ProcesorStav			*TcpuStav
	Stack				uint32
	Používateľstack_2		uint32
	PoužívateľstackVeľkosť_2	uint32
	Pid				uint32
	Rodičpid			uint32

	STRANAAdresárpoložka	uint32

	ThreadStav	uint8
	BlockedStav	uint8

	časdelta	uint32

	TlsSegmenty	[Gdtpoložka]TSegmentdescriptor
	FpuPosunutie	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (vlastný *TThread) Nový() {
}

type TThreadhelper struct {
	mem *mem.TPamäťmanager
}

var konzola_2 = TKonzola{}

func (vlastný *TThreadhelper) Init(mem *mem.TPamäťmanager) {
	vlastný.mem = mem
	konzola_2.MTlačiťxy(([]byte)("thread:"), 1, 14)
}
func (vlastný *TThreadhelper) CreatezFunkcia(položkapoint_2 func(), STRANAAdresárpoložka uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(vlastný.mem.Malloc(ThreadstackVeľkosť)))
	if result.Stack == 0 {
		return result
	}
	konzola_2.MTlačiť(([]byte)("[mem:"))
	konzola_2.MUnsignedinteger32Tlačiť(result.Stack)

	result.ProcesorStav = (*TcpuStav)(Pointer(uintptr(result.Stack) + ThreadstackVeľkosť - Sizeof(TcpuStav{})))
	result.ProcesorStav.Esp = result.Stack + ThreadstackVeľkosť
	result.ProcesorStav.Ebp = result.ProcesorStav.Esp
	result.ProcesorStav.Eip = uint32(ValueOf(položkapoint_2).Pointer())
	result.Používateľstack_2 = Používateľstack
	result.PoužívateľstackVeľkosť_2 = PoužívateľstackVeľkosť
	result.Pid = 0
	result.Rodičpid = 0
	result.STRANAAdresárpoložka = STRANAAdresárpoložka
	konzola_2.MTlačiť((([]byte)("cpu")))

	konzola_2.MUnsignedinteger32Tlačiť(uint32(uintptr(Pointer(result.ProcesorStav))))

	konzola_2.MTlačiť((([]byte)(":")))
	konzola_2.MUnsignedinteger32Tlačiť(result.ProcesorStav.Eip)

	konzola_2.MTlačiť("]")
	if iskernel == true {
		result.ProcesorStav.Cs = Segkernelcode
		result.ProcesorStav.Ds = Segkerneldata
		result.ProcesorStav.Es = Segkerneldata
		result.ProcesorStav.Fs = Segkerneldata
		result.ProcesorStav.Gs = Segkernelgs
		result.ProcesorStav.Ss = Segkerneldata
		result.ThreadStav = Pripravený
		result.ProcesorStav.Eflags = 0x202
	} else {
		result.ProcesorStav.Cs = SegPoužívateľcode
		result.ProcesorStav.Ds = SegPoužívateľdata
		result.ProcesorStav.Es = SegPoužívateľdata
		result.ProcesorStav.Fs = SegPoužívateľdata
		result.ProcesorStav.Gs = SegPoužívateľgs
		result.ProcesorStav.Ss = SegPoužívateľdata
		result.ThreadStav = Začaté
		result.ProcesorStav.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.FpuPosunutie = 0xffffffff

	return result
}

func (vlastný *TThreadhelper) CreateKurzorzFunkcia(položkapoint_2 func(), STRANAAdresárpoložka uint32, iskernel bool) *TThread {
	result := (*TThread)(vlastný.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = vlastný.CreatezFunkcia(položkapoint_2, STRANAAdresárpoložka, iskernel)
	if result.ProcesorStav == nil {
		vlastný.mem.Voľné(Pointer(result))
		return nil
	}
	return result
}
