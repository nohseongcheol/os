package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "ingatanmanager"
import . "virtualIngatan"

const (
	Blocked		= 1
	Sedia		= 2
	Berhenti	= 3
	Bermula		= 4
)

const ThreadstackSaiz = 32 * 1024

type TThread struct {
	CpuKeadaan		*TcpuKeadaan
	Stack			uint32
	Penggunastack_2		uint32
	PenggunastackSaiz_2	uint32
	IDP			uint32
	IndukIDP		uint32

	Halamandirektorientry	uint32

	ThreadKeadaan	uint8
	BlockedKeadaan	uint8

	masadelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (diri *TThread) Baharu() {
}

type TThreadhelper struct {
	mem *mem.TIngatanmanager
}

var console_2 = TConsole{}

func (diri *TThreadhelper) Init(mem *mem.TIngatanmanager) {
	diri.mem = mem
	console_2.MCetakxy(([]byte)("thread:"), 1, 14)
}
func (diri *TThreadhelper) CreatefromFungsi(entrypoint_2 func(), Halamandirektorientry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(diri.mem.Peruntukkan_ingatan(ThreadstackSaiz)))
	if result.Stack == 0 {
		return result
	}
	console_2.MCetak(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Cetak(result.Stack)

	result.CpuKeadaan = (*TcpuKeadaan)(Pointer(uintptr(result.Stack) + ThreadstackSaiz - Sizeof(TcpuKeadaan{})))
	result.CpuKeadaan.Esp = result.Stack + ThreadstackSaiz
	result.CpuKeadaan.Ebp = result.CpuKeadaan.Esp
	result.CpuKeadaan.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Penggunastack_2 = Penggunastack
	result.PenggunastackSaiz_2 = PenggunastackSaiz
	result.IDP = 0
	result.IndukIDP = 0
	result.Halamandirektorientry = Halamandirektorientry
	console_2.MCetak((([]byte)("cpu")))

	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(result.CpuKeadaan))))

	console_2.MCetak((([]byte)(":")))
	console_2.MUnsignedinteger32Cetak(result.CpuKeadaan.Eip)

	console_2.MCetak("]")
	if iskernel == true {
		result.CpuKeadaan.Cs = Segkernelcode
		result.CpuKeadaan.Ds = Segkerneldata
		result.CpuKeadaan.Es = Segkerneldata
		result.CpuKeadaan.Fs = Segkerneldata
		result.CpuKeadaan.Gs = Segkernelgs
		result.CpuKeadaan.Ss = Segkerneldata
		result.ThreadKeadaan = Sedia
		result.CpuKeadaan.Eflags = 0x202
	} else {
		result.CpuKeadaan.Cs = SegPenggunacode
		result.CpuKeadaan.Ds = SegPenggunadata
		result.CpuKeadaan.Es = SegPenggunadata
		result.CpuKeadaan.Fs = SegPenggunadata
		result.CpuKeadaan.Gs = SegPenggunags
		result.CpuKeadaan.Ss = SegPenggunadata
		result.ThreadKeadaan = Bermula
		result.CpuKeadaan.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (diri *TThreadhelper) CreatePenudingfromFungsi(entrypoint_2 func(), Halamandirektorientry uint32, iskernel bool) *TThread {
	result := (*TThread)(diri.mem.Peruntukkan_ingatan(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = diri.CreatefromFungsi(entrypoint_2, Halamandirektorientry, iskernel)
	if result.CpuKeadaan == nil {
		diri.mem.Bebas(Pointer(result))
		return nil
	}
	return result
}
