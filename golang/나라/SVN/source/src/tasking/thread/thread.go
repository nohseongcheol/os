/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "pomnilnikmanager"
import . "navideznoPomnilnik"

const (
	Blocked		= 1
	Pripravljen	= 2
	Zaustavljeno	= 3
	Začeto		= 4
)

const ThreadstackVelikost = 32 * 1024

type TThread struct {
	CPEStanje			*TcpuStanje
	Stack				uint32
	Uporabnikstack_2		uint32
	UporabnikstackVelikost_2	uint32
	Pid				uint32
	Nadrejenipredmetpid		uint32

	StranMapavnos	uint32

	ThreadStanje	uint8
	BlockedStanje	uint8

	časdelta	uint32

	Tlssegments	[Gdtvnos]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (sam *TThread) Nova() {
}

type TThreadhelper struct {
	mem *mem.TPomnilnikmanager
}

var console_2 = TConsole{}

func (sam *TThreadhelper) Init(mem *mem.TPomnilnikmanager) {
	sam.mem = mem
	console_2.MNatisnixy(([]byte)("thread:"), 1, 14)
}
func (sam *TThreadhelper) CreatefromFunkcija(vnospoint_2 func(), StranMapavnos uint32, iskernel bool) TThread {
	rEZULTAT := TThread{}

	rEZULTAT.Stack = uint32(uintptr(sam.mem.Malloc(ThreadstackVelikost)))
	if rEZULTAT.Stack == 0 {
		return rEZULTAT
	}
	console_2.MNatisni(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Natisni(rEZULTAT.Stack)

	rEZULTAT.CPEStanje = (*TcpuStanje)(Pointer(uintptr(rEZULTAT.Stack) + ThreadstackVelikost - Sizeof(TcpuStanje{})))
	rEZULTAT.CPEStanje.Esp = rEZULTAT.Stack + ThreadstackVelikost
	rEZULTAT.CPEStanje.Ebp = rEZULTAT.CPEStanje.Esp
	rEZULTAT.CPEStanje.Eip = uint32(ValueOf(vnospoint_2).Pointer())
	rEZULTAT.Uporabnikstack_2 = Uporabnikstack
	rEZULTAT.UporabnikstackVelikost_2 = UporabnikstackVelikost
	rEZULTAT.Pid = 0
	rEZULTAT.Nadrejenipredmetpid = 0
	rEZULTAT.StranMapavnos = StranMapavnos
	console_2.MNatisni((([]byte)("cpu")))

	console_2.MUnsignedinteger32Natisni(uint32(uintptr(Pointer(rEZULTAT.CPEStanje))))

	console_2.MNatisni((([]byte)(":")))
	console_2.MUnsignedinteger32Natisni(rEZULTAT.CPEStanje.Eip)

	console_2.MNatisni("]")
	if iskernel == true {
		rEZULTAT.CPEStanje.Cs = Segkernelcode
		rEZULTAT.CPEStanje.Ds = Segkerneldata
		rEZULTAT.CPEStanje.Es = Segkerneldata
		rEZULTAT.CPEStanje.Fs = Segkerneldata
		rEZULTAT.CPEStanje.Gs = Segkernelgs
		rEZULTAT.CPEStanje.Ss = Segkerneldata
		rEZULTAT.ThreadStanje = Pripravljen
		rEZULTAT.CPEStanje.Eflags = 0x202
	} else {
		rEZULTAT.CPEStanje.Cs = SegUporabnikcode
		rEZULTAT.CPEStanje.Ds = SegUporabnikdata
		rEZULTAT.CPEStanje.Es = SegUporabnikdata
		rEZULTAT.CPEStanje.Fs = SegUporabnikdata
		rEZULTAT.CPEStanje.Gs = SegUporabnikgs
		rEZULTAT.CPEStanje.Ss = SegUporabnikdata
		rEZULTAT.ThreadStanje = Začeto
		rEZULTAT.CPEStanje.Eflags = 0x222
	}
	rEZULTAT.Iskernel = iskernel
	rEZULTAT.Fpuoffset = 0xffffffff

	return rEZULTAT
}

func (sam *TThreadhelper) CreateKazalnikfromFunkcija(vnospoint_2 func(), StranMapavnos uint32, iskernel bool) *TThread {
	rEZULTAT := (*TThread)(sam.mem.Malloc(uint32(Sizeof(TThread{}))))
	if rEZULTAT == nil {
		return nil
	}
	*rEZULTAT = sam.CreatefromFunkcija(vnospoint_2, StranMapavnos, iskernel)
	if rEZULTAT.CPEStanje == nil {
		sam.mem.Prosto(Pointer(rEZULTAT))
		return nil
	}
	return rEZULTAT
}
