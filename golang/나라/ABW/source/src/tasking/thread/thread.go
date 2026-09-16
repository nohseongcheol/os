/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "geheugenmanager"
import . "virtueelGeheugen"

const (
	Blocked		= 1
	Klaar		= 2
	Gestaakt	= 3
	Gestart		= 4
)

const ThreadstackGrootte = 32 * 1024

type TThread struct {
	CpuStatus		*TcpuStatus
	Stack			uint32
	Gebruikerstack_2	uint32
	GebruikerstackGrootte_2	uint32
	Pid			uint32
	Ouderpid		uint32

	PaginaMapItem	uint32

	ThreadStatus	uint8
	BlockedStatus	uint8

	tijddelta	uint32

	TlsSegmenten	[GdtItem]TSegmentdescriptor
	FpuVerschuiving	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (zelf *TThread) Nieuw() {
}

type TThreadhelper struct {
	mem *mem.TGeheugenmanager
}

var console_2 = TConsole{}

func (zelf *TThreadhelper) Init(mem *mem.TGeheugenmanager) {
	zelf.mem = mem
	console_2.MAfdrukkenxy(([]byte)("thread:"), 1, 14)
}
func (zelf *TThreadhelper) CreatevanFunctie(itempoint_2 func(), PaginaMapItem uint32, iskernel bool) TThread {
	rESULTAAT := TThread{}

	rESULTAAT.Stack = uint32(uintptr(zelf.mem.Geheugen_toewijzen(ThreadstackGrootte)))
	if rESULTAAT.Stack == 0 {
		return rESULTAAT
	}
	console_2.MAfdrukken(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Afdrukken(rESULTAAT.Stack)

	rESULTAAT.CpuStatus = (*TcpuStatus)(Pointer(uintptr(rESULTAAT.Stack) + ThreadstackGrootte - Sizeof(TcpuStatus{})))
	rESULTAAT.CpuStatus.Esp = rESULTAAT.Stack + ThreadstackGrootte
	rESULTAAT.CpuStatus.Ebp = rESULTAAT.CpuStatus.Esp
	rESULTAAT.CpuStatus.Eip = uint32(ValueOf(itempoint_2).Pointer())
	rESULTAAT.Gebruikerstack_2 = Gebruikerstack
	rESULTAAT.GebruikerstackGrootte_2 = GebruikerstackGrootte
	rESULTAAT.Pid = 0
	rESULTAAT.Ouderpid = 0
	rESULTAAT.PaginaMapItem = PaginaMapItem
	console_2.MAfdrukken((([]byte)("cpu")))

	console_2.MUnsignedinteger32Afdrukken(uint32(uintptr(Pointer(rESULTAAT.CpuStatus))))

	console_2.MAfdrukken((([]byte)(":")))
	console_2.MUnsignedinteger32Afdrukken(rESULTAAT.CpuStatus.Eip)

	console_2.MAfdrukken("]")
	if iskernel == true {
		rESULTAAT.CpuStatus.Cs = Segkernelcode
		rESULTAAT.CpuStatus.Ds = Segkerneldata
		rESULTAAT.CpuStatus.Es = Segkerneldata
		rESULTAAT.CpuStatus.Fs = Segkerneldata
		rESULTAAT.CpuStatus.Gs = Segkernelgs
		rESULTAAT.CpuStatus.Ss = Segkerneldata
		rESULTAAT.ThreadStatus = Klaar
		rESULTAAT.CpuStatus.Eflags = 0x202
	} else {
		rESULTAAT.CpuStatus.Cs = SegGebruikercode
		rESULTAAT.CpuStatus.Ds = SegGebruikerdata
		rESULTAAT.CpuStatus.Es = SegGebruikerdata
		rESULTAAT.CpuStatus.Fs = SegGebruikerdata
		rESULTAAT.CpuStatus.Gs = SegGebruikergs
		rESULTAAT.CpuStatus.Ss = SegGebruikerdata
		rESULTAAT.ThreadStatus = Gestart
		rESULTAAT.CpuStatus.Eflags = 0x222
	}
	rESULTAAT.Iskernel = iskernel
	rESULTAAT.FpuVerschuiving = 0xffffffff

	return rESULTAAT
}

func (zelf *TThreadhelper) CreateMuisaanwijzervanFunctie(itempoint_2 func(), PaginaMapItem uint32, iskernel bool) *TThread {
	rESULTAAT := (*TThread)(zelf.mem.Geheugen_toewijzen(uint32(Sizeof(TThread{}))))
	if rESULTAAT == nil {
		return nil
	}
	*rESULTAAT = zelf.CreatevanFunctie(itempoint_2, PaginaMapItem, iskernel)
	if rESULTAAT.CpuStatus == nil {
		zelf.mem.Vrij(Pointer(rESULTAAT))
		return nil
	}
	return rESULTAAT
}
