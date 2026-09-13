package ausführbares_und_bindbares_Format

import . "unsafe"
import . "konsole"

import mem "speicherVerwalter"

type Verknüpfung struct {
	Dynamisch	uintptr
	Previous	*Verknüpfung
	Weiter		*Verknüpfung
}
type VerknüpfungAbbildung struct {
	First	*Verknüpfung
	Letzter	*Verknüpfung

	Größe_2	int

	mem	*mem.TSpeicherVerwalter
}

func (selbst *VerknüpfungAbbildung) Init(mem *mem.TSpeicherVerwalter) {
	selbst.mem = mem
}
func (selbst *VerknüpfungAbbildung) Clone() VerknüpfungAbbildung {
	var verknüpfungAbbildung VerknüpfungAbbildung

	verknüpfungAbbildung.Init(selbst.mem)

	Verknüpfung := selbst.First

	for ; Verknüpfung != nil; Verknüpfung = Verknüpfung.Weiter {
		verknüpfungAbbildung.Am_Listenende_anfügen(Verknüpfung.Dynamisch)
	}
	return verknüpfungAbbildung
}
func (selbst *VerknüpfungAbbildung) Am_Listenanfang_einfügen(Dynamisch uintptr) {
	neuVerknüpfung := (*Verknüpfung)(selbst.mem.Speicher_reservieren(uint32(Sizeof(Verknüpfung{}))))
	neuVerknüpfung.Dynamisch = Dynamisch
	neuVerknüpfung.Weiter = selbst.First
	selbst.First = neuVerknüpfung
	selbst.Größe_2++

	if selbst.First.Weiter == nil {
		selbst.Letzter = selbst.First
	}
}
func (selbst *VerknüpfungAbbildung) Am_Listenende_anfügen(Dynamisch uintptr) {
	if Dynamisch == 0 {
		return
	}

	if selbst.Größe_2 == 0 {
		selbst.Am_Listenanfang_einfügen(Dynamisch)
	} else {
		neuVerknüpfung := (*Verknüpfung)(selbst.mem.Speicher_reservieren(uint32(Sizeof(Verknüpfung{}))))
		neuVerknüpfung.Dynamisch = Dynamisch
		neuVerknüpfung.Weiter = nil
		selbst.Letzter.Weiter = neuVerknüpfung
		selbst.Letzter = neuVerknüpfung
		selbst.Größe_2++
	}
}
func (selbst *VerknüpfungAbbildung) Drucken(x uint16, y uint16) {
	Verknüpfung := selbst.First
	konsole_2 := TKonsole{}
	konsole_2.MDruckenxy("linkmap : ", x, y)
	for ; Verknüpfung != nil; Verknüpfung = Verknüpfung.Weiter {
		konsole_2.MUnsignedinteger32Drucken(uint32(Verknüpfung.Dynamisch))
		konsole_2.MDrucken("+")

	}
}
