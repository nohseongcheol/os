package memorymananger

import . "unsafe"

const MaksqueueStørrelse uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TMinnechunk struct {
	neste		*TMinnechunk
	previous	*TMinnechunk
	allocated	bool

	størrelse	uint32
}

type TMinnemanager struct {
}

var first *TMinnechunk
var AktivMinnemanager *TMinnemanager = nil
var minnechunkStørrelse uint32

func (selv *TMinnemanager) Init(start uint32, størrelse uint32) {

	AktivMinnemanager = selv

	minnechunkStørrelse = uint32(Sizeof(TMinnechunk{}))

	if størrelse < minnechunkStørrelse {
		first = nil
	} else {
		first = (*TMinnechunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.neste = nil
		first.størrelse = størrelse - minnechunkStørrelse
	}
}
func (selv *TMinnemanager) Ødelegg() {
	if AktivMinnemanager == selv {
		AktivMinnemanager = nil
	}
}
func (selv *TMinnemanager) Malloc(størrelse uint32) Pointer {
	var result *TMinnechunk = nil

	var chunk *TMinnechunk = first
	for ; chunk != nil && result == nil; chunk = chunk.neste {
		if chunk.størrelse > størrelse && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.størrelse >= (størrelse + minnechunkStørrelse + 1) {

		var temporary *TMinnechunk
		temporary = (*TMinnechunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + minnechunkStørrelse + størrelse)))

		temporary.allocated = false
		temporary.størrelse = result.størrelse - størrelse - minnechunkStørrelse
		temporary.previous = result
		temporary.neste = result.neste

		if temporary.neste != nil {
			temporary.neste.previous = temporary
		}

		result.størrelse = størrelse
		result.neste = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(minnechunkStørrelse))
}
func (selv *TMinnemanager) Alignedmalloc(størrelse uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if størrelse == 0 || størrelse > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMinnechunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.neste {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(minnechunkStørrelse))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.størrelse && størrelse <= chunk.størrelse-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	størrelse += diff
	if result.størrelse-størrelse >= minnechunkStørrelse+1 {
		temporary := (*TMinnechunk)(Pointer(uintptr(Pointer(result)) + uintptr(minnechunkStørrelse) + uintptr(størrelse)))
		temporary.allocated = false
		temporary.størrelse = result.størrelse - størrelse - minnechunkStørrelse
		temporary.previous = result
		temporary.neste = result.neste
		if temporary.neste != nil {
			temporary.neste.previous = temporary
		}
		result.størrelse = størrelse
		result.neste = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(minnechunkStørrelse) + uintptr(diff)), diff
}
func (selv *TMinnemanager) Ledig(peker_2 Pointer) {
	var chunk *TMinnechunk = (*TMinnechunk)(Pointer(uintptr(peker_2) - uintptr(minnechunkStørrelse)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.neste = chunk.neste
		chunk.previous.størrelse += chunk.størrelse + minnechunkStørrelse
		if chunk.neste != nil {
			chunk.neste.previous = chunk.previous
		}
	}

	if chunk.neste != nil && !chunk.neste.allocated {
		chunk.størrelse += chunk.neste.størrelse + minnechunkStørrelse
		chunk.neste = chunk.neste.neste
		if chunk.neste != nil {
			chunk.neste.previous = chunk
		}
	}
}
func Ny(størrelse int) Pointer {
	if AktivMinnemanager == nil {
		return nil
	}
	return AktivMinnemanager.Malloc(uint32(størrelse))
}
func Slett(peker_2 Pointer) {
	if AktivMinnemanager != nil {
		AktivMinnemanager.Ledig(peker_2)
	}
}
