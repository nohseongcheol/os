/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueMărime uint32 = 0x1FFFFFF
const QueuePorneșteaddress uint32 = 0x1000000

type TMemoriechunk struct {
	înainte		*TMemoriechunk
	previous	*TMemoriechunk
	allocated	bool

	mărime	uint32
}

type TMemoriemanager struct {
}

var first *TMemoriechunk
var ActivMemoriemanager *TMemoriemanager = nil
var memoriechunkMărime uint32

func (sine *TMemoriemanager) Init(pornește uint32, mărime uint32) {

	ActivMemoriemanager = sine

	memoriechunkMărime = uint32(Sizeof(TMemoriechunk{}))

	if mărime < memoriechunkMărime {
		first = nil
	} else {
		first = (*TMemoriechunk)(Pointer(uintptr(QueuePorneșteaddress) + uintptr(pornește)))
		first.allocated = false
		first.previous = nil
		first.înainte = nil
		first.mărime = mărime - memoriechunkMărime
	}
}
func (sine *TMemoriemanager) Distruge() {
	if ActivMemoriemanager == sine {
		ActivMemoriemanager = nil
	}
}
func (sine *TMemoriemanager) Malloc(mărime uint32) Pointer {
	var result *TMemoriechunk = nil

	var chunk *TMemoriechunk = first
	for ; chunk != nil && result == nil; chunk = chunk.înainte {
		if chunk.mărime > mărime && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.mărime >= (mărime + memoriechunkMărime + 1) {

		var temporary *TMemoriechunk
		temporary = (*TMemoriechunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memoriechunkMărime + mărime)))

		temporary.allocated = false
		temporary.mărime = result.mărime - mărime - memoriechunkMărime
		temporary.previous = result
		temporary.înainte = result.înainte

		if temporary.înainte != nil {
			temporary.înainte.previous = temporary
		}

		result.mărime = mărime
		result.înainte = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memoriechunkMărime))
}
func (sine *TMemoriemanager) Alignedmalloc(mărime uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if mărime == 0 || mărime > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemoriechunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.înainte {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memoriechunkMărime))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.mărime && mărime <= chunk.mărime-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	mărime += diff
	if result.mărime-mărime >= memoriechunkMărime+1 {
		temporary := (*TMemoriechunk)(Pointer(uintptr(Pointer(result)) + uintptr(memoriechunkMărime) + uintptr(mărime)))
		temporary.allocated = false
		temporary.mărime = result.mărime - mărime - memoriechunkMărime
		temporary.previous = result
		temporary.înainte = result.înainte
		if temporary.înainte != nil {
			temporary.înainte.previous = temporary
		}
		result.mărime = mărime
		result.înainte = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memoriechunkMărime) + uintptr(diff)), diff
}
func (sine *TMemoriemanager) Liber(indicator_2 Pointer) {
	var chunk *TMemoriechunk = (*TMemoriechunk)(Pointer(uintptr(indicator_2) - uintptr(memoriechunkMărime)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.înainte = chunk.înainte
		chunk.previous.mărime += chunk.mărime + memoriechunkMărime
		if chunk.înainte != nil {
			chunk.înainte.previous = chunk.previous
		}
	}

	if chunk.înainte != nil && !chunk.înainte.allocated {
		chunk.mărime += chunk.înainte.mărime + memoriechunkMărime
		chunk.înainte = chunk.înainte.înainte
		if chunk.înainte != nil {
			chunk.înainte.previous = chunk
		}
	}
}
func Nou(mărime int) Pointer {
	if ActivMemoriemanager == nil {
		return nil
	}
	return ActivMemoriemanager.Malloc(uint32(mărime))
}
func Șterge(indicator_2 Pointer) {
	if ActivMemoriemanager != nil {
		ActivMemoriemanager.Liber(indicator_2)
	}
}
