/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueVeľkosť uint32 = 0x1FFFFFF
const QueueSpustiťaddress uint32 = 0x1000000

type TPamäťchunk struct {
	nasledujúci	*TPamäťchunk
	previous	*TPamäťchunk
	allocated	bool

	veľkosť	uint32
}

type TPamäťmanager struct {
}

var first *TPamäťchunk
var AktívnyPamäťmanager *TPamäťmanager = nil
var pamäťchunkVeľkosť uint32

func (vlastný *TPamäťmanager) Init(spustiť uint32, veľkosť uint32) {

	AktívnyPamäťmanager = vlastný

	pamäťchunkVeľkosť = uint32(Sizeof(TPamäťchunk{}))

	if veľkosť < pamäťchunkVeľkosť {
		first = nil
	} else {
		first = (*TPamäťchunk)(Pointer(uintptr(QueueSpustiťaddress) + uintptr(spustiť)))
		first.allocated = false
		first.previous = nil
		first.nasledujúci = nil
		first.veľkosť = veľkosť - pamäťchunkVeľkosť
	}
}
func (vlastný *TPamäťmanager) Zničiť() {
	if AktívnyPamäťmanager == vlastný {
		AktívnyPamäťmanager = nil
	}
}
func (vlastný *TPamäťmanager) Malloc(veľkosť uint32) Pointer {
	var result *TPamäťchunk = nil

	var chunk *TPamäťchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.nasledujúci {
		if chunk.veľkosť > veľkosť && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.veľkosť >= (veľkosť + pamäťchunkVeľkosť + 1) {

		var temporary *TPamäťchunk
		temporary = (*TPamäťchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + pamäťchunkVeľkosť + veľkosť)))

		temporary.allocated = false
		temporary.veľkosť = result.veľkosť - veľkosť - pamäťchunkVeľkosť
		temporary.previous = result
		temporary.nasledujúci = result.nasledujúci

		if temporary.nasledujúci != nil {
			temporary.nasledujúci.previous = temporary
		}

		result.veľkosť = veľkosť
		result.nasledujúci = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(pamäťchunkVeľkosť))
}
func (vlastný *TPamäťmanager) Alignedmalloc(veľkosť uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if veľkosť == 0 || veľkosť > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TPamäťchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.nasledujúci {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(pamäťchunkVeľkosť))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.veľkosť && veľkosť <= chunk.veľkosť-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	veľkosť += diff
	if result.veľkosť-veľkosť >= pamäťchunkVeľkosť+1 {
		temporary := (*TPamäťchunk)(Pointer(uintptr(Pointer(result)) + uintptr(pamäťchunkVeľkosť) + uintptr(veľkosť)))
		temporary.allocated = false
		temporary.veľkosť = result.veľkosť - veľkosť - pamäťchunkVeľkosť
		temporary.previous = result
		temporary.nasledujúci = result.nasledujúci
		if temporary.nasledujúci != nil {
			temporary.nasledujúci.previous = temporary
		}
		result.veľkosť = veľkosť
		result.nasledujúci = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(pamäťchunkVeľkosť) + uintptr(diff)), diff
}
func (vlastný *TPamäťmanager) Voľné(kurzor_2 Pointer) {
	var chunk *TPamäťchunk = (*TPamäťchunk)(Pointer(uintptr(kurzor_2) - uintptr(pamäťchunkVeľkosť)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.nasledujúci = chunk.nasledujúci
		chunk.previous.veľkosť += chunk.veľkosť + pamäťchunkVeľkosť
		if chunk.nasledujúci != nil {
			chunk.nasledujúci.previous = chunk.previous
		}
	}

	if chunk.nasledujúci != nil && !chunk.nasledujúci.allocated {
		chunk.veľkosť += chunk.nasledujúci.veľkosť + pamäťchunkVeľkosť
		chunk.nasledujúci = chunk.nasledujúci.nasledujúci
		if chunk.nasledujúci != nil {
			chunk.nasledujúci.previous = chunk
		}
	}
}
func Nový(veľkosť int) Pointer {
	if AktívnyPamäťmanager == nil {
		return nil
	}
	return AktívnyPamäťmanager.Malloc(uint32(veľkosť))
}
func Odstrániť(kurzor_2 Pointer) {
	if AktívnyPamäťmanager != nil {
		AktívnyPamäťmanager.Voľné(kurzor_2)
	}
}
