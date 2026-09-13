package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "bộnhớmanager"
import . "ảoBộnhớ"

const (
	Blocked		= 1
	Sẵnsàng		= 2
	Bịdừng		= 3
	Đãbắtđầu	= 4
)

const ThreadstackCỡ = 32 * 1024

type TThread struct {
	CpuTrạngthái		*TcpuTrạngthái
	Stack			uint32
	Ngườidùngstack_2	uint32
	NgườidùngstackCỡ_2	uint32
	Pid			uint32
	Mẹpid			uint32

	TrangThưmụcentry	uint32

	ThreadTrạngthái		uint8
	BlockedTrạngthái	uint8

	giờdelta	uint32

	TlsĐoạn		[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (mình *TThread) Mới() {
}

type TThreadhelper struct {
	mem *mem.TBộnhớmanager
}

var console_2 = TConsole{}

func (mình *TThreadhelper) Init(mem *mem.TBộnhớmanager) {
	mình.mem = mem
	console_2.MInxy(([]byte)("thread:"), 1, 14)
}
func (mình *TThreadhelper) CreatefromHàm(entrypoint_2 func(), TrangThưmụcentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(mình.mem.Cấp_phát_bộ_nhớ(ThreadstackCỡ)))
	if result.Stack == 0 {
		return result
	}
	console_2.MIn(([]byte)("[mem:"))
	console_2.MUnsignedinteger32In(result.Stack)

	result.CpuTrạngthái = (*TcpuTrạngthái)(Pointer(uintptr(result.Stack) + ThreadstackCỡ - Sizeof(TcpuTrạngthái{})))
	result.CpuTrạngthái.Esp = result.Stack + ThreadstackCỡ
	result.CpuTrạngthái.Ebp = result.CpuTrạngthái.Esp
	result.CpuTrạngthái.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Ngườidùngstack_2 = Ngườidùngstack
	result.NgườidùngstackCỡ_2 = NgườidùngstackCỡ
	result.Pid = 0
	result.Mẹpid = 0
	result.TrangThưmụcentry = TrangThưmụcentry
	console_2.MIn((([]byte)("cpu")))

	console_2.MUnsignedinteger32In(uint32(uintptr(Pointer(result.CpuTrạngthái))))

	console_2.MIn((([]byte)(":")))
	console_2.MUnsignedinteger32In(result.CpuTrạngthái.Eip)

	console_2.MIn("]")
	if iskernel == true {
		result.CpuTrạngthái.Cs = Segkernelcode
		result.CpuTrạngthái.Ds = Segkerneldata
		result.CpuTrạngthái.Es = Segkerneldata
		result.CpuTrạngthái.Fs = Segkerneldata
		result.CpuTrạngthái.Gs = Segkernelgs
		result.CpuTrạngthái.Ss = Segkerneldata
		result.ThreadTrạngthái = Sẵnsàng
		result.CpuTrạngthái.Eflags = 0x202
	} else {
		result.CpuTrạngthái.Cs = SegNgườidùngcode
		result.CpuTrạngthái.Ds = SegNgườidùngdata
		result.CpuTrạngthái.Es = SegNgườidùngdata
		result.CpuTrạngthái.Fs = SegNgườidùngdata
		result.CpuTrạngthái.Gs = SegNgườidùnggs
		result.CpuTrạngthái.Ss = SegNgườidùngdata
		result.ThreadTrạngthái = Đãbắtđầu
		result.CpuTrạngthái.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (mình *TThreadhelper) CreateContrỏfromHàm(entrypoint_2 func(), TrangThưmụcentry uint32, iskernel bool) *TThread {
	result := (*TThread)(mình.mem.Cấp_phát_bộ_nhớ(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = mình.CreatefromHàm(entrypoint_2, TrangThưmụcentry, iskernel)
	if result.CpuTrạngthái == nil {
		mình.mem.Rảnh(Pointer(result))
		return nil
	}
	return result
}
