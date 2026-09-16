/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueStødd uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TMemorychunk struct {
	næsta		*TMemorychunk
	previous	*TMemorychunk
	allocated	bool

	stødd	uint32
}

type TMemorymanager struct {
}

var first *TMemorychunk
var Activememorymanager *TMemorymanager = nil
var memorychunkStødd uint32

func (self *TMemorymanager) Init(start uint32, stødd uint32) {

	Activememorymanager = self

	memorychunkStødd = uint32(Sizeof(TMemorychunk{}))

	if stødd < memorychunkStødd {
		first = nil
	} else {
		first = (*TMemorychunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.næsta = nil
		first.stødd = stødd - memorychunkStødd
	}
}
func (self *TMemorymanager) Destroy() {
	if Activememorymanager == self {
		Activememorymanager = nil
	}
}
func (self *TMemorymanager) Malloc(stødd uint32) Pointer {
	var result *TMemorychunk = nil

	var chunk *TMemorychunk = first
	for ; chunk != nil && result == nil; chunk = chunk.næsta {
		if chunk.stødd > stødd && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.stødd >= (stødd + memorychunkStødd + 1) {

		var temporary *TMemorychunk
		temporary = (*TMemorychunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memorychunkStødd + stødd)))

		temporary.allocated = false
		temporary.stødd = result.stødd - stødd - memorychunkStødd
		temporary.previous = result
		temporary.næsta = result.næsta

		if temporary.næsta != nil {
			temporary.næsta.previous = temporary
		}

		result.stødd = stødd
		result.næsta = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkStødd))
}
func (self *TMemorymanager) Alignedmalloc(stødd uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if stødd == 0 || stødd > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemorychunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.næsta {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorychunkStødd))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.stødd && stødd <= chunk.stødd-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	stødd += diff
	if result.stødd-stødd >= memorychunkStødd+1 {
		temporary := (*TMemorychunk)(Pointer(uintptr(Pointer(result)) + uintptr(memorychunkStødd) + uintptr(stødd)))
		temporary.allocated = false
		temporary.stødd = result.stødd - stødd - memorychunkStødd
		temporary.previous = result
		temporary.næsta = result.næsta
		if temporary.næsta != nil {
			temporary.næsta.previous = temporary
		}
		result.stødd = stødd
		result.næsta = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkStødd) + uintptr(diff)), diff
}
func (self *TMemorymanager) Free(pointer_2 Pointer) {
	var chunk *TMemorychunk = (*TMemorychunk)(Pointer(uintptr(pointer_2) - uintptr(memorychunkStødd)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.næsta = chunk.næsta
		chunk.previous.stødd += chunk.stødd + memorychunkStødd
		if chunk.næsta != nil {
			chunk.næsta.previous = chunk.previous
		}
	}

	if chunk.næsta != nil && !chunk.næsta.allocated {
		chunk.stødd += chunk.næsta.stødd + memorychunkStødd
		chunk.næsta = chunk.næsta.næsta
		if chunk.næsta != nil {
			chunk.næsta.previous = chunk
		}
	}
}
func New(stødd int) Pointer {
	if Activememorymanager == nil {
		return nil
	}
	return Activememorymanager.Malloc(uint32(stødd))
}
func Delete(pointer_2 Pointer) {
	if Activememorymanager != nil {
		Activememorymanager.Free(pointer_2)
	}
}
