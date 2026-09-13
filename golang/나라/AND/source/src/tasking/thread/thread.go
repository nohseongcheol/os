package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "consola"
import . "multitasking"
import mem "memòriamanager"
import . "virtualMemòria"

const (
	Blocked		= 1
	Preparat	= 2
	Aturat		= 3
	Iniciat		= 4
)

const ThreadstackMida = 32 * 1024

type TThread struct {
	CpuEstat		*TcpuEstat
	Stack			uint32
	Usuaristack_2		uint32
	UsuaristackMida_2	uint32
	Pid			uint32
	Parepid			uint32

	PàginaDirectorientrada	uint32

	ThreadEstat	uint8
	BlockedEstat	uint8

	horadelta	uint32

	Tlssegments	[Gdtentrada]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (unmateix *TThread) Nou() {
}

type TThreadhelper struct {
	mem *mem.TMemòriamanager
}

var consola_2 = TConsola{}

func (unmateix *TThreadhelper) Init(mem *mem.TMemòriamanager) {
	unmateix.mem = mem
	consola_2.MImprimeixxy(([]byte)("thread:"), 1, 14)
}
func (unmateix *TThreadhelper) CreatedesdeFunció(entradapoint_2 func(), PàginaDirectorientrada uint32, iskernel bool) TThread {
	rESULTAT := TThread{}

	rESULTAT.Stack = uint32(uintptr(unmateix.mem.Malloc(ThreadstackMida)))
	if rESULTAT.Stack == 0 {
		return rESULTAT
	}
	consola_2.MImprimeix(([]byte)("[mem:"))
	consola_2.MUnsignedinteger32Imprimeix(rESULTAT.Stack)

	rESULTAT.CpuEstat = (*TcpuEstat)(Pointer(uintptr(rESULTAT.Stack) + ThreadstackMida - Sizeof(TcpuEstat{})))
	rESULTAT.CpuEstat.Esp = rESULTAT.Stack + ThreadstackMida
	rESULTAT.CpuEstat.Ebp = rESULTAT.CpuEstat.Esp
	rESULTAT.CpuEstat.Eip = uint32(ValueOf(entradapoint_2).Pointer())
	rESULTAT.Usuaristack_2 = Usuaristack
	rESULTAT.UsuaristackMida_2 = UsuaristackMida
	rESULTAT.Pid = 0
	rESULTAT.Parepid = 0
	rESULTAT.PàginaDirectorientrada = PàginaDirectorientrada
	consola_2.MImprimeix((([]byte)("cpu")))

	consola_2.MUnsignedinteger32Imprimeix(uint32(uintptr(Pointer(rESULTAT.CpuEstat))))

	consola_2.MImprimeix((([]byte)(":")))
	consola_2.MUnsignedinteger32Imprimeix(rESULTAT.CpuEstat.Eip)

	consola_2.MImprimeix("]")
	if iskernel == true {
		rESULTAT.CpuEstat.Cs = Segkernelcode
		rESULTAT.CpuEstat.Ds = Segkerneldata
		rESULTAT.CpuEstat.Es = Segkerneldata
		rESULTAT.CpuEstat.Fs = Segkerneldata
		rESULTAT.CpuEstat.Gs = Segkernelgs
		rESULTAT.CpuEstat.Ss = Segkerneldata
		rESULTAT.ThreadEstat = Preparat
		rESULTAT.CpuEstat.Eflags = 0x202
	} else {
		rESULTAT.CpuEstat.Cs = SegUsuaricode
		rESULTAT.CpuEstat.Ds = SegUsuaridata
		rESULTAT.CpuEstat.Es = SegUsuaridata
		rESULTAT.CpuEstat.Fs = SegUsuaridata
		rESULTAT.CpuEstat.Gs = SegUsuarigs
		rESULTAT.CpuEstat.Ss = SegUsuaridata
		rESULTAT.ThreadEstat = Iniciat
		rESULTAT.CpuEstat.Eflags = 0x222
	}
	rESULTAT.Iskernel = iskernel
	rESULTAT.Fpuoffset = 0xffffffff

	return rESULTAT
}

func (unmateix *TThreadhelper) CreatePunterdesdeFunció(entradapoint_2 func(), PàginaDirectorientrada uint32, iskernel bool) *TThread {
	rESULTAT := (*TThread)(unmateix.mem.Malloc(uint32(Sizeof(TThread{}))))
	if rESULTAT == nil {
		return nil
	}
	*rESULTAT = unmateix.CreatedesdeFunció(entradapoint_2, PàginaDirectorientrada, iskernel)
	if rESULTAT.CpuEstat == nil {
		unmateix.mem.Lliure(Pointer(rESULTAT))
		return nil
	}
	return rESULTAT
}
