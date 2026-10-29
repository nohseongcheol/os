/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MàxqueueMida uint32 = 0x1FFFFFF
const QueueIniciaAdreça uint32 = 0x1000000

type TMemòriachunk struct {
	següent		*TMemòriachunk
	previous	*TMemòriachunk
	allocated	bool

	mida	uint32
}

type TMemòriamanager struct {
}

var first *TMemòriachunk
var ActiuMemòriamanager *TMemòriamanager = nil
var memòriachunkMida uint32

func (unmateix *TMemòriamanager) Init(inicia uint32, mida uint32) {

	ActiuMemòriamanager = unmateix

	memòriachunkMida = uint32(Sizeof(TMemòriachunk{}))

	if mida < memòriachunkMida {
		first = nil
	} else {
		first = (*TMemòriachunk)(Pointer(uintptr(QueueIniciaAdreça) + uintptr(inicia)))
		first.allocated = false
		first.previous = nil
		first.següent = nil
		first.mida = mida - memòriachunkMida
	}
}
func (unmateix *TMemòriamanager) Destrueix() {
	if ActiuMemòriamanager == unmateix {
		ActiuMemòriamanager = nil
	}
}
func (unmateix *TMemòriamanager) Malloc(mida uint32) Pointer {
	var rESULTAT *TMemòriachunk = nil

	var chunk *TMemòriachunk = first
	for ; chunk != nil && rESULTAT == nil; chunk = chunk.següent {
		if chunk.mida > mida && !chunk.allocated {
			rESULTAT = chunk
		}
	}

	if rESULTAT == nil {
		return nil
	}

	if rESULTAT.mida >= (mida + memòriachunkMida + 1) {

		var temporary *TMemòriachunk
		temporary = (*TMemòriachunk)(Pointer(uintptr(uint32(uintptr(Pointer(rESULTAT))) + memòriachunkMida + mida)))

		temporary.allocated = false
		temporary.mida = rESULTAT.mida - mida - memòriachunkMida
		temporary.previous = rESULTAT
		temporary.següent = rESULTAT.següent

		if temporary.següent != nil {
			temporary.següent.previous = temporary
		}

		rESULTAT.mida = mida
		rESULTAT.següent = temporary
	}
	rESULTAT.allocated = true

	return Pointer(uintptr(Pointer(rESULTAT)) + uintptr(memòriachunkMida))
}
func (unmateix *TMemòriamanager) Alignedmalloc(mida uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if mida == 0 || mida > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rESULTAT *TMemòriachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.següent {
		if chunk.allocated {
			continue
		}
		adreça := uint32(uintptr(Pointer(chunk)) + uintptr(memòriachunkMida))
		diff = (0x1000 - (adreça & 0xFFF)) & 0xFFF
		if adreça+diff < adreça {
			continue
		}
		if diff <= chunk.mida && mida <= chunk.mida-diff {
			rESULTAT = chunk
			break
		}
	}
	if rESULTAT == nil {
		return nil, 0
	}
	mida += diff
	if rESULTAT.mida-mida >= memòriachunkMida+1 {
		temporary := (*TMemòriachunk)(Pointer(uintptr(Pointer(rESULTAT)) + uintptr(memòriachunkMida) + uintptr(mida)))
		temporary.allocated = false
		temporary.mida = rESULTAT.mida - mida - memòriachunkMida
		temporary.previous = rESULTAT
		temporary.següent = rESULTAT.següent
		if temporary.següent != nil {
			temporary.següent.previous = temporary
		}
		rESULTAT.mida = mida
		rESULTAT.següent = temporary
	}
	rESULTAT.allocated = true
	return Pointer(uintptr(Pointer(rESULTAT)) + uintptr(memòriachunkMida) + uintptr(diff)), diff
}
func (unmateix *TMemòriamanager) Lliure(punter_2 Pointer) {
	var chunk *TMemòriachunk = (*TMemòriachunk)(Pointer(uintptr(punter_2) - uintptr(memòriachunkMida)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.següent = chunk.següent
		chunk.previous.mida += chunk.mida + memòriachunkMida
		if chunk.següent != nil {
			chunk.següent.previous = chunk.previous
		}
	}

	if chunk.següent != nil && !chunk.següent.allocated {
		chunk.mida += chunk.següent.mida + memòriachunkMida
		chunk.següent = chunk.següent.següent
		if chunk.següent != nil {
			chunk.següent.previous = chunk
		}
	}
}
func Nou(mida int) Pointer {
	if ActiuMemòriamanager == nil {
		return nil
	}
	return ActiuMemòriamanager.Malloc(uint32(mida))
}
func Suprimeix(punter_2 Pointer) {
	if ActiuMemòriamanager != nil {
		ActiuMemòriamanager.Lliure(punter_2)
	}
}
