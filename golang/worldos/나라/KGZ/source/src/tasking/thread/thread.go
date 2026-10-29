/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "эсиmanager"
import . "virtualЭси"

const (
	Blocked		= 1
	Даяр		= 2
	Токтотулган	= 3
	Жүргүзүлгөнкүнү	= 4
)

const ThreadstackӨлчөм = 32 * 1024

type TThread struct {
	БПАбал			*TcpuАбал
	Stack			uint32
	Колдонуучуstack_2	uint32
	КолдонуучуstackӨлчөм_2	uint32
	Pid			uint32
	Атаэнеpid		uint32

	БАРАКкаталогentry	uint32

	ThreadАбал	uint8
	BlockedАбал	uint8

	timedelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Жаңы() {
}

type TThreadhelper struct {
	mem *mem.TЭсиmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TЭсиmanager) {
	self.mem = mem
	console_2.MБасмаxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), БАРАКкаталогentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackӨлчөм)))
	if result.Stack == 0 {
		return result
	}
	console_2.MБасма(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Басма(result.Stack)

	result.БПАбал = (*TcpuАбал)(Pointer(uintptr(result.Stack) + ThreadstackӨлчөм - Sizeof(TcpuАбал{})))
	result.БПАбал.Esp = result.Stack + ThreadstackӨлчөм
	result.БПАбал.Ebp = result.БПАбал.Esp
	result.БПАбал.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Колдонуучуstack_2 = Колдонуучуstack
	result.КолдонуучуstackӨлчөм_2 = КолдонуучуstackӨлчөм
	result.Pid = 0
	result.Атаэнеpid = 0
	result.БАРАКкаталогentry = БАРАКкаталогentry
	console_2.MБасма((([]byte)("cpu")))

	console_2.MUnsignedinteger32Басма(uint32(uintptr(Pointer(result.БПАбал))))

	console_2.MБасма((([]byte)(":")))
	console_2.MUnsignedinteger32Басма(result.БПАбал.Eip)

	console_2.MБасма("]")
	if iskernel == true {
		result.БПАбал.Cs = Segkernelcode
		result.БПАбал.Ds = Segkerneldata
		result.БПАбал.Es = Segkerneldata
		result.БПАбал.Fs = Segkerneldata
		result.БПАбал.Gs = Segkernelgs
		result.БПАбал.Ss = Segkerneldata
		result.ThreadАбал = Даяр
		result.БПАбал.Eflags = 0x202
	} else {
		result.БПАбал.Cs = SegКолдонуучуcode
		result.БПАбал.Ds = SegКолдонуучуdata
		result.БПАбал.Es = SegКолдонуучуdata
		result.БПАбал.Fs = SegКолдонуучуdata
		result.БПАбал.Gs = SegКолдонуучуgs
		result.БПАбал.Ss = SegКолдонуучуdata
		result.ThreadАбал = Жүргүзүлгөнкүнү
		result.БПАбал.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) CreateКөрсөткүчfromfunction(entrypoint_2 func(), БАРАКкаталогentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, БАРАКкаталогentry, iskernel)
	if result.БПАбал == nil {
		self.mem.Бош(Pointer(result))
		return nil
	}
	return result
}
