/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueVeličina uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TMemorijachunk struct {
	sljedeće	*TMemorijachunk
	previous	*TMemorijachunk
	allocated	bool

	veličina	uint32
}

type TMemorijamanager struct {
}

var first *TMemorijachunk
var ActiveMemorijamanager *TMemorijamanager = nil
var memorijachunkVeličina uint32

func (self *TMemorijamanager) Init(start uint32, veličina uint32) {

	ActiveMemorijamanager = self

	memorijachunkVeličina = uint32(Sizeof(TMemorijachunk{}))

	if veličina < memorijachunkVeličina {
		first = nil
	} else {
		first = (*TMemorijachunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.sljedeće = nil
		first.veličina = veličina - memorijachunkVeličina
	}
}
func (self *TMemorijamanager) Destroy() {
	if ActiveMemorijamanager == self {
		ActiveMemorijamanager = nil
	}
}
func (self *TMemorijamanager) Malloc(veličina uint32) Pointer {
	var result *TMemorijachunk = nil

	var chunk *TMemorijachunk = first
	for ; chunk != nil && result == nil; chunk = chunk.sljedeće {
		if chunk.veličina > veličina && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.veličina >= (veličina + memorijachunkVeličina + 1) {

		var temporary *TMemorijachunk
		temporary = (*TMemorijachunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memorijachunkVeličina + veličina)))

		temporary.allocated = false
		temporary.veličina = result.veličina - veličina - memorijachunkVeličina
		temporary.previous = result
		temporary.sljedeće = result.sljedeće

		if temporary.sljedeće != nil {
			temporary.sljedeće.previous = temporary
		}

		result.veličina = veličina
		result.sljedeće = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memorijachunkVeličina))
}
func (self *TMemorijamanager) Alignedmalloc(veličina uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if veličina == 0 || veličina > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemorijachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.sljedeće {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorijachunkVeličina))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.veličina && veličina <= chunk.veličina-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	veličina += diff
	if result.veličina-veličina >= memorijachunkVeličina+1 {
		temporary := (*TMemorijachunk)(Pointer(uintptr(Pointer(result)) + uintptr(memorijachunkVeličina) + uintptr(veličina)))
		temporary.allocated = false
		temporary.veličina = result.veličina - veličina - memorijachunkVeličina
		temporary.previous = result
		temporary.sljedeće = result.sljedeće
		if temporary.sljedeće != nil {
			temporary.sljedeće.previous = temporary
		}
		result.veličina = veličina
		result.sljedeće = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memorijachunkVeličina) + uintptr(diff)), diff
}
func (self *TMemorijamanager) Slobodno(pointer_2 Pointer) {
	var chunk *TMemorijachunk = (*TMemorijachunk)(Pointer(uintptr(pointer_2) - uintptr(memorijachunkVeličina)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.sljedeće = chunk.sljedeće
		chunk.previous.veličina += chunk.veličina + memorijachunkVeličina
		if chunk.sljedeće != nil {
			chunk.sljedeće.previous = chunk.previous
		}
	}

	if chunk.sljedeće != nil && !chunk.sljedeće.allocated {
		chunk.veličina += chunk.sljedeće.veličina + memorijachunkVeličina
		chunk.sljedeće = chunk.sljedeće.sljedeće
		if chunk.sljedeće != nil {
			chunk.sljedeće.previous = chunk
		}
	}
}
func Nova(veličina int) Pointer {
	if ActiveMemorijamanager == nil {
		return nil
	}
	return ActiveMemorijamanager.Malloc(uint32(veličina))
}
func Obriši_2(pointer_2 Pointer) {
	if ActiveMemorijamanager != nil {
		ActiveMemorijamanager.Slobodno(pointer_2)
	}
}
