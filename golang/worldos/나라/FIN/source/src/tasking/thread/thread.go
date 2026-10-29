/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konsoli"
import . "multitasking"
import mem "muistimanager"
import . "virtuaalinenMuisti"

const (
	Blocked		= 1
	Valmis		= 2
	Pysäytetty	= 3
	Aloitettu	= 4
)

const ThreadstackKoko = 32 * 1024

type TThread struct {
	CpuTila			*TcpuTila
	Stack			uint32
	Käyttäjästack_2		uint32
	KäyttäjästackKoko_2	uint32
	Pid			uint32
	Vanhempipid		uint32

	SivuKansiohakusana	uint32

	ThreadTila	uint8
	BlockedTila	uint8

	aikadelta	uint32

	Tlssegments	[Gdthakusana]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (itse *TThread) Uusi() {
}

type TThreadhelper struct {
	mem *mem.TMuistimanager
}

var konsoli_2 = TKonsoli{}

func (itse *TThreadhelper) Init(mem *mem.TMuistimanager) {
	itse.mem = mem
	konsoli_2.MTulostaxy(([]byte)("thread:"), 1, 14)
}
func (itse *TThreadhelper) LuolähteestäFunktio(hakusanapoint_2 func(), SivuKansiohakusana uint32, iskernel bool) TThread {
	tULOS := TThread{}

	tULOS.Stack = uint32(uintptr(itse.mem.Varaa_muistia(ThreadstackKoko)))
	if tULOS.Stack == 0 {
		return tULOS
	}
	konsoli_2.MTulosta(([]byte)("[mem:"))
	konsoli_2.MUnsignedinteger32Tulosta(tULOS.Stack)

	tULOS.CpuTila = (*TcpuTila)(Pointer(uintptr(tULOS.Stack) + ThreadstackKoko - Sizeof(TcpuTila{})))
	tULOS.CpuTila.Esp = tULOS.Stack + ThreadstackKoko
	tULOS.CpuTila.Ebp = tULOS.CpuTila.Esp
	tULOS.CpuTila.Eip = uint32(ValueOf(hakusanapoint_2).Pointer())
	tULOS.Käyttäjästack_2 = Käyttäjästack
	tULOS.KäyttäjästackKoko_2 = KäyttäjästackKoko
	tULOS.Pid = 0
	tULOS.Vanhempipid = 0
	tULOS.SivuKansiohakusana = SivuKansiohakusana
	konsoli_2.MTulosta((([]byte)("cpu")))

	konsoli_2.MUnsignedinteger32Tulosta(uint32(uintptr(Pointer(tULOS.CpuTila))))

	konsoli_2.MTulosta((([]byte)(":")))
	konsoli_2.MUnsignedinteger32Tulosta(tULOS.CpuTila.Eip)

	konsoli_2.MTulosta("]")
	if iskernel == true {
		tULOS.CpuTila.Cs = Segkernelcode
		tULOS.CpuTila.Ds = Segkerneldata
		tULOS.CpuTila.Es = Segkerneldata
		tULOS.CpuTila.Fs = Segkerneldata
		tULOS.CpuTila.Gs = Segkernelgs
		tULOS.CpuTila.Ss = Segkerneldata
		tULOS.ThreadTila = Valmis
		tULOS.CpuTila.Eflags = 0x202
	} else {
		tULOS.CpuTila.Cs = SegKäyttäjäcode
		tULOS.CpuTila.Ds = SegKäyttäjädata
		tULOS.CpuTila.Es = SegKäyttäjädata
		tULOS.CpuTila.Fs = SegKäyttäjädata
		tULOS.CpuTila.Gs = SegKäyttäjägs
		tULOS.CpuTila.Ss = SegKäyttäjädata
		tULOS.ThreadTila = Aloitettu
		tULOS.CpuTila.Eflags = 0x222
	}
	tULOS.Iskernel = iskernel
	tULOS.Fpuoffset = 0xffffffff

	return tULOS
}

func (itse *TThreadhelper) LuoOsoitinlähteestäFunktio(hakusanapoint_2 func(), SivuKansiohakusana uint32, iskernel bool) *TThread {
	tULOS := (*TThread)(itse.mem.Varaa_muistia(uint32(Sizeof(TThread{}))))
	if tULOS == nil {
		return nil
	}
	*tULOS = itse.LuolähteestäFunktio(hakusanapoint_2, SivuKansiohakusana, iskernel)
	if tULOS.CpuTila == nil {
		itse.mem.Vapaana(Pointer(tULOS))
		return nil
	}
	return tULOS
}
