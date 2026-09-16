/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konsol"
import . "multitasking"
import mem "bellekmanager"
import . "sanalBellek"

const (
	Blocked		= 1
	Hazır		= 2
	Durdurulmuş	= 3
	Başlamış	= 4
)

const ThreadstackBoyut = 32 * 1024

type TThread struct {
	MİBDurum		*TcpuDurum
	Stack			uint32
	Kullanıcıstack_2	uint32
	KullanıcıstackBoyut_2	uint32
	Pid			uint32
	Üstpid			uint32

	SayfaDizingirdi	uint32

	ThreadDurum	uint8
	BlockedDurum	uint8

	saatdelta	uint32

	Tlssegments	[Gdtgirdi]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Yeni() {
}

type TThreadhelper struct {
	mem *mem.TBellekmanager
}

var konsol_2 = TKonsol{}

func (self *TThreadhelper) Init(mem *mem.TBellekmanager) {
	self.mem = mem
	konsol_2.MYazdırxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatefromFonksiyon(girdipoint_2 func(), SayfaDizingirdi uint32, iskernel bool) TThread {
	sONUÇ := TThread{}

	sONUÇ.Stack = uint32(uintptr(self.mem.Bellek_ayır(ThreadstackBoyut)))
	if sONUÇ.Stack == 0 {
		return sONUÇ
	}
	konsol_2.MYazdır(([]byte)("[mem:"))
	konsol_2.MUnsignedinteger32Yazdır(sONUÇ.Stack)

	sONUÇ.MİBDurum = (*TcpuDurum)(Pointer(uintptr(sONUÇ.Stack) + ThreadstackBoyut - Sizeof(TcpuDurum{})))
	sONUÇ.MİBDurum.Esp = sONUÇ.Stack + ThreadstackBoyut
	sONUÇ.MİBDurum.Ebp = sONUÇ.MİBDurum.Esp
	sONUÇ.MİBDurum.Eip = uint32(ValueOf(girdipoint_2).Pointer())
	sONUÇ.Kullanıcıstack_2 = Kullanıcıstack
	sONUÇ.KullanıcıstackBoyut_2 = KullanıcıstackBoyut
	sONUÇ.Pid = 0
	sONUÇ.Üstpid = 0
	sONUÇ.SayfaDizingirdi = SayfaDizingirdi
	konsol_2.MYazdır((([]byte)("cpu")))

	konsol_2.MUnsignedinteger32Yazdır(uint32(uintptr(Pointer(sONUÇ.MİBDurum))))

	konsol_2.MYazdır((([]byte)(":")))
	konsol_2.MUnsignedinteger32Yazdır(sONUÇ.MİBDurum.Eip)

	konsol_2.MYazdır("]")
	if iskernel == true {
		sONUÇ.MİBDurum.Cs = Segkernelcode
		sONUÇ.MİBDurum.Ds = Segkerneldata
		sONUÇ.MİBDurum.Es = Segkerneldata
		sONUÇ.MİBDurum.Fs = Segkerneldata
		sONUÇ.MİBDurum.Gs = Segkernelgs
		sONUÇ.MİBDurum.Ss = Segkerneldata
		sONUÇ.ThreadDurum = Hazır
		sONUÇ.MİBDurum.Eflags = 0x202
	} else {
		sONUÇ.MİBDurum.Cs = SegKullanıcıcode
		sONUÇ.MİBDurum.Ds = SegKullanıcıdata
		sONUÇ.MİBDurum.Es = SegKullanıcıdata
		sONUÇ.MİBDurum.Fs = SegKullanıcıdata
		sONUÇ.MİBDurum.Gs = SegKullanıcıgs
		sONUÇ.MİBDurum.Ss = SegKullanıcıdata
		sONUÇ.ThreadDurum = Başlamış
		sONUÇ.MİBDurum.Eflags = 0x222
	}
	sONUÇ.Iskernel = iskernel
	sONUÇ.Fpuoffset = 0xffffffff

	return sONUÇ
}

func (self *TThreadhelper) CreateBelirteçfromFonksiyon(girdipoint_2 func(), SayfaDizingirdi uint32, iskernel bool) *TThread {
	sONUÇ := (*TThread)(self.mem.Bellek_ayır(uint32(Sizeof(TThread{}))))
	if sONUÇ == nil {
		return nil
	}
	*sONUÇ = self.CreatefromFonksiyon(girdipoint_2, SayfaDizingirdi, iskernel)
	if sONUÇ.MİBDurum == nil {
		self.mem.Boş(Pointer(sONUÇ))
		return nil
	}
	return sONUÇ
}
