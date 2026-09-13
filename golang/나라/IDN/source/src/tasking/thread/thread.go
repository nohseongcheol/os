package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "memorimanager"
import . "virtualMemori"

const (
	Blocked		= 1
	Siap		= 2
	Berhenti	= 3
	Dimulai		= 4
)

const ThreadstackUkuran = 32 * 1024

type TThread struct {
	CpuStatus		*TcpuStatus
	Stack			uint32
	Penggunastack_2		uint32
	PenggunastackUkuran_2	uint32
	Pid			uint32
	Orangtuapid		uint32

	HalamanDirektorientri	uint32

	ThreadStatus	uint8
	BlockedStatus	uint8

	waktudelta	uint32

	Tlssegments	[Gdtentri]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (dirisendiri *TThread) Baru() {
}

type TThreadhelper struct {
	mem *mem.TMemorimanager
}

var console_2 = TConsole{}

func (dirisendiri *TThreadhelper) Init(mem *mem.TMemorimanager) {
	dirisendiri.mem = mem
	console_2.MCetakxy(([]byte)("thread:"), 1, 14)
}
func (dirisendiri *TThreadhelper) CreatefromFungsi(entripoint_2 func(), HalamanDirektorientri uint32, iskernel bool) TThread {
	hASIL := TThread{}

	hASIL.Stack = uint32(uintptr(dirisendiri.mem.Alokasikan_memori(ThreadstackUkuran)))
	if hASIL.Stack == 0 {
		return hASIL
	}
	console_2.MCetak(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Cetak(hASIL.Stack)

	hASIL.CpuStatus = (*TcpuStatus)(Pointer(uintptr(hASIL.Stack) + ThreadstackUkuran - Sizeof(TcpuStatus{})))
	hASIL.CpuStatus.Esp = hASIL.Stack + ThreadstackUkuran
	hASIL.CpuStatus.Ebp = hASIL.CpuStatus.Esp
	hASIL.CpuStatus.Eip = uint32(ValueOf(entripoint_2).Pointer())
	hASIL.Penggunastack_2 = Penggunastack
	hASIL.PenggunastackUkuran_2 = PenggunastackUkuran
	hASIL.Pid = 0
	hASIL.Orangtuapid = 0
	hASIL.HalamanDirektorientri = HalamanDirektorientri
	console_2.MCetak((([]byte)("cpu")))

	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(hASIL.CpuStatus))))

	console_2.MCetak((([]byte)(":")))
	console_2.MUnsignedinteger32Cetak(hASIL.CpuStatus.Eip)

	console_2.MCetak("]")
	if iskernel == true {
		hASIL.CpuStatus.Cs = Segkernelcode
		hASIL.CpuStatus.Ds = Segkerneldata
		hASIL.CpuStatus.Es = Segkerneldata
		hASIL.CpuStatus.Fs = Segkerneldata
		hASIL.CpuStatus.Gs = Segkernelgs
		hASIL.CpuStatus.Ss = Segkerneldata
		hASIL.ThreadStatus = Siap
		hASIL.CpuStatus.Eflags = 0x202
	} else {
		hASIL.CpuStatus.Cs = SegPenggunacode
		hASIL.CpuStatus.Ds = SegPenggunadata
		hASIL.CpuStatus.Es = SegPenggunadata
		hASIL.CpuStatus.Fs = SegPenggunadata
		hASIL.CpuStatus.Gs = SegPenggunags
		hASIL.CpuStatus.Ss = SegPenggunadata
		hASIL.ThreadStatus = Dimulai
		hASIL.CpuStatus.Eflags = 0x222
	}
	hASIL.Iskernel = iskernel
	hASIL.Fpuoffset = 0xffffffff

	return hASIL
}

func (dirisendiri *TThreadhelper) CreatePenunjukfromFungsi(entripoint_2 func(), HalamanDirektorientri uint32, iskernel bool) *TThread {
	hASIL := (*TThread)(dirisendiri.mem.Alokasikan_memori(uint32(Sizeof(TThread{}))))
	if hASIL == nil {
		return nil
	}
	*hASIL = dirisendiri.CreatefromFungsi(entripoint_2, HalamanDirektorientri, iskernel)
	if hASIL.CpuStatus == nil {
		dirisendiri.mem.Bebas(Pointer(hASIL))
		return nil
	}
	return hASIL
}
