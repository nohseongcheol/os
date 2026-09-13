package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konzola"
import . "multitasking"
import mem "memorijamanager"
import . "virtuelnoMemorija"

const (
	Blocked		= 1
	Spreman		= 2
	Zaustavljen	= 3
	Pokrenut		= 4
)

const ThreadstackVeličina = 32 * 1024

type TThread struct {
	ProcesorStanje		*TcpuStanje
	Stack			uint32
	Korisnikstack_2		uint32
	KorisnikstackVeličina_2	uint32
	PID			uint32
	NadređeniPID		uint32

	STRANADirektorijumunos	uint32

	ThreadStanje	uint8
	BlockedStanje	uint8

	vremeDelta	uint32

	Tlssegments	[Gdtunos]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (isti *TThread) Nova() {
}

type TThreadhelper struct {
	mem *mem.TMemorijamanager
}

var konzola_2 = TKonzola{}

func (isti *TThreadhelper) Init(mem *mem.TMemorijamanager) {
	isti.mem = mem
	konzola_2.MŠtampajxy(([]byte)("thread:"), 1, 14)
}
func (isti *TThreadhelper) Createsafunkcija(unospoint_2 func(), STRANADirektorijumunos uint32, iskernel bool) TThread {
	iSHOD := TThread{}

	iSHOD.Stack = uint32(uintptr(isti.mem.Malloc(ThreadstackVeličina)))
	if iSHOD.Stack == 0 {
		return iSHOD
	}
	konzola_2.MŠtampaj(([]byte)("[mem:"))
	konzola_2.MUnsignedinteger32Štampaj(iSHOD.Stack)

	iSHOD.ProcesorStanje = (*TcpuStanje)(Pointer(uintptr(iSHOD.Stack) + ThreadstackVeličina - Sizeof(TcpuStanje{})))
	iSHOD.ProcesorStanje.Esp = iSHOD.Stack + ThreadstackVeličina
	iSHOD.ProcesorStanje.Ebp = iSHOD.ProcesorStanje.Esp
	iSHOD.ProcesorStanje.Eip = uint32(ValueOf(unospoint_2).Pointer())
	iSHOD.Korisnikstack_2 = Korisnikstack
	iSHOD.KorisnikstackVeličina_2 = KorisnikstackVeličina
	iSHOD.PID = 0
	iSHOD.NadređeniPID = 0
	iSHOD.STRANADirektorijumunos = STRANADirektorijumunos
	konzola_2.MŠtampaj((([]byte)("cpu")))

	konzola_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(iSHOD.ProcesorStanje))))

	konzola_2.MŠtampaj((([]byte)(":")))
	konzola_2.MUnsignedinteger32Štampaj(iSHOD.ProcesorStanje.Eip)

	konzola_2.MŠtampaj("]")
	if iskernel == true {
		iSHOD.ProcesorStanje.Cs = Segkernelcode
		iSHOD.ProcesorStanje.Ds = Segkerneldata
		iSHOD.ProcesorStanje.Es = Segkerneldata
		iSHOD.ProcesorStanje.Fs = Segkerneldata
		iSHOD.ProcesorStanje.Gs = Segkernelgs
		iSHOD.ProcesorStanje.Ss = Segkerneldata
		iSHOD.ThreadStanje = Spreman
		iSHOD.ProcesorStanje.Eflags = 0x202
	} else {
		iSHOD.ProcesorStanje.Cs = SegKorisnikcode
		iSHOD.ProcesorStanje.Ds = SegKorisnikdata
		iSHOD.ProcesorStanje.Es = SegKorisnikdata
		iSHOD.ProcesorStanje.Fs = SegKorisnikdata
		iSHOD.ProcesorStanje.Gs = SegKorisnikgs
		iSHOD.ProcesorStanje.Ss = SegKorisnikdata
		iSHOD.ThreadStanje = Pokrenut
		iSHOD.ProcesorStanje.Eflags = 0x222
	}
	iSHOD.Iskernel = iskernel
	iSHOD.Fpuoffset = 0xffffffff

	return iSHOD
}

func (isti *TThreadhelper) CreatePokazivačsafunkcija(unospoint_2 func(), STRANADirektorijumunos uint32, iskernel bool) *TThread {
	iSHOD := (*TThread)(isti.mem.Malloc(uint32(Sizeof(TThread{}))))
	if iSHOD == nil {
		return nil
	}
	*iSHOD = isti.Createsafunkcija(unospoint_2, STRANADirektorijumunos, iskernel)
	if iSHOD.ProcesorStanje == nil {
		isti.mem.Slobodno(Pointer(iSHOD))
		return nil
	}
	return iSHOD
}
