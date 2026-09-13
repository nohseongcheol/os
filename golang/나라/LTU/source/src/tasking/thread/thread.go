package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "atmintismanager"
import . "virtualiAtmintis"

const (
	Blocked		= 1
	Pasiruošęs	= 2
	Sustabdyta	= 3
	Paleista	= 4
)

const ThreadstackDydis = 32 * 1024

type TThread struct {
	CpuBūsena		*TcpuBūsena
	Stack			uint32
	Naudotojasstack_2	uint32
	NaudotojasstackDydis_2	uint32
	Pid			uint32
	Parentpid		uint32

	Puslapiskatalogasįrašas	uint32

	ThreadBūsena	uint8
	BlockedBūsena	uint8

	laikasDeltosvalstija	uint32

	Tlssegments	[Gdtįrašas]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Naujas() {
}

type TThreadhelper struct {
	mem *mem.TAtmintismanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TAtmintismanager) {
	self.mem = mem
	console_2.MSpausdintixy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatefromFunkcija(įrašaspoint_2 func(), Puslapiskatalogasįrašas uint32, iskernel bool) TThread {
	rEZULTATAS := TThread{}

	rEZULTATAS.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackDydis)))
	if rEZULTATAS.Stack == 0 {
		return rEZULTATAS
	}
	console_2.MSpausdinti(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Spausdinti(rEZULTATAS.Stack)

	rEZULTATAS.CpuBūsena = (*TcpuBūsena)(Pointer(uintptr(rEZULTATAS.Stack) + ThreadstackDydis - Sizeof(TcpuBūsena{})))
	rEZULTATAS.CpuBūsena.Esp = rEZULTATAS.Stack + ThreadstackDydis
	rEZULTATAS.CpuBūsena.Ebp = rEZULTATAS.CpuBūsena.Esp
	rEZULTATAS.CpuBūsena.Eip = uint32(ValueOf(įrašaspoint_2).Pointer())
	rEZULTATAS.Naudotojasstack_2 = Naudotojasstack
	rEZULTATAS.NaudotojasstackDydis_2 = NaudotojasstackDydis
	rEZULTATAS.Pid = 0
	rEZULTATAS.Parentpid = 0
	rEZULTATAS.Puslapiskatalogasįrašas = Puslapiskatalogasįrašas
	console_2.MSpausdinti((([]byte)("cpu")))

	console_2.MUnsignedinteger32Spausdinti(uint32(uintptr(Pointer(rEZULTATAS.CpuBūsena))))

	console_2.MSpausdinti((([]byte)(":")))
	console_2.MUnsignedinteger32Spausdinti(rEZULTATAS.CpuBūsena.Eip)

	console_2.MSpausdinti("]")
	if iskernel == true {
		rEZULTATAS.CpuBūsena.Cs = Segkernelcode
		rEZULTATAS.CpuBūsena.Ds = Segkerneldata
		rEZULTATAS.CpuBūsena.Es = Segkerneldata
		rEZULTATAS.CpuBūsena.Fs = Segkerneldata
		rEZULTATAS.CpuBūsena.Gs = Segkernelgs
		rEZULTATAS.CpuBūsena.Ss = Segkerneldata
		rEZULTATAS.ThreadBūsena = Pasiruošęs
		rEZULTATAS.CpuBūsena.Eflags = 0x202
	} else {
		rEZULTATAS.CpuBūsena.Cs = SegNaudotojascode
		rEZULTATAS.CpuBūsena.Ds = SegNaudotojasdata
		rEZULTATAS.CpuBūsena.Es = SegNaudotojasdata
		rEZULTATAS.CpuBūsena.Fs = SegNaudotojasdata
		rEZULTATAS.CpuBūsena.Gs = SegNaudotojasgs
		rEZULTATAS.CpuBūsena.Ss = SegNaudotojasdata
		rEZULTATAS.ThreadBūsena = Paleista
		rEZULTATAS.CpuBūsena.Eflags = 0x222
	}
	rEZULTATAS.Iskernel = iskernel
	rEZULTATAS.Fpuoffset = 0xffffffff

	return rEZULTATAS
}

func (self *TThreadhelper) CreateRodyklėfromFunkcija(įrašaspoint_2 func(), Puslapiskatalogasįrašas uint32, iskernel bool) *TThread {
	rEZULTATAS := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if rEZULTATAS == nil {
		return nil
	}
	*rEZULTATAS = self.CreatefromFunkcija(įrašaspoint_2, Puslapiskatalogasįrašas, iskernel)
	if rEZULTATAS.CpuBūsena == nil {
		self.mem.Laisva(Pointer(rEZULTATAS))
		return nil
	}
	return rEZULTATAS
}
