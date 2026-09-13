package Ausführungsfaden

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konsole"
import . "mehrfachAufgabenverwaltung"
import mem "speicherVerwalter"
import . "virtuellSpeicher"

const (
	Blocked		= 1
	Bereit		= 2
	Angehalten	= 3
	Gestartet	= 4
)

const AusführungsfadenstackGröße = 32 * 1024

type TAusführungsfaden struct {
	CpuStatus			*TcpuStatus
	Stack				uint32
	Benutzerstack_2			uint32
	BenutzerstackGröße_2		uint32
	Prozesskennung			uint32
	ElternelementProzesskennung	uint32

	SeiteOrdnerEintrag	uint32

	AusführungsfadenStatus	uint8
	BlockedStatus		uint8

	zeitdelta	uint32

	TlsSegmente	[GdtEintrag]TSegmentdescriptor
	FpuVersatz	uintptr
	Fpubuffer	[512 + 16]byte
	IsKern		bool
}

func (selbst *TAusführungsfaden) Neu() {
}

type TAusführungsfadenhelper struct {
	mem *mem.TSpeicherVerwalter
}

var konsole_2 = TKonsole{}

func (selbst *TAusführungsfadenhelper) Init(mem *mem.TSpeicherVerwalter) {
	selbst.mem = mem
	konsole_2.MDruckenxy(([]byte)("thread:"), 1, 14)
}
func (selbst *TAusführungsfadenhelper) ErstellenvonFunktion(eintragpoint_2 func(), SeiteOrdnerEintrag uint32, isKern bool) TAusführungsfaden {
	ergebnis := TAusführungsfaden{}

	ergebnis.Stack = uint32(uintptr(selbst.mem.Speicher_reservieren(AusführungsfadenstackGröße)))
	if ergebnis.Stack == 0 {
		return ergebnis
	}
	konsole_2.MDrucken(([]byte)("[mem:"))
	konsole_2.MUnsignedinteger32Drucken(ergebnis.Stack)

	ergebnis.CpuStatus = (*TcpuStatus)(Pointer(uintptr(ergebnis.Stack) + AusführungsfadenstackGröße - Sizeof(TcpuStatus{})))
	ergebnis.CpuStatus.Esp = ergebnis.Stack + AusführungsfadenstackGröße
	ergebnis.CpuStatus.Ebp = ergebnis.CpuStatus.Esp
	ergebnis.CpuStatus.Eip = uint32(ValueOf(eintragpoint_2).Pointer())
	ergebnis.Benutzerstack_2 = Benutzerstack
	ergebnis.BenutzerstackGröße_2 = BenutzerstackGröße
	ergebnis.Prozesskennung = 0
	ergebnis.ElternelementProzesskennung = 0
	ergebnis.SeiteOrdnerEintrag = SeiteOrdnerEintrag
	konsole_2.MDrucken((([]byte)("cpu")))

	konsole_2.MUnsignedinteger32Drucken(uint32(uintptr(Pointer(ergebnis.CpuStatus))))

	konsole_2.MDrucken((([]byte)(":")))
	konsole_2.MUnsignedinteger32Drucken(ergebnis.CpuStatus.Eip)

	konsole_2.MDrucken("]")
	if isKern == true {
		ergebnis.CpuStatus.Cs = SegKerncode
		ergebnis.CpuStatus.Ds = SegKernDaten
		ergebnis.CpuStatus.Es = SegKernDaten
		ergebnis.CpuStatus.Fs = SegKernDaten
		ergebnis.CpuStatus.Gs = SegKerngs
		ergebnis.CpuStatus.Ss = SegKernDaten
		ergebnis.AusführungsfadenStatus = Bereit
		ergebnis.CpuStatus.Eflags = 0x202
	} else {
		ergebnis.CpuStatus.Cs = SegBenutzercode
		ergebnis.CpuStatus.Ds = SegBenutzerDaten
		ergebnis.CpuStatus.Es = SegBenutzerDaten
		ergebnis.CpuStatus.Fs = SegBenutzerDaten
		ergebnis.CpuStatus.Gs = SegBenutzergs
		ergebnis.CpuStatus.Ss = SegBenutzerDaten
		ergebnis.AusführungsfadenStatus = Gestartet
		ergebnis.CpuStatus.Eflags = 0x222
	}
	ergebnis.IsKern = isKern
	ergebnis.FpuVersatz = 0xffffffff

	return ergebnis
}

func (selbst *TAusführungsfadenhelper) ErstellenZeigervonFunktion(eintragpoint_2 func(), SeiteOrdnerEintrag uint32, isKern bool) *TAusführungsfaden {
	ergebnis := (*TAusführungsfaden)(selbst.mem.Speicher_reservieren(uint32(Sizeof(TAusführungsfaden{}))))
	if ergebnis == nil {
		return nil
	}
	*ergebnis = selbst.ErstellenvonFunktion(eintragpoint_2, SeiteOrdnerEintrag, isKern)
	if ergebnis.CpuStatus == nil {
		selbst.mem.Frei(Pointer(ergebnis))
		return nil
	}
	return ergebnis
}
