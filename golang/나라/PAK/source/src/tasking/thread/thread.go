package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "یادداشتmanager"
import . "virtualیادداشت"

const (
	Blocked		= 1
	Rتیار		= 2
	Sرکےہوئے	= 3
	Sشروعکردہ	= 4
)

const Threadstackحجم = 32 * 1024

type TThread struct {
	Cسیپییوحالت	*Tcpuحالت
	Stack		uint32
	Uصارفstack_2	uint32
	Uصارفstackحجم_2	uint32
	Pid		uint32
	Pآبائیpid	uint32

	Pصفحہڈائریکٹریentry	uint32

	Threadحالت	uint8
	Blockedحالت	uint8

	وقتdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Nنیا() {
}

type TThreadhelper struct {
	mem *mem.Tیادداشتmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.Tیادداشتmanager) {
	self.mem = mem
	console_2.Mچھاپیںxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), Pصفحہڈائریکٹریentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(Threadstackحجم)))
	if result.Stack == 0 {
		return result
	}
	console_2.Mچھاپیں(([]byte)("[mem:"))
	console_2.MUnsignedinteger32چھاپیں(result.Stack)

	result.Cسیپییوحالت = (*Tcpuحالت)(Pointer(uintptr(result.Stack) + Threadstackحجم - Sizeof(Tcpuحالت{})))
	result.Cسیپییوحالت.Esp = result.Stack + Threadstackحجم
	result.Cسیپییوحالت.Ebp = result.Cسیپییوحالت.Esp
	result.Cسیپییوحالت.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Uصارفstack_2 = Uصارفstack
	result.Uصارفstackحجم_2 = Uصارفstackحجم
	result.Pid = 0
	result.Pآبائیpid = 0
	result.Pصفحہڈائریکٹریentry = Pصفحہڈائریکٹریentry
	console_2.Mچھاپیں((([]byte)("cpu")))

	console_2.MUnsignedinteger32چھاپیں(uint32(uintptr(Pointer(result.Cسیپییوحالت))))

	console_2.Mچھاپیں((([]byte)(":")))
	console_2.MUnsignedinteger32چھاپیں(result.Cسیپییوحالت.Eip)

	console_2.Mچھاپیں("]")
	if iskernel == true {
		result.Cسیپییوحالت.Cs = Segkernelcode
		result.Cسیپییوحالت.Ds = Segkerneldata
		result.Cسیپییوحالت.Es = Segkerneldata
		result.Cسیپییوحالت.Fs = Segkerneldata
		result.Cسیپییوحالت.Gs = Segkernelgs
		result.Cسیپییوحالت.Ss = Segkerneldata
		result.Threadحالت = Rتیار
		result.Cسیپییوحالت.Eflags = 0x202
	} else {
		result.Cسیپییوحالت.Cs = Segصارفcode
		result.Cسیپییوحالت.Ds = Segصارفdata
		result.Cسیپییوحالت.Es = Segصارفdata
		result.Cسیپییوحالت.Fs = Segصارفdata
		result.Cسیپییوحالت.Gs = Segصارفgs
		result.Cسیپییوحالت.Ss = Segصارفdata
		result.Threadحالت = Sشروعکردہ
		result.Cسیپییوحالت.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createپؤائنٹرfromfunction(entrypoint_2 func(), Pصفحہڈائریکٹریentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, Pصفحہڈائریکٹریentry, iskernel)
	if result.Cسیپییوحالت == nil {
		self.mem.Fخالی(Pointer(result))
		return nil
	}
	return result
}
