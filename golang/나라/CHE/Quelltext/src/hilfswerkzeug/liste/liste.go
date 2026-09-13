package liste

import . "unsafe"
import . "konsole"
import mem "speicherVerwalter"

type TListenknoten struct {
	adressverweis		uintptr
	previous	*TListenknoten
	weiter		*TListenknoten
}

type LinkedListe struct {
	head	*TListenknoten
	tail	*TListenknoten
	Größe_2	int

	mem	*mem.TSpeicherVerwalter
}

func (selbst *LinkedListe) Init(mem *mem.TSpeicherVerwalter) {
	selbst.head = nil
	selbst.tail = nil
	selbst.Größe_2 = 0

	selbst.mem = mem
}
func (selbst *LinkedListe) Am_Listenanfang_einfügen(adressverweis uintptr) {
	neuKnoten := (*TListenknoten)(selbst.mem.Speicher_reservieren(uint32(Sizeof(TListenknoten{}))))
	if neuKnoten == nil {
		return
	}
	neuKnoten.adressverweis = adressverweis
	neuKnoten.previous = nil
	neuKnoten.weiter = selbst.head
	if selbst.head != nil {
		selbst.head.previous = neuKnoten
	}
	selbst.head = neuKnoten
	selbst.Größe_2++

	if selbst.head.weiter == nil {
		selbst.tail = selbst.head
	}

}
func (selbst *LinkedListe) Am_Listenende_anfügen(adressverweis uintptr) {
	if selbst.Größe_2 == 0 {
		selbst.Am_Listenanfang_einfügen(adressverweis)
	} else {
		neuKnoten := (*TListenknoten)(selbst.mem.Speicher_reservieren(uint32(Sizeof(TListenknoten{}))))
		if neuKnoten == nil {
			return
		}
		neuKnoten.adressverweis = adressverweis
		neuKnoten.previous = selbst.tail
		neuKnoten.weiter = nil
		selbst.tail.weiter = neuKnoten
		selbst.tail = neuKnoten
		selbst.Größe_2++
	}
}
func (selbst *LinkedListe) An_Position_einfügen(inhalt int, adressverweis uintptr) {
	if inhalt == 0 {
		selbst.Am_Listenanfang_einfügen(adressverweis)
	} else {
		previousKnoten := selbst.GetKnotenat(inhalt - 1)
		weiterKnoten := previousKnoten.weiter
		neuKnoten := (*TListenknoten)(selbst.mem.Speicher_reservieren(uint32(Sizeof(TListenknoten{}))))
		if neuKnoten == nil {
			return
		}
		neuKnoten.adressverweis = adressverweis

		previousKnoten.weiter = neuKnoten
		neuKnoten.previous = previousKnoten
		neuKnoten.weiter = weiterKnoten
		if weiterKnoten != nil {
			weiterKnoten.previous = neuKnoten
		}

		selbst.Größe_2++

		if neuKnoten.weiter == nil {
			selbst.tail = neuKnoten
		}
	}
}
func (selbst *LinkedListe) GetKnotenat(inhalt int) *TListenknoten {
	if inhalt < 0 || inhalt >= selbst.Größe_2 {
		return nil
	}
	var x *TListenknoten = selbst.head
	for i := 0; i < inhalt; i++ {
		x = x.weiter
	}
	return x
}

func (selbst *LinkedListe) SetzenKnotenat(inhalt int, adressverweis uintptr) {
	var x *TListenknoten = selbst.head
	for i := 0; i < inhalt; i++ {
		x = x.weiter
	}
	if x != nil {
		x.adressverweis = adressverweis
	}
}
func (selbst *LinkedListe) Getat(inhalt int) Pointer {
	listenknoten := selbst.GetKnotenat(inhalt)
	if listenknoten == nil {
		return nil
	}
	var adressverweis uintptr = listenknoten.adressverweis
	return Pointer(adressverweis)
}
func (selbst *LinkedListe) Inhaltvon(adressverweis uintptr) int {
	var n *TListenknoten = selbst.head
	i := 0
	for ; i < selbst.Größe_2; i++ {
		if adressverweis == n.adressverweis {
			return i
		}
		n = n.weiter
	}
	return -1
}
func (selbst *LinkedListe) Entfernen(adressverweis uintptr) {
	inhalt := selbst.Inhaltvon(adressverweis)
	if inhalt < 0 {
		return
	}
	selbst.Entfernenat(inhalt)
}
func (selbst *LinkedListe) Entfernenat(inhalt int) {
	if inhalt < 0 || inhalt >= selbst.Größe_2 {
		return
	}
	listenknoten := selbst.GetKnotenat(inhalt)
	if listenknoten == nil {
		return
	}
	if listenknoten.previous != nil {
		listenknoten.previous.weiter = listenknoten.weiter
	} else {
		selbst.head = listenknoten.weiter
	}
	if listenknoten.weiter != nil {
		listenknoten.weiter.previous = listenknoten.previous
	} else {
		selbst.tail = listenknoten.previous
	}
	selbst.Größe_2 = selbst.Größe_2 - 1

	if selbst.mem != nil {
		selbst.mem.Frei(Pointer(listenknoten))
	}
}

var konsole_2 = TKonsole{}

func (selbst *LinkedListe) Drucken() {
	konsole_2.MDruckenxy("LinkedList:", 1, 1)
	konsole_2.MUnsignedinteger32Drucken(uint32(uintptr(Pointer(selbst))))
	for i := 0; i < selbst.Größe_2; i++ {
		listenknoten := (*TListenknoten)(selbst.Getat(i))
		konsole_2.MUnsignedinteger32Drucken(uint32(listenknoten.adressverweis))
		konsole_2.MDrucken(":")
	}
}
