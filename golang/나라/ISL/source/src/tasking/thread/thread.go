package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "minnimanager"
import . "sýndarMinni"

const (
	Blocked	= 1
	Tilbúið	= 2
	Stopped	= 3
	Started	= 4
)

const ThreadstackStærð = 32 * 1024

type TThread struct {
	CpuStaða		*TcpuStaða
	Stack			uint32
	Notandistack_2		uint32
	NotandistackStærð_2	uint32
	Pid			uint32
	Foreldripid		uint32

	Síðamappaentry	uint32

	ThreadStaða	uint8
	BlockedStaða	uint8

	tímidelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (sjálft *TThread) Nýtt() {
}

type TThreadhelper struct {
	mem *mem.TMinnimanager
}

var console_2 = TConsole{}

func (sjálft *TThreadhelper) Init(mem *mem.TMinnimanager) {
	sjálft.mem = mem
	console_2.MPrentaxy(([]byte)("thread:"), 1, 14)
}
func (sjálft *TThreadhelper) CreatefromAðgerð(entrypoint_2 func(), Síðamappaentry uint32, iskernel bool) TThread {
	nIÐURSTAÐA := TThread{}

	nIÐURSTAÐA.Stack = uint32(uintptr(sjálft.mem.Malloc(ThreadstackStærð)))
	if nIÐURSTAÐA.Stack == 0 {
		return nIÐURSTAÐA
	}
	console_2.MPrenta(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Prenta(nIÐURSTAÐA.Stack)

	nIÐURSTAÐA.CpuStaða = (*TcpuStaða)(Pointer(uintptr(nIÐURSTAÐA.Stack) + ThreadstackStærð - Sizeof(TcpuStaða{})))
	nIÐURSTAÐA.CpuStaða.Esp = nIÐURSTAÐA.Stack + ThreadstackStærð
	nIÐURSTAÐA.CpuStaða.Ebp = nIÐURSTAÐA.CpuStaða.Esp
	nIÐURSTAÐA.CpuStaða.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	nIÐURSTAÐA.Notandistack_2 = Notandistack
	nIÐURSTAÐA.NotandistackStærð_2 = NotandistackStærð
	nIÐURSTAÐA.Pid = 0
	nIÐURSTAÐA.Foreldripid = 0
	nIÐURSTAÐA.Síðamappaentry = Síðamappaentry
	console_2.MPrenta((([]byte)("cpu")))

	console_2.MUnsignedinteger32Prenta(uint32(uintptr(Pointer(nIÐURSTAÐA.CpuStaða))))

	console_2.MPrenta((([]byte)(":")))
	console_2.MUnsignedinteger32Prenta(nIÐURSTAÐA.CpuStaða.Eip)

	console_2.MPrenta("]")
	if iskernel == true {
		nIÐURSTAÐA.CpuStaða.Cs = Segkernelcode
		nIÐURSTAÐA.CpuStaða.Ds = Segkerneldata
		nIÐURSTAÐA.CpuStaða.Es = Segkerneldata
		nIÐURSTAÐA.CpuStaða.Fs = Segkerneldata
		nIÐURSTAÐA.CpuStaða.Gs = Segkernelgs
		nIÐURSTAÐA.CpuStaða.Ss = Segkerneldata
		nIÐURSTAÐA.ThreadStaða = Tilbúið
		nIÐURSTAÐA.CpuStaða.Eflags = 0x202
	} else {
		nIÐURSTAÐA.CpuStaða.Cs = SegNotandicode
		nIÐURSTAÐA.CpuStaða.Ds = SegNotandidata
		nIÐURSTAÐA.CpuStaða.Es = SegNotandidata
		nIÐURSTAÐA.CpuStaða.Fs = SegNotandidata
		nIÐURSTAÐA.CpuStaða.Gs = SegNotandigs
		nIÐURSTAÐA.CpuStaða.Ss = SegNotandidata
		nIÐURSTAÐA.ThreadStaða = Started
		nIÐURSTAÐA.CpuStaða.Eflags = 0x222
	}
	nIÐURSTAÐA.Iskernel = iskernel
	nIÐURSTAÐA.Fpuoffset = 0xffffffff

	return nIÐURSTAÐA
}

func (sjálft *TThreadhelper) CreateBendillfromAðgerð(entrypoint_2 func(), Síðamappaentry uint32, iskernel bool) *TThread {
	nIÐURSTAÐA := (*TThread)(sjálft.mem.Malloc(uint32(Sizeof(TThread{}))))
	if nIÐURSTAÐA == nil {
		return nil
	}
	*nIÐURSTAÐA = sjálft.CreatefromAðgerð(entrypoint_2, Síðamappaentry, iskernel)
	if nIÐURSTAÐA.CpuStaða == nil {
		sjálft.mem.Laust(Pointer(nIÐURSTAÐA))
		return nil
	}
	return nIÐURSTAÐA
}
