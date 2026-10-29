/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueUlulyk uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TMemorychunk struct {
	next		*TMemorychunk
	previous	*TMemorychunk
	allocated	bool

	ululyk	uint32
}

type TMemorymanager struct {
}

var first *TMemorychunk
var Activememorymanager *TMemorymanager = nil
var memorychunkUlulyk uint32

func (self *TMemorymanager) Init(start uint32, ululyk uint32) {

	Activememorymanager = self

	memorychunkUlulyk = uint32(Sizeof(TMemorychunk{}))

	if ululyk < memorychunkUlulyk {
		first = nil
	} else {
		first = (*TMemorychunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.next = nil
		first.ululyk = ululyk - memorychunkUlulyk
	}
}
func (self *TMemorymanager) Destroy() {
	if Activememorymanager == self {
		Activememorymanager = nil
	}
}
func (self *TMemorymanager) Malloc(ululyk uint32) Pointer {
	var result *TMemorychunk = nil

	var chunk *TMemorychunk = first
	for ; chunk != nil && result == nil; chunk = chunk.next {
		if chunk.ululyk > ululyk && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.ululyk >= (ululyk + memorychunkUlulyk + 1) {

		var temporary *TMemorychunk
		temporary = (*TMemorychunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memorychunkUlulyk + ululyk)))

		temporary.allocated = false
		temporary.ululyk = result.ululyk - ululyk - memorychunkUlulyk
		temporary.previous = result
		temporary.next = result.next

		if temporary.next != nil {
			temporary.next.previous = temporary
		}

		result.ululyk = ululyk
		result.next = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkUlulyk))
}
func (self *TMemorymanager) Alignedmalloc(ululyk uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if ululyk == 0 || ululyk > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemorychunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.next {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorychunkUlulyk))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.ululyk && ululyk <= chunk.ululyk-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	ululyk += diff
	if result.ululyk-ululyk >= memorychunkUlulyk+1 {
		temporary := (*TMemorychunk)(Pointer(uintptr(Pointer(result)) + uintptr(memorychunkUlulyk) + uintptr(ululyk)))
		temporary.allocated = false
		temporary.ululyk = result.ululyk - ululyk - memorychunkUlulyk
		temporary.previous = result
		temporary.next = result.next
		if temporary.next != nil {
			temporary.next.previous = temporary
		}
		result.ululyk = ululyk
		result.next = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkUlulyk) + uintptr(diff)), diff
}
func (self *TMemorymanager) Free(pointer_2 Pointer) {
	var chunk *TMemorychunk = (*TMemorychunk)(Pointer(uintptr(pointer_2) - uintptr(memorychunkUlulyk)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.next = chunk.next
		chunk.previous.ululyk += chunk.ululyk + memorychunkUlulyk
		if chunk.next != nil {
			chunk.next.previous = chunk.previous
		}
	}

	if chunk.next != nil && !chunk.next.allocated {
		chunk.ululyk += chunk.next.ululyk + memorychunkUlulyk
		chunk.next = chunk.next.next
		if chunk.next != nil {
			chunk.next.previous = chunk
		}
	}
}
func Täze(ululyk int) Pointer {
	if Activememorymanager == nil {
		return nil
	}
	return Activememorymanager.Malloc(uint32(ululyk))
}
func Poz_2(pointer_2 Pointer) {
	if Activememorymanager != nil {
		Activememorymanager.Free(pointer_2)
	}
}
