/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package listaa

import . "unsafe"
import . "konsoli"
import mem "muistimanager"

type TListasolmu struct {
	osoiteviite		uintptr
	previous	*TListasolmu
	seuraava	*TListasolmu
}

type Linkedlistaa struct {
	head	*TListasolmu
	tail	*TListasolmu
	Koko_2	int

	mem	*mem.TMuistimanager
}

func (itse *Linkedlistaa) Init(mem *mem.TMuistimanager) {
	itse.head = nil
	itse.tail = nil
	itse.Koko_2 = 0

	itse.mem = mem
}
func (itse *Linkedlistaa) Lisää_listan_alkuun(osoiteviite uintptr) {
	uusiLaite := (*TListasolmu)(itse.mem.Varaa_muistia(uint32(Sizeof(TListasolmu{}))))
	if uusiLaite == nil {
		return
	}
	uusiLaite.osoiteviite = osoiteviite
	uusiLaite.previous = nil
	uusiLaite.seuraava = itse.head
	if itse.head != nil {
		itse.head.previous = uusiLaite
	}
	itse.head = uusiLaite
	itse.Koko_2++

	if itse.head.seuraava == nil {
		itse.tail = itse.head
	}

}
func (itse *Linkedlistaa) Lisää_listan_loppuun(osoiteviite uintptr) {
	if itse.Koko_2 == 0 {
		itse.Lisää_listan_alkuun(osoiteviite)
	} else {
		uusiLaite := (*TListasolmu)(itse.mem.Varaa_muistia(uint32(Sizeof(TListasolmu{}))))
		if uusiLaite == nil {
			return
		}
		uusiLaite.osoiteviite = osoiteviite
		uusiLaite.previous = itse.tail
		uusiLaite.seuraava = nil
		itse.tail.seuraava = uusiLaite
		itse.tail = uusiLaite
		itse.Koko_2++
	}
}
func (itse *Linkedlistaa) Lisää_indeksin_kohdalle(hakemisto int, osoiteviite uintptr) {
	if hakemisto == 0 {
		itse.Lisää_listan_alkuun(osoiteviite)
	} else {
		previousLaite := itse.GetLaiteat(hakemisto - 1)
		seuraavaLaite := previousLaite.seuraava
		uusiLaite := (*TListasolmu)(itse.mem.Varaa_muistia(uint32(Sizeof(TListasolmu{}))))
		if uusiLaite == nil {
			return
		}
		uusiLaite.osoiteviite = osoiteviite

		previousLaite.seuraava = uusiLaite
		uusiLaite.previous = previousLaite
		uusiLaite.seuraava = seuraavaLaite
		if seuraavaLaite != nil {
			seuraavaLaite.previous = uusiLaite
		}

		itse.Koko_2++

		if uusiLaite.seuraava == nil {
			itse.tail = uusiLaite
		}
	}
}
func (itse *Linkedlistaa) GetLaiteat(hakemisto int) *TListasolmu {
	if hakemisto < 0 || hakemisto >= itse.Koko_2 {
		return nil
	}
	var x *TListasolmu = itse.head
	for i := 0; i < hakemisto; i++ {
		x = x.seuraava
	}
	return x
}

func (itse *Linkedlistaa) AsetaLaiteat(hakemisto int, osoiteviite uintptr) {
	var x *TListasolmu = itse.head
	for i := 0; i < hakemisto; i++ {
		x = x.seuraava
	}
	if x != nil {
		x.osoiteviite = osoiteviite
	}
}
func (itse *Linkedlistaa) Getat(hakemisto int) Pointer {
	listasolmu := itse.GetLaiteat(hakemisto)
	if listasolmu == nil {
		return nil
	}
	var osoiteviite uintptr = listasolmu.osoiteviite
	return Pointer(osoiteviite)
}
func (itse *Linkedlistaa) Hakemistoof(osoiteviite uintptr) int {
	var n *TListasolmu = itse.head
	i := 0
	for ; i < itse.Koko_2; i++ {
		if osoiteviite == n.osoiteviite {
			return i
		}
		n = n.seuraava
	}
	return -1
}
func (itse *Linkedlistaa) Poista_2(osoiteviite uintptr) {
	hakemisto := itse.Hakemistoof(osoiteviite)
	if hakemisto < 0 {
		return
	}
	itse.Poistaat(hakemisto)
}
func (itse *Linkedlistaa) Poistaat(hakemisto int) {
	if hakemisto < 0 || hakemisto >= itse.Koko_2 {
		return
	}
	listasolmu := itse.GetLaiteat(hakemisto)
	if listasolmu == nil {
		return
	}
	if listasolmu.previous != nil {
		listasolmu.previous.seuraava = listasolmu.seuraava
	} else {
		itse.head = listasolmu.seuraava
	}
	if listasolmu.seuraava != nil {
		listasolmu.seuraava.previous = listasolmu.previous
	} else {
		itse.tail = listasolmu.previous
	}
	itse.Koko_2 = itse.Koko_2 - 1

	if itse.mem != nil {
		itse.mem.Vapaana(Pointer(listasolmu))
	}
}

var konsoli_2 = TKonsoli{}

func (itse *Linkedlistaa) Tulosta() {
	konsoli_2.MTulostaxy("LinkedList:", 1, 1)
	konsoli_2.MUnsignedinteger32Tulosta(uint32(uintptr(Pointer(itse))))
	for i := 0; i < itse.Koko_2; i++ {
		listasolmu := (*TListasolmu)(itse.Getat(i))
		konsoli_2.MUnsignedinteger32Tulosta(uint32(listasolmu.osoiteviite))
		konsoli_2.MTulosta(":")
	}
}
