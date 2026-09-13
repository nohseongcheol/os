package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konsola"
import . "multitasking"
import mem "pamięćmanager"
import . "wirtualnePamięć"

const (
	Blocked		= 1
	Gotowy		= 2
	Zatrzymany	= 3
	Uruchomiono	= 4
)

const ThreadstackRozmiar = 32 * 1024

type TThread struct {
	ProcesorStan			*TcpuStan
	Stack				uint32
	Użytkownikstack_2		uint32
	UżytkownikstackRozmiar_2	uint32
	Identyfikator			uint32
	RodzicIdentyfikator		uint32

	StronaKatalogwpis	uint32

	ThreadStan	uint8
	BlockedStan	uint8

	czasdelta	uint32

	TlsSegmenty	[Gdtwpis]TSegmentdescriptor
	FpuPrzesunięcie	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (bieżący *TThread) Nowy() {
}

type TThreadhelper struct {
	mem *mem.TPamięćmanager
}

var konsola_2 = TKonsola{}

func (bieżący *TThreadhelper) Init(mem *mem.TPamięćmanager) {
	bieżący.mem = mem
	konsola_2.MWydrukujxy(([]byte)("thread:"), 1, 14)
}
func (bieżący *TThreadhelper) CreatezFunkcja(wpispoint_2 func(), StronaKatalogwpis uint32, iskernel bool) TThread {
	wYNIK := TThread{}

	wYNIK.Stack = uint32(uintptr(bieżący.mem.Przydziel_pamięć(ThreadstackRozmiar)))
	if wYNIK.Stack == 0 {
		return wYNIK
	}
	konsola_2.MWydrukuj(([]byte)("[mem:"))
	konsola_2.MUnsignedinteger32Wydrukuj(wYNIK.Stack)

	wYNIK.ProcesorStan = (*TcpuStan)(Pointer(uintptr(wYNIK.Stack) + ThreadstackRozmiar - Sizeof(TcpuStan{})))
	wYNIK.ProcesorStan.Esp = wYNIK.Stack + ThreadstackRozmiar
	wYNIK.ProcesorStan.Ebp = wYNIK.ProcesorStan.Esp
	wYNIK.ProcesorStan.Eip = uint32(ValueOf(wpispoint_2).Pointer())
	wYNIK.Użytkownikstack_2 = Użytkownikstack
	wYNIK.UżytkownikstackRozmiar_2 = UżytkownikstackRozmiar
	wYNIK.Identyfikator = 0
	wYNIK.RodzicIdentyfikator = 0
	wYNIK.StronaKatalogwpis = StronaKatalogwpis
	konsola_2.MWydrukuj((([]byte)("cpu")))

	konsola_2.MUnsignedinteger32Wydrukuj(uint32(uintptr(Pointer(wYNIK.ProcesorStan))))

	konsola_2.MWydrukuj((([]byte)(":")))
	konsola_2.MUnsignedinteger32Wydrukuj(wYNIK.ProcesorStan.Eip)

	konsola_2.MWydrukuj("]")
	if iskernel == true {
		wYNIK.ProcesorStan.Cs = Segkernelcode
		wYNIK.ProcesorStan.Ds = Segkerneldata
		wYNIK.ProcesorStan.Es = Segkerneldata
		wYNIK.ProcesorStan.Fs = Segkerneldata
		wYNIK.ProcesorStan.Gs = Segkernelgs
		wYNIK.ProcesorStan.Ss = Segkerneldata
		wYNIK.ThreadStan = Gotowy
		wYNIK.ProcesorStan.Eflags = 0x202
	} else {
		wYNIK.ProcesorStan.Cs = SegUżytkownikcode
		wYNIK.ProcesorStan.Ds = SegUżytkownikdata
		wYNIK.ProcesorStan.Es = SegUżytkownikdata
		wYNIK.ProcesorStan.Fs = SegUżytkownikdata
		wYNIK.ProcesorStan.Gs = SegUżytkownikgs
		wYNIK.ProcesorStan.Ss = SegUżytkownikdata
		wYNIK.ThreadStan = Uruchomiono
		wYNIK.ProcesorStan.Eflags = 0x222
	}
	wYNIK.Iskernel = iskernel
	wYNIK.FpuPrzesunięcie = 0xffffffff

	return wYNIK
}

func (bieżący *TThreadhelper) CreateKursorzFunkcja(wpispoint_2 func(), StronaKatalogwpis uint32, iskernel bool) *TThread {
	wYNIK := (*TThread)(bieżący.mem.Przydziel_pamięć(uint32(Sizeof(TThread{}))))
	if wYNIK == nil {
		return nil
	}
	*wYNIK = bieżący.CreatezFunkcja(wpispoint_2, StronaKatalogwpis, iskernel)
	if wYNIK.ProcesorStan == nil {
		bieżący.mem.Wolne(Pointer(wYNIK))
		return nil
	}
	return wYNIK
}
