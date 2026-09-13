package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "конзола"
import . "multitasking"
import mem "memorijamanager"
import . "virtuelnoMemorija"

const (
	Blocked		= 1
	Спреман		= 2
	Заустављен	= 3
	Započet		= 4
)

const ThreadstackВеличина = 32 * 1024

type TThread struct {
	ПроцесорСтање		*TcpuСтање
	Stack			uint32
	Korisnikstack_2		uint32
	KorisnikstackВеличина_2	uint32
	ПИД			uint32
	NadređeniПИД		uint32

	ListDirektorijumунос	uint32

	ThreadСтање	uint8
	BlockedСтање	uint8

	времеДелта	uint32

	Tlssegments	[Gdtунос]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (isti *TThread) Нова() {
}

type TThreadhelper struct {
	mem *mem.TMemorijamanager
}

var конзола_2 = TКонзола{}

func (isti *TThreadhelper) Init(mem *mem.TMemorijamanager) {
	isti.mem = mem
	конзола_2.MŠtampajxy(([]byte)("thread:"), 1, 14)
}
func (isti *TThreadhelper) Createsaфункција(уносpoint_2 func(), ListDirektorijumунос uint32, iskernel bool) TThread {
	иСХОД := TThread{}

	иСХОД.Stack = uint32(uintptr(isti.mem.Malloc(ThreadstackВеличина)))
	if иСХОД.Stack == 0 {
		return иСХОД
	}
	конзола_2.MŠtampaj(([]byte)("[mem:"))
	конзола_2.MUnsignedinteger32Štampaj(иСХОД.Stack)

	иСХОД.ПроцесорСтање = (*TcpuСтање)(Pointer(uintptr(иСХОД.Stack) + ThreadstackВеличина - Sizeof(TcpuСтање{})))
	иСХОД.ПроцесорСтање.Esp = иСХОД.Stack + ThreadstackВеличина
	иСХОД.ПроцесорСтање.Ebp = иСХОД.ПроцесорСтање.Esp
	иСХОД.ПроцесорСтање.Eip = uint32(ValueOf(уносpoint_2).Pointer())
	иСХОД.Korisnikstack_2 = Korisnikstack
	иСХОД.KorisnikstackВеличина_2 = KorisnikstackВеличина
	иСХОД.ПИД = 0
	иСХОД.NadređeniПИД = 0
	иСХОД.ListDirektorijumунос = ListDirektorijumунос
	конзола_2.MŠtampaj((([]byte)("cpu")))

	конзола_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(иСХОД.ПроцесорСтање))))

	конзола_2.MŠtampaj((([]byte)(":")))
	конзола_2.MUnsignedinteger32Štampaj(иСХОД.ПроцесорСтање.Eip)

	конзола_2.MŠtampaj("]")
	if iskernel == true {
		иСХОД.ПроцесорСтање.Cs = Segkernelcode
		иСХОД.ПроцесорСтање.Ds = Segkerneldata
		иСХОД.ПроцесорСтање.Es = Segkerneldata
		иСХОД.ПроцесорСтање.Fs = Segkerneldata
		иСХОД.ПроцесорСтање.Gs = Segkernelgs
		иСХОД.ПроцесорСтање.Ss = Segkerneldata
		иСХОД.ThreadСтање = Спреман
		иСХОД.ПроцесорСтање.Eflags = 0x202
	} else {
		иСХОД.ПроцесорСтање.Cs = SegKorisnikcode
		иСХОД.ПроцесорСтање.Ds = SegKorisnikdata
		иСХОД.ПроцесорСтање.Es = SegKorisnikdata
		иСХОД.ПроцесорСтање.Fs = SegKorisnikdata
		иСХОД.ПроцесорСтање.Gs = SegKorisnikgs
		иСХОД.ПроцесорСтање.Ss = SegKorisnikdata
		иСХОД.ThreadСтање = Započet
		иСХОД.ПроцесорСтање.Eflags = 0x222
	}
	иСХОД.Iskernel = iskernel
	иСХОД.Fpuoffset = 0xffffffff

	return иСХОД
}

func (isti *TThreadhelper) CreatePokazivačsaфункција(уносpoint_2 func(), ListDirektorijumунос uint32, iskernel bool) *TThread {
	иСХОД := (*TThread)(isti.mem.Malloc(uint32(Sizeof(TThread{}))))
	if иСХОД == nil {
		return nil
	}
	*иСХОД = isti.Createsaфункција(уносpoint_2, ListDirektorijumунос, iskernel)
	if иСХОД.ПроцесорСтање == nil {
		isti.mem.Slobodno(Pointer(иСХОД))
		return nil
	}
	return иСХОД
}
