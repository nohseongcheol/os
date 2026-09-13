package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "hukommelsemanager"
import . "virtuelHukommelse"

const (
	Blocked	= 1
	Klar	= 2
	Stoppet	= 3
	Startet	= 4
)

const ThreadstackStørrelse = 32 * 1024

type TThread struct {
	CpuStatus		*TcpuStatus
	Stack			uint32
	Brugerstack_2		uint32
	BrugerstackStørrelse_2	uint32
	Pid			uint32
	Forælderpid		uint32

	SideMappeemne	uint32

	ThreadStatus	uint8
	BlockedStatus	uint8

	tiddelta	uint32

	TlsSegmenter	[Gdtemne]TSegmentdescriptor
	FpuForskydning	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (selv *TThread) Ny() {
}

type TThreadhelper struct {
	mem *mem.THukommelsemanager
}

var console_2 = TConsole{}

func (selv *TThreadhelper) Init(mem *mem.THukommelsemanager) {
	selv.mem = mem
	console_2.MUdskrivxy(([]byte)("thread:"), 1, 14)
}
func (selv *TThreadhelper) CreatefraFunktion(emnepoint_2 func(), SideMappeemne uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(selv.mem.Malloc(ThreadstackStørrelse)))
	if result.Stack == 0 {
		return result
	}
	console_2.MUdskriv(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Udskriv(result.Stack)

	result.CpuStatus = (*TcpuStatus)(Pointer(uintptr(result.Stack) + ThreadstackStørrelse - Sizeof(TcpuStatus{})))
	result.CpuStatus.Esp = result.Stack + ThreadstackStørrelse
	result.CpuStatus.Ebp = result.CpuStatus.Esp
	result.CpuStatus.Eip = uint32(ValueOf(emnepoint_2).Pointer())
	result.Brugerstack_2 = Brugerstack
	result.BrugerstackStørrelse_2 = BrugerstackStørrelse
	result.Pid = 0
	result.Forælderpid = 0
	result.SideMappeemne = SideMappeemne
	console_2.MUdskriv((([]byte)("cpu")))

	console_2.MUnsignedinteger32Udskriv(uint32(uintptr(Pointer(result.CpuStatus))))

	console_2.MUdskriv((([]byte)(":")))
	console_2.MUnsignedinteger32Udskriv(result.CpuStatus.Eip)

	console_2.MUdskriv("]")
	if iskernel == true {
		result.CpuStatus.Cs = Segkernelcode
		result.CpuStatus.Ds = Segkerneldata
		result.CpuStatus.Es = Segkerneldata
		result.CpuStatus.Fs = Segkerneldata
		result.CpuStatus.Gs = Segkernelgs
		result.CpuStatus.Ss = Segkerneldata
		result.ThreadStatus = Klar
		result.CpuStatus.Eflags = 0x202
	} else {
		result.CpuStatus.Cs = SegBrugercode
		result.CpuStatus.Ds = SegBrugerdata
		result.CpuStatus.Es = SegBrugerdata
		result.CpuStatus.Fs = SegBrugerdata
		result.CpuStatus.Gs = SegBrugergs
		result.CpuStatus.Ss = SegBrugerdata
		result.ThreadStatus = Startet
		result.CpuStatus.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.FpuForskydning = 0xffffffff

	return result
}

func (selv *TThreadhelper) CreateMarkørfraFunktion(emnepoint_2 func(), SideMappeemne uint32, iskernel bool) *TThread {
	result := (*TThread)(selv.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = selv.CreatefraFunktion(emnepoint_2, SideMappeemne, iskernel)
	if result.CpuStatus == nil {
		selv.mem.Fri(Pointer(result))
		return nil
	}
	return result
}
