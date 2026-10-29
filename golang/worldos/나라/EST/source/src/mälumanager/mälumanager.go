/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const SuurimqueueSuurus uint32 = 0x1FFFFFF
const QueueKäivitaaddress uint32 = 0x1000000

type TMäluchunk struct {
	järgmine	*TMäluchunk
	previous	*TMäluchunk
	allocated	bool

	suurus	uint32
}

type TMälumanager struct {
}

var first *TMäluchunk
var AktiivneMälumanager *TMälumanager = nil
var mäluchunkSuurus uint32

func (ise *TMälumanager) Init(käivita uint32, suurus uint32) {

	AktiivneMälumanager = ise

	mäluchunkSuurus = uint32(Sizeof(TMäluchunk{}))

	if suurus < mäluchunkSuurus {
		first = nil
	} else {
		first = (*TMäluchunk)(Pointer(uintptr(QueueKäivitaaddress) + uintptr(käivita)))
		first.allocated = false
		first.previous = nil
		first.järgmine = nil
		first.suurus = suurus - mäluchunkSuurus
	}
}
func (ise *TMälumanager) Hävita() {
	if AktiivneMälumanager == ise {
		AktiivneMälumanager = nil
	}
}
func (ise *TMälumanager) Malloc(suurus uint32) Pointer {
	var tULEMUS *TMäluchunk = nil

	var chunk *TMäluchunk = first
	for ; chunk != nil && tULEMUS == nil; chunk = chunk.järgmine {
		if chunk.suurus > suurus && !chunk.allocated {
			tULEMUS = chunk
		}
	}

	if tULEMUS == nil {
		return nil
	}

	if tULEMUS.suurus >= (suurus + mäluchunkSuurus + 1) {

		var temporary *TMäluchunk
		temporary = (*TMäluchunk)(Pointer(uintptr(uint32(uintptr(Pointer(tULEMUS))) + mäluchunkSuurus + suurus)))

		temporary.allocated = false
		temporary.suurus = tULEMUS.suurus - suurus - mäluchunkSuurus
		temporary.previous = tULEMUS
		temporary.järgmine = tULEMUS.järgmine

		if temporary.järgmine != nil {
			temporary.järgmine.previous = temporary
		}

		tULEMUS.suurus = suurus
		tULEMUS.järgmine = temporary
	}
	tULEMUS.allocated = true

	return Pointer(uintptr(Pointer(tULEMUS)) + uintptr(mäluchunkSuurus))
}
func (ise *TMälumanager) Alignedmalloc(suurus uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if suurus == 0 || suurus > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var tULEMUS *TMäluchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.järgmine {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(mäluchunkSuurus))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.suurus && suurus <= chunk.suurus-diff {
			tULEMUS = chunk
			break
		}
	}
	if tULEMUS == nil {
		return nil, 0
	}
	suurus += diff
	if tULEMUS.suurus-suurus >= mäluchunkSuurus+1 {
		temporary := (*TMäluchunk)(Pointer(uintptr(Pointer(tULEMUS)) + uintptr(mäluchunkSuurus) + uintptr(suurus)))
		temporary.allocated = false
		temporary.suurus = tULEMUS.suurus - suurus - mäluchunkSuurus
		temporary.previous = tULEMUS
		temporary.järgmine = tULEMUS.järgmine
		if temporary.järgmine != nil {
			temporary.järgmine.previous = temporary
		}
		tULEMUS.suurus = suurus
		tULEMUS.järgmine = temporary
	}
	tULEMUS.allocated = true
	return Pointer(uintptr(Pointer(tULEMUS)) + uintptr(mäluchunkSuurus) + uintptr(diff)), diff
}
func (ise *TMälumanager) Vaba(kursor_2 Pointer) {
	var chunk *TMäluchunk = (*TMäluchunk)(Pointer(uintptr(kursor_2) - uintptr(mäluchunkSuurus)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.järgmine = chunk.järgmine
		chunk.previous.suurus += chunk.suurus + mäluchunkSuurus
		if chunk.järgmine != nil {
			chunk.järgmine.previous = chunk.previous
		}
	}

	if chunk.järgmine != nil && !chunk.järgmine.allocated {
		chunk.suurus += chunk.järgmine.suurus + mäluchunkSuurus
		chunk.järgmine = chunk.järgmine.järgmine
		if chunk.järgmine != nil {
			chunk.järgmine.previous = chunk
		}
	}
}
func Uus(suurus int) Pointer {
	if AktiivneMälumanager == nil {
		return nil
	}
	return AktiivneMälumanager.Malloc(uint32(suurus))
}
func Kustuta(kursor_2 Pointer) {
	if AktiivneMälumanager != nil {
		AktiivneMälumanager.Vaba(kursor_2)
	}
}
