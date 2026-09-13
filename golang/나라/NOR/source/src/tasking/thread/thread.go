package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "minnemanager"
import . "virtuellMinne"

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
	Brukerstack_2		uint32
	BrukerstackStørrelse_2	uint32
	Pid			uint32
	Opphavpid		uint32

	SideKatalogentry	uint32

	ThreadStatus	uint8
	BlockedStatus	uint8

	tiddelta	uint32

	TlsSegmenter	[Gdtentry]TSegmentdescriptor
	FpuAvstand	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (selv *TThread) Ny() {
}

type TThreadhelper struct {
	mem *mem.TMinnemanager
}

var console_2 = TConsole{}

func (selv *TThreadhelper) Init(mem *mem.TMinnemanager) {
	selv.mem = mem
	console_2.MSkrivutxy(([]byte)("thread:"), 1, 14)
}
func (selv *TThreadhelper) CreatefromFunksjon(entrypoint_2 func(), SideKatalogentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(selv.mem.Malloc(ThreadstackStørrelse)))
	if result.Stack == 0 {
		return result
	}
	console_2.MSkrivut(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Skrivut(result.Stack)

	result.CpuStatus = (*TcpuStatus)(Pointer(uintptr(result.Stack) + ThreadstackStørrelse - Sizeof(TcpuStatus{})))
	result.CpuStatus.Esp = result.Stack + ThreadstackStørrelse
	result.CpuStatus.Ebp = result.CpuStatus.Esp
	result.CpuStatus.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Brukerstack_2 = Brukerstack
	result.BrukerstackStørrelse_2 = BrukerstackStørrelse
	result.Pid = 0
	result.Opphavpid = 0
	result.SideKatalogentry = SideKatalogentry
	console_2.MSkrivut((([]byte)("cpu")))

	console_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(result.CpuStatus))))

	console_2.MSkrivut((([]byte)(":")))
	console_2.MUnsignedinteger32Skrivut(result.CpuStatus.Eip)

	console_2.MSkrivut("]")
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
		result.CpuStatus.Cs = SegBrukercode
		result.CpuStatus.Ds = SegBrukerdata
		result.CpuStatus.Es = SegBrukerdata
		result.CpuStatus.Fs = SegBrukerdata
		result.CpuStatus.Gs = SegBrukergs
		result.CpuStatus.Ss = SegBrukerdata
		result.ThreadStatus = Startet
		result.CpuStatus.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.FpuAvstand = 0xffffffff

	return result
}

func (selv *TThreadhelper) CreatePekerfromFunksjon(entrypoint_2 func(), SideKatalogentry uint32, iskernel bool) *TThread {
	result := (*TThread)(selv.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = selv.CreatefromFunksjon(entrypoint_2, SideKatalogentry, iskernel)
	if result.CpuStatus == nil {
		selv.mem.Ledig(Pointer(result))
		return nil
	}
	return result
}
