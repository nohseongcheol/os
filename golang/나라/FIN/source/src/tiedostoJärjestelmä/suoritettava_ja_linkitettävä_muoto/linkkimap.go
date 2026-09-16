/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package suoritettava_ja_linkitettävä_muoto

import . "unsafe"
import . "konsoli"

import mem "muistimanager"

type Linkki struct {
	Dynaaminen	uintptr
	Previous	*Linkki
	Seuraava	*Linkki
}
type Linkkimap struct {
	First		*Linkki
	Viimeinen	*Linkki

	Koko_2	int

	mem	*mem.TMuistimanager
}

func (itse *Linkkimap) Init(mem *mem.TMuistimanager) {
	itse.mem = mem
}
func (itse *Linkkimap) Clone() Linkkimap {
	var linkkimap Linkkimap

	linkkimap.Init(itse.mem)

	Linkki := itse.First

	for ; Linkki != nil; Linkki = Linkki.Seuraava {
		linkkimap.Lisää_listan_loppuun(Linkki.Dynaaminen)
	}
	return linkkimap
}
func (itse *Linkkimap) Lisää_listan_alkuun(Dynaaminen uintptr) {
	uusiLinkki := (*Linkki)(itse.mem.Varaa_muistia(uint32(Sizeof(Linkki{}))))
	uusiLinkki.Dynaaminen = Dynaaminen
	uusiLinkki.Seuraava = itse.First
	itse.First = uusiLinkki
	itse.Koko_2++

	if itse.First.Seuraava == nil {
		itse.Viimeinen = itse.First
	}
}
func (itse *Linkkimap) Lisää_listan_loppuun(Dynaaminen uintptr) {
	if Dynaaminen == 0 {
		return
	}

	if itse.Koko_2 == 0 {
		itse.Lisää_listan_alkuun(Dynaaminen)
	} else {
		uusiLinkki := (*Linkki)(itse.mem.Varaa_muistia(uint32(Sizeof(Linkki{}))))
		uusiLinkki.Dynaaminen = Dynaaminen
		uusiLinkki.Seuraava = nil
		itse.Viimeinen.Seuraava = uusiLinkki
		itse.Viimeinen = uusiLinkki
		itse.Koko_2++
	}
}
func (itse *Linkkimap) Tulosta(x uint16, y uint16) {
	Linkki := itse.First
	konsoli_2 := TKonsoli{}
	konsoli_2.MTulostaxy("linkmap : ", x, y)
	for ; Linkki != nil; Linkki = Linkki.Seuraava {
		konsoli_2.MUnsignedinteger32Tulosta(uint32(Linkki.Dynaaminen))
		konsoli_2.MTulosta("+")

	}
}
