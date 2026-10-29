/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konzole"
import . "multitasking"
import mem "paměťmanager"
import . "virtuálníPaměť"

const (
	Blocked		= 1
	Připraven	= 2
	Zastaven	= 3
	Spuštěn		= 4
)

const ThreadstackVelikost = 32 * 1024

type TThread struct {
	CpuStav			*TcpuStav
	Stack			uint32
	Uživatelstack_2		uint32
	UživatelstackVelikost_2	uint32
	Pid			uint32
	Rodičpid		uint32

	StránkaadresářZáznam	uint32

	ThreadStav	uint8
	BlockedStav	uint8

	časdelta	uint32

	Tlssegments	[GdtZáznam]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Nový() {
}

type TThreadhelper struct {
	mem *mem.TPaměťmanager
}

var konzole_2 = TKonzole{}

func (self *TThreadhelper) Init(mem *mem.TPaměťmanager) {
	self.mem = mem
	konzole_2.MTisknoutxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatezFunkce(záznampoint_2 func(), StránkaadresářZáznam uint32, iskernel bool) TThread {
	vÝSLEDEK := TThread{}

	vÝSLEDEK.Stack = uint32(uintptr(self.mem.Přidělit_paměť(ThreadstackVelikost)))
	if vÝSLEDEK.Stack == 0 {
		return vÝSLEDEK
	}
	konzole_2.MTisknout(([]byte)("[mem:"))
	konzole_2.MUnsignedinteger32Tisknout(vÝSLEDEK.Stack)

	vÝSLEDEK.CpuStav = (*TcpuStav)(Pointer(uintptr(vÝSLEDEK.Stack) + ThreadstackVelikost - Sizeof(TcpuStav{})))
	vÝSLEDEK.CpuStav.Esp = vÝSLEDEK.Stack + ThreadstackVelikost
	vÝSLEDEK.CpuStav.Ebp = vÝSLEDEK.CpuStav.Esp
	vÝSLEDEK.CpuStav.Eip = uint32(ValueOf(záznampoint_2).Pointer())
	vÝSLEDEK.Uživatelstack_2 = Uživatelstack
	vÝSLEDEK.UživatelstackVelikost_2 = UživatelstackVelikost
	vÝSLEDEK.Pid = 0
	vÝSLEDEK.Rodičpid = 0
	vÝSLEDEK.StránkaadresářZáznam = StránkaadresářZáznam
	konzole_2.MTisknout((([]byte)("cpu")))

	konzole_2.MUnsignedinteger32Tisknout(uint32(uintptr(Pointer(vÝSLEDEK.CpuStav))))

	konzole_2.MTisknout((([]byte)(":")))
	konzole_2.MUnsignedinteger32Tisknout(vÝSLEDEK.CpuStav.Eip)

	konzole_2.MTisknout("]")
	if iskernel == true {
		vÝSLEDEK.CpuStav.Cs = Segkernelcode
		vÝSLEDEK.CpuStav.Ds = Segkerneldata
		vÝSLEDEK.CpuStav.Es = Segkerneldata
		vÝSLEDEK.CpuStav.Fs = Segkerneldata
		vÝSLEDEK.CpuStav.Gs = Segkernelgs
		vÝSLEDEK.CpuStav.Ss = Segkerneldata
		vÝSLEDEK.ThreadStav = Připraven
		vÝSLEDEK.CpuStav.Eflags = 0x202
	} else {
		vÝSLEDEK.CpuStav.Cs = SegUživatelcode
		vÝSLEDEK.CpuStav.Ds = SegUživateldata
		vÝSLEDEK.CpuStav.Es = SegUživateldata
		vÝSLEDEK.CpuStav.Fs = SegUživateldata
		vÝSLEDEK.CpuStav.Gs = SegUživatelgs
		vÝSLEDEK.CpuStav.Ss = SegUživateldata
		vÝSLEDEK.ThreadStav = Spuštěn
		vÝSLEDEK.CpuStav.Eflags = 0x222
	}
	vÝSLEDEK.Iskernel = iskernel
	vÝSLEDEK.Fpuoffset = 0xffffffff

	return vÝSLEDEK
}

func (self *TThreadhelper) CreateKurzorzFunkce(záznampoint_2 func(), StránkaadresářZáznam uint32, iskernel bool) *TThread {
	vÝSLEDEK := (*TThread)(self.mem.Přidělit_paměť(uint32(Sizeof(TThread{}))))
	if vÝSLEDEK == nil {
		return nil
	}
	*vÝSLEDEK = self.CreatezFunkce(záznampoint_2, StránkaadresářZáznam, iskernel)
	if vÝSLEDEK.CpuStav == nil {
		self.mem.Volné(Pointer(vÝSLEDEK))
		return nil
	}
	return vÝSLEDEK
}
