package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "bộnhớmanager"
import . "gdt"

var Thử uint8

func halt()

type TcpuTrạngthái struct {
	p1	uint32
	p2	uint32

	Eax	uint32
	Ebx	uint32
	Ecx	uint32
	Edx	uint32

	Esi	uint32
	Edi	uint32
	Ebp	uint32

	Gs	uint32
	Fs	uint32
	Es	uint32
	Ds	uint32

	Eip	uint32

	Cs	uint32
	Eflags	uint32

	Esp	uint32
	Ss	uint32
}

type TTácvụ struct {
	bộ_nhớ_ngăn_xếp		[4096]uint8
	cpuTrạngthái	*TcpuTrạngthái
}

func (mình *TTácvụ) Init(gdt *TShareddescriptorBảng, mem *mem.TBộnhớmanager, entrypoint_2 func()) {

	mình.cpuTrạngthái = (*TcpuTrạngthái)(Pointer(uintptr(mem.Cấp_phát_bộ_nhớ(1024*1024)) + 1024*1024 - Sizeof(TcpuTrạngthái{})))

	mình.cpuTrạngthái.Eax = 0
	mình.cpuTrạngthái.Ebx = 0
	mình.cpuTrạngthái.Ecx = 0
	mình.cpuTrạngthái.Edx = 0

	mình.cpuTrạngthái.Esi = 0
	mình.cpuTrạngthái.Edi = 0

	mình.cpuTrạngthái.Gs = 0
	mình.cpuTrạngthái.Fs = 0
	mình.cpuTrạngthái.Es = 0
	mình.cpuTrạngthái.Ds = 0

	mình.cpuTrạngthái.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	mình.cpuTrạngthái.Cs = Segkernelcode
	mình.cpuTrạngthái.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(mình.cpuTrạngthái)))

	mình.cpuTrạngthái.Esp = stackaddress
	mình.cpuTrạngthái.Ebp = stackaddress
	mình.cpuTrạngthái.Ss = 0

}

type TTácvụmanager struct {
}

var tácvụ_2 [256]TTácvụ
var sỐTácvụ int
var hiệnhànhTácvụ int

func (mình *TTácvụmanager) Init() {
	sỐTácvụ = 0
	hiệnhànhTácvụ = -1
}

func (mình *TTácvụmanager) ThêmTácvụ(tácvụ TTácvụ) bool {
	if sỐTácvụ >= 255 {
		return false
	}
	tácvụ_2[sỐTácvụ] = tácvụ
	sỐTácvụ++
	return true
}

func (mình *TTácvụmanager) Schedule(cpuTrạngthái *TcpuTrạngthái) *TcpuTrạngthái {

	console_2 := TConsole{}
	for i := 0; i < sỐTácvụ; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tácvụ_2[i].cpuTrạngthái)))

		console_2.MUnsignedinteger32Inxy(x, 10, uint16(15+i))
	}
	if sỐTácvụ <= 0 {
		return cpuTrạngthái
	}

	if hiệnhànhTácvụ >= 0 {
		tácvụ_2[hiệnhànhTácvụ].cpuTrạngthái = cpuTrạngthái
	}

	hiệnhànhTácvụ++
	if hiệnhànhTácvụ >= sỐTácvụ {
		hiệnhànhTácvụ %= sỐTácvụ

	}

	return tácvụ_2[hiệnhànhTácvụ].cpuTrạngthái
}
