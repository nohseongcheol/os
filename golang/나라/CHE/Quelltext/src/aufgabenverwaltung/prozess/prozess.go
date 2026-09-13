package prozess

import . "unsafe"
import . "hilfswerkzeug/liste"
import mem "speicherVerwalter"
import . "aufgabenverwaltung/ausführungsfaden"
import . "aufgabenverwaltung/planer"
import . "hilfswerkzeug"

const ProcBenutzerheapGröße = 1 * 1024 * 1024

type Prozess struct {
	kennung			uint32
	syscallKennung		int
	IsBenutzerLeerzeichen	bool
	argumente		*[]byte

	AusführungsfadenListe	LinkedListe
	Threads			*LinkedListe
	DateiElementname	[]byte

	SeiteOrdnerEintrag	uintptr
}

func (selbst *Prozess) Init(mem *mem.TSpeicherVerwalter) {
	selbst.AusführungsfadenListe = LinkedListe{}
	selbst.Threads = &selbst.AusführungsfadenListe
	selbst.Threads.Init(mem)
}

type Prozesshelper struct {
	prozesse		LinkedListe
	mem			*mem.TSpeicherVerwalter
	kernSeiteOrdnerEintrag	uintptr
}

func (selbst *Prozesshelper) Init(mem *mem.TSpeicherVerwalter, kernSeiteOrdnerEintrag uintptr) {
	selbst.mem = mem
	selbst.prozesse = LinkedListe{}
	selbst.prozesse.Init(selbst.mem)
	selbst.kernSeiteOrdnerEintrag = kernSeiteOrdnerEintrag
}

func (selbst *Prozesshelper) Erstellen(eintragpoint func(), ausführungsfadenhelper *TAusführungsfadenhelper, SeiteOrdnerEintrag uint32, isKern bool) Prozess {
	prozess := (*Prozess)(selbst.mem.Speicher_reservieren(uint32(Sizeof(Prozess{}))))
	if prozess == nil {
		return Prozess{}
	}
	prozess.Init(selbst.mem)
	prozess.kennung = AllocateProzesskennung()
	prozess.SeiteOrdnerEintrag = uintptr(SeiteOrdnerEintrag)
	hauptAusführungsfaden := ausführungsfadenhelper.ErstellenZeigervonFunktion(eintragpoint, SeiteOrdnerEintrag, isKern)
	if hauptAusführungsfaden != nil {
		hauptAusführungsfaden.Prozesskennung = prozess.kennung
		hauptAusführungsfaden.ElternelementProzesskennung = 0
		prozess.Threads.Am_Listenende_anfügen(uintptr(Pointer(hauptAusführungsfaden)))
	}

	selbst.prozesse.Am_Listenende_anfügen(uintptr(Pointer(prozess)))

	return *prozess
}

func (selbst *Prozesshelper) Spawn(eintragpoint func(), ausführungsfadenhelper *TAusführungsfadenhelper, planer *Planer, SeiteOrdnerEintrag uint32, isKern bool) Prozess {
	prozess := selbst.Erstellen(eintragpoint, ausführungsfadenhelper, SeiteOrdnerEintrag, isKern)
	if prozess.Threads != nil && prozess.Threads.Größe_2 > 0 {
		ausführungsfaden := (*TAusführungsfaden)(prozess.Threads.Getat(0))
		if ausführungsfaden != nil && planer != nil {
			planer.HinzufügenAusführungsfaden(ausführungsfaden)
		}
	}
	return prozess
}

func (selbst *Prozesshelper) kopierenSeiteOrdner(quelleEintrag uintptr, zielEintrag uintptr) {
	quelle_2 := Getunsignedinteger32FeldvonZeiger(quelleEintrag, 1024, 1024)
	ziel_2 := Getunsignedinteger32FeldvonZeiger(zielEintrag, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		ziel_2[i] = quelle_2[i]
	}
}
func (selbst *Prozesshelper) ErstellenvonDaten() Prozess {
	prozess := Prozess{}
	return prozess
}
