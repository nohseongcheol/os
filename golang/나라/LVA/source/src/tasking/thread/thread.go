package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "atmiņamanager"
import . "virtuālaAtmiņa"

const (
	Blocked		= 1
	Gatavs		= 2
	Apturēts	= 3
	Palaists	= 4
)

const ThreadstackIzmērs = 32 * 1024

type TThread struct {
	CpuStāvoklis		*TcpuStāvoklis
	Stack			uint32
	Lietotājsstack_2	uint32
	LietotājsstackIzmērs_2	uint32
	Pid			uint32
	Vecākspid		uint32

	LapaMapeieraksts	uint32

	ThreadStāvoklis		uint8
	BlockedStāvoklis	uint8

	laiksdelta	uint32

	Tlssegments	[Gdtieraksts]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (pats *TThread) Jauns() {
}

type TThreadhelper struct {
	mem *mem.TAtmiņamanager
}

var console_2 = TConsole{}

func (pats *TThreadhelper) Init(mem *mem.TAtmiņamanager) {
	pats.mem = mem
	console_2.MDrukātxy(([]byte)("thread:"), 1, 14)
}
func (pats *TThreadhelper) CreatefromFunkcija(ierakstspoint_2 func(), LapaMapeieraksts uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(pats.mem.Malloc(ThreadstackIzmērs)))
	if result.Stack == 0 {
		return result
	}
	console_2.MDrukāt(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Drukāt(result.Stack)

	result.CpuStāvoklis = (*TcpuStāvoklis)(Pointer(uintptr(result.Stack) + ThreadstackIzmērs - Sizeof(TcpuStāvoklis{})))
	result.CpuStāvoklis.Esp = result.Stack + ThreadstackIzmērs
	result.CpuStāvoklis.Ebp = result.CpuStāvoklis.Esp
	result.CpuStāvoklis.Eip = uint32(ValueOf(ierakstspoint_2).Pointer())
	result.Lietotājsstack_2 = Lietotājsstack
	result.LietotājsstackIzmērs_2 = LietotājsstackIzmērs
	result.Pid = 0
	result.Vecākspid = 0
	result.LapaMapeieraksts = LapaMapeieraksts
	console_2.MDrukāt((([]byte)("cpu")))

	console_2.MUnsignedinteger32Drukāt(uint32(uintptr(Pointer(result.CpuStāvoklis))))

	console_2.MDrukāt((([]byte)(":")))
	console_2.MUnsignedinteger32Drukāt(result.CpuStāvoklis.Eip)

	console_2.MDrukāt("]")
	if iskernel == true {
		result.CpuStāvoklis.Cs = Segkernelcode
		result.CpuStāvoklis.Ds = Segkerneldata
		result.CpuStāvoklis.Es = Segkerneldata
		result.CpuStāvoklis.Fs = Segkerneldata
		result.CpuStāvoklis.Gs = Segkernelgs
		result.CpuStāvoklis.Ss = Segkerneldata
		result.ThreadStāvoklis = Gatavs
		result.CpuStāvoklis.Eflags = 0x202
	} else {
		result.CpuStāvoklis.Cs = SegLietotājscode
		result.CpuStāvoklis.Ds = SegLietotājsdata
		result.CpuStāvoklis.Es = SegLietotājsdata
		result.CpuStāvoklis.Fs = SegLietotājsdata
		result.CpuStāvoklis.Gs = SegLietotājsgs
		result.CpuStāvoklis.Ss = SegLietotājsdata
		result.ThreadStāvoklis = Palaists
		result.CpuStāvoklis.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (pats *TThreadhelper) CreateKursorsfromFunkcija(ierakstspoint_2 func(), LapaMapeieraksts uint32, iskernel bool) *TThread {
	result := (*TThread)(pats.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = pats.CreatefromFunkcija(ierakstspoint_2, LapaMapeieraksts, iskernel)
	if result.CpuStāvoklis == nil {
		pats.mem.Brīvs(Pointer(result))
		return nil
	}
	return result
}
