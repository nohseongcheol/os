/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "memorijamanager"
import . "virtualnoMemorija"

const (
	Blocked		= 1
	Spreman		= 2
	Zaustavljen	= 3
	Pokrenuto	= 4
)

const ThreadstackVeličina = 32 * 1024

type TThread struct {
	ProcesorStanje		*TcpuStanje
	Stack			uint32
	Korisnikstack_2		uint32
	KorisnikstackVeličina_2	uint32
	Pid			uint32
	Roditeljpid		uint32

	StranicaDirektorijentry	uint32

	ThreadStanje	uint8
	BlockedStanje	uint8

	vrijemedelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (sam *TThread) Novi() {
}

type TThreadhelper struct {
	mem *mem.TMemorijamanager
}

var console_2 = TConsole{}

func (sam *TThreadhelper) Init(mem *mem.TMemorijamanager) {
	sam.mem = mem
	console_2.MIspisxy(([]byte)("thread:"), 1, 14)
}
func (sam *TThreadhelper) CreatefromFunkcija(entrypoint_2 func(), StranicaDirektorijentry uint32, iskernel bool) TThread {
	rEZULTAT := TThread{}

	rEZULTAT.Stack = uint32(uintptr(sam.mem.Malloc(ThreadstackVeličina)))
	if rEZULTAT.Stack == 0 {
		return rEZULTAT
	}
	console_2.MIspis(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Ispis(rEZULTAT.Stack)

	rEZULTAT.ProcesorStanje = (*TcpuStanje)(Pointer(uintptr(rEZULTAT.Stack) + ThreadstackVeličina - Sizeof(TcpuStanje{})))
	rEZULTAT.ProcesorStanje.Esp = rEZULTAT.Stack + ThreadstackVeličina
	rEZULTAT.ProcesorStanje.Ebp = rEZULTAT.ProcesorStanje.Esp
	rEZULTAT.ProcesorStanje.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	rEZULTAT.Korisnikstack_2 = Korisnikstack
	rEZULTAT.KorisnikstackVeličina_2 = KorisnikstackVeličina
	rEZULTAT.Pid = 0
	rEZULTAT.Roditeljpid = 0
	rEZULTAT.StranicaDirektorijentry = StranicaDirektorijentry
	console_2.MIspis((([]byte)("cpu")))

	console_2.MUnsignedinteger32Ispis(uint32(uintptr(Pointer(rEZULTAT.ProcesorStanje))))

	console_2.MIspis((([]byte)(":")))
	console_2.MUnsignedinteger32Ispis(rEZULTAT.ProcesorStanje.Eip)

	console_2.MIspis("]")
	if iskernel == true {
		rEZULTAT.ProcesorStanje.Cs = Segkernelcode
		rEZULTAT.ProcesorStanje.Ds = Segkerneldata
		rEZULTAT.ProcesorStanje.Es = Segkerneldata
		rEZULTAT.ProcesorStanje.Fs = Segkerneldata
		rEZULTAT.ProcesorStanje.Gs = Segkernelgs
		rEZULTAT.ProcesorStanje.Ss = Segkerneldata
		rEZULTAT.ThreadStanje = Spreman
		rEZULTAT.ProcesorStanje.Eflags = 0x202
	} else {
		rEZULTAT.ProcesorStanje.Cs = SegKorisnikcode
		rEZULTAT.ProcesorStanje.Ds = SegKorisnikdata
		rEZULTAT.ProcesorStanje.Es = SegKorisnikdata
		rEZULTAT.ProcesorStanje.Fs = SegKorisnikdata
		rEZULTAT.ProcesorStanje.Gs = SegKorisnikgs
		rEZULTAT.ProcesorStanje.Ss = SegKorisnikdata
		rEZULTAT.ThreadStanje = Pokrenuto
		rEZULTAT.ProcesorStanje.Eflags = 0x222
	}
	rEZULTAT.Iskernel = iskernel
	rEZULTAT.Fpuoffset = 0xffffffff

	return rEZULTAT
}

func (sam *TThreadhelper) CreatePokazivačfromFunkcija(entrypoint_2 func(), StranicaDirektorijentry uint32, iskernel bool) *TThread {
	rEZULTAT := (*TThread)(sam.mem.Malloc(uint32(Sizeof(TThread{}))))
	if rEZULTAT == nil {
		return nil
	}
	*rEZULTAT = sam.CreatefromFunkcija(entrypoint_2, StranicaDirektorijentry, iskernel)
	if rEZULTAT.ProcesorStanje == nil {
		sam.mem.Slobodno(Pointer(rEZULTAT))
		return nil
	}
	return rEZULTAT
}
