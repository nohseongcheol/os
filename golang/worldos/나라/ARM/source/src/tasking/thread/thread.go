/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "հիշողությունmanager"
import . "virtualՀիշողություն"

const (
	Blocked		= 1
	Պատրաստ		= 2
	Կանգնեցված	= 3
	Սկսված		= 4
)

const ThreadstackՉափս = 32 * 1024

type TThread struct {
	ԿՄՀՎիճակ		*TcpuՎիճակ
	Stack			uint32
	Օգտագործողstack_2	uint32
	ՕգտագործողstackՉափս_2	uint32
	Pid			uint32
	Ծնողpid			uint32

	Էջֆայլապանակentry	uint32

	ThreadՎիճակ	uint8
	BlockedՎիճակ	uint8

	ժամանակdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (ինքնուրույն *TThread) Նոր() {
}

type TThreadhelper struct {
	mem *mem.TՀիշողությունmanager
}

var console_2 = TConsole{}

func (ինքնուրույն *TThreadhelper) Init(mem *mem.TՀիշողությունmanager) {
	ինքնուրույն.mem = mem
	console_2.MՏպելxy(([]byte)("thread:"), 1, 14)
}
func (ինքնուրույն *TThreadhelper) Createիցfunction(entrypoint_2 func(), Էջֆայլապանակentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(ինքնուրույն.mem.Malloc(ThreadstackՉափս)))
	if result.Stack == 0 {
		return result
	}
	console_2.MՏպել(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Տպել(result.Stack)

	result.ԿՄՀՎիճակ = (*TcpuՎիճակ)(Pointer(uintptr(result.Stack) + ThreadstackՉափս - Sizeof(TcpuՎիճակ{})))
	result.ԿՄՀՎիճակ.Esp = result.Stack + ThreadstackՉափս
	result.ԿՄՀՎիճակ.Ebp = result.ԿՄՀՎիճակ.Esp
	result.ԿՄՀՎիճակ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Օգտագործողstack_2 = Օգտագործողstack
	result.ՕգտագործողstackՉափս_2 = ՕգտագործողstackՉափս
	result.Pid = 0
	result.Ծնողpid = 0
	result.Էջֆայլապանակentry = Էջֆայլապանակentry
	console_2.MՏպել((([]byte)("cpu")))

	console_2.MUnsignedinteger32Տպել(uint32(uintptr(Pointer(result.ԿՄՀՎիճակ))))

	console_2.MՏպել((([]byte)(":")))
	console_2.MUnsignedinteger32Տպել(result.ԿՄՀՎիճակ.Eip)

	console_2.MՏպել("]")
	if iskernel == true {
		result.ԿՄՀՎիճակ.Cs = Segkernelcode
		result.ԿՄՀՎիճակ.Ds = Segkerneldata
		result.ԿՄՀՎիճակ.Es = Segkerneldata
		result.ԿՄՀՎիճակ.Fs = Segkerneldata
		result.ԿՄՀՎիճակ.Gs = Segkernelgs
		result.ԿՄՀՎիճակ.Ss = Segkerneldata
		result.ThreadՎիճակ = Պատրաստ
		result.ԿՄՀՎիճակ.Eflags = 0x202
	} else {
		result.ԿՄՀՎիճակ.Cs = SegՕգտագործողcode
		result.ԿՄՀՎիճակ.Ds = SegՕգտագործողdata
		result.ԿՄՀՎիճակ.Es = SegՕգտագործողdata
		result.ԿՄՀՎիճակ.Fs = SegՕգտագործողdata
		result.ԿՄՀՎիճակ.Gs = SegՕգտագործողgs
		result.ԿՄՀՎիճակ.Ss = SegՕգտագործողdata
		result.ThreadՎիճակ = Սկսված
		result.ԿՄՀՎիճակ.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (ինքնուրույն *TThreadhelper) CreateՑուցիչիցfunction(entrypoint_2 func(), Էջֆայլապանակentry uint32, iskernel bool) *TThread {
	result := (*TThread)(ինքնուրույն.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = ինքնուրույն.Createիցfunction(entrypoint_2, Էջֆայլապանակentry, iskernel)
	if result.ԿՄՀՎիճակ == nil {
		ինքնուրույն.mem.Ազատ(Pointer(result))
		return nil
	}
	return result
}
