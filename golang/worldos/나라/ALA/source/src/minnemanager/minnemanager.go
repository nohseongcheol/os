/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaximalqueueStorlek uint32 = 0x1FFFFFF
const QueueStartaAdress uint32 = 0x1000000

type TMinnechunk struct {
	nästa		*TMinnechunk
	previous	*TMinnechunk
	allocated	bool

	storlek	uint32
}

type TMinnemanager struct {
}

var first *TMinnechunk
var AktivMinnemanager *TMinnemanager = nil
var minnechunkStorlek uint32

func (själv *TMinnemanager) Init(starta uint32, storlek uint32) {

	AktivMinnemanager = själv

	minnechunkStorlek = uint32(Sizeof(TMinnechunk{}))

	if storlek < minnechunkStorlek {
		first = nil
	} else {
		first = (*TMinnechunk)(Pointer(uintptr(QueueStartaAdress) + uintptr(starta)))
		first.allocated = false
		first.previous = nil
		first.nästa = nil
		first.storlek = storlek - minnechunkStorlek
	}
}
func (själv *TMinnemanager) Förstör() {
	if AktivMinnemanager == själv {
		AktivMinnemanager = nil
	}
}
func (själv *TMinnemanager) Tilldela_minne(storlek uint32) Pointer {
	var rESULTAT *TMinnechunk = nil

	var chunk *TMinnechunk = first
	for ; chunk != nil && rESULTAT == nil; chunk = chunk.nästa {
		if chunk.storlek > storlek && !chunk.allocated {
			rESULTAT = chunk
		}
	}

	if rESULTAT == nil {
		return nil
	}

	if rESULTAT.storlek >= (storlek + minnechunkStorlek + 1) {

		var temporary *TMinnechunk
		temporary = (*TMinnechunk)(Pointer(uintptr(uint32(uintptr(Pointer(rESULTAT))) + minnechunkStorlek + storlek)))

		temporary.allocated = false
		temporary.storlek = rESULTAT.storlek - storlek - minnechunkStorlek
		temporary.previous = rESULTAT
		temporary.nästa = rESULTAT.nästa

		if temporary.nästa != nil {
			temporary.nästa.previous = temporary
		}

		rESULTAT.storlek = storlek
		rESULTAT.nästa = temporary
	}
	rESULTAT.allocated = true

	return Pointer(uintptr(Pointer(rESULTAT)) + uintptr(minnechunkStorlek))
}
func (själv *TMinnemanager) Alignedmalloc(storlek uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if storlek == 0 || storlek > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rESULTAT *TMinnechunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.nästa {
		if chunk.allocated {
			continue
		}
		adress := uint32(uintptr(Pointer(chunk)) + uintptr(minnechunkStorlek))
		diff = (0x1000 - (adress & 0xFFF)) & 0xFFF
		if adress+diff < adress {
			continue
		}
		if diff <= chunk.storlek && storlek <= chunk.storlek-diff {
			rESULTAT = chunk
			break
		}
	}
	if rESULTAT == nil {
		return nil, 0
	}
	storlek += diff
	if rESULTAT.storlek-storlek >= minnechunkStorlek+1 {
		temporary := (*TMinnechunk)(Pointer(uintptr(Pointer(rESULTAT)) + uintptr(minnechunkStorlek) + uintptr(storlek)))
		temporary.allocated = false
		temporary.storlek = rESULTAT.storlek - storlek - minnechunkStorlek
		temporary.previous = rESULTAT
		temporary.nästa = rESULTAT.nästa
		if temporary.nästa != nil {
			temporary.nästa.previous = temporary
		}
		rESULTAT.storlek = storlek
		rESULTAT.nästa = temporary
	}
	rESULTAT.allocated = true
	return Pointer(uintptr(Pointer(rESULTAT)) + uintptr(minnechunkStorlek) + uintptr(diff)), diff
}
func (själv *TMinnemanager) Ledigt(adressreferens_2 Pointer) {
	var chunk *TMinnechunk = (*TMinnechunk)(Pointer(uintptr(adressreferens_2) - uintptr(minnechunkStorlek)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.nästa = chunk.nästa
		chunk.previous.storlek += chunk.storlek + minnechunkStorlek
		if chunk.nästa != nil {
			chunk.nästa.previous = chunk.previous
		}
	}

	if chunk.nästa != nil && !chunk.nästa.allocated {
		chunk.storlek += chunk.nästa.storlek + minnechunkStorlek
		chunk.nästa = chunk.nästa.nästa
		if chunk.nästa != nil {
			chunk.nästa.previous = chunk
		}
	}
}
func Ny(storlek int) Pointer {
	if AktivMinnemanager == nil {
		return nil
	}
	return AktivMinnemanager.Tilldela_minne(uint32(storlek))
}
func Tabort(adressreferens_2 Pointer) {
	if AktivMinnemanager != nil {
		AktivMinnemanager.Ledigt(adressreferens_2)
	}
}
