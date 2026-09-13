package memorymananger

import . "unsafe"

const MaksymalnaqueueRozmiar uint32 = 0x1FFFFFF
const QueueUruchomAdres uint32 = 0x1000000

type TPamięćchunk struct {
	następny	*TPamięćchunk
	previous	*TPamięćchunk
	allocated	bool

	rozmiar	uint32
}

type TPamięćmanager struct {
}

var first *TPamięćchunk
var AktywnePamięćmanager *TPamięćmanager = nil
var pamięćchunkRozmiar uint32

func (bieżący *TPamięćmanager) Init(uruchom uint32, rozmiar uint32) {

	AktywnePamięćmanager = bieżący

	pamięćchunkRozmiar = uint32(Sizeof(TPamięćchunk{}))

	if rozmiar < pamięćchunkRozmiar {
		first = nil
	} else {
		first = (*TPamięćchunk)(Pointer(uintptr(QueueUruchomAdres) + uintptr(uruchom)))
		first.allocated = false
		first.previous = nil
		first.następny = nil
		first.rozmiar = rozmiar - pamięćchunkRozmiar
	}
}
func (bieżący *TPamięćmanager) Zniszcz() {
	if AktywnePamięćmanager == bieżący {
		AktywnePamięćmanager = nil
	}
}
func (bieżący *TPamięćmanager) Przydziel_pamięć(rozmiar uint32) Pointer {
	var wYNIK *TPamięćchunk = nil

	var chunk *TPamięćchunk = first
	for ; chunk != nil && wYNIK == nil; chunk = chunk.następny {
		if chunk.rozmiar > rozmiar && !chunk.allocated {
			wYNIK = chunk
		}
	}

	if wYNIK == nil {
		return nil
	}

	if wYNIK.rozmiar >= (rozmiar + pamięćchunkRozmiar + 1) {

		var temporary *TPamięćchunk
		temporary = (*TPamięćchunk)(Pointer(uintptr(uint32(uintptr(Pointer(wYNIK))) + pamięćchunkRozmiar + rozmiar)))

		temporary.allocated = false
		temporary.rozmiar = wYNIK.rozmiar - rozmiar - pamięćchunkRozmiar
		temporary.previous = wYNIK
		temporary.następny = wYNIK.następny

		if temporary.następny != nil {
			temporary.następny.previous = temporary
		}

		wYNIK.rozmiar = rozmiar
		wYNIK.następny = temporary
	}
	wYNIK.allocated = true

	return Pointer(uintptr(Pointer(wYNIK)) + uintptr(pamięćchunkRozmiar))
}
func (bieżący *TPamięćmanager) Alignedmalloc(rozmiar uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if rozmiar == 0 || rozmiar > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var wYNIK *TPamięćchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.następny {
		if chunk.allocated {
			continue
		}
		adres := uint32(uintptr(Pointer(chunk)) + uintptr(pamięćchunkRozmiar))
		diff = (0x1000 - (adres & 0xFFF)) & 0xFFF
		if adres+diff < adres {
			continue
		}
		if diff <= chunk.rozmiar && rozmiar <= chunk.rozmiar-diff {
			wYNIK = chunk
			break
		}
	}
	if wYNIK == nil {
		return nil, 0
	}
	rozmiar += diff
	if wYNIK.rozmiar-rozmiar >= pamięćchunkRozmiar+1 {
		temporary := (*TPamięćchunk)(Pointer(uintptr(Pointer(wYNIK)) + uintptr(pamięćchunkRozmiar) + uintptr(rozmiar)))
		temporary.allocated = false
		temporary.rozmiar = wYNIK.rozmiar - rozmiar - pamięćchunkRozmiar
		temporary.previous = wYNIK
		temporary.następny = wYNIK.następny
		if temporary.następny != nil {
			temporary.następny.previous = temporary
		}
		wYNIK.rozmiar = rozmiar
		wYNIK.następny = temporary
	}
	wYNIK.allocated = true
	return Pointer(uintptr(Pointer(wYNIK)) + uintptr(pamięćchunkRozmiar) + uintptr(diff)), diff
}
func (bieżący *TPamięćmanager) Wolne(odwołanie_do_adresu_2 Pointer) {
	var chunk *TPamięćchunk = (*TPamięćchunk)(Pointer(uintptr(odwołanie_do_adresu_2) - uintptr(pamięćchunkRozmiar)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.następny = chunk.następny
		chunk.previous.rozmiar += chunk.rozmiar + pamięćchunkRozmiar
		if chunk.następny != nil {
			chunk.następny.previous = chunk.previous
		}
	}

	if chunk.następny != nil && !chunk.następny.allocated {
		chunk.rozmiar += chunk.następny.rozmiar + pamięćchunkRozmiar
		chunk.następny = chunk.następny.następny
		if chunk.następny != nil {
			chunk.następny.previous = chunk
		}
	}
}
func Nowy(rozmiar int) Pointer {
	if AktywnePamięćmanager == nil {
		return nil
	}
	return AktywnePamięćmanager.Przydziel_pamięć(uint32(rozmiar))
}
func Usuń(odwołanie_do_adresu_2 Pointer) {
	if AktywnePamięćmanager != nil {
		AktywnePamięćmanager.Wolne(odwołanie_do_adresu_2)
	}
}
