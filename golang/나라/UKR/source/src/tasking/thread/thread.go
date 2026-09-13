package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "консоль"
import . "multitasking"
import mem "памятьmanager"
import . "віртуальнийПамять"

const (
	Blocked		= 1
	Готово		= 2
	Зупинено	= 3
	Запущено	= 4
)

const ThreadstackРозмір = 32 * 1024

type TThread struct {
	ПроцесорСтан		*TcpuСтан
	Stack			uint32
	Користувачstack_2	uint32
	КористувачstackРозмір_2	uint32
	ІдентифікаторPID	uint32
	БатькоІдентифікаторPID	uint32

	СторінкаТеказапис	uint32

	ThreadСтан	uint8
	BlockedСтан	uint8

	часДелта	uint32

	Tlssegments	[Gdtзапис]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (поточний *TThread) Новий() {
}

type TThreadhelper struct {
	mem *mem.TПамятьmanager
}

var консоль_2 = TКонсоль{}

func (поточний *TThreadhelper) Init(mem *mem.TПамятьmanager) {
	поточний.mem = mem
	консоль_2.MДрукxy(([]byte)("thread:"), 1, 14)
}
func (поточний *TThreadhelper) CreateзФункція(записpoint_2 func(), СторінкаТеказапис uint32, iskernel bool) TThread {
	яРЛИК := TThread{}

	яРЛИК.Stack = uint32(uintptr(поточний.mem.Виділити_памʼять(ThreadstackРозмір)))
	if яРЛИК.Stack == 0 {
		return яРЛИК
	}
	консоль_2.MДрук(([]byte)("[mem:"))
	консоль_2.MUnsignedinteger32Друк(яРЛИК.Stack)

	яРЛИК.ПроцесорСтан = (*TcpuСтан)(Pointer(uintptr(яРЛИК.Stack) + ThreadstackРозмір - Sizeof(TcpuСтан{})))
	яРЛИК.ПроцесорСтан.Esp = яРЛИК.Stack + ThreadstackРозмір
	яРЛИК.ПроцесорСтан.Ebp = яРЛИК.ПроцесорСтан.Esp
	яРЛИК.ПроцесорСтан.Eip = uint32(ValueOf(записpoint_2).Pointer())
	яРЛИК.Користувачstack_2 = Користувачstack
	яРЛИК.КористувачstackРозмір_2 = КористувачstackРозмір
	яРЛИК.ІдентифікаторPID = 0
	яРЛИК.БатькоІдентифікаторPID = 0
	яРЛИК.СторінкаТеказапис = СторінкаТеказапис
	консоль_2.MДрук((([]byte)("cpu")))

	консоль_2.MUnsignedinteger32Друк(uint32(uintptr(Pointer(яРЛИК.ПроцесорСтан))))

	консоль_2.MДрук((([]byte)(":")))
	консоль_2.MUnsignedinteger32Друк(яРЛИК.ПроцесорСтан.Eip)

	консоль_2.MДрук("]")
	if iskernel == true {
		яРЛИК.ПроцесорСтан.Cs = Segkernelcode
		яРЛИК.ПроцесорСтан.Ds = Segkerneldata
		яРЛИК.ПроцесорСтан.Es = Segkerneldata
		яРЛИК.ПроцесорСтан.Fs = Segkerneldata
		яРЛИК.ПроцесорСтан.Gs = Segkernelgs
		яРЛИК.ПроцесорСтан.Ss = Segkerneldata
		яРЛИК.ThreadСтан = Готово
		яРЛИК.ПроцесорСтан.Eflags = 0x202
	} else {
		яРЛИК.ПроцесорСтан.Cs = SegКористувачcode
		яРЛИК.ПроцесорСтан.Ds = SegКористувачdata
		яРЛИК.ПроцесорСтан.Es = SegКористувачdata
		яРЛИК.ПроцесорСтан.Fs = SegКористувачdata
		яРЛИК.ПроцесорСтан.Gs = SegКористувачgs
		яРЛИК.ПроцесорСтан.Ss = SegКористувачdata
		яРЛИК.ThreadСтан = Запущено
		яРЛИК.ПроцесорСтан.Eflags = 0x222
	}
	яРЛИК.Iskernel = iskernel
	яРЛИК.Fpuoffset = 0xffffffff

	return яРЛИК
}

func (поточний *TThreadhelper) CreateВказівникзФункція(записpoint_2 func(), СторінкаТеказапис uint32, iskernel bool) *TThread {
	яРЛИК := (*TThread)(поточний.mem.Виділити_памʼять(uint32(Sizeof(TThread{}))))
	if яРЛИК == nil {
		return nil
	}
	*яРЛИК = поточний.CreateзФункція(записpoint_2, СторінкаТеказапис, iskernel)
	if яРЛИК.ПроцесорСтан == nil {
		поточний.mem.Вільно(Pointer(яРЛИК))
		return nil
	}
	return яРЛИК
}
