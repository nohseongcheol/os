/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "mälumanager"
import . "virtuaalMälu"

const (
	Blocked		= 1
	Valmis		= 2
	Seisatud	= 3
	Käivitatud	= 4
)

const ThreadstackSuurus = 32 * 1024

type TThread struct {
	ProtsessorOlek		*TcpuOlek
	Stack			uint32
	Kasutajastack_2		uint32
	KasutajastackSuurus_2	uint32
	Pid			uint32
	Vanempid		uint32

	LehekülgKataloogkirje	uint32

	ThreadOlek	uint8
	BlockedOlek	uint8

	aegdelta	uint32

	Tlssegments	[Gdtkirje]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (ise *TThread) Uus() {
}

type TThreadhelper struct {
	mem *mem.TMälumanager
}

var console_2 = TConsole{}

func (ise *TThreadhelper) Init(mem *mem.TMälumanager) {
	ise.mem = mem
	console_2.MPrindixy(([]byte)("thread:"), 1, 14)
}
func (ise *TThreadhelper) CreatefromFunktsioon(kirjepoint_2 func(), LehekülgKataloogkirje uint32, iskernel bool) TThread {
	tULEMUS := TThread{}

	tULEMUS.Stack = uint32(uintptr(ise.mem.Malloc(ThreadstackSuurus)))
	if tULEMUS.Stack == 0 {
		return tULEMUS
	}
	console_2.MPrindi(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Prindi(tULEMUS.Stack)

	tULEMUS.ProtsessorOlek = (*TcpuOlek)(Pointer(uintptr(tULEMUS.Stack) + ThreadstackSuurus - Sizeof(TcpuOlek{})))
	tULEMUS.ProtsessorOlek.Esp = tULEMUS.Stack + ThreadstackSuurus
	tULEMUS.ProtsessorOlek.Ebp = tULEMUS.ProtsessorOlek.Esp
	tULEMUS.ProtsessorOlek.Eip = uint32(ValueOf(kirjepoint_2).Pointer())
	tULEMUS.Kasutajastack_2 = Kasutajastack
	tULEMUS.KasutajastackSuurus_2 = KasutajastackSuurus
	tULEMUS.Pid = 0
	tULEMUS.Vanempid = 0
	tULEMUS.LehekülgKataloogkirje = LehekülgKataloogkirje
	console_2.MPrindi((([]byte)("cpu")))

	console_2.MUnsignedinteger32Prindi(uint32(uintptr(Pointer(tULEMUS.ProtsessorOlek))))

	console_2.MPrindi((([]byte)(":")))
	console_2.MUnsignedinteger32Prindi(tULEMUS.ProtsessorOlek.Eip)

	console_2.MPrindi("]")
	if iskernel == true {
		tULEMUS.ProtsessorOlek.Cs = Segkernelcode
		tULEMUS.ProtsessorOlek.Ds = Segkerneldata
		tULEMUS.ProtsessorOlek.Es = Segkerneldata
		tULEMUS.ProtsessorOlek.Fs = Segkerneldata
		tULEMUS.ProtsessorOlek.Gs = Segkernelgs
		tULEMUS.ProtsessorOlek.Ss = Segkerneldata
		tULEMUS.ThreadOlek = Valmis
		tULEMUS.ProtsessorOlek.Eflags = 0x202
	} else {
		tULEMUS.ProtsessorOlek.Cs = SegKasutajacode
		tULEMUS.ProtsessorOlek.Ds = SegKasutajadata
		tULEMUS.ProtsessorOlek.Es = SegKasutajadata
		tULEMUS.ProtsessorOlek.Fs = SegKasutajadata
		tULEMUS.ProtsessorOlek.Gs = SegKasutajags
		tULEMUS.ProtsessorOlek.Ss = SegKasutajadata
		tULEMUS.ThreadOlek = Käivitatud
		tULEMUS.ProtsessorOlek.Eflags = 0x222
	}
	tULEMUS.Iskernel = iskernel
	tULEMUS.Fpuoffset = 0xffffffff

	return tULEMUS
}

func (ise *TThreadhelper) CreateKursorfromFunktsioon(kirjepoint_2 func(), LehekülgKataloogkirje uint32, iskernel bool) *TThread {
	tULEMUS := (*TThread)(ise.mem.Malloc(uint32(Sizeof(TThread{}))))
	if tULEMUS == nil {
		return nil
	}
	*tULEMUS = ise.CreatefromFunktsioon(kirjepoint_2, LehekülgKataloogkirje, iskernel)
	if tULEMUS.ProtsessorOlek == nil {
		ise.mem.Vaba(Pointer(tULEMUS))
		return nil
	}
	return tULEMUS
}
