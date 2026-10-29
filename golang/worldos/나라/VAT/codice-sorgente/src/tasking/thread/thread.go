/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "memoriamanager"
import . "virtualeMemoria"

const (
	Blocked	= 1
	Pronto	= 2
	Fermato	= 3
	Avviato	= 4
)

const ThreadstackDimensione = 32 * 1024

type TThread struct {
	CpuStato		*TcpuStato
	Stack			uint32
	Utentestack_2		uint32
	UtentestackDimensione_2	uint32
	Pid			uint32
	Genitorepid		uint32

	PAGINACartellavoce	uint32

	ThreadStato	uint8
	BlockedStato	uint8

	oradelta	uint32

	Tlssegments	[Gdtvoce]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (séstesso *TThread) Nuovo() {
}

type TThreadhelper struct {
	mem *mem.TMemoriamanager
}

var console_2 = TConsole{}

func (séstesso *TThreadhelper) Init(mem *mem.TMemoriamanager) {
	séstesso.mem = mem
	console_2.MStampaxy(([]byte)("thread:"), 1, 14)
}
func (séstesso *TThreadhelper) CreatefromFunzione(vocepoint_2 func(), PAGINACartellavoce uint32, iskernel bool) TThread {
	rISULTATO := TThread{}

	rISULTATO.Stack = uint32(uintptr(séstesso.mem.Alloca_memoria(ThreadstackDimensione)))
	if rISULTATO.Stack == 0 {
		return rISULTATO
	}
	console_2.MStampa(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Stampa(rISULTATO.Stack)

	rISULTATO.CpuStato = (*TcpuStato)(Pointer(uintptr(rISULTATO.Stack) + ThreadstackDimensione - Sizeof(TcpuStato{})))
	rISULTATO.CpuStato.Esp = rISULTATO.Stack + ThreadstackDimensione
	rISULTATO.CpuStato.Ebp = rISULTATO.CpuStato.Esp
	rISULTATO.CpuStato.Eip = uint32(ValueOf(vocepoint_2).Pointer())
	rISULTATO.Utentestack_2 = Utentestack
	rISULTATO.UtentestackDimensione_2 = UtentestackDimensione
	rISULTATO.Pid = 0
	rISULTATO.Genitorepid = 0
	rISULTATO.PAGINACartellavoce = PAGINACartellavoce
	console_2.MStampa((([]byte)("cpu")))

	console_2.MUnsignedinteger32Stampa(uint32(uintptr(Pointer(rISULTATO.CpuStato))))

	console_2.MStampa((([]byte)(":")))
	console_2.MUnsignedinteger32Stampa(rISULTATO.CpuStato.Eip)

	console_2.MStampa("]")
	if iskernel == true {
		rISULTATO.CpuStato.Cs = Segkernelcode
		rISULTATO.CpuStato.Ds = Segkerneldata
		rISULTATO.CpuStato.Es = Segkerneldata
		rISULTATO.CpuStato.Fs = Segkerneldata
		rISULTATO.CpuStato.Gs = Segkernelgs
		rISULTATO.CpuStato.Ss = Segkerneldata
		rISULTATO.ThreadStato = Pronto
		rISULTATO.CpuStato.Eflags = 0x202
	} else {
		rISULTATO.CpuStato.Cs = SegUtentecode
		rISULTATO.CpuStato.Ds = SegUtentedata
		rISULTATO.CpuStato.Es = SegUtentedata
		rISULTATO.CpuStato.Fs = SegUtentedata
		rISULTATO.CpuStato.Gs = SegUtentegs
		rISULTATO.CpuStato.Ss = SegUtentedata
		rISULTATO.ThreadStato = Avviato
		rISULTATO.CpuStato.Eflags = 0x222
	}
	rISULTATO.Iskernel = iskernel
	rISULTATO.Fpuoffset = 0xffffffff

	return rISULTATO
}

func (séstesso *TThreadhelper) CreatePuntatorefromFunzione(vocepoint_2 func(), PAGINACartellavoce uint32, iskernel bool) *TThread {
	rISULTATO := (*TThread)(séstesso.mem.Alloca_memoria(uint32(Sizeof(TThread{}))))
	if rISULTATO == nil {
		return nil
	}
	*rISULTATO = séstesso.CreatefromFunzione(vocepoint_2, PAGINACartellavoce, iskernel)
	if rISULTATO.CpuStato == nil {
		séstesso.mem.Libero(Pointer(rISULTATO))
		return nil
	}
	return rISULTATO
}
