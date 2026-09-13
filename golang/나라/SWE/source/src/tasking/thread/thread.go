package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konsol"
import . "multitasking"
import mem "minnemanager"
import . "virtuellMinne"

const (
	Blocked	= 1
	Redo	= 2
	Stoppad	= 3
	Startad	= 4
)

const ThreadstackStorlek = 32 * 1024

type TThread struct {
	ProcessorTillstånd	*TcpuTillstånd
	Stack			uint32
	Användarestack_2	uint32
	AnvändarestackStorlek_2	uint32
	Processid		uint32
	Förälderprocessid	uint32

	SidaKatalogpost	uint32

	ThreadTillstånd		uint8
	BlockedTillstånd	uint8

	tiddelta	uint32

	TlsSegment	[Gdtpost]TSegmentdescriptor
	FpuFörskjutning	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (själv *TThread) Ny() {
}

type TThreadhelper struct {
	mem *mem.TMinnemanager
}

var konsol_2 = TKonsol{}

func (själv *TThreadhelper) Init(mem *mem.TMinnemanager) {
	själv.mem = mem
	konsol_2.MSkrivutxy(([]byte)("thread:"), 1, 14)
}
func (själv *TThreadhelper) CreatefromFunktion(postpoint_2 func(), SidaKatalogpost uint32, iskernel bool) TThread {
	rESULTAT := TThread{}

	rESULTAT.Stack = uint32(uintptr(själv.mem.Tilldela_minne(ThreadstackStorlek)))
	if rESULTAT.Stack == 0 {
		return rESULTAT
	}
	konsol_2.MSkrivut(([]byte)("[mem:"))
	konsol_2.MUnsignedinteger32Skrivut(rESULTAT.Stack)

	rESULTAT.ProcessorTillstånd = (*TcpuTillstånd)(Pointer(uintptr(rESULTAT.Stack) + ThreadstackStorlek - Sizeof(TcpuTillstånd{})))
	rESULTAT.ProcessorTillstånd.Esp = rESULTAT.Stack + ThreadstackStorlek
	rESULTAT.ProcessorTillstånd.Ebp = rESULTAT.ProcessorTillstånd.Esp
	rESULTAT.ProcessorTillstånd.Eip = uint32(ValueOf(postpoint_2).Pointer())
	rESULTAT.Användarestack_2 = Användarestack
	rESULTAT.AnvändarestackStorlek_2 = AnvändarestackStorlek
	rESULTAT.Processid = 0
	rESULTAT.Förälderprocessid = 0
	rESULTAT.SidaKatalogpost = SidaKatalogpost
	konsol_2.MSkrivut((([]byte)("cpu")))

	konsol_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(rESULTAT.ProcessorTillstånd))))

	konsol_2.MSkrivut((([]byte)(":")))
	konsol_2.MUnsignedinteger32Skrivut(rESULTAT.ProcessorTillstånd.Eip)

	konsol_2.MSkrivut("]")
	if iskernel == true {
		rESULTAT.ProcessorTillstånd.Cs = Segkernelcode
		rESULTAT.ProcessorTillstånd.Ds = Segkerneldata
		rESULTAT.ProcessorTillstånd.Es = Segkerneldata
		rESULTAT.ProcessorTillstånd.Fs = Segkerneldata
		rESULTAT.ProcessorTillstånd.Gs = Segkernelgs
		rESULTAT.ProcessorTillstånd.Ss = Segkerneldata
		rESULTAT.ThreadTillstånd = Redo
		rESULTAT.ProcessorTillstånd.Eflags = 0x202
	} else {
		rESULTAT.ProcessorTillstånd.Cs = SegAnvändarecode
		rESULTAT.ProcessorTillstånd.Ds = SegAnvändaredata
		rESULTAT.ProcessorTillstånd.Es = SegAnvändaredata
		rESULTAT.ProcessorTillstånd.Fs = SegAnvändaredata
		rESULTAT.ProcessorTillstånd.Gs = SegAnvändaregs
		rESULTAT.ProcessorTillstånd.Ss = SegAnvändaredata
		rESULTAT.ThreadTillstånd = Startad
		rESULTAT.ProcessorTillstånd.Eflags = 0x222
	}
	rESULTAT.Iskernel = iskernel
	rESULTAT.FpuFörskjutning = 0xffffffff

	return rESULTAT
}

func (själv *TThreadhelper) CreateMuspekarefromFunktion(postpoint_2 func(), SidaKatalogpost uint32, iskernel bool) *TThread {
	rESULTAT := (*TThread)(själv.mem.Tilldela_minne(uint32(Sizeof(TThread{}))))
	if rESULTAT == nil {
		return nil
	}
	*rESULTAT = själv.CreatefromFunktion(postpoint_2, SidaKatalogpost, iskernel)
	if rESULTAT.ProcessorTillstånd == nil {
		själv.mem.Ledigt(Pointer(rESULTAT))
		return nil
	}
	return rESULTAT
}
