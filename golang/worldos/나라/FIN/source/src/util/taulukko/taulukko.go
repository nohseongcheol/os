/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package taulukko

import . "unsafe"
import . "konsoli"

var laiteTaulukko [100]uintptr

type TTaulukko struct {
	Koko_2 int
}

func (itse *TTaulukko) Lisää(osoiteviite uintptr) {
	laiteTaulukko[itse.Koko_2] = osoiteviite
	itse.Koko_2++
}
func (itse *TTaulukko) Getat(hakemisto int) Pointer {
	return Pointer(laiteTaulukko[hakemisto])
}
func (itse *TTaulukko) Hakemistoof(osoiteviite uintptr) int {
	i := 0
	for ; i < itse.Koko_2; i++ {
		if osoiteviite == laiteTaulukko[i] {
			return i
		}
	}
	return -1
}

var konsoli_2 = TKonsoli{}

func (itse *TTaulukko) Tulosta() {
	konsoli_2.MTulostaxy("array:", 1, 1)

	for i := 0; i < itse.Koko_2; i++ {
		konsoli_2.MUnsignedinteger32Tulosta(uint32(laiteTaulukko[i]))
		konsoli_2.MTulosta(":")
	}
}
