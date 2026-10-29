/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Maxqueueขนาด uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TMemorychunk struct {
	next		*TMemorychunk
	previous	*TMemorychunk
	allocated	bool

	ขนาด	uint32
}

type TMemorymanager struct {
}

var first *TMemorychunk
var Aทำงานmemorymanager *TMemorymanager = nil
var memorychunkขนาด uint32

func (self *TMemorymanager) Init(start uint32, ขนาด uint32) {

	Aทำงานmemorymanager = self

	memorychunkขนาด = uint32(Sizeof(TMemorychunk{}))

	if ขนาด < memorychunkขนาด {
		first = nil
	} else {
		first = (*TMemorychunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.next = nil
		first.ขนาด = ขนาด - memorychunkขนาด
	}
}
func (self *TMemorymanager) Dทำลาย() {
	if Aทำงานmemorymanager == self {
		Aทำงานmemorymanager = nil
	}
}
func (self *TMemorymanager) Malloc(ขนาด uint32) Pointer {
	var result *TMemorychunk = nil

	var chunk *TMemorychunk = first
	for ; chunk != nil && result == nil; chunk = chunk.next {
		if chunk.ขนาด > ขนาด && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.ขนาด >= (ขนาด + memorychunkขนาด + 1) {

		var temporary *TMemorychunk
		temporary = (*TMemorychunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memorychunkขนาด + ขนาด)))

		temporary.allocated = false
		temporary.ขนาด = result.ขนาด - ขนาด - memorychunkขนาด
		temporary.previous = result
		temporary.next = result.next

		if temporary.next != nil {
			temporary.next.previous = temporary
		}

		result.ขนาด = ขนาด
		result.next = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkขนาด))
}
func (self *TMemorymanager) Alignedmalloc(ขนาด uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if ขนาด == 0 || ขนาด > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemorychunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.next {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorychunkขนาด))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.ขนาด && ขนาด <= chunk.ขนาด-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	ขนาด += diff
	if result.ขนาด-ขนาด >= memorychunkขนาด+1 {
		temporary := (*TMemorychunk)(Pointer(uintptr(Pointer(result)) + uintptr(memorychunkขนาด) + uintptr(ขนาด)))
		temporary.allocated = false
		temporary.ขนาด = result.ขนาด - ขนาด - memorychunkขนาด
		temporary.previous = result
		temporary.next = result.next
		if temporary.next != nil {
			temporary.next.previous = temporary
		}
		result.ขนาด = ขนาด
		result.next = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkขนาด) + uintptr(diff)), diff
}
func (self *TMemorymanager) Free(pointer_2 Pointer) {
	var chunk *TMemorychunk = (*TMemorychunk)(Pointer(uintptr(pointer_2) - uintptr(memorychunkขนาด)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.next = chunk.next
		chunk.previous.ขนาด += chunk.ขนาด + memorychunkขนาด
		if chunk.next != nil {
			chunk.next.previous = chunk.previous
		}
	}

	if chunk.next != nil && !chunk.next.allocated {
		chunk.ขนาด += chunk.next.ขนาด + memorychunkขนาด
		chunk.next = chunk.next.next
		if chunk.next != nil {
			chunk.next.previous = chunk
		}
	}
}
func New(ขนาด int) Pointer {
	if Aทำงานmemorymanager == nil {
		return nil
	}
	return Aทำงานmemorymanager.Malloc(uint32(ขนาด))
}
func Dลบ(pointer_2 Pointer) {
	if Aทำงานmemorymanager != nil {
		Aทำงานmemorymanager.Free(pointer_2)
	}
}
