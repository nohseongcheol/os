/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "памяцьmanager"
import . "virtualПамяць"

const (
	Blocked		= 1
	Гатова		= 2
	Спынены		= 3
	Калізапушчаны	= 4
)

const ThreadstackПамер = 32 * 1024

type TThread struct {
	ЦПСтан				*TcpuСтан
	Stack				uint32
	Карыстальнікstack_2		uint32
	КарыстальнікstackПамер_2	uint32
	Pid				uint32
	Parentpid			uint32

	СтаронкаКаталогentry	uint32

	ThreadСтан	uint8
	BlockedСтан	uint8

	часДэлта	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Новы() {
}

type TThreadhelper struct {
	mem *mem.TПамяцьmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TПамяцьmanager) {
	self.mem = mem
	console_2.MДрукавацьxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatefromФункцыя(entrypoint_2 func(), СтаронкаКаталогentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackПамер)))
	if result.Stack == 0 {
		return result
	}
	console_2.MДрукаваць(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Друкаваць(result.Stack)

	result.ЦПСтан = (*TcpuСтан)(Pointer(uintptr(result.Stack) + ThreadstackПамер - Sizeof(TcpuСтан{})))
	result.ЦПСтан.Esp = result.Stack + ThreadstackПамер
	result.ЦПСтан.Ebp = result.ЦПСтан.Esp
	result.ЦПСтан.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Карыстальнікstack_2 = Карыстальнікstack
	result.КарыстальнікstackПамер_2 = КарыстальнікstackПамер
	result.Pid = 0
	result.Parentpid = 0
	result.СтаронкаКаталогentry = СтаронкаКаталогentry
	console_2.MДрукаваць((([]byte)("cpu")))

	console_2.MUnsignedinteger32Друкаваць(uint32(uintptr(Pointer(result.ЦПСтан))))

	console_2.MДрукаваць((([]byte)(":")))
	console_2.MUnsignedinteger32Друкаваць(result.ЦПСтан.Eip)

	console_2.MДрукаваць("]")
	if iskernel == true {
		result.ЦПСтан.Cs = Segkernelcode
		result.ЦПСтан.Ds = Segkerneldata
		result.ЦПСтан.Es = Segkerneldata
		result.ЦПСтан.Fs = Segkerneldata
		result.ЦПСтан.Gs = Segkernelgs
		result.ЦПСтан.Ss = Segkerneldata
		result.ThreadСтан = Гатова
		result.ЦПСтан.Eflags = 0x202
	} else {
		result.ЦПСтан.Cs = SegКарыстальнікcode
		result.ЦПСтан.Ds = SegКарыстальнікdata
		result.ЦПСтан.Es = SegКарыстальнікdata
		result.ЦПСтан.Fs = SegКарыстальнікdata
		result.ЦПСтан.Gs = SegКарыстальнікgs
		result.ЦПСтан.Ss = SegКарыстальнікdata
		result.ThreadСтан = Калізапушчаны
		result.ЦПСтан.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) CreateПаказальнікfromФункцыя(entrypoint_2 func(), СтаронкаКаталогentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.CreatefromФункцыя(entrypoint_2, СтаронкаКаталогentry, iskernel)
	if result.ЦПСтан == nil {
		self.mem.Вольна(Pointer(result))
		return nil
	}
	return result
}
