/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxfileAttenteTaille uint32 = 0x1FFFFFF
const FileAttenteDémarreraddress uint32 = 0x1000000

type TMémoirechunk struct {
	suivant		*TMémoirechunk
	previous	*TMémoirechunk
	allocated	bool

	taille	uint32
}

type TMémoiregestionnaire struct {
}

var first *TMémoirechunk
var Actifmémoiregestionnaire *TMémoiregestionnaire = nil
var mémoirechunkTaille uint32

func (self *TMémoiregestionnaire) Init(démarrer uint32, taille uint32) {

	Actifmémoiregestionnaire = self

	mémoirechunkTaille = uint32(Sizeof(TMémoirechunk{}))

	if taille < mémoirechunkTaille {
		first = nil
	} else {
		first = (*TMémoirechunk)(Pointer(uintptr(FileAttenteDémarreraddress) + uintptr(démarrer)))
		first.allocated = false
		first.previous = nil
		first.suivant = nil
		first.taille = taille - mémoirechunkTaille
	}
}
func (self *TMémoiregestionnaire) Détruire() {
	if Actifmémoiregestionnaire == self {
		Actifmémoiregestionnaire = nil
	}
}
func (self *TMémoiregestionnaire) Allouer_la_mémoire(taille uint32) Pointer {
	var rÉSULTAT *TMémoirechunk = nil

	var chunk *TMémoirechunk = first
	for ; chunk != nil && rÉSULTAT == nil; chunk = chunk.suivant {
		if chunk.taille > taille && !chunk.allocated {
			rÉSULTAT = chunk
		}
	}

	if rÉSULTAT == nil {
		return nil
	}

	if rÉSULTAT.taille >= (taille + mémoirechunkTaille + 1) {

		var temporary *TMémoirechunk
		temporary = (*TMémoirechunk)(Pointer(uintptr(uint32(uintptr(Pointer(rÉSULTAT))) + mémoirechunkTaille + taille)))

		temporary.allocated = false
		temporary.taille = rÉSULTAT.taille - taille - mémoirechunkTaille
		temporary.previous = rÉSULTAT
		temporary.suivant = rÉSULTAT.suivant

		if temporary.suivant != nil {
			temporary.suivant.previous = temporary
		}

		rÉSULTAT.taille = taille
		rÉSULTAT.suivant = temporary
	}
	rÉSULTAT.allocated = true

	return Pointer(uintptr(Pointer(rÉSULTAT)) + uintptr(mémoirechunkTaille))
}
func (self *TMémoiregestionnaire) Alignedmalloc(taille uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if taille == 0 || taille > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rÉSULTAT *TMémoirechunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.suivant {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(mémoirechunkTaille))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.taille && taille <= chunk.taille-diff {
			rÉSULTAT = chunk
			break
		}
	}
	if rÉSULTAT == nil {
		return nil, 0
	}
	taille += diff
	if rÉSULTAT.taille-taille >= mémoirechunkTaille+1 {
		temporary := (*TMémoirechunk)(Pointer(uintptr(Pointer(rÉSULTAT)) + uintptr(mémoirechunkTaille) + uintptr(taille)))
		temporary.allocated = false
		temporary.taille = rÉSULTAT.taille - taille - mémoirechunkTaille
		temporary.previous = rÉSULTAT
		temporary.suivant = rÉSULTAT.suivant
		if temporary.suivant != nil {
			temporary.suivant.previous = temporary
		}
		rÉSULTAT.taille = taille
		rÉSULTAT.suivant = temporary
	}
	rÉSULTAT.allocated = true
	return Pointer(uintptr(Pointer(rÉSULTAT)) + uintptr(mémoirechunkTaille) + uintptr(diff)), diff
}
func (self *TMémoiregestionnaire) Libre(référence_mémoire_2 Pointer) {
	var chunk *TMémoirechunk = (*TMémoirechunk)(Pointer(uintptr(référence_mémoire_2) - uintptr(mémoirechunkTaille)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.suivant = chunk.suivant
		chunk.previous.taille += chunk.taille + mémoirechunkTaille
		if chunk.suivant != nil {
			chunk.suivant.previous = chunk.previous
		}
	}

	if chunk.suivant != nil && !chunk.suivant.allocated {
		chunk.taille += chunk.suivant.taille + mémoirechunkTaille
		chunk.suivant = chunk.suivant.suivant
		if chunk.suivant != nil {
			chunk.suivant.previous = chunk
		}
	}
}
func Nouveau(taille int) Pointer {
	if Actifmémoiregestionnaire == nil {
		return nil
	}
	return Actifmémoiregestionnaire.Allouer_la_mémoire(uint32(taille))
}
func Supprimer(référence_mémoire_2 Pointer) {
	if Actifmémoiregestionnaire != nil {
		Actifmémoiregestionnaire.Libre(référence_mémoire_2)
	}
}
