package memorymananger

import . "unsafe"

const Maxqueueཚད uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TMemorychunk struct {
	next		*TMemorychunk
	previous	*TMemorychunk
	allocated	bool

	ཚད	uint32
}

type TMemorymanager struct {
}

var first *TMemorychunk
var Activememorymanager *TMemorymanager = nil
var memorychunkཚད uint32

func (self *TMemorymanager) Init(start uint32, ཚད uint32) {

	Activememorymanager = self

	memorychunkཚད = uint32(Sizeof(TMemorychunk{}))

	if ཚད < memorychunkཚད {
		first = nil
	} else {
		first = (*TMemorychunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.next = nil
		first.ཚད = ཚད - memorychunkཚད
	}
}
func (self *TMemorymanager) Destroy() {
	if Activememorymanager == self {
		Activememorymanager = nil
	}
}
func (self *TMemorymanager) Malloc(ཚད uint32) Pointer {
	var result *TMemorychunk = nil

	var chunk *TMemorychunk = first
	for ; chunk != nil && result == nil; chunk = chunk.next {
		if chunk.ཚད > ཚད && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.ཚད >= (ཚད + memorychunkཚད + 1) {

		var temporary *TMemorychunk
		temporary = (*TMemorychunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memorychunkཚད + ཚད)))

		temporary.allocated = false
		temporary.ཚད = result.ཚད - ཚད - memorychunkཚད
		temporary.previous = result
		temporary.next = result.next

		if temporary.next != nil {
			temporary.next.previous = temporary
		}

		result.ཚད = ཚད
		result.next = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkཚད))
}
func (self *TMemorymanager) Alignedmalloc(ཚད uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if ཚད == 0 || ཚད > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemorychunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.next {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorychunkཚད))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.ཚད && ཚད <= chunk.ཚད-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	ཚད += diff
	if result.ཚད-ཚད >= memorychunkཚད+1 {
		temporary := (*TMemorychunk)(Pointer(uintptr(Pointer(result)) + uintptr(memorychunkཚད) + uintptr(ཚད)))
		temporary.allocated = false
		temporary.ཚད = result.ཚད - ཚད - memorychunkཚད
		temporary.previous = result
		temporary.next = result.next
		if temporary.next != nil {
			temporary.next.previous = temporary
		}
		result.ཚད = ཚད
		result.next = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunkཚད) + uintptr(diff)), diff
}
func (self *TMemorymanager) Free(pointer_2 Pointer) {
	var chunk *TMemorychunk = (*TMemorychunk)(Pointer(uintptr(pointer_2) - uintptr(memorychunkཚད)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.next = chunk.next
		chunk.previous.ཚད += chunk.ཚད + memorychunkཚད
		if chunk.next != nil {
			chunk.next.previous = chunk.previous
		}
	}

	if chunk.next != nil && !chunk.next.allocated {
		chunk.ཚད += chunk.next.ཚད + memorychunkཚད
		chunk.next = chunk.next.next
		if chunk.next != nil {
			chunk.next.previous = chunk
		}
	}
}
func New(ཚད int) Pointer {
	if Activememorymanager == nil {
		return nil
	}
	return Activememorymanager.Malloc(uint32(ཚད))
}
func Delete(pointer_2 Pointer) {
	if Activememorymanager != nil {
		Activememorymanager.Free(pointer_2)
	}
}
