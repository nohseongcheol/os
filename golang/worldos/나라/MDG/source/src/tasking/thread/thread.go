/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konsoly"
import . "multitasking"
import mem "arikaMpandrindra"
import . "virtualArika"

const (
	Blocked		= 1
	Vonona		= 2
	Najanona	= 3
	Natomboka	= 4
)

const ThreadstackHabe = 32 * 1024

type TThread struct {
	Cpustate		*Tcpustate
	Stack			uint32
	Mpampiasastack_2	uint32
	MpampiasastackHabe_2	uint32
	Pid			uint32
	Renypid			uint32

	PEJYLahatahiryentry	uint32

	Threadstate	uint8
	Blockedstate	uint8

	fotoanadelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (nytena *TThread) Vaovao() {
}

type TThreadhelper struct {
	mem *mem.TArikaMpandrindra
}

var konsoly_2 = TKonsoly{}

func (nytena *TThreadhelper) Init(mem *mem.TArikaMpandrindra) {
	nytena.mem = mem
	konsoly_2.MAtontayxy(([]byte)("thread:"), 1, 14)
}
func (nytena *TThreadhelper) Createfromfunction(entrypoint_2 func(), PEJYLahatahiryentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(nytena.mem.Malloc(ThreadstackHabe)))
	if result.Stack == 0 {
		return result
	}
	konsoly_2.MAtontay(([]byte)("[mem:"))
	konsoly_2.MUnsignedinteger32Atontay(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + ThreadstackHabe - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + ThreadstackHabe
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Mpampiasastack_2 = Mpampiasastack
	result.MpampiasastackHabe_2 = MpampiasastackHabe
	result.Pid = 0
	result.Renypid = 0
	result.PEJYLahatahiryentry = PEJYLahatahiryentry
	konsoly_2.MAtontay((([]byte)("cpu")))

	konsoly_2.MUnsignedinteger32Atontay(uint32(uintptr(Pointer(result.Cpustate))))

	konsoly_2.MAtontay((([]byte)(":")))
	konsoly_2.MUnsignedinteger32Atontay(result.Cpustate.Eip)

	konsoly_2.MAtontay("]")
	if iskernel == true {
		result.Cpustate.Cs = Segkernelcode
		result.Cpustate.Ds = Segkerneldata
		result.Cpustate.Es = Segkerneldata
		result.Cpustate.Fs = Segkerneldata
		result.Cpustate.Gs = Segkernelgs
		result.Cpustate.Ss = Segkerneldata
		result.Threadstate = Vonona
		result.Cpustate.Eflags = 0x202
	} else {
		result.Cpustate.Cs = SegMpampiasacode
		result.Cpustate.Ds = SegMpampiasadata
		result.Cpustate.Es = SegMpampiasadata
		result.Cpustate.Fs = SegMpampiasadata
		result.Cpustate.Gs = SegMpampiasags
		result.Cpustate.Ss = SegMpampiasadata
		result.Threadstate = Natomboka
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (nytena *TThreadhelper) Createpointerfromfunction(entrypoint_2 func(), PEJYLahatahiryentry uint32, iskernel bool) *TThread {
	result := (*TThread)(nytena.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = nytena.Createfromfunction(entrypoint_2, PEJYLahatahiryentry, iskernel)
	if result.Cpustate == nil {
		nytena.mem.Malalaka(Pointer(result))
		return nil
	}
	return result
}
