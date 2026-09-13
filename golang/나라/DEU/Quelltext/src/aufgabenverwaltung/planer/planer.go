package planer

import . "unsafe"
import . "reflect"

import . "konsole"
import . "gdt"
import . "anschluss"
import . "hilfswerkzeug/liste"

import . "unterbrechung"
import . "aufgabenverwaltung/ausführungsfaden"
import . "aufgabenverwaltung/tss"
import . "mehrfachAufgabenverwaltung"
import mem "speicherVerwalter"

const PlanerHäufigkeit = 1
const KernheapStarten = 1024 * 1024
const planerDebuggen = false
const pitHäufigkeit = 100

var liste LinkedListe

type PlanerDaten struct {
	häufigkeit	uint32
	tickAnzahl	uint32

	switchforced	bool

	Aktiviert	bool

	systemzeitAusführungsfaden	*TAusführungsfaden
	tss				*TssEintrag
}

var scheDaten PlanerDaten = PlanerDaten{}

func (selbst *PlanerDaten) Init() {
	scheDaten.tickAnzahl = 0
	scheDaten.häufigkeit = PlanerHäufigkeit
	scheDaten.systemzeitAusführungsfaden = nil
	scheDaten.Aktiviert = false
	scheDaten.switchforced = false

}

var konsole_2 = TKonsole{}
var systemzeitAusführungsfadenInhalt int = 0
var weiterProzessKennung uint32 = 1

func AllocateProzesskennung() uint32 {
	prozesskennung := weiterProzessKennung
	weiterProzessKennung++
	return prozesskennung
}

func (selbst *PlanerDaten) GetWeiterBereitAusführungsfaden() *TAusführungsfaden {
	if liste.Größe_2 <= 0 {
		return nil
	}

	if scheDaten.systemzeitAusführungsfaden != nil {
		systemzeitAusführungsfadenInhalt = liste.Inhaltvon(uintptr(Pointer(scheDaten.systemzeitAusführungsfaden)))
		if systemzeitAusführungsfadenInhalt < 0 {
			systemzeitAusführungsfadenInhalt = 0
		}
	} else {
		systemzeitAusführungsfadenInhalt = -1
	}

	for checked := 0; checked < liste.Größe_2; checked++ {
		systemzeitAusführungsfadenInhalt++
		if systemzeitAusführungsfadenInhalt >= liste.Größe_2 {
			systemzeitAusführungsfadenInhalt = 0
		}
		ausführungsfaden := (*TAusführungsfaden)(liste.Getat(systemzeitAusführungsfadenInhalt))
		if ausführungsfaden != nil && ausführungsfaden.AusführungsfadenStatus != Blocked && ausführungsfaden.AusführungsfadenStatus != Angehalten {
			if planerDebuggen {
				konsole_2.MDrucken("ti:")
				konsole_2.MUnsignedinteger32Drucken(uint32(systemzeitAusführungsfadenInhalt))
				konsole_2.MDrucken(":")
				konsole_2.MUnsignedinteger32Drucken(uint32(uintptr(Pointer(ausführungsfaden))))
			}
			return ausführungsfaden
		}
	}
	return scheDaten.systemzeitAusführungsfaden

}
func (selbst *Planer) HinzufügenAusführungsfaden(ausführungsfaden *TAusführungsfaden) {
	if ausführungsfaden == nil {
		return
	}
	liste.Am_Listenende_anfügen(uintptr(Pointer(ausführungsfaden)))
}
func HinzufügenrunnableAusführungsfaden(ausführungsfaden *TAusführungsfaden) {
	if ausführungsfaden == nil {
		return
	}
	liste.Am_Listenende_anfügen(uintptr(Pointer(ausführungsfaden)))
}

func SystemzeitProzesskennung() uint32 {
	if scheDaten.systemzeitAusführungsfaden == nil || scheDaten.systemzeitAusführungsfaden.Prozesskennung == 0 {
		return 1
	}
	return scheDaten.systemzeitAusführungsfaden.Prozesskennung
}

func SystemzeitElternelementProzesskennung() uint32 {
	if scheDaten.systemzeitAusführungsfaden == nil {
		return 0
	}
	return scheDaten.systemzeitAusführungsfaden.ElternelementProzesskennung
}
func (selbst *Planer) EntfernenAusführungsfaden(ausführungsfaden *TAusführungsfaden) {
	liste.Entfernen(uintptr(Pointer(ausführungsfaden)))
}

func (selbst *Planer) EntfernenAusführungsfadenat(inhalt int) {
	liste.Entfernenat(inhalt)
}

type Planer struct {
	TUnterbrechunghandler
}

func (selbst *Planer) Init(verwalter *TUnterbrechungVerwalter, mem *mem.TSpeicherVerwalter, tss *TssEintrag) {
	scheDaten.Init()
	scheDaten.tss = tss
	initpit(pitHäufigkeit)

	liste = LinkedListe{}
	liste.Init(mem)
	konsole_2.MDrucken("list:")
	konsole_2.MUnsignedinteger32Drucken(uint32(uintptr(Pointer(&liste))))

	unterbrechunghandler = griffUnterbrechung
	var address uintptr
	address = uintptr(Pointer(&unterbrechunghandler))
	selbst.TUnterbrechunghandler.Init(0x20, uintptr(Pointer(verwalter)), address)
}

func (selbst *Planer) Aktiviert(aktiviert bool) {
	scheDaten.Aktiviert = aktiviert
}

func initpit(häufigkeit uint32) {
	if häufigkeit == 0 {
		return
	}
	divisor := uint32(1193180) / häufigkeit
	AnschlussSchreibenByte(0x43, 0x36)
	AnschlussSchreibenByte(0x40, uint8(divisor&0xFF))
	AnschlussSchreibenByte(0x40, uint8((divisor>>8)&0xFF))
}

func setzends(dssegment uint32)
func setzengs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func wiederherstellenfpregs(buffer_2 uintptr)

var jmpBenutzer uint32 = 0
var unterbrechunghandler func(uint32) uint32

func schedulestack(fn func())
func setzencr3(address uint32)
func getcr3() uint32

func griffUnterbrechung(esp uint32) uint32 {

	scheDaten.tickAnzahl++

	if planerDebuggen {
		konsole_2.MDruckenxy(([]byte)("sche1:"), 1, 17)

		konsole_2.MDrucken(":")
		konsole_2.MUnsignedinteger32Drucken(esp)
		konsole_2.MDrucken(":")

		konsole_2.MUnsignedinteger32Drucken(uint32(scheDaten.tickAnzahl))
		konsole_2.MDrucken(":")
		konsole_2.MUnsignedinteger32Drucken(KernheapStarten)
	}

	if scheDaten.tickAnzahl == scheDaten.häufigkeit {
		scheDaten.tickAnzahl = 0

		if liste.Größe_2 > 0 && scheDaten.Aktiviert == true {
			var weiterAusführungsfaden = scheDaten.GetWeiterBereitAusführungsfaden()
			if weiterAusführungsfaden == nil {
				return esp
			}
			if scheDaten.systemzeitAusführungsfaden == nil {
				MEmergencyProtokollZeichenkette("\nSCHED first esp=")
				MEmergencyProtokollunsignedinteger32(esp)
				MEmergencyProtokollZeichenkette(" thread=")
				MEmergencyProtokollunsignedinteger32(uint32(uintptr(Pointer(weiterAusführungsfaden))))
				MEmergencyProtokollZeichenkette(" cpu=")
				MEmergencyProtokollunsignedinteger32(uint32(uintptr(Pointer(weiterAusführungsfaden.CpuStatus))))
				MEmergencyProtokollZeichenkette(" state=")
				MEmergencyProtokollunsignedinteger32(uint32(weiterAusführungsfaden.AusführungsfadenStatus))
				MEmergencyProtokollZeichenkette(" eip=")
				MEmergencyProtokollunsignedinteger32(weiterAusführungsfaden.CpuStatus.Eip)
				MEmergencyProtokollZeichenkette(" cs=")
				MEmergencyProtokollunsignedinteger32(weiterAusführungsfaden.CpuStatus.Cs)
				MEmergencyProtokollZeichenkette("\n")
			}

			if esp >= KernheapStarten && scheDaten.systemzeitAusführungsfaden != nil {
				scheDaten.systemzeitAusführungsfaden.CpuStatus = (*TcpuStatus)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(scheDaten.systemzeitAusführungsfaden.Fpubuffer)))
				versatz := (16 - (address % 16)) & 0xF
				scheDaten.systemzeitAusführungsfaden.FpuVersatz = versatz
				backupfpregs(address + versatz)
				if planerDebuggen {
					konsole_2.MDrucken(([]byte)("backup"))
					konsole_2.MUnsignedinteger32Drucken(esp)
				}
			}

			address := uintptr(Pointer(&(weiterAusführungsfaden.Fpubuffer)))
			versatz := weiterAusführungsfaden.FpuVersatz
			if versatz != 0xffffffff {
				wiederherstellenfpregs(address + versatz)
				if planerDebuggen {
					konsole_2.MDrucken(([]byte)("restore"))
				}
			}

			scheDaten.systemzeitAusführungsfaden = weiterAusführungsfaden

			if scheDaten.systemzeitAusführungsfaden.AusführungsfadenStatus == Gestartet {
				scheDaten.systemzeitAusführungsfaden.AusführungsfadenStatus = Bereit

				InitialAusführungsfadenBenutzerjump(scheDaten.systemzeitAusführungsfaden)
				return esp
			}

			esp = uint32(uintptr(Pointer(weiterAusführungsfaden.CpuStatus)))
			if weiterAusführungsfaden.Stack != 0 {
				scheDaten.tss.Setzenstack(SegKernDaten, weiterAusführungsfaden.Stack+AusführungsfadenstackGröße)
			}

			setzencr3(weiterAusführungsfaden.SeiteOrdnerEintrag)
			setzengs(weiterAusführungsfaden.CpuStatus.Gs)

		}

	}

	return esp
}

func jumpBenutzermodusiret(uint32, uint32, uint32, uint32, uint32, uint32)
func DeaktivierenGanzzahl()

func getesp() uint32
func ausführungsfadenBeendenSchleife()

func setzenAusführungsfadenBeendenSchleifeStatus(cpuStatus *TcpuStatus) {
	cpuStatus.Eip = uint32(ValueOf(ausführungsfadenBeendenSchleife).Pointer())
	cpuStatus.Cs = SegKerncode
	cpuStatus.Ds = SegKernDaten
	cpuStatus.Es = SegKernDaten
	cpuStatus.Fs = SegKernDaten
	cpuStatus.Gs = SegKerngs
	cpuStatus.Ss = SegKernDaten
	cpuStatus.Eflags = 0x202
}

func AnhaltenSystemzeitAusführungsfaden(cpuStatus *TcpuStatus) *TcpuStatus {
	if scheDaten.systemzeitAusführungsfaden == nil {
		setzenAusführungsfadenBeendenSchleifeStatus(cpuStatus)
		return cpuStatus
	}

	angehaltenAusführungsfaden := scheDaten.systemzeitAusführungsfaden
	for i := 0; i < liste.Größe_2; i++ {
		ausführungsfaden := (*TAusführungsfaden)(liste.Getat(i))
		if ausführungsfaden != nil && ausführungsfaden.CpuStatus == cpuStatus {
			angehaltenAusführungsfaden = ausführungsfaden
			break
		}
	}
	angehaltenAusführungsfaden.CpuStatus = cpuStatus
	angehaltenAusführungsfaden.AusführungsfadenStatus = Angehalten
	scheDaten.systemzeitAusführungsfaden = angehaltenAusführungsfaden

	weiterAusführungsfaden := scheDaten.GetWeiterBereitAusführungsfaden()
	if weiterAusführungsfaden == nil || weiterAusführungsfaden == angehaltenAusführungsfaden || weiterAusführungsfaden.CpuStatus == nil || weiterAusführungsfaden.CpuStatus == cpuStatus {
		setzenAusführungsfadenBeendenSchleifeStatus(cpuStatus)
		return cpuStatus
	}

	scheDaten.systemzeitAusführungsfaden = weiterAusführungsfaden
	if weiterAusführungsfaden.Stack != 0 && scheDaten.tss != nil {
		scheDaten.tss.Setzenstack(SegKernDaten, weiterAusführungsfaden.Stack+AusführungsfadenstackGröße)
	}
	setzencr3(weiterAusführungsfaden.SeiteOrdnerEintrag)
	setzengs(weiterAusführungsfaden.CpuStatus.Gs)
	return weiterAusführungsfaden.CpuStatus
}

func InitialAusführungsfadenBenutzerjump(ausführungsfaden *TAusführungsfaden) {

	DeaktivierenGanzzahl()

	scheDaten.tss.Setzenstack(SegKernDaten, ausführungsfaden.Stack+AusführungsfadenstackGröße)

	setzencr3(ausführungsfaden.SeiteOrdnerEintrag)
	setzengs(ausführungsfaden.CpuStatus.Gs)

	scheDaten.systemzeitAusführungsfaden = ausführungsfaden
	scheDaten.Aktiviert = true

	eip := ausführungsfaden.CpuStatus.Eip
	benutzeresp := ausführungsfaden.Benutzerstack_2 + ausführungsfaden.BenutzerstackGröße_2
	eflags := ausführungsfaden.CpuStatus.Eflags
	cs := ausführungsfaden.CpuStatus.Cs
	esp := scheDaten.tss.Getesp0()

	konsole_2.MDrucken(([]byte)("jump["))
	konsole_2.MUnsignedinteger32Drucken(eip)
	konsole_2.MDrucken(([]byte)(":"))
	konsole_2.MUnsignedinteger32Drucken(benutzeresp)
	konsole_2.MDrucken(([]byte)(":"))
	konsole_2.MUnsignedinteger32Drucken(eflags)
	konsole_2.MDrucken(([]byte)(":"))
	konsole_2.MUnsignedinteger32Drucken(cs)
	konsole_2.MDrucken(([]byte)(":"))

	konsole_2.MUnsignedinteger32Drucken(esp)
	konsole_2.MDrucken(([]byte)("]"))

	userprocEintrag := ausführungsfaden.CpuStatus.Ecx
	globalVersatzTabelle_2 := ausführungsfaden.CpuStatus.Edx
	dynamisch := ausführungsfaden.CpuStatus.Esi

	AnschlussSchreibenByte(0x20, 0x20)
	jumpBenutzermodusiret(eip, benutzeresp, eflags, userprocEintrag, globalVersatzTabelle_2, dynamisch)
	konsole_2.MDrucken(([]byte)("usermode end"))
}
func druckenesp(esp uint32) {
	konsole_2.MDrucken(([]byte)("esp["))
	konsole_2.MUnsignedinteger32Drucken(esp)
}
