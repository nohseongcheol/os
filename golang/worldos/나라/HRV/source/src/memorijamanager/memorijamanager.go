/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaksqueueVeličina uint32 = 0x1FFFFFF
const QueuePokreniaddress uint32 = 0x1000000

type TMemorijachunk struct {
	slijedeće	*TMemorijachunk
	previous	*TMemorijachunk
	allocated	bool

	veličina	uint32
}

type TMemorijamanager struct {
}

var first *TMemorijachunk
var AktivanMemorijamanager *TMemorijamanager = nil
var memorijachunkVeličina uint32

func (sam *TMemorijamanager) Init(pokreni uint32, veličina uint32) {

	AktivanMemorijamanager = sam

	memorijachunkVeličina = uint32(Sizeof(TMemorijachunk{}))

	if veličina < memorijachunkVeličina {
		first = nil
	} else {
		first = (*TMemorijachunk)(Pointer(uintptr(QueuePokreniaddress) + uintptr(pokreni)))
		first.allocated = false
		first.previous = nil
		first.slijedeće = nil
		first.veličina = veličina - memorijachunkVeličina
	}
}
func (sam *TMemorijamanager) Uništi() {
	if AktivanMemorijamanager == sam {
		AktivanMemorijamanager = nil
	}
}
func (sam *TMemorijamanager) Malloc(veličina uint32) Pointer {
	var rEZULTAT *TMemorijachunk = nil

	var chunk *TMemorijachunk = first
	for ; chunk != nil && rEZULTAT == nil; chunk = chunk.slijedeće {
		if chunk.veličina > veličina && !chunk.allocated {
			rEZULTAT = chunk
		}
	}

	if rEZULTAT == nil {
		return nil
	}

	if rEZULTAT.veličina >= (veličina + memorijachunkVeličina + 1) {

		var temporary *TMemorijachunk
		temporary = (*TMemorijachunk)(Pointer(uintptr(uint32(uintptr(Pointer(rEZULTAT))) + memorijachunkVeličina + veličina)))

		temporary.allocated = false
		temporary.veličina = rEZULTAT.veličina - veličina - memorijachunkVeličina
		temporary.previous = rEZULTAT
		temporary.slijedeće = rEZULTAT.slijedeće

		if temporary.slijedeće != nil {
			temporary.slijedeće.previous = temporary
		}

		rEZULTAT.veličina = veličina
		rEZULTAT.slijedeće = temporary
	}
	rEZULTAT.allocated = true

	return Pointer(uintptr(Pointer(rEZULTAT)) + uintptr(memorijachunkVeličina))
}
func (sam *TMemorijamanager) Alignedmalloc(veličina uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if veličina == 0 || veličina > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rEZULTAT *TMemorijachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.slijedeće {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorijachunkVeličina))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.veličina && veličina <= chunk.veličina-diff {
			rEZULTAT = chunk
			break
		}
	}
	if rEZULTAT == nil {
		return nil, 0
	}
	veličina += diff
	if rEZULTAT.veličina-veličina >= memorijachunkVeličina+1 {
		temporary := (*TMemorijachunk)(Pointer(uintptr(Pointer(rEZULTAT)) + uintptr(memorijachunkVeličina) + uintptr(veličina)))
		temporary.allocated = false
		temporary.veličina = rEZULTAT.veličina - veličina - memorijachunkVeličina
		temporary.previous = rEZULTAT
		temporary.slijedeće = rEZULTAT.slijedeće
		if temporary.slijedeće != nil {
			temporary.slijedeće.previous = temporary
		}
		rEZULTAT.veličina = veličina
		rEZULTAT.slijedeće = temporary
	}
	rEZULTAT.allocated = true
	return Pointer(uintptr(Pointer(rEZULTAT)) + uintptr(memorijachunkVeličina) + uintptr(diff)), diff
}
func (sam *TMemorijamanager) Slobodno(pokazivač_2 Pointer) {
	var chunk *TMemorijachunk = (*TMemorijachunk)(Pointer(uintptr(pokazivač_2) - uintptr(memorijachunkVeličina)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.slijedeće = chunk.slijedeće
		chunk.previous.veličina += chunk.veličina + memorijachunkVeličina
		if chunk.slijedeće != nil {
			chunk.slijedeće.previous = chunk.previous
		}
	}

	if chunk.slijedeće != nil && !chunk.slijedeće.allocated {
		chunk.veličina += chunk.slijedeće.veličina + memorijachunkVeličina
		chunk.slijedeće = chunk.slijedeće.slijedeće
		if chunk.slijedeće != nil {
			chunk.slijedeće.previous = chunk
		}
	}
}
func Novi(veličina int) Pointer {
	if AktivanMemorijamanager == nil {
		return nil
	}
	return AktivanMemorijamanager.Malloc(uint32(veličina))
}
func Obriši(pokazivač_2 Pointer) {
	if AktivanMemorijamanager != nil {
		AktivanMemorijamanager.Slobodno(pokazivač_2)
	}
}
