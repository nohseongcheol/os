/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "حافظهmanager"
import . "مجازیحافظه"

const (
	Blocked	= 1
	Rآماده	= 2
	Stopped	= 3
	Started	= 4
)

const Threadstackاندازه = 32 * 1024

type TThread struct {
	Cpuحالت			*Tcpuحالت
	Stack			uint32
	Uکاربرstack_2		uint32
	Uکاربرstackاندازه_2	uint32
	Pمشخصهبرنامه		uint32
	Pوالدمشخصهبرنامه	uint32

	Pصفحهشاخهentry	uint32

	Threadحالت	uint8
	Blockedحالت	uint8

	زمانdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (خود *TThread) Nجدید() {
}

type TThreadhelper struct {
	mem *mem.Tحافظهmanager
}

var console_2 = TConsole{}

func (خود *TThreadhelper) Init(mem *mem.Tحافظهmanager) {
	خود.mem = mem
	console_2.Mچاپxy(([]byte)("thread:"), 1, 14)
}
func (خود *TThreadhelper) Createfromتابع(entrypoint_2 func(), Pصفحهشاخهentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(خود.mem.Malloc(Threadstackاندازه)))
	if result.Stack == 0 {
		return result
	}
	console_2.Mچاپ(([]byte)("[mem:"))
	console_2.MUnsignedinteger32چاپ(result.Stack)

	result.Cpuحالت = (*Tcpuحالت)(Pointer(uintptr(result.Stack) + Threadstackاندازه - Sizeof(Tcpuحالت{})))
	result.Cpuحالت.Esp = result.Stack + Threadstackاندازه
	result.Cpuحالت.Ebp = result.Cpuحالت.Esp
	result.Cpuحالت.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Uکاربرstack_2 = Uکاربرstack
	result.Uکاربرstackاندازه_2 = Uکاربرstackاندازه
	result.Pمشخصهبرنامه = 0
	result.Pوالدمشخصهبرنامه = 0
	result.Pصفحهشاخهentry = Pصفحهشاخهentry
	console_2.Mچاپ((([]byte)("cpu")))

	console_2.MUnsignedinteger32چاپ(uint32(uintptr(Pointer(result.Cpuحالت))))

	console_2.Mچاپ((([]byte)(":")))
	console_2.MUnsignedinteger32چاپ(result.Cpuحالت.Eip)

	console_2.Mچاپ("]")
	if iskernel == true {
		result.Cpuحالت.Cs = Segkernelcode
		result.Cpuحالت.Ds = Segkerneldata
		result.Cpuحالت.Es = Segkerneldata
		result.Cpuحالت.Fs = Segkerneldata
		result.Cpuحالت.Gs = Segkernelgs
		result.Cpuحالت.Ss = Segkerneldata
		result.Threadحالت = Rآماده
		result.Cpuحالت.Eflags = 0x202
	} else {
		result.Cpuحالت.Cs = Segکاربرcode
		result.Cpuحالت.Ds = Segکاربرdata
		result.Cpuحالت.Es = Segکاربرdata
		result.Cpuحالت.Fs = Segکاربرdata
		result.Cpuحالت.Gs = Segکاربرgs
		result.Cpuحالت.Ss = Segکاربرdata
		result.Threadحالت = Started
		result.Cpuحالت.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (خود *TThreadhelper) Createpointerfromتابع(entrypoint_2 func(), Pصفحهشاخهentry uint32, iskernel bool) *TThread {
	result := (*TThread)(خود.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = خود.Createfromتابع(entrypoint_2, Pصفحهشاخهentry, iskernel)
	if result.Cpuحالت == nil {
		خود.mem.Fآزاد(Pointer(result))
		return nil
	}
	return result
}
