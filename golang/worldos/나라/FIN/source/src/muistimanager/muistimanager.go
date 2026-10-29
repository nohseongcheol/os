/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaksimiqueueKoko uint32 = 0x1FFFFFF
const QueueKäynnistäaddress uint32 = 0x1000000

type TMuistichunk struct {
	seuraava	*TMuistichunk
	previous	*TMuistichunk
	allocated	bool

	koko	uint32
}

type TMuistimanager struct {
}

var first *TMuistichunk
var AktiivinenMuistimanager *TMuistimanager = nil
var muistichunkKoko uint32

func (itse *TMuistimanager) Init(käynnistä uint32, koko uint32) {

	AktiivinenMuistimanager = itse

	muistichunkKoko = uint32(Sizeof(TMuistichunk{}))

	if koko < muistichunkKoko {
		first = nil
	} else {
		first = (*TMuistichunk)(Pointer(uintptr(QueueKäynnistäaddress) + uintptr(käynnistä)))
		first.allocated = false
		first.previous = nil
		first.seuraava = nil
		first.koko = koko - muistichunkKoko
	}
}
func (itse *TMuistimanager) Tuhoa() {
	if AktiivinenMuistimanager == itse {
		AktiivinenMuistimanager = nil
	}
}
func (itse *TMuistimanager) Varaa_muistia(koko uint32) Pointer {
	var tULOS *TMuistichunk = nil

	var chunk *TMuistichunk = first
	for ; chunk != nil && tULOS == nil; chunk = chunk.seuraava {
		if chunk.koko > koko && !chunk.allocated {
			tULOS = chunk
		}
	}

	if tULOS == nil {
		return nil
	}

	if tULOS.koko >= (koko + muistichunkKoko + 1) {

		var temporary *TMuistichunk
		temporary = (*TMuistichunk)(Pointer(uintptr(uint32(uintptr(Pointer(tULOS))) + muistichunkKoko + koko)))

		temporary.allocated = false
		temporary.koko = tULOS.koko - koko - muistichunkKoko
		temporary.previous = tULOS
		temporary.seuraava = tULOS.seuraava

		if temporary.seuraava != nil {
			temporary.seuraava.previous = temporary
		}

		tULOS.koko = koko
		tULOS.seuraava = temporary
	}
	tULOS.allocated = true

	return Pointer(uintptr(Pointer(tULOS)) + uintptr(muistichunkKoko))
}
func (itse *TMuistimanager) Alignedmalloc(koko uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if koko == 0 || koko > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var tULOS *TMuistichunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.seuraava {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(muistichunkKoko))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.koko && koko <= chunk.koko-diff {
			tULOS = chunk
			break
		}
	}
	if tULOS == nil {
		return nil, 0
	}
	koko += diff
	if tULOS.koko-koko >= muistichunkKoko+1 {
		temporary := (*TMuistichunk)(Pointer(uintptr(Pointer(tULOS)) + uintptr(muistichunkKoko) + uintptr(koko)))
		temporary.allocated = false
		temporary.koko = tULOS.koko - koko - muistichunkKoko
		temporary.previous = tULOS
		temporary.seuraava = tULOS.seuraava
		if temporary.seuraava != nil {
			temporary.seuraava.previous = temporary
		}
		tULOS.koko = koko
		tULOS.seuraava = temporary
	}
	tULOS.allocated = true
	return Pointer(uintptr(Pointer(tULOS)) + uintptr(muistichunkKoko) + uintptr(diff)), diff
}
func (itse *TMuistimanager) Vapaana(osoiteviite_2 Pointer) {
	var chunk *TMuistichunk = (*TMuistichunk)(Pointer(uintptr(osoiteviite_2) - uintptr(muistichunkKoko)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.seuraava = chunk.seuraava
		chunk.previous.koko += chunk.koko + muistichunkKoko
		if chunk.seuraava != nil {
			chunk.seuraava.previous = chunk.previous
		}
	}

	if chunk.seuraava != nil && !chunk.seuraava.allocated {
		chunk.koko += chunk.seuraava.koko + muistichunkKoko
		chunk.seuraava = chunk.seuraava.seuraava
		if chunk.seuraava != nil {
			chunk.seuraava.previous = chunk
		}
	}
}
func Uusi(koko int) Pointer {
	if AktiivinenMuistimanager == nil {
		return nil
	}
	return AktiivinenMuistimanager.Varaa_muistia(uint32(koko))
}
func Poista(osoiteviite_2 Pointer) {
	if AktiivinenMuistimanager != nil {
		AktiivinenMuistimanager.Vapaana(osoiteviite_2)
	}
}
