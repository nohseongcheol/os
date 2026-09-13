package format_wykonywalny_i_konsolidowalny

import . "unsafe"
import . "konsola"

import mem "pamięćmanager"

type Odnośnik struct {
	Dynamicznie	uintptr
	Previous	*Odnośnik
	Następny	*Odnośnik
}
type Odnośnikmap struct {
	First	*Odnośnik
	Ostatni	*Odnośnik

	Rozmiar_2	int

	mem	*mem.TPamięćmanager
}

func (bieżący *Odnośnikmap) Init(mem *mem.TPamięćmanager) {
	bieżący.mem = mem
}
func (bieżący *Odnośnikmap) Clone() Odnośnikmap {
	var odnośnikmap Odnośnikmap

	odnośnikmap.Init(bieżący.mem)

	Odnośnik := bieżący.First

	for ; Odnośnik != nil; Odnośnik = Odnośnik.Następny {
		odnośnikmap.Dodaj_na_końcu_listy(Odnośnik.Dynamicznie)
	}
	return odnośnikmap
}
func (bieżący *Odnośnikmap) Dodaj_na_początku_listy(Dynamicznie uintptr) {
	nowyOdnośnik := (*Odnośnik)(bieżący.mem.Przydziel_pamięć(uint32(Sizeof(Odnośnik{}))))
	nowyOdnośnik.Dynamicznie = Dynamicznie
	nowyOdnośnik.Następny = bieżący.First
	bieżący.First = nowyOdnośnik
	bieżący.Rozmiar_2++

	if bieżący.First.Następny == nil {
		bieżący.Ostatni = bieżący.First
	}
}
func (bieżący *Odnośnikmap) Dodaj_na_końcu_listy(Dynamicznie uintptr) {
	if Dynamicznie == 0 {
		return
	}

	if bieżący.Rozmiar_2 == 0 {
		bieżący.Dodaj_na_początku_listy(Dynamicznie)
	} else {
		nowyOdnośnik := (*Odnośnik)(bieżący.mem.Przydziel_pamięć(uint32(Sizeof(Odnośnik{}))))
		nowyOdnośnik.Dynamicznie = Dynamicznie
		nowyOdnośnik.Następny = nil
		bieżący.Ostatni.Następny = nowyOdnośnik
		bieżący.Ostatni = nowyOdnośnik
		bieżący.Rozmiar_2++
	}
}
func (bieżący *Odnośnikmap) Wydrukuj(x uint16, y uint16) {
	Odnośnik := bieżący.First
	konsola_2 := TKonsola{}
	konsola_2.MWydrukujxy("linkmap : ", x, y)
	for ; Odnośnik != nil; Odnośnik = Odnośnik.Następny {
		konsola_2.MUnsignedinteger32Wydrukuj(uint32(Odnośnik.Dynamicznie))
		konsola_2.MWydrukuj("+")

	}
}
