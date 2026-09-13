package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "memorijamanager"
import . "virtuelnoMemorija"

const (
	Blocked		= 1
	Ready		= 2
	Zaustavljeno	= 3
	Started		= 4
)

const ThreadstackVeličina = 32 * 1024

type TThread struct {
	Cpustate		*Tcpustate
	Stack			uint32
	Korisnikstack_2		uint32
	KorisnikstackVeličina_2	uint32
	Pid			uint32
	Parentpid		uint32

	StranicaDirektorijunos	uint32

	Threadstate	uint8
	Blockedstate	uint8

	vrijemedelta	uint32

	Tlssegments	[Gdtunos]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Nova() {
}

type TThreadhelper struct {
	mem *mem.TMemorijamanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TMemorijamanager) {
	self.mem = mem
	console_2.MŠtampajxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatefromFunkcija(unospoint_2 func(), StranicaDirektorijunos uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackVeličina)))
	if result.Stack == 0 {
		return result
	}
	console_2.MŠtampaj(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Štampaj(result.Stack)

	result.Cpustate = (*Tcpustate)(Pointer(uintptr(result.Stack) + ThreadstackVeličina - Sizeof(Tcpustate{})))
	result.Cpustate.Esp = result.Stack + ThreadstackVeličina
	result.Cpustate.Ebp = result.Cpustate.Esp
	result.Cpustate.Eip = uint32(ValueOf(unospoint_2).Pointer())
	result.Korisnikstack_2 = Korisnikstack
	result.KorisnikstackVeličina_2 = KorisnikstackVeličina
	result.Pid = 0
	result.Parentpid = 0
	result.StranicaDirektorijunos = StranicaDirektorijunos
	console_2.MŠtampaj((([]byte)("cpu")))

	console_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(result.Cpustate))))

	console_2.MŠtampaj((([]byte)(":")))
	console_2.MUnsignedinteger32Štampaj(result.Cpustate.Eip)

	console_2.MŠtampaj("]")
	if iskernel == true {
		result.Cpustate.Cs = Segkernelcode
		result.Cpustate.Ds = Segkerneldata
		result.Cpustate.Es = Segkerneldata
		result.Cpustate.Fs = Segkerneldata
		result.Cpustate.Gs = Segkernelgs
		result.Cpustate.Ss = Segkerneldata
		result.Threadstate = Ready
		result.Cpustate.Eflags = 0x202
	} else {
		result.Cpustate.Cs = SegKorisnikcode
		result.Cpustate.Ds = SegKorisnikdata
		result.Cpustate.Es = SegKorisnikdata
		result.Cpustate.Fs = SegKorisnikdata
		result.Cpustate.Gs = SegKorisnikgs
		result.Cpustate.Ss = SegKorisnikdata
		result.Threadstate = Started
		result.Cpustate.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) CreatepointerfromFunkcija(unospoint_2 func(), StranicaDirektorijunos uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.CreatefromFunkcija(unospoint_2, StranicaDirektorijunos, iskernel)
	if result.Cpustate == nil {
		self.mem.Slobodno(Pointer(result))
		return nil
	}
	return result
}
