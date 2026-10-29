/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "паметmanager"
import . "virtualПамет"

const (
	Blocked		= 1
	Готово		= 2
	Спрян		= 3
	Стартиранна	= 4
)

const ThreadstackРазмер = 32 * 1024

type TThread struct {
	ПроцесорСъстояние	*TcpuСъстояние
	Stack			uint32
	Собственикstack_2	uint32
	СобственикstackРазмер_2	uint32
	ИдПр			uint32
	РодителИдПр		uint32

	Страницапапказапис	uint32

	ThreadСъстояние		uint8
	BlockedСъстояние	uint8

	времеdelta	uint32

	Tlssegments	[Gdtзапис]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (себеси *TThread) Нов() {
}

type TThreadhelper struct {
	mem *mem.TПаметmanager
}

var console_2 = TConsole{}

func (себеси *TThreadhelper) Init(mem *mem.TПаметmanager) {
	себеси.mem = mem
	console_2.MПечатxy(([]byte)("thread:"), 1, 14)
}
func (себеси *TThreadhelper) Createfromфункция(записpoint_2 func(), Страницапапказапис uint32, iskernel bool) TThread {
	рЕЗУЛТАТ := TThread{}

	рЕЗУЛТАТ.Stack = uint32(uintptr(себеси.mem.Malloc(ThreadstackРазмер)))
	if рЕЗУЛТАТ.Stack == 0 {
		return рЕЗУЛТАТ
	}
	console_2.MПечат(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Печат(рЕЗУЛТАТ.Stack)

	рЕЗУЛТАТ.ПроцесорСъстояние = (*TcpuСъстояние)(Pointer(uintptr(рЕЗУЛТАТ.Stack) + ThreadstackРазмер - Sizeof(TcpuСъстояние{})))
	рЕЗУЛТАТ.ПроцесорСъстояние.Esp = рЕЗУЛТАТ.Stack + ThreadstackРазмер
	рЕЗУЛТАТ.ПроцесорСъстояние.Ebp = рЕЗУЛТАТ.ПроцесорСъстояние.Esp
	рЕЗУЛТАТ.ПроцесорСъстояние.Eip = uint32(ValueOf(записpoint_2).Pointer())
	рЕЗУЛТАТ.Собственикstack_2 = Собственикstack
	рЕЗУЛТАТ.СобственикstackРазмер_2 = СобственикstackРазмер
	рЕЗУЛТАТ.ИдПр = 0
	рЕЗУЛТАТ.РодителИдПр = 0
	рЕЗУЛТАТ.Страницапапказапис = Страницапапказапис
	console_2.MПечат((([]byte)("cpu")))

	console_2.MUnsignedinteger32Печат(uint32(uintptr(Pointer(рЕЗУЛТАТ.ПроцесорСъстояние))))

	console_2.MПечат((([]byte)(":")))
	console_2.MUnsignedinteger32Печат(рЕЗУЛТАТ.ПроцесорСъстояние.Eip)

	console_2.MПечат("]")
	if iskernel == true {
		рЕЗУЛТАТ.ПроцесорСъстояние.Cs = Segkernelcode
		рЕЗУЛТАТ.ПроцесорСъстояние.Ds = Segkerneldata
		рЕЗУЛТАТ.ПроцесорСъстояние.Es = Segkerneldata
		рЕЗУЛТАТ.ПроцесорСъстояние.Fs = Segkerneldata
		рЕЗУЛТАТ.ПроцесорСъстояние.Gs = Segkernelgs
		рЕЗУЛТАТ.ПроцесорСъстояние.Ss = Segkerneldata
		рЕЗУЛТАТ.ThreadСъстояние = Готово
		рЕЗУЛТАТ.ПроцесорСъстояние.Eflags = 0x202
	} else {
		рЕЗУЛТАТ.ПроцесорСъстояние.Cs = SegСобственикcode
		рЕЗУЛТАТ.ПроцесорСъстояние.Ds = SegСобственикdata
		рЕЗУЛТАТ.ПроцесорСъстояние.Es = SegСобственикdata
		рЕЗУЛТАТ.ПроцесорСъстояние.Fs = SegСобственикdata
		рЕЗУЛТАТ.ПроцесорСъстояние.Gs = SegСобственикgs
		рЕЗУЛТАТ.ПроцесорСъстояние.Ss = SegСобственикdata
		рЕЗУЛТАТ.ThreadСъстояние = Стартиранна
		рЕЗУЛТАТ.ПроцесорСъстояние.Eflags = 0x222
	}
	рЕЗУЛТАТ.Iskernel = iskernel
	рЕЗУЛТАТ.Fpuoffset = 0xffffffff

	return рЕЗУЛТАТ
}

func (себеси *TThreadhelper) CreateПоказалциfromфункция(записpoint_2 func(), Страницапапказапис uint32, iskernel bool) *TThread {
	рЕЗУЛТАТ := (*TThread)(себеси.mem.Malloc(uint32(Sizeof(TThread{}))))
	if рЕЗУЛТАТ == nil {
		return nil
	}
	*рЕЗУЛТАТ = себеси.Createfromфункция(записpoint_2, Страницапапказапис, iskernel)
	if рЕЗУЛТАТ.ПроцесорСъстояние == nil {
		себеси.mem.Свободно(Pointer(рЕЗУЛТАТ))
		return nil
	}
	return рЕЗУЛТАТ
}
